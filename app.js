document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const fileInfo = document.getElementById('fileInfo');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const errorElement = document.getElementById('error');
    const resultsSection = document.getElementById('results');
    
    let selectedFile = null;
    let charts = {};

    // Handle drag and drop events
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => {
            dropZone.classList.add('drag-over');
        });
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => {
            dropZone.classList.remove('drag-over');
        });
    });

    // Handle file selection
    dropZone.addEventListener('drop', handleDrop);
    dropZone.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', handleFileSelect);

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const file = dt.files[0];
        handleFile(file);
    }

    function handleFileSelect(e) {
        const file = e.target.files[0];
        handleFile(file);
    }

    function handleFile(file) {
        if (file && file.name.endsWith('.txt')) {
            selectedFile = file;
            showFileInfo(file);
            hideError();
        } else {
            showError('Please upload a valid WhatsApp chat export file (.txt)');
        }
    }

    function showFileInfo(file) {
        const fileName = fileInfo.querySelector('.file-name');
        fileName.textContent = `${file.name} (${formatFileSize(file.size)})`;
        fileInfo.classList.remove('hidden');
    }

    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    function showError(message) {
        errorElement.textContent = message;
        errorElement.classList.remove('hidden');
    }

    function hideError() {
        errorElement.classList.add('hidden');
    }

    // Handle analysis
    analyzeBtn.addEventListener('click', async () => {
        if (!selectedFile) return;

        const formData = new FormData();
        formData.append('file', selectedFile);

        try {
            analyzeBtn.disabled = true;
            analyzeBtn.textContent = 'Analyzing...';

            const response = await fetch('http://localhost:5000/api/analyze', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Analysis failed. Please try again.');
            }

            const results = await response.json();
            displayResults(results);
        } catch (error) {
            showError(error.message);
        } finally {
            analyzeBtn.disabled = false;
            analyzeBtn.textContent = 'Analyze Chat';
        }
    });

    function displayResults(data) {
        // Update statistics
        document.getElementById('totalMessages').textContent = data.totalMessages.toLocaleString();
        document.getElementById('totalWords').textContent = data.totalWords.toLocaleString();
        document.getElementById('totalEmojis').textContent = data.totalEmojis.toLocaleString();
        document.getElementById('participants').textContent = data.participants.length;

        // Create/update charts
        createWordChart(data.topWords);
        createEmojiChart(data.topEmojis);
        createHourlyChart(data.hourlyActivity);

        // Show results section
        resultsSection.classList.remove('hidden');
    }

    function createWordChart(data) {
        const ctx = document.getElementById('wordChart');
        if (charts.wordChart) charts.wordChart.destroy();

        charts.wordChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.map(item => item.word),
                datasets: [{
                    label: 'Word Frequency',
                    data: data.map(item => item.count),
                    backgroundColor: 'rgba(12, 182, 167, 0.7)',
                    borderColor: 'rgba(12, 182, 167, 1)',
                    borderWidth: 1,
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    function createEmojiChart(data) {
        const ctx = document.getElementById('emojiChart');
        if (charts.emojiChart) charts.emojiChart.destroy();

        charts.emojiChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.map(item => item.emoji),
                datasets: [{
                    label: 'Emoji Frequency',
                    data: data.map(item => item.count),
                    backgroundColor: 'rgba(109, 96, 248, 0.7)',
                    borderColor: 'rgba(109, 96, 248, 1)',
                    borderWidth: 1,
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    function createHourlyChart(data) {
        const ctx = document.getElementById('hourlyChart');
        if (charts.hourlyChart) charts.hourlyChart.destroy();

        const sortedData = [...data].sort((a, b) => a.hour - b.hour);
        const formatHour = hour => {
            const ampm = hour < 12 ? 'AM' : 'PM';
            const displayHour = hour % 12 || 12;
            return `${displayHour} ${ampm}`;
        };

        charts.hourlyChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: sortedData.map(item => formatHour(item.hour)),
                datasets: [{
                    label: 'Messages',
                    data: sortedData.map(item => item.count),
                    borderColor: 'rgba(16, 185, 129, 1)',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    borderWidth: 2,
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
});