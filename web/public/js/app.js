// Main Application Entry Point
import { state, setStatus, setRootLabel, render } from './modules/state.js';
import { loadRootPath } from './modules/api.js';
import { initExplorer, renderFileTree, collapseAllLevels, collapseNextLevel, expandAllLevels, expandNextLevel } from './modules/explorer.js';
import { openRootModal, bindRootModalEvents } from './modules/modal.js';
import { initTasks, handleRunTask } from './modules/tasks.js';
import { initializeTemplates } from './modules/templates.js';
import { showNewFileModal, showNewFolderModal } from './modules/fileops.js';
import { renderTabs } from './modules/tabs.js';

function setActiveView(view) {
  state.activeView = view;
  const explorerSection = document.getElementById('explorer-section');
  const tasksSection = document.getElementById('tasks-section');
  const runSection = document.getElementById('run-section');
  const sidebarTitle = document.getElementById('sidebar-title');
  
  if (explorerSection) explorerSection.classList.toggle('hidden', view !== 'files');
  if (tasksSection) tasksSection.classList.toggle('hidden', view !== 'tasks');
  if (runSection) runSection.classList.toggle('hidden', view !== 'run');
  if (sidebarTitle) {
    sidebarTitle.textContent = view === 'files' ? 'Explorer' : view === 'tasks' ? 'Tasks' : 'Run';
  }
  render();
}

function bindActivityButtons() {
  document.querySelectorAll('.activity-btn').forEach((btn) => {
    btn.addEventListener('click', () => {
      setActiveView(btn.dataset.view);
      document.querySelectorAll('.activity-btn').forEach((b) => {
        b.classList.remove('bg-[#2d2d2d]', 'text-[#d4d4d4]');
      });
      btn.classList.add('bg-[#2d2d2d]', 'text-[#d4d4d4]');
    });
  });
}

function bindMenuEvents() {
  const menuFileBtn = document.getElementById('menu-file-btn');
  const menuFile = document.getElementById('menu-file');
  const menuOpenRoot = document.getElementById('menu-open-root');
  const menuViewBtn = document.getElementById('menu-view-btn');
  const menuView = document.getElementById('menu-view');
  const menuCollapseAll = document.getElementById('menu-collapse-all');
  const menuCollapseLevel = document.getElementById('menu-collapse-level');
  const menuExpandLevel = document.getElementById('menu-expand-level');
  const menuExpandAll = document.getElementById('menu-expand-all');
  
  if (menuFileBtn) {
    menuFileBtn.addEventListener('click', (event) => {
      event.stopPropagation();
      if (menuView) menuView.classList.add('hidden');
      menuFile.classList.toggle('hidden');
    });
  }
  if (menuOpenRoot) {
    menuOpenRoot.addEventListener('click', () => {
      menuFile.classList.add('hidden');
      openRootModal();
    });
  }
  if (menuViewBtn) {
    menuViewBtn.addEventListener('click', (event) => {
      event.stopPropagation();
      if (menuFile) menuFile.classList.add('hidden');
      menuView.classList.toggle('hidden');
    });
  }
  if (menuCollapseAll) {
    menuCollapseAll.addEventListener('click', () => {
      menuView.classList.add('hidden');
      collapseAllLevels();
    });
  }
  if (menuCollapseLevel) {
    menuCollapseLevel.addEventListener('click', () => {
      menuView.classList.add('hidden');
      collapseNextLevel();
    });
  }
  if (menuExpandLevel) {
    menuExpandLevel.addEventListener('click', () => {
      menuView.classList.add('hidden');
      expandNextLevel();
    });
  }
  if (menuExpandAll) {
    menuExpandAll.addEventListener('click', () => {
      menuView.classList.add('hidden');
      expandAllLevels();
    });
  }
  document.addEventListener('click', () => {
    if (menuFile) menuFile.classList.add('hidden');
    if (menuView) menuView.classList.add('hidden');
  });
}

function bindActionEvents() {
  const runBtn = document.getElementById('run-btn');
  const refreshBtn = document.getElementById('refresh-btn');
  const newFileBtn = document.getElementById('new-file-btn');
  const newFolderBtn = document.getElementById('new-folder-btn');
  
  if (runBtn) runBtn.addEventListener('click', handleRunTask);
  if (refreshBtn) {
    refreshBtn.addEventListener('click', async () => {
      await initExplorer();
      render();
    });
  }
  if (newFileBtn) {
    newFileBtn.addEventListener('click', showNewFileModal);
  }
  if (newFolderBtn) {
    newFolderBtn.addEventListener('click', showNewFolderModal);
  }
}

async function initApp() {
  // Load templates first
  await initializeTemplates();
  
  bindActivityButtons();
  bindMenuEvents();
  bindRootModalEvents();
  bindActionEvents();
  
  state.rootPath = await loadRootPath();
  setRootLabel(state.rootPath);
  
  renderTabs();
  await initExplorer();
  await initTasks();
  setActiveView('files');
}

initApp();
