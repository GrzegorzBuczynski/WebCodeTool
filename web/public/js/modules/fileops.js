// File Operations Module
import { state, setStatus, render } from './state.js';
import { createFile, deleteFile, createFolder } from './api.js';
import { initExplorer, selectFile } from './explorer.js';

let fileOpsModalOpen = false;

export function showNewFileModal() {
  const modalHtml = `
    <div id="file-ops-modal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div class="w-96 rounded-lg border border-[#3c3c3c] bg-[#252526] p-6 shadow-xl">
        <h2 class="mb-4 text-lg font-semibold text-[#d4d4d4]">Create New File</h2>
        <div class="mb-4">
          <label class="mb-2 block text-sm text-[#8a8a8a]">File Path</label>
          <input 
            id="new-file-path" 
            type="text" 
            class="w-full rounded border border-[#3c3c3c] bg-[#1e1e1e] px-3 py-2 text-sm text-[#d4d4d4] outline-none focus:border-[#007acc]"
            placeholder="e.g., src/newfile.txt or newfile.js"
          />
          <p class="mt-1 text-xs text-[#8a8a8a]">Enter relative path from project root</p>
        </div>
        <div class="flex justify-end gap-2">
          <button id="file-ops-cancel" class="rounded border border-[#3c3c3c] bg-[#1e1e1e] px-4 py-2 text-sm text-[#d4d4d4] hover:bg-white/10">
            Cancel
          </button>
          <button id="file-ops-create" class="rounded bg-[#007acc] px-4 py-2 text-sm font-semibold text-white hover:bg-[#3794ff]">
            Create
          </button>
        </div>
      </div>
    </div>
  `;
  
  document.body.insertAdjacentHTML('beforeend', modalHtml);
  fileOpsModalOpen = true;
  
  const modal = document.getElementById('file-ops-modal');
  const input = document.getElementById('new-file-path');
  const cancelBtn = document.getElementById('file-ops-cancel');
  const createBtn = document.getElementById('file-ops-create');
  
  input.focus();
  
  const close = () => {
    modal.remove();
    fileOpsModalOpen = false;
  };
  
  cancelBtn.addEventListener('click', close);
  
  modal.addEventListener('click', (e) => {
    if (e.target === modal) close();
  });
  
  createBtn.addEventListener('click', async () => {
    const filePath = input.value.trim();
    if (!filePath) {
      alert('Please enter a file path');
      return;
    }
    
    close();
    await handleCreateFile(filePath);
  });
  
  input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      createBtn.click();
    } else if (e.key === 'Escape') {
      close();
    }
  });
}

export function showNewFolderModal() {
  const modalHtml = `
    <div id="file-ops-modal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div class="w-96 rounded-lg border border-[#3c3c3c] bg-[#252526] p-6 shadow-xl">
        <h2 class="mb-4 text-lg font-semibold text-[#d4d4d4]">Create New Folder</h2>
        <div class="mb-4">
          <label class="mb-2 block text-sm text-[#8a8a8a]">Folder Path</label>
          <input 
            id="new-folder-path" 
            type="text" 
            class="w-full rounded border border-[#3c3c3c] bg-[#1e1e1e] px-3 py-2 text-sm text-[#d4d4d4] outline-none focus:border-[#007acc]"
            placeholder="e.g., src/components or utils"
          />
          <p class="mt-1 text-xs text-[#8a8a8a]">Enter relative path from project root</p>
        </div>
        <div class="flex justify-end gap-2">
          <button id="folder-ops-cancel" class="rounded border border-[#3c3c3c] bg-[#1e1e1e] px-4 py-2 text-sm text-[#d4d4d4] hover:bg-white/10">
            Cancel
          </button>
          <button id="folder-ops-create" class="rounded bg-[#007acc] px-4 py-2 text-sm font-semibold text-white hover:bg-[#3794ff]">
            Create
          </button>
        </div>
      </div>
    </div>
  `;
  
  document.body.insertAdjacentHTML('beforeend', modalHtml);
  fileOpsModalOpen = true;
  
  const modal = document.getElementById('file-ops-modal');
  const input = document.getElementById('new-folder-path');
  const cancelBtn = document.getElementById('folder-ops-cancel');
  const createBtn = document.getElementById('folder-ops-create');
  
  input.focus();
  
  const close = () => {
    modal.remove();
    fileOpsModalOpen = false;
  };
  
  cancelBtn.addEventListener('click', close);
  
  modal.addEventListener('click', (e) => {
    if (e.target === modal) close();
  });
  
  createBtn.addEventListener('click', async () => {
    const folderPath = input.value.trim();
    if (!folderPath) {
      alert('Please enter a folder path');
      return;
    }
    
    close();
    await handleCreateFolder(folderPath);
  });
  
  input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      createBtn.click();
    } else if (e.key === 'Escape') {
      close();
    }
  });
}

