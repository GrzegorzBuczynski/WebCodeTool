// Tasks Component
import { state, setStatus, render } from './state.js';
import { loadTasks, loadTask, runTask } from './api.js';

export async function initTasks() {
  setStatus('Loading tasks...');
  const { tasks, total } = await loadTasks();
  state.tasks = tasks;
  renderTaskList();
  setStatus(`Ready • ${total} tasks`);
  render();
  
  if (!state.selectedTaskId && state.tasks.length) {
    await selectTask(state.tasks[0].id);
  }
}

export function renderTaskList() {
  const taskListEl = document.getElementById('task-list');
  if (!taskListEl) return;
  
  taskListEl.innerHTML = '';
  if (!state.tasks.length) {
    taskListEl.innerHTML = '<div class="text-[#8a8a8a]">No tasks</div>';
    return;
  }
  state.tasks.forEach((task) => {
    const item = document.createElement('div');
    item.className = taskCardClass(task.id);
    item.innerHTML = taskCardHtml(task);
    item.onclick = () => selectTask(task.id);
    taskListEl.appendChild(item);
  });
}

function taskCardClass(taskId) {
  return `cursor-pointer rounded border bg-[#1f1f1f] p-2 text-xs ${
    state.selectedTaskId === taskId
      ? 'border-[#007acc] ring-1 ring-[#007acc]/60'
      : 'border-[#3c3c3c]'
  }`;
}

function taskCardHtml(task) {
  const badgeClass = task.verified
    ? 'bg-emerald-500/20 text-emerald-300'
    : task.status === 'failed'
      ? 'bg-rose-500/20 text-rose-300'
      : 'bg-amber-500/20 text-amber-300';
  return `
    <div class="flex items-center justify-between">
      <span class="font-semibold">${task.id}</span>
      <span class="rounded-full px-2 py-0.5 text-[10px] ${badgeClass}">${task.verified ? 'OK' : task.status}</span>
    </div>
    <div class="mt-1 text-[11px] text-[#8a8a8a]">${task.description}</div>
    <div class="mt-1 text-[11px] text-[#d4d4d4]/80">${task.preview}</div>
  `;
}

export async function selectTask(taskId) {
  state.selectedTaskId = taskId;
  state.taskData = {};
  renderTaskList();
  setStatus(`Loading ${taskId}...`);
  state.taskData = await loadTask(taskId);
  setStatus(`Showing ${taskId}`);
  render();
}

export async function handleRunTask() {
  const taskInput = document.getElementById('task-input');
  const runHint = document.getElementById('run-hint');
  
  const description = taskInput.value.trim();
  if (!description) {
    runHint.textContent = 'Enter a task description.';
    return;
  }
  runHint.textContent = '';
  setStatus('Running task...');
  
  await runTask(description);
  taskInput.value = '';
  runHint.textContent = 'Task started. Refresh in a moment.';
  setTimeout(initTasks, 4000);
}
