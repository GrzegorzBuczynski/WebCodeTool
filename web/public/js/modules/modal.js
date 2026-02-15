// Root Selection Modal Component
import { state, setRootLabel, setStatus } from './state.js';
import { loadModalFolders, applyRootSelection } from './api.js';

export function openRootModal() {
  state.modalCurrentPath = state.rootPath || getHomeDir();
  state.modalSelectedPath = state.modalCurrentPath;
  const rootModal = document.getElementById('root-modal');
  rootModal.classList.remove('hidden');
  rootModal.classList.add('flex');
  loadModalFoldersAndRender();
}

export function closeRootModal() {
  const rootModal = document.getElementById('root-modal');
  rootModal.classList.add('hidden');
  rootModal.classList.remove('flex');
}

function getHomeDir() {
  return '/home';
}

function getParentPath(path) {
  const parts = path.split('/').filter(Boolean);
  parts.pop();
  return '/' + parts.join('/');
}

export function renderBreadcrumb() {
  const rootBreadcrumbEl = document.getElementById('root-breadcrumb');
  if (!rootBreadcrumbEl) return;
  
  rootBreadcrumbEl.innerHTML = '';
  const parts = state.modalCurrentPath.split('/').filter(Boolean);
  
  const rootBtn = document.createElement('button');
  rootBtn.className = 'px-2 py-1 hover:bg-white/10 rounded';
  rootBtn.textContent = '/';
  rootBtn.onclick = () => navigateToPath('/');
  rootBreadcrumbEl.appendChild(rootBtn);
  
  let currentPath = '';
  parts.forEach((part) => {
    currentPath += '/' + part;
    const sep = document.createElement('span');
    sep.className = 'text-[#8a8a8a]';
    sep.textContent = '/';
    rootBreadcrumbEl.appendChild(sep);
    
    const btn = document.createElement('button');
    btn.className = 'px-2 py-1 hover:bg-white/10 rounded';
    btn.textContent = part;
    const pathToNavigate = currentPath;
    btn.onclick = () => navigateToPath(pathToNavigate);
    rootBreadcrumbEl.appendChild(btn);
  });
}

export function renderModalExplorer() {
  const rootExplorerEl = document.getElementById('root-explorer');
  if (!rootExplorerEl) return;
  
  rootExplorerEl.innerHTML = '';
  if (!state.modalFolders.length) {
    rootExplorerEl.innerHTML = '<div class="text-[#8a8a8a] py-2">No folders</div>';
    return;
  }
  
  state.modalFolders.forEach((folder) => {
    const row = document.createElement('div');
    row.className = 'flex items-center gap-2 rounded px-2 py-2 text-[#d4d4d4] hover:bg-white/10 cursor-pointer';
    if (state.modalSelectedPath === folder.path) {
      row.classList.add('bg-[#007acc]/20');
    }
    
    row.innerHTML = `
      <span class="text-[14px]">📁</span>
      <span class="flex-1">${folder.name}</span>
    `;
    
    row.ondblclick = () => navigateToPath(folder.path);
    row.onclick = () => {
      state.modalSelectedPath = folder.path;
      renderModalExplorer();
      renderSelectedPath();
    };
    
    rootExplorerEl.appendChild(row);
  });
}

export function renderSelectedPath() {
  const rootSelectedEl = document.getElementById('root-selected');
  if (rootSelectedEl) {
    rootSelectedEl.textContent = state.modalSelectedPath || 'Not selected';
  }
}

export async function navigateToPath(path) {
  state.modalCurrentPath = path;
  state.modalSelectedPath = path;
  renderBreadcrumb();
  renderSelectedPath();
  await loadModalFoldersAndRender();
}

async function loadModalFoldersAndRender() {
  try {
    state.modalFolders = await loadModalFolders(state.modalCurrentPath);
    renderModalExplorer();
    renderBreadcrumb();
    renderSelectedPath();
  } catch (err) {
    console.error('Failed to load folders:', err);
    state.modalFolders = [];
    renderModalExplorer();
  }
}

export function bindRootModalEvents() {
  const rootCloseBtn = document.getElementById('root-close');
  const rootCancelBtn = document.getElementById('root-cancel');
  const rootApplyBtn = document.getElementById('root-apply');
  const rootUpBtn = document.getElementById('root-up');
  const rootHomeBtn = document.getElementById('root-home');
  
  if (rootCloseBtn) rootCloseBtn.addEventListener('click', closeRootModal);
  if (rootCancelBtn) rootCancelBtn.addEventListener('click', closeRootModal);
  if (rootApplyBtn) {
    rootApplyBtn.addEventListener('click', async () => {
      const path = await applyRootSelection(state.modalSelectedPath);
      state.rootPath = path;
      setRootLabel(path);
      state.openFiles = [];
      state.selectedFilePath = null;
      state.collapsedDirs = new Set();
      closeRootModal();
      
      const { initExplorer } = await import('./explorer.js');
      await initExplorer();
      const { renderTabs } = await import('./tabs.js');
      const { renderEditor } = await import('./editor.js');
      renderTabs();
      renderEditor();
    });
  }
  if (rootUpBtn) {
    rootUpBtn.addEventListener('click', () => {
      const parentPath = getParentPath(state.modalCurrentPath);
      if (parentPath !== state.modalCurrentPath) {
        navigateToPath(parentPath);
      }
    });
  }
  if (rootHomeBtn) {
    rootHomeBtn.addEventListener('click', () => navigateToPath(getHomeDir()));
  }
}
