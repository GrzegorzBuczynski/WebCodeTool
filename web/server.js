/**
 * Server Express - backend dla UI systemu wieloagentowego
 */
require('dotenv').config({ path: require('path').join(__dirname, '..', '.env') });
require('dotenv').config({ path: require('path').join(__dirname, '..', 'config', '.env') });

const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const path = require('path');
const fs = require('fs');
const { spawn } = require('child_process');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'public')));

// Ścieżka do folderu results i workspace
const RESULTS_DIR = path.join(__dirname, '..', 'results');
const WORKSPACE_DIR = process.env.WORKSPACE_DIR || path.join(__dirname, '..');
const ROOT_DIR = path.resolve(WORKSPACE_DIR);
const FS_EXCLUDE = new Set(['node_modules', 'venv', '__pycache__', '.git', 'results']);
const PUBLIC_DIR = path.join(__dirname, 'public');

const reloadClients = new Set();

function notifyReload() {
  reloadClients.forEach((res) => {
    res.write('data: reload\n\n');
  });
}

fs.watch(PUBLIC_DIR, { recursive: true }, (event, filename) => {
  if (!filename) return;
  if (filename.endsWith('.js') || filename.endsWith('.html')) {
    notifyReload();
  }
});

function safeResolve(relPath) {
  const target = path.resolve(ROOT_DIR, relPath || '.');
  if (!target.startsWith(ROOT_DIR)) {
    throw new Error('Nieprawidłowa ścieżka');
  }
  return target;
}

function buildTree(dirPath, relBase, depth) {
  const items = [];
  if (depth < 0) return items;

  const entries = fs.readdirSync(dirPath, { withFileTypes: true })
    .filter((entry) => !FS_EXCLUDE.has(entry.name))
    .sort((a, b) => a.name.localeCompare(b.name));

  for (const entry of entries) {
    const fullPath = path.join(dirPath, entry.name);
    const relPath = path.join(relBase, entry.name);

    if (entry.isDirectory()) {
      items.push({
        type: 'dir',
        name: entry.name,
        path: relPath,
        children: buildTree(fullPath, relPath, depth - 1)
      });
    } else if (entry.isFile()) {
      const stat = fs.statSync(fullPath);
      items.push({
        type: 'file',
        name: entry.name,
        path: relPath,
        size: stat.size
      });
    }
  }

  return items;
}

/**
 * GET /api/reload - SSE hot reload
 */
app.get('/api/reload', (req, res) => {
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');
  res.flushHeaders();

  reloadClients.add(res);
  res.write('data: connected\n\n');

  req.on('close', () => {
    reloadClients.delete(res);
  });
});

/**
 * GET /api/results - lista wszystkich zadań
 */
