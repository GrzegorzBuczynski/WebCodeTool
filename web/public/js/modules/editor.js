// Editor Component
import { state, setStatus, render } from './state.js';
import { loadFile, saveFile } from './api.js';

let editorShortcutsBound = false;

export function renderEditor() {
  const editorEl = document.getElementById('editor-content');
  const panelEl = document.getElementById('panel-content');
  if (!editorEl || !panelEl) return;

  bindEditorShortcuts();
  
  if (state.activeView === 'files') {
    renderFileEditor(editorEl, panelEl);
    return;
  }
  if (state.activeView === 'tasks') {
    renderTaskEditor(editorEl, panelEl);
    return;
  }
  editorEl.innerHTML = '<div class="text-[#8a8a8a]">Select a panel on the left</div>';
  panelEl.textContent = 'No data';
}

function renderFileEditor(editorEl, panelEl) {
  if (!state.selectedFilePath) {
    editorEl.innerHTML = '<div class="text-[#8a8a8a]">Select a file from the tree</div>';
    panelEl.textContent = 'No data';
    return;
  }
  const file = state.openFiles.find((f) => f.path === state.selectedFilePath);
  if (!file) {
    editorEl.innerHTML = '<div class="text-[#8a8a8a]">File is not open</div>';
    panelEl.textContent = 'No data';
    return;
  }
  const content = file.draft ?? file.content ?? '';
  const isDirty = file.isDirty ?? content !== (file.content ?? '');
  
  editorEl.innerHTML = `
    <div class="flex h-full flex-col gap-0 overflow-hidden bg-[#1e1e1e]">
      <div class="flex items-center justify-between border-b border-[#3c3c3c] bg-[#252526] px-3 py-2 text-xs flex-shrink-0">
        <div class="text-[#8a8a8a]">${file.path}</div>
        <div class="flex items-center gap-2">
          <span id="editor-cursor-pos" class="text-[10px] text-[#8a8a8a]">Ln 1, Col 1</span>
          <span id="editor-dirty-badge" class="rounded-full px-2 py-0.5 text-[10px] ${
            isDirty ? 'bg-amber-500/20 text-amber-300' : 'bg-emerald-500/20 text-emerald-300'
          }">${isDirty ? 'UNSAVED' : 'SAVED'}</span>
          <button id="editor-save-btn" class="rounded border border-[#3c3c3c] bg-[#1e1e1e] px-2 py-1 hover:bg-white/10" ${
            isDirty ? '' : 'disabled'
          }>Save</button>
          <button id="editor-reload-btn" class="rounded border border-[#3c3c3c] bg-[#1e1e1e] px-2 py-1 hover:bg-white/10">Reload</button>
        </div>
      </div>
      <div class="flex flex-1 overflow-hidden">
        <div id="editor-line-numbers" class="flex-shrink-0 border-r border-[#3c3c3c] bg-[#1e1e1e] px-2 py-3 text-right text-[13px] leading-6 text-[#858585] select-none overflow-hidden"></div>
        <textarea id="editor-textarea" class="flex-1 w-full resize-none bg-[#111] p-3 text-[13px] leading-6 text-[#d4d4d4] outline-none focus:ring-1 focus:ring-[#007acc] overflow-auto" spellcheck="false"></textarea>
      </div>
    </div>
  `;
  
  const textarea = editorEl.querySelector('#editor-textarea');
  const lineNumbers = editorEl.querySelector('#editor-line-numbers');
  const saveBtn = editorEl.querySelector('#editor-save-btn');
  const reloadBtn = editorEl.querySelector('#editor-reload-btn');
  const badge = editorEl.querySelector('#editor-dirty-badge');
  const cursorPos = editorEl.querySelector('#editor-cursor-pos');
  
  if (textarea) {
    textarea.value = content;
    
    // Update line numbers
    const updateLineNumbers = () => {
      const lines = textarea.value.split('\n').length;
      lineNumbers.innerHTML = Array.from({ length: lines }, (_, i) => i + 1).join('\n');
    };
    
    // Update cursor position
    const updateCursorPosition = () => {
      const pos = textarea.selectionStart;
      const textBeforeCursor = textarea.value.substring(0, pos);
      const line = textBeforeCursor.split('\n').length;
      const col = textBeforeCursor.split('\n').pop().length + 1;
      if (cursorPos) {
        cursorPos.textContent = `Ln ${line}, Col ${col}`;
      }
    };
    
    updateLineNumbers();
    updateCursorPosition();
    
    textarea.addEventListener('input', () => {
      file.draft = textarea.value;
      file.isDirty = file.draft !== (file.content ?? '');
      updateFileEditorState(saveBtn, badge, file.isDirty);
      updateLineNumbers();
      render();
    });
    
    textarea.addEventListener('keyup', updateCursorPosition);
    textarea.addEventListener('click', updateCursorPosition);
    textarea.addEventListener('scroll', () => {
      // Sync line numbers scroll with textarea
      lineNumbers.scrollTop = textarea.scrollTop;
    });
  }
  if (saveBtn) {
    saveBtn.addEventListener('click', async () => {
      await saveActiveFile();
    });
  }
  if (reloadBtn) {
    reloadBtn.addEventListener('click', async () => {
      if (file.isDirty) {
        const confirmed = window.confirm('Discard unsaved changes and reload from disk?');
        if (!confirmed) return;
      }
      await reloadActiveFile();
    });
  }
  panelEl.innerHTML = fileDetailsHtml(file);
}

