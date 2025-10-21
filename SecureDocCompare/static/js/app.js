// Global state
let currentDocumentPairId = null;
let currentProcessId = null;
let statusCheckInterval = null;
let lastResult = null;

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    if (uploadForm) {
        uploadForm.addEventListener('submit', handleUpload);
    }
});

// Handle file upload
async function handleUpload(event) {
    event.preventDefault();

    const uploadBtn = document.getElementById('uploadBtn');
    const oldFile = document.getElementById('oldDocument').files[0];
    const newFile = document.getElementById('newDocument').files[0];

    if (!oldFile || !newFile) {
        showStatus('Wybierz oba pliki', 'error');
        return;
    }

    // Disable button
    uploadBtn.disabled = true;
    uploadBtn.innerHTML = '<span class="spinner"></span> Wysyłanie...';

    try {
        const formData = new FormData();
        formData.append('old_document', oldFile);
        formData.append('new_document', newFile);

        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || 'Błąd uploadu');
        }

        currentDocumentPairId = result.document_pair_id;

        showStatus('✅ Dokumenty zostały wgrane pomyślnie!', 'success');
        showActionArea();

    } catch (error) {
        console.error('Upload error:', error);
        showStatus('❌ ' + error.message, 'error');
    } finally {
        uploadBtn.disabled = false;
        uploadBtn.innerHTML = '📤 Wgraj dokumenty';
    }
}

// Start processing
async function startProcessing() {
    if (!currentDocumentPairId) {
        showStatus('Najpierw wgraj dokumenty', 'error');
        return;
    }

    showProgress(0, 'Rozpoczynam analizę...');

    try {
        const response = await fetch(`/api/process/${currentDocumentPairId}`, {
            method: 'POST'
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || 'Błąd przetwarzania');
        }

        currentProcessId = result.process_id;
        showStatus('⚙️ Analiza rozpoczęta', 'info');

        // Show status button
        document.getElementById('statusBtn').style.display = 'inline-block';

        // Start checking status
        startStatusPolling();

    } catch (error) {
        console.error('Processing error:', error);
        showStatus('❌ ' + error.message, 'error');
        hideProgress();
    }
}

// Check status manually
async function checkStatus() {
    if (!currentProcessId) {
        showStatus('Brak aktywnego procesu', 'error');
        return;
    }

    try {
        const response = await fetch(`/api/status/${currentProcessId}`);
        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || 'Błąd pobierania statusu');
        }

        updateProgress(result);

    } catch (error) {
        console.error('Status error:', error);
        showStatus('❌ ' + error.message, 'error');
    }
}

// Start polling status
function startStatusPolling() {
    if (statusCheckInterval) {
        clearInterval(statusCheckInterval);
    }

    statusCheckInterval = setInterval(async () => {
        try {
            const response = await fetch(`/api/status/${currentProcessId}`);
            const result = await response.json();

            if (response.ok) {
                updateProgress(result);

                if (result.status === 'completed') {
                    stopStatusPolling();
                    showStatus('✅ Analiza zakończona pomyślnie!', 'success');
                    showResultsArea();
                } else if (result.status === 'error') {
                    stopStatusPolling();
                    showStatus('❌ Błąd: ' + (result.error || 'Nieznany błąd'), 'error');
                    hideProgress();
                }
            }
        } catch (error) {
            console.error('Polling error:', error);
        }
    }, 2000); // Check every 2 seconds
}

// Stop polling
function stopStatusPolling() {
    if (statusCheckInterval) {
        clearInterval(statusCheckInterval);
        statusCheckInterval = null;
    }
}

// Update progress
function updateProgress(status) {
    const progress = status.progress || 0;
    const message = status.message || 'Przetwarzanie...';

    showProgress(progress, message);
}

// Get full result
async function getFullResult() {
    await getResult('full', 'Pełny dokument');
}

// Get modified
async function getModified() {
    await getResult('modified', 'Zmodyfikowane zdania');
}

// Get added
async function getAdded() {
    await getResult('added', 'Dodane zdania');
}

// Get deleted
async function getDeleted() {
    await getResult('deleted', 'Usunięte zdania');
}

// Generic get result
async function getResult(type, title) {
    if (!currentProcessId) {
        showStatus('Brak wyników do wyświetlenia', 'error');
        return;
    }

    try {
        const response = await fetch(`/api/result/${currentProcessId}/${type}`);
        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || 'Błąd pobierania wyników');
        }

        lastResult = result;
        displayResult(result, title);

    } catch (error) {
        console.error('Result error:', error);
        showStatus('❌ ' + error.message, 'error');
    }
}

// Display result
function displayResult(result, title) {
    const resultDisplay = document.getElementById('resultDisplay');
    const resultTitle = document.getElementById('resultTitle');
    const resultContent = document.getElementById('resultContent');

    resultTitle.textContent = title;
    resultContent.textContent = JSON.stringify(result, null, 2);

    resultDisplay.style.display = 'block';
    resultDisplay.scrollIntoView({ behavior: 'smooth' });
}

// Download result as JSON
function downloadResult() {
    if (!lastResult) {
        showStatus('Brak wyniku do pobrania', 'error');
        return;
    }

    const dataStr = JSON.stringify(lastResult, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });

    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `result_${currentProcessId}.json`;
    link.click();

    URL.revokeObjectURL(url);
    showStatus('✅ Wynik został pobrany', 'success');
}

// Copy result to clipboard
async function copyResult() {
    if (!lastResult) {
        showStatus('Brak wyniku do skopiowania', 'error');
        return;
    }

    try {
        const text = JSON.stringify(lastResult, null, 2);
        await navigator.clipboard.writeText(text);
        showStatus('✅ Wynik skopiowany do schowka', 'success');
    } catch (error) {
        console.error('Copy error:', error);
        showStatus('❌ Nie można skopiować', 'error');
    }
}

// UI Helpers
function showStatus(message, type) {
    const statusArea = document.getElementById('statusArea');
    const statusMessage = document.getElementById('statusMessage');

    statusMessage.className = `alert alert-${type}`;
    statusMessage.textContent = message;
    statusArea.style.display = 'block';
}

function showProgress(progress, message) {
    const progressArea = document.getElementById('progressArea');
    const progressBar = document.getElementById('progressBar');
    const progressText = document.getElementById('progressText');

    progressBar.style.width = progress + '%';
    progressText.textContent = `${progress}% - ${message}`;
    progressArea.style.display = 'block';
}

function hideProgress() {
    const progressArea = document.getElementById('progressArea');
    progressArea.style.display = 'none';
}

function showActionArea() {
    document.getElementById('actionArea').style.display = 'block';
}

function showResultsArea() {
    document.getElementById('resultsArea').style.display = 'block';
}