app.get('/api/results', (req, res) => {
  try {
    if (!fs.existsSync(RESULTS_DIR)) {
      return res.json({ tasks: [], total: 0 });
    }

    const tasks = [];
    const files = fs.readdirSync(RESULTS_DIR).sort();
    
    files.forEach(file => {
      const taskPath = path.join(RESULTS_DIR, file);
      const stat = fs.statSync(taskPath);
      
      if (stat.isDirectory() && file.startsWith('task_')) {
        const resultFile = path.join(taskPath, 'result.json');
        const outputFile = path.join(taskPath, 'output.txt');
        
        let result = null;
        let output = null;
        
        if (fs.existsSync(resultFile)) {
          result = JSON.parse(fs.readFileSync(resultFile, 'utf-8'));
        }
        if (fs.existsSync(outputFile)) {
          output = fs.readFileSync(outputFile, 'utf-8').substring(0, 200);
        }
        
        tasks.push({
          id: file,
          description: result?.description || '(brak)',
          status: result?.status || 'unknown',
          verified: result?.verification?.passed || false,
          score: result?.verification?.score || 0,
          preview: output || '(brak wyniku)',
          timestamp: stat.birthtime
        });
      }
    });

    res.json({ 
      tasks: tasks.reverse(), 
      total: tasks.length 
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

/**
 * GET /api/task/:taskId - szczegóły konkretnego zadania
 */
app.get('/api/task/:taskId', (req, res) => {
  try {
    const { taskId } = req.params;
    const taskPath = path.join(RESULTS_DIR, taskId);
    
    if (!fs.existsSync(taskPath)) {
      return res.status(404).json({ error: 'Zadanie nie znalezione' });
    }

    const data = {};
    
    // Czytaj dostępne pliki
    const files = ['result.json', 'output.txt', 'report.txt', 'detailed_report.json', 'hierarchy.json', 'stats.json'];
    
    files.forEach(file => {
      const filePath = path.join(taskPath, file);
      if (fs.existsSync(filePath)) {
        if (file.endsWith('.json')) {
          data[file] = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
        } else {
          data[file] = fs.readFileSync(filePath, 'utf-8');
        }
      }
    });

    res.json(data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

/**
 * POST /api/run - uruchom test
 */
app.post('/api/run', (req, res) => {
  try {
    const { taskDescription } = req.body || {};
    const description = taskDescription || 'Zaplanuj prosty obiad dla 4 osób: zupa, drugie danie i deser.';
    
    res.json({ 
      status: 'running', 
      message: 'Uruchamianie testu w tle...',
      taskDescription: description 
    });

    // Uruchom test w tle (nie czekaj na zakończenie)
    runTestInBackground(description);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

/**
 * GET /api/fs/root - aktualny katalog główny
 */
app.get('/api/fs/root', (req, res) => {
  res.json({ root: WORKSPACE_DIR });
});

/**
 * POST /api/fs/root - ustaw katalog główny (opcjonalne)
 */
app.post('/api/fs/root', (req, res) => {
  const { root } = req.body;
  // W prostej implementacji zawsze używamy WORKSPACE_DIR z .env
  res.json({ root: root || WORKSPACE_DIR });
});

/**
 * GET /api/fs/tree - drzewo plików projektu
 */
app.get('/api/fs/tree', (req, res) => {
  try {
    const relPath = req.query.path || '.';
    const depth = Number(req.query.depth || 4);
    const target = safeResolve(relPath);

    if (!fs.existsSync(target) || !fs.statSync(target).isDirectory()) {
      return res.status(404).json({ error: 'Katalog nie istnieje' });
    }

    const tree = buildTree(target, relPath === '.' ? '' : relPath, depth);
    res.json({ root: relPath, tree });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

/**
 * GET /api/fs/file - zawartość pliku
 */
app.get('/api/fs/file', (req, res) => {
  try {
    const relPath = req.query.path;
    if (!relPath) {
      return res.status(400).json({ error: 'Brak parametru path' });
    }

    const target = safeResolve(relPath);
    if (!fs.existsSync(target) || !fs.statSync(target).isFile()) {
      return res.status(404).json({ error: 'Plik nie istnieje' });
    }

    const stat = fs.statSync(target);
    if (stat.size > 200 * 1024) {
      return res.status(413).json({ error: 'Plik zbyt duży do podglądu' });
    }

    const content = fs.readFileSync(target, 'utf-8');
    res.json({ path: relPath, size: stat.size, content });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

/**
 * POST /api/fs/file - zapisz/utwórz plik
 */
app.post('/api/fs/file', (req, res) => {
  try {
    const { path: relPath, content } = req.body;
    if (!relPath) {
      return res.status(400).json({ error: 'Brak parametru path' });
    }
    if (content === undefined) {
      return res.status(400).json({ error: 'Brak zawartości pliku' });
    }

    const target = safeResolve(relPath);
    
    // Ensure directory exists
    const dir = path.dirname(target);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }

    fs.writeFileSync(target, content, 'utf-8');
    const stat = fs.statSync(target);
    
    res.json({ 
      path: relPath, 
      size: stat.size, 
      message: 'Plik zapisany pomyślnie' 
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

/**
 * DELETE /api/fs/file - usuń plik
 */
app.delete('/api/fs/file', (req, res) => {
  try {
    const relPath = req.query.path;
    if (!relPath) {
      return res.status(400).json({ error: 'Brak parametru path' });
    }

    const target = safeResolve(relPath);
    if (!fs.existsSync(target)) {
      return res.status(404).json({ error: 'Plik nie istnieje' });
    }

    if (fs.statSync(target).isDirectory()) {
      return res.status(400).json({ error: 'Nie można usunąć katalogu jako pliku' });
    }

    fs.unlinkSync(target);
    res.json({ message: 'Plik usunięty pomyślnie', path: relPath });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

/**
 * POST /api/fs/mkdir - utwórz katalog
 */
app.post('/api/fs/mkdir', (req, res) => {
  try {
    const { path: relPath } = req.body;
    if (!relPath) {
      return res.status(400).json({ error: 'Brak parametru path' });
    }

    const target = safeResolve(relPath);
    if (fs.existsSync(target)) {
      return res.status(409).json({ error: 'Katalog już istnieje' });
    }

    fs.mkdirSync(target, { recursive: true });
    res.json({ message: 'Katalog utworzony pomyślnie', path: relPath });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

/**
 * Uruchomienie testu w tle
 */
function runTestInBackground(taskDescription) {
  const pythonProcess = spawn('python', [path.join('..', 'scripts', 'test_run.py')], {
    cwd: __dirname,
    stdio: ['pipe', 'pipe', 'pipe']
  });

  let stdout = '';
  let stderr = '';

  pythonProcess.stdout.on('data', (data) => {
    stdout += data.toString();
    console.log('[Python stdout]', data.toString());
  });

  pythonProcess.stderr.on('data', (data) => {
    stderr += data.toString();
    console.log('[Python stderr]', data.toString());
  });

  pythonProcess.on('close', (code) => {
    console.log(`Python process zakończony z kodem: ${code}`);
    console.log('=== Pełny output stdout ===');
    console.log(stdout);
    if (stderr) {
      console.log('=== Pełny output stderr ===');
      console.log(stderr);
    }
  });
}

/**
 * GET /api/status - status serwera
 */
app.get('/api/status', (req, res) => {
  res.json({ 
    status: 'ok',
    uptime: process.uptime(),
    resultsDir: RESULTS_DIR,
    resultsExist: fs.existsSync(RESULTS_DIR)
  });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({ error: 'Nieznana ścieżka' });
});

// Startuj serwer
app.listen(PORT, () => {
  console.log(`
╔════════════════════════════════════════════════════════════════════╗
║   Multi-Agent AI System - Web UI                                   ║
║   http://localhost:${PORT}                                         ║
╚════════════════════════════════════════════════════════════════════╝
  `);
});