function fileContentHtml(content) {
  return `<div class="rounded border border-[#3c3c3c] bg-[#111] p-3 text-[13px] leading-6 whitespace-pre-wrap">${content}</div>`;
}

function fileDetailsHtml(file) {
  return `
    <div><strong>${file.path}</strong></div>
    <div class="mt-1 text-[#8a8a8a]">Size: ${file.size} B</div>
  `;
}

function updateFileEditorState(saveBtn, badge, isDirty) {
  if (saveBtn) saveBtn.disabled = !isDirty;
  if (badge) {
    badge.textContent = isDirty ? 'UNSAVED' : 'SAVED';
    badge.className = `rounded-full px-2 py-0.5 text-[10px] ${
      isDirty ? 'bg-amber-500/20 text-amber-300' : 'bg-emerald-500/20 text-emerald-300'
    }`;
  }
}

async function saveActiveFile() {
  if (!state.selectedFilePath) return;
  const file = state.openFiles.find((f) => f.path === state.selectedFilePath);
  if (!file) return;
  const draft = file.draft ?? file.content ?? '';
  if (draft === (file.content ?? '')) {
    setStatus('No changes to save');
    return;
  }
  try {
    setStatus(`Saving ${file.path}...`);
    const data = await saveFile(file.path, draft);
    file.content = draft;
    file.draft = draft;
    file.isDirty = false;
    if (typeof data?.size === 'number') file.size = data.size;
    setStatus(`Saved ${file.path}`);
    render();
  } catch (err) {
    setStatus(`Save failed: ${err.message}`);
  }
}

async function reloadActiveFile() {
  if (!state.selectedFilePath) return;
  const file = state.openFiles.find((f) => f.path === state.selectedFilePath);
  if (!file) return;
  try {
    setStatus(`Reloading ${file.path}...`);
    const data = await loadFile(file.path);
    file.content = data.content;
    file.draft = data.content;
    file.isDirty = false;
    file.size = data.size;
    setStatus(`Reloaded ${file.path}`);
    render();
  } catch (err) {
    setStatus(`Reload failed: ${err.message}`);
  }
}

function bindEditorShortcuts() {
  if (editorShortcutsBound) return;
  editorShortcutsBound = true;
  document.addEventListener('keydown', (event) => {
    if (state.activeView !== 'files') return;
    if (!(event.ctrlKey || event.metaKey)) return;
    if (event.key.toLowerCase() !== 's') return;
    event.preventDefault();
    saveActiveFile();
  });
}

function renderTaskEditor(editorEl, panelEl) {
  if (!state.selectedTaskId) {
    editorEl.innerHTML = '<div class="text-[#8a8a8a]">Select a task on the left</div>';
    panelEl.textContent = 'No data';
    return;
  }
  const data = state.taskData || {};
  renderTaskContent(editorEl, data);
  renderTaskDetails(panelEl, data);
}

function renderTaskContent(editorEl, data) {
  const content = data[state.selectedTab];
  if (content === undefined) {
    editorEl.innerHTML = '<div class="text-[#8a8a8a]">No data for this tab</div>';
    return;
  }
  if (typeof content === 'object') {
    editorEl.innerHTML = fileContentHtml(JSON.stringify(content, null, 2));
    return;
  }
  editorEl.innerHTML = fileContentHtml(content);
}

function renderTaskDetails(panelEl, data) {
  const result = data['result.json'];
  if (!result) {
    panelEl.textContent = 'No data';
    return;
  }
  panelEl.innerHTML = taskDetailsHtml(result);
}

function taskDetailsHtml(result) {
  const statusBadge = result.verification?.passed
    ? '<span class="ml-2 rounded-full bg-emerald-500/20 px-2 py-0.5 text-[10px] text-emerald-300">PASS</span>'
    : '<span class="ml-2 rounded-full bg-rose-500/20 px-2 py-0.5 text-[10px] text-rose-300">FAIL</span>';
  return `
    <div><strong>${result.id}</strong> ${statusBadge}</div>
    <div class="mt-1 text-[#8a8a8a]">${result.description}</div>
    <div style="margin-top:8px;">Status: ${result.status}</div>
    <div>Score: ${result.verification?.score ?? 0}</div>
  `;
}
