/**
 * FileLens - Frontend Application
 */

const API_BASE = 'http://127.0.0.1:8000';

// State
let currentView = 'search';
let searchCount = 0;
let totalSearchTime = 0;

// DOM Elements
const searchInput = document.getElementById('search-input');
const searchBtn = document.getElementById('search-btn');
const resultsContainer = document.getElementById('results-container');
const navItems = document.querySelectorAll('.nav-item');
const views = document.querySelectorAll('.view');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    initSearch();
    initIndexView();
    initSettings();
    loadStats();
    checkHealth();
});

/**
 * Navigation
 */
function initNavigation() {
    navItems.forEach(item => {
        item.addEventListener('click', () => {
            const view = item.dataset.view;
            switchView(view);
            
            if (view === 'stats') {
                loadStats();
            }
        });
    });
}

function switchView(viewName) {
    currentView = viewName;
    
    // Update nav
    navItems.forEach(item => {
        item.classList.toggle('active', item.dataset.view === viewName);
    });
    
    // Update view
    views.forEach(view => {
        view.classList.toggle('active', view.id === `${viewName}-view`);
    });
}

/**
 * Search
 */
function initSearch() {
    searchBtn.addEventListener('click', performSearch);
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            performSearch();
        }
    });
}

async function performSearch() {
    const query = searchInput.value.trim();
    if (!query) return;
    
    const mode = document.querySelector('input[name="search-mode"]:checked').value;
    
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE}/search`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                query: query,
                mode: mode,
                max_results: parseInt(document.getElementById('setting-max-results')?.value || 20),
                threshold: parseFloat(document.querySelector('.threshold-value')?.textContent || 0.3)
            })
        });
        
        if (!response.ok) throw new Error('Search failed');
        
        const data = await response.json();
        
        // Update stats
        searchCount++;
        totalSearchTime += data.search_time_ms;
        
        displayResults(data);
    } catch (error) {
        showError('搜索失败: ' + error.message);
    }
}

function displayResults(data) {
    if (data.total_results === 0) {
        resultsContainer.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">😕</div>
                <p>未找到相关结果</p>
                <p class="empty-hint">尝试使用不同的关键词或搜索模式</p>
            </div>
        `;
        return;
    }
    
    const template = document.getElementById('result-template');
    const html = document.createElement('div');
    
    // Add search info
    const infoDiv = document.createElement('div');
    infoDiv.className = 'search-info';
    infoDiv.innerHTML = `<p style="color: var(--text-secondary); margin-bottom: 16px;">
        找到 ${data.total_results} 个结果 (${data.search_time_ms}ms)
    </p>`;
    html.appendChild(infoDiv);
    
    data.results.forEach(result => {
        const clone = template.content.cloneNode(true);
        const item = clone.querySelector('.result-item');
        
        // Set content
        clone.querySelector('.result-filename').textContent = result.document.filename;
        clone.querySelector('.result-path').textContent = result.document.filepath;
        clone.querySelector('.result-score').textContent = `Score: ${result.score.toFixed(3)}`;
        
        // Set icon based on file type
        const icon = clone.querySelector('.result-icon');
        icon.textContent = getFileIcon(result.document.file_type);
        
        // Set highlights
        const highlightsDiv = clone.querySelector('.result-highlights');
        if (result.highlights && result.highlights.length > 0) {
            result.highlights.forEach(hl => {
                const p = document.createElement('p');
                p.textContent = hl;
                highlightsDiv.appendChild(p);
            });
        }
        
        // Set up action buttons
        const openBtn = clone.querySelector('.open-btn');
        const folderBtn = clone.querySelector('.folder-btn');
        
        openBtn.addEventListener('click', () => openFile(result.document.filepath));
        folderBtn.addEventListener('click', () => showInFolder(result.document.filepath));
        
        html.appendChild(item);
    });
    
    resultsContainer.innerHTML = '';
    resultsContainer.appendChild(html);
}

function getFileIcon(fileType) {
    const icons = {
        'document': '📄',
        'code': '💻',
        'config': '⚙️',
        'other': '📎'
    };
    return icons[fileType] || '📎';
}

function showLoading() {
    resultsContainer.innerHTML = '<div class="loading">🔍 搜索中...</div>';
}

