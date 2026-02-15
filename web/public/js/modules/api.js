// API Module
export async function fetchJson(url, options) {
  const res = await fetch(url, options);
  if (!res.ok) {
    throw new Error(`Błąd ${res.status}`);
  }
  return res.json();
}

export async function loadRootPath() {
  const data = await fetchJson('/api/fs/root');
  return data.root || '';
}

export async function applyRootSelection(path) {
  if (!path) return;
  await fetchJson('/api/fs/root', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ root: path })
  });
  return path;
}

export async function loadFileTree() {
  const data = await fetchJson('/api/fs/tree');
  return data.tree || [];
}

export async function loadFile(filePath) {
  const data = await fetchJson(`/api/fs/file?path=${encodeURIComponent(filePath)}`);
  return data;
}

export async function saveFile(filePath, content) {
  const data = await fetchJson('/api/fs/file', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ path: filePath, content })
  });
  return data;
}

export async function createFile(filePath, content = '') {
  const data = await fetchJson('/api/fs/file', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ path: filePath, content })
  });
  return data;
}

export async function deleteFile(filePath) {
  const data = await fetchJson(`/api/fs/file?path=${encodeURIComponent(filePath)}`, {
    method: 'DELETE'
  });
  return data;
}

export async function createFolder(folderPath) {
  const data = await fetchJson('/api/fs/mkdir', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ path: folderPath })
  });
  return data;
}

export async function loadTasks() {
  const data = await fetchJson('/api/results');
  return { tasks: data.tasks || [], total: data.total || 0 };
}

export async function loadTask(taskId) {
  const data = await fetchJson(`/api/task/${taskId}`);
  return data || {};
}

export async function runTask(description) {
  await fetchJson('/api/run', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ taskDescription: description })
  });
}

export async function loadModalFolders(path) {
  const data = await fetchJson(`/api/fs/browse?path=${encodeURIComponent(path)}`);
  return data.folders || [];
}
