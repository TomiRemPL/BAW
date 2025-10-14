// Frontend JavaScript for document comparison application

// Configuration
const API_BASE = '';
const POLL_INTERVAL = 2000; // 2 seconds

// Active comparisons being polled
const activeComparisons = new Map();

/**
 * Start a document comparison
 */
async function startComparison(oldPath, newPath, mode) {
    try {
        // Disable buttons to prevent double-click
        const card = event.target.closest('[data-pair-name]');
        if (card) {
            const buttons = card.querySelectorAll('button');
            buttons.forEach(btn => btn.disabled = true);
        }

        // Show loading state
        showNotification(`Rozpoczynam porównanie w trybie ${mode}...`, 'info');

        // Convert backslashes to forward slashes for JSON compatibility
        const normalizedOldPath = oldPath.replace(/\\/g, '/');
        const normalizedNewPath = newPath.replace(/\\/g, '/');

        const response = await fetch(`${API_BASE}/api/compare`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                old_path: normalizedOldPath,
                new_path: normalizedNewPath,
                mode: mode
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        if (data.comparison_id) {
            showNotification('Porównanie rozpoczęte! Sprawdzam status...', 'success');

            // Start polling for status
            startPolling(data.comparison_id);

            // Refresh page after a short delay to show updated status
            setTimeout(() => {
                location.reload();
            }, 1000);
        } else {
            throw new Error('Nie otrzymano comparison_id');
        }

    } catch (error) {
        console.error('Error starting comparison:', error);
        showNotification(`Błąd podczas rozpoczynania porównania: ${error.message}`, 'error');

        // Re-enable buttons
        const card = event.target.closest('[data-pair-name]');
        if (card) {
            const buttons = card.querySelectorAll('button');
            buttons.forEach(btn => btn.disabled = false);
        }
    }
}

/**
 * Start polling for comparison status
 */
function startPolling(comparisonId) {
    if (activeComparisons.has(comparisonId)) {
        return; // Already polling
    }

    const intervalId = setInterval(async () => {
        try {
            const status = await checkComparisonStatus(comparisonId);

            if (status === 'completed') {
                clearInterval(intervalId);
                activeComparisons.delete(comparisonId);
                showNotification('Porównanie zakończone!', 'success');
                // Reload page to show completed status
                setTimeout(() => location.reload(), 1000);
            } else if (status === 'error') {
                clearInterval(intervalId);
                activeComparisons.delete(comparisonId);
                showNotification('Błąd podczas porównywania', 'error');
                setTimeout(() => location.reload(), 1000);
            }
        } catch (error) {
            console.error('Error polling status:', error);
            clearInterval(intervalId);
            activeComparisons.delete(comparisonId);
        }
    }, POLL_INTERVAL);

    activeComparisons.set(comparisonId, intervalId);
}

/**
 * Check comparison status
 */
async function checkComparisonStatus(comparisonId) {
    const response = await fetch(`${API_BASE}/api/compare/${comparisonId}/status`);

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data.status;
}

/**
 * View comparison report
 */
function viewReport(comparisonId) {
    window.location.href = `/report/${comparisonId}`;
}

/**
 * Download PDF report
 */
async function downloadPDF(comparisonId) {
    try {
        showNotification('Generuję PDF...', 'info');

        const response = await fetch(`${API_BASE}/api/download/${comparisonId}`);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        // Get filename from Content-Disposition header if available
        const contentDisposition = response.headers.get('Content-Disposition');
        let filename = `comparison_${comparisonId}.pdf`;

        if (contentDisposition) {
            const matches = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/.exec(contentDisposition);
            if (matches != null && matches[1]) {
                filename = matches[1].replace(/['"]/g, '');
            }
        }

        // Download file
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);

        showNotification('PDF pobrano pomyślnie!', 'success');

    } catch (error) {
        console.error('Error downloading PDF:', error);
        showNotification(`Błąd podczas pobierania PDF: ${error.message}`, 'error');
    }
}

/**
 * Show notification
 */
function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existing = document.querySelectorAll('.notification');
    existing.forEach(el => el.remove());

    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification fixed top-4 right-4 px-6 py-4 rounded-lg shadow-lg z-50 animate-fade-in`;

    // Set colors based on type
    const colors = {
        'info': 'bg-blue-500 text-white',
        'success': 'bg-green-500 text-white',
        'error': 'bg-red-500 text-white',
        'warning': 'bg-yellow-500 text-white'
    };

    notification.className += ` ${colors[type] || colors.info}`;
    notification.textContent = message;

    document.body.appendChild(notification);

    // Auto-remove after 5 seconds
    setTimeout(() => {
        notification.style.opacity = '0';
        notification.style.transition = 'opacity 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 5000);
}

/**
 * Search functionality for reports
 */
function setupSearch() {
    const searchInput = document.getElementById('report-search');
    if (!searchInput) return;

    searchInput.addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase();
        const rows = document.querySelectorAll('tbody tr');

        rows.forEach(row => {
            const text = row.textContent.toLowerCase();
            if (text.includes(query)) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    });
}

/**
 * Collapsible sections
 */
function setupCollapsible() {
    const collapsibleHeaders = document.querySelectorAll('.collapsible-header');

    collapsibleHeaders.forEach(header => {
        header.addEventListener('click', () => {
            const content = header.nextElementSibling;
            if (content && content.classList.contains('collapsible-content')) {
                content.classList.toggle('open');

                // Rotate arrow icon if exists
                const arrow = header.querySelector('.arrow-icon');
                if (arrow) {
                    arrow.style.transform = content.classList.contains('open')
                        ? 'rotate(90deg)'
                        : 'rotate(0deg)';
                }
            }
        });
    });
}

/**
 * Highlight text on hover
 */
function setupHighlighting() {
    const changeSections = document.querySelectorAll('[data-change-section]');

    changeSections.forEach(section => {
        section.addEventListener('mouseenter', () => {
            section.style.backgroundColor = 'rgba(0, 149, 151, 0.1)';
        });

        section.addEventListener('mouseleave', () => {
            section.style.backgroundColor = '';
        });
    });
}

/**
 * Copy to clipboard
 */
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showNotification('Skopiowano do schowka!', 'success');
    }).catch(err => {
        console.error('Error copying to clipboard:', err);
        showNotification('Nie udało się skopiować', 'error');
    });
}

/**
 * Initialize on page load
 */
document.addEventListener('DOMContentLoaded', () => {
    console.log('Document comparison app initialized');

    setupSearch();
    setupCollapsible();
    setupHighlighting();

    // Check if there are any processing comparisons to poll
    const processingElements = document.querySelectorAll('[data-comparison-id][data-status="processing"]');
    processingElements.forEach(el => {
        const comparisonId = el.dataset.comparisonId;
        if (comparisonId) {
            startPolling(comparisonId);
        }
    });
});

/**
 * Handle errors globally
 */
window.addEventListener('error', (event) => {
    console.error('Global error:', event.error);
});

window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason);
});
