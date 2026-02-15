/**
 * Template loader module
 * Loads HTML templates and injects them into the DOM
 */

async function loadTemplate(templateName) {
  try {
    const response = await fetch(`/templates/${templateName}.html`);
    if (!response.ok) throw new Error(`Failed to load template: ${templateName}`);
    return await response.text();
  } catch (error) {
    console.error(error);
    return '';
  }
}

function createElementFromHTML(htmlString) {
  const div = document.createElement('div');
  div.innerHTML = htmlString.trim();
  return div.firstChild;
}

async function initializeTemplates() {
  const mainGrid = document.getElementById('main-grid');
  if (!mainGrid) return;
  
  // Load and insert header
  const headerHTML = await loadTemplate('header');
  const headerEl = createElementFromHTML(headerHTML);
  mainGrid.appendChild(headerEl);
  
  // Create middle grid container
  const middleGrid = document.createElement('div');
  middleGrid.className = 'grid grid-cols-[52px_300px_1fr] overflow-hidden';
  
  // Load and insert sidebar
  const sidebarHTML = await loadTemplate('sidebar');
  const sidebarEl = createElementFromHTML(sidebarHTML);
  middleGrid.appendChild(sidebarEl);
  
  // Load and insert explorer panel
  const explorerHTML = await loadTemplate('explorer-panel');
  const explorerEl = createElementFromHTML(explorerHTML);
  middleGrid.appendChild(explorerEl);
  
  // Load and insert editor
  const editorHTML = await loadTemplate('editor');
  const editorEl = createElementFromHTML(editorHTML);
  middleGrid.appendChild(editorEl);
  
  mainGrid.appendChild(middleGrid);
  
  // Load and insert details panel
  const detailsHTML = await loadTemplate('details-panel');
  const detailsEl = createElementFromHTML(detailsHTML);
  mainGrid.appendChild(detailsEl);
  
  // Load and insert modal
  const modalHTML = await loadTemplate('modal');
  const modalEl = createElementFromHTML(modalHTML);
  document.body.appendChild(modalEl);
}

export { loadTemplate, initializeTemplates };

