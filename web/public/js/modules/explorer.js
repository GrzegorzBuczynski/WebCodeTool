// File Explorer Component
import { state, setStatus, render } from './state.js';
import { loadFileTree, loadFile } from './api.js';

export async function initExplorer() {
  state.fileTree = await loadFileTree();
  state.collapsedDirs = new Set(getAllDirPaths(state.fileTree));
  state.expandLevel = 1;
  renderFileTree();
}

export function renderFileTree() {
  const fileTreeEl = document.getElementById('file-tree');
  if (!fileTreeEl) return;
  
  fileTreeEl.innerHTML = '';
  if (!state.fileTree.length) {
    fileTreeEl.innerHTML = '<div class="text-[#8a8a8a]">No files</div>';
    return;
  }
  state.fileTree.forEach((node) => renderTreeNode(node, fileTreeEl, 0));
}

export function collapseAllLevels() {
  state.collapsedDirs = new Set(getAllDirPaths(state.fileTree));
  renderFileTree();
}

export function expandAllLevels() {
  state.collapsedDirs = new Set();
  state.expandLevel = getMaxDepth(state.fileTree) || 1;
  renderFileTree();
}

export function expandNextLevel() {
  const maxDepth = getMaxDepth(state.fileTree) || 1;
  const nextLevel = state.expandLevel >= maxDepth ? 1 : state.expandLevel + 1;
  state.expandLevel = nextLevel;
  state.collapsedDirs = new Set(getDirsDeeperThan(state.fileTree, nextLevel));
  renderFileTree();
}

export function collapseNextLevel() {
  const currentLevel = getExpandedLevel(state.fileTree);
  const nextLevel = Math.min(1, currentLevel - 1);
  state.expandLevel = nextLevel;
  state.collapsedDirs = new Set(getDirsDeeperThan(state.fileTree, nextLevel));
  renderFileTree();
}

function renderTreeNode(node, container, depth) {
  if (node.type === 'dir') {
    renderDirNode(node, container, depth);
    return;
  }
  renderFileNode(node, container, depth);
}

function renderDirNode(node, container, depth) {
  const row = createTreeRow(depth, node.path);
  const isCollapsed = state.collapsedDirs.has(node.path);
  row.innerHTML = `
    <span class="w-3 text-[#8a8a8a]">${isCollapsed ? '▸' : '▾'}</span>
    <span class="text-[11px] text-[#8a8a8a]">📁</span>
    <span>${node.name || 'root'}</span>
  `;
  row.onclick = () => toggleDir(node.path);
  container.appendChild(row);
  if (!isCollapsed && node.children) {
    node.children.forEach((child) => renderTreeNode(child, container, depth + 1));
  }
}

function renderFileNode(node, container, depth) {
  const row = createTreeRow(depth, node.path);
  if (state.selectedFilePath === node.path) {
    row.classList.add('bg-[#007acc]/20', 'text-white');
  }
  row.innerHTML = `
    <span class="w-3"></span>
    <span class="text-[11px] text-[#8a8a8a]">📄</span>
    <span>${node.name}</span>
  `;
  row.onclick = () => selectFile(node.path);
  container.appendChild(row);
}

function createTreeRow(depth, path) {
  const row = document.createElement('div');
  row.className = 'flex items-center gap-2 rounded px-1 py-0.5 text-[#d4d4d4] hover:bg-white/5 cursor-pointer';
  row.style.paddingLeft = `${depth * 12}px`;
  row.dataset.path = path || '';
  return row;
}

function toggleDir(path) {
  if (state.collapsedDirs.has(path)) {
    state.collapsedDirs.delete(path);
  } else {
    state.collapsedDirs.add(path);
  }
  state.expandLevel = getExpandedLevel(state.fileTree);
  renderFileTree();
}

function getAllDirPaths(nodes, acc = []) {
  nodes.forEach((node) => {
    if (node.type === 'dir') {
      acc.push(node.path);
      if (node.children?.length) {
        getAllDirPaths(node.children, acc);
      }
    }
  });
  return acc;
}

function getDirsDeeperThan(nodes, level, depth = 0, acc = []) {
  nodes.forEach((node) => {
    if (node.type === 'dir') {
      if (depth >= level) {
        acc.push(node.path);
      }
      if (node.children?.length) {
        getDirsDeeperThan(node.children, level, depth + 1, acc);
      }
    }
  });
  return acc;
}

function getMaxDepth(nodes, depth = 0) {
  let max = depth;
  nodes.forEach((node) => {
    if (node.type === 'dir' && node.children?.length) {
      const childDepth = getMaxDepth(node.children, depth + 1);
      if (childDepth > max) max = childDepth;
    }
  });
  return max;
}

function getExpandedLevel(nodes, depth = 0, parentExpanded = true) {
  let maxLevel = 1;
  nodes.forEach((node) => {
    if (node.type !== 'dir') return;
    const isExpanded = parentExpanded && !state.collapsedDirs.has(node.path);
    if (isExpanded) {
      maxLevel = Math.max(maxLevel, depth + 1);
    }
    if (isExpanded && node.children?.length) {
      const childMax = getExpandedLevel(node.children, depth + 1, isExpanded);
      if (childMax > maxLevel) maxLevel = childMax;
    }
  });
  return maxLevel;
}

export async function selectFile(filePath) {
  state.selectedFilePath = filePath;
  renderFileTree();
  setStatus(`Loading ${filePath}...`);
  
  const existing = state.openFiles.find((f) => f.path === filePath);
  if (existing) {
    setStatus(`Showing ${filePath}`);
    render();
    return;
  }
  
  const data = await loadFile(filePath);
  state.openFiles.push({
    path: data.path,
    size: data.size,
    content: data.content,
    draft: data.content,
    isDirty: false
  });
  setStatus(`Showing ${filePath}`);
  render();
}
