// Tabs Component
import { state, tabs, render } from './state.js';

export function renderTabs() {
  const tabsEl = document.getElementById('tabs');
  if (!tabsEl) return;
  
  tabsEl.innerHTML = '';
  if (state.activeView === 'files') {
    renderFileTabs();
    return;
  }
  if (state.activeView === 'tasks') {
    renderTaskTabs();
  }
}

function renderFileTabs() {
  const tabsEl = document.getElementById('tabs');
  if (!state.openFiles.length) {
    tabsEl.innerHTML = '<div class="rounded border border-[#3c3c3c] bg-[#1e1e1e] px-2 py-1 text-xs text-[#d4d4d4]">No open files</div>';
    return;
  }
  state.openFiles.forEach((file) => {
    const name = file.path.split('/').pop();
    const el = document.createElement('div');
    el.className = tabClass(state.selectedFilePath === file.path) + ' flex items-center gap-2';
    
    const label = document.createElement('span');
    label.textContent = file.isDirty ? `${name} ●` : name;
    label.onclick = () => selectOpenFile(file.path);
    el.appendChild(label);
    
    const closeBtn = document.createElement('button');
    closeBtn.className = 'hover:bg-white/20 rounded px-1';
    closeBtn.textContent = '✕';
    closeBtn.onclick = (e) => {
      e.stopPropagation();
      closeFile(file.path);
    };
    el.appendChild(closeBtn);
    
    tabsEl.appendChild(el);
  });
}

function renderTaskTabs() {
  const tabsEl = document.getElementById('tabs');
  tabs.forEach((tab) => {
    const el = document.createElement('div');
    el.className = tabClass(state.selectedTab === tab);
    el.textContent = tab;
    el.onclick = () => selectTaskTab(tab);
    tabsEl.appendChild(el);
  });
}

function tabClass(isActive) {
  return `cursor-pointer rounded border px-2 py-1 text-xs ${
    isActive
      ? 'border-[#3c3c3c] bg-[#1e1e1e] text-[#d4d4d4]'
      : 'border-transparent bg-[#2d2d2d] text-[#8a8a8a] hover:text-[#d4d4d4]'
  }`;
}

export function selectOpenFile(path) {
  state.selectedFilePath = path;
  render();
}

export function closeFile(path) {
  const index = state.openFiles.findIndex((f) => f.path === path);
  if (index === -1) return;
  state.openFiles.splice(index, 1);
  if (state.selectedFilePath === path) {
    state.selectedFilePath = state.openFiles[0]?.path || null;
  }
  render();
}

export function selectTaskTab(tab) {
  state.selectedTab = tab;
  render();
}