export function showDeleteConfirmModal(filePath, callback) {
  const modalHtml = `
    <div id="file-ops-modal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div class="w-96 rounded-lg border border-[#3c3c3c] bg-[#252526] p-6 shadow-xl">
        <h2 class="mb-4 text-lg font-semibold text-rose-400">Delete File</h2>
        <p class="mb-4 text-sm text-[#d4d4d4]">
          Are you sure you want to delete this file?
        </p>
        <p class="mb-4 rounded bg-[#1e1e1e] p-2 text-xs text-[#8a8a8a]">${filePath}</p>
        <p class="mb-4 text-xs text-rose-400">This action cannot be undone.</p>
        <div class="flex justify-end gap-2">
          <button id="delete-cancel" class="rounded border border-[#3c3c3c] bg-[#1e1e1e] px-4 py-2 text-sm text-[#d4d4d4] hover:bg-white/10">
            Cancel
          </button>
          <button id="delete-confirm" class="rounded bg-rose-600 px-4 py-2 text-sm font-semibold text-white hover:bg-rose-700">
            Delete
          </button>
        </div>
      </div>
    </div>
  `;
  
  document.body.insertAdjacentHTML('beforeend', modalHtml);
  fileOpsModalOpen = true;
  
  const modal = document.getElementById('file-ops-modal');
  const cancelBtn = document.getElementById('delete-cancel');
  const confirmBtn = document.getElementById('delete-confirm');
  
  const close = () => {
    modal.remove();
    fileOpsModalOpen = false;
  };
  
  cancelBtn.addEventListener('click', close);
  
  modal.addEventListener('click', (e) => {
    if (e.target === modal) close();
  });
  
  confirmBtn.addEventListener('click', () => {
    close();
    callback();
  });
}

async function handleCreateFile(filePath) {
  try {
    setStatus(`Creating file ${filePath}...`);
    await createFile(filePath, '');
    setStatus(`File created: ${filePath}`);
    await initExplorer();
    await selectFile(filePath);
    render();
  } catch (err) {
    setStatus(`Failed to create file: ${err.message}`);
    alert(`Failed to create file: ${err.message}`);
  }
}

async function handleCreateFolder(folderPath) {
  try {
    setStatus(`Creating folder ${folderPath}...`);
    await createFolder(folderPath);
    setStatus(`Folder created: ${folderPath}`);
    await initExplorer();
    render();
  } catch (err) {
    setStatus(`Failed to create folder: ${err.message}`);
    alert(`Failed to create folder: ${err.message}`);
  }
}

export async function handleDeleteFile(filePath) {
  showDeleteConfirmModal(filePath, async () => {
    try {
      setStatus(`Deleting file ${filePath}...`);
      await deleteFile(filePath);
      
      // Remove from open files
      const index = state.openFiles.findIndex((f) => f.path === filePath);
      if (index !== -1) {
        state.openFiles.splice(index, 1);
      }
      
      // Clear selection if deleted file was selected
      if (state.selectedFilePath === filePath) {
        state.selectedFilePath = null;
      }
      
      setStatus(`File deleted: ${filePath}`);
      await initExplorer();
      render();
    } catch (err) {
      setStatus(`Failed to delete file: ${err.message}`);
      alert(`Failed to delete file: ${err.message}`);
    }
  });
}