function showError(message) {
    resultsContainer.innerHTML = `<div class="error-message">${message}</div>`;
}

/**
 * Index View
 */
function initIndexView() {
    document.getElementById('add-folder-btn').addEventListener('click', addFolder);
    document.getElementById('clear-index-btn').addEventListener('click', clearIndex);
}

async function addFolder() {
    let folderPath;
    
    // Use Electron dialog if available
    if (window.electronAPI) {
        folderPath = await window.electronAPI.selectDirectory();
    } else {
        // Fallback for browser
        folderPath = prompt('请输入文件夹路径:');
    }
    
    if (!folderPath) return;
    
    showIndexingProgress(true);
    
    try {
        const response = await fetch(`${API_BASE}/index`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                paths: [folderPath],
                recursive: true,
                skip_existing: true
            })
        });
        
        if (!response.ok) throw new Error('Indexing failed');
        
        const data = await response.json();
        
        showIndexingProgress(false);
        
        if (data.success) {
            showSuccess(`索引完成! 成功: ${data.indexed_count}, 失败: ${data.failed_count}`);
            loadStats();
        } else {
            showError('索引失败: ' + (data.error || 'Unknown error'));
        }
    } catch (error) {
        showIndexingProgress(false);
        showError('索引失败: ' + error.message);
    }
}

async function clearIndex() {
    if (!confirm('确定要清空所有索引吗? 此操作不可恢复。')) return;
    
    try {
        const response = await fetch(`${API_BASE}/index`, {
            method: 'DELETE'
        });
        
        if (!response.ok) throw new Error('Clear failed');
        
        showSuccess('索引已清空');
        loadStats();
    } catch (error) {
        showError('清空失败: ' + error.message);
    }
}

function showIndexingProgress(show) {
    const progressDiv = document.getElementById('indexing-progress');
    progressDiv.style.display = show ? 'block' : 'none';
    
    if (show) {
        document.getElementById('progress-fill').style.width = '50%';
        document.getElementById('progress-text').textContent = '正在索引文件...';
    }
}

function showSuccess(message) {
    const div = document.createElement('div');
    div.className = 'success-message';
    div.textContent = message;
    
    const container = document.querySelector('.index-container');
    container.insertBefore(div, container.firstChild);
    
    setTimeout(() => div.remove(), 5000);
}

/**
 * Stats
 */
async function loadStats() {
    try {
        const response = await fetch(`${API_BASE}/stats`);
        if (!response.ok) throw new Error('Failed to load stats');
        
        const data = await response.json();
        
        // Update index view
        document.getElementById('doc-count').textContent = data.total_documents;
        document.getElementById('chunk-count').textContent = data.total_chunks;
        
        // Update stats view
        document.getElementById('stat-docs').textContent = data.total_documents;
        document.getElementById('stat-chunks').textContent = data.total_chunks;
        document.getElementById('stat-searches').textContent = searchCount;
        document.getElementById('stat-avg-time').textContent = 
            searchCount > 0 ? Math.round(totalSearchTime / searchCount) + 'ms' : '0ms';
        
    } catch (error) {
        console.error('Failed to load stats:', error);
    }
}

/**
 * Settings
 */
function initSettings() {
    const thresholdSlider = document.getElementById('setting-threshold');
    const thresholdValue = document.querySelector('.threshold-value');
    
    if (thresholdSlider) {
        thresholdSlider.addEventListener('input', (e) => {
            thresholdValue.textContent = (e.target.value / 100).toFixed(2);
        });
    }
}

/**
 * File Operations
 */
async function openFile(filePath) {
    if (window.electronAPI) {
        await window.electronAPI.openFile(filePath);
    } else {
        console.log('Open file:', filePath);
    }
}

async function showInFolder(filePath) {
    if (window.electronAPI) {
        await window.electronAPI.showInFolder(filePath);
    } else {
        console.log('Show in folder:', filePath);
    }
}

/**
 * Health Check
 */
async function checkHealth() {
    try {
        const response = await fetch(`${API_BASE}/health`);
        if (!response.ok) {
            showError('后端服务未运行，请检查服务状态');
        }
    } catch (error) {
        showError('无法连接到后端服务，请确保服务已启动');
    }
}
