// State Management Module
export const state = {
  tasks: [],
  selectedTaskId: null,
  selectedTab: 'output.txt',
  taskData: {},
  fileTree: [],
  openFiles: [],
  selectedFilePath: null,
  collapsedDirs: new Set(),
  activeView: 'files',
  rootPath: '',
  rootOptions: [],
  modalCurrentPath: '',
  modalSelectedPath: '',
  modalFolders: [],
  expandLevel: 1
};

export const tabs = [
  'output.txt',
  'report.txt',
  'result.json',
  'stats.json',
  'hierarchy.json',
  'detailed_report.json'
];

export function setStatus(text) {
  const statusEl = document.getElementById('status-text');
  if (statusEl) statusEl.textContent = text;
}

export function setRootLabel(path) {
  const rootLabel = document.getElementById('root-label');
  if (rootLabel) rootLabel.textContent = path || 'none';
}

export async function render() {
  const { renderTabs } = await import('./tabs.js');
  const { renderEditor } = await import('./editor.js');
  renderTabs();
  renderEditor();
}
