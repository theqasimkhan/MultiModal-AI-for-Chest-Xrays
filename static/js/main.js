document.addEventListener('DOMContentLoaded', () => {
    // Elements
    const elements = {
        imageInput: document.getElementById('imageInput'),
        dropZone: document.getElementById('dropZone'),
        fileInfo: document.getElementById('fileInfo'),
        fileName: document.getElementById('fileName'),
        previewImage: document.getElementById('previewImage'),
        analyzeBtn: document.getElementById('analyzeBtn'),
        loadingOverlay: document.getElementById('loadingOverlay'),
        resultsSection: document.getElementById('resultsSection'),
        findingsList: document.getElementById('findingsList'),
        reportText: document.getElementById('reportText'),
        reportDate: document.getElementById('reportDate'),
        clinicalIndication: document.getElementById('clinicalIndication'),
        examDate: document.getElementById('examDate'),
        patientName: document.getElementById('patientName'),
        xrayDisplay: document.querySelector('.xray-display'),
        askBtn: document.getElementById('askBtn'),
        questionInput: document.getElementById('questionInput'),
        chatMessages: document.getElementById('chatMessages'),

        // Tabs
        newReportTab: document.getElementById('newReportTab'),
        historyTab: document.getElementById('historyTab'),
        newReportView: document.getElementById('newReportView'),
        historyView: document.getElementById('historyView'),
        historyList: document.getElementById('historyList'),
        searchInput: document.getElementById('searchInput')
    };

    let currentFile = null;
    let currentImagePath = null;

    // Set default date
    elements.examDate.valueAsDate = new Date();
    elements.reportDate.textContent = new Date().toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });

    // Tab Switching
    elements.newReportTab.addEventListener('click', () => {
        elements.newReportTab.classList.add('active');
        elements.historyTab.classList.remove('active');
        elements.newReportTab.style.borderBottom = '2px solid var(--primary)';
        elements.newReportTab.style.color = 'var(--primary)';
        elements.historyTab.style.borderBottom = 'none';
        elements.historyTab.style.color = 'var(--text-muted)';

        elements.newReportView.style.display = 'block';
        elements.historyView.style.display = 'none';
    });

    elements.historyTab.addEventListener('click', () => {
        elements.historyTab.classList.add('active');
        elements.newReportTab.classList.remove('active');
        elements.historyTab.style.borderBottom = '2px solid var(--primary)';
        elements.historyTab.style.color = 'var(--primary)';
        elements.newReportTab.style.borderBottom = 'none';
        elements.newReportTab.style.color = 'var(--text-muted)';

        elements.historyView.style.display = 'flex';
        elements.newReportView.style.display = 'none';
        loadHistory();
    });

    // History & Search
    async function loadHistory(query = '') {
        elements.historyList.innerHTML = '<div style="text-align:center; padding: 1rem;">Loading...</div>';
        try {
            const res = await fetch(`/history?q=${encodeURIComponent(query)}`);
            const data = await res.json();

            elements.historyList.innerHTML = '';
            if (data.reports.length === 0) {
                elements.historyList.innerHTML = '<div style="text-align:center; padding: 1rem; color: var(--text-muted);">No reports found</div>';
                return;
            }

            data.reports.forEach(report => {
                const item = document.createElement('div');
                item.style.padding = '1rem';
                item.style.border = '1px solid var(--border)';
                item.style.borderRadius = '0.5rem';
                item.style.cursor = 'pointer';
                item.style.background = 'var(--surface)';
                item.style.marginBottom = '0.5rem';
                item.innerHTML = `
                    <div style="font-weight: 600; color: var(--text-main);">${report.patient_name}</div>
                    <div style="font-size: 0.8rem; color: var(--text-muted);">${report.exam_date}</div>
                `;
                item.onclick = () => loadReport(report);
                elements.historyList.appendChild(item);
            });
        } catch (e) {
            elements.historyList.innerHTML = `<div style="color: red; padding: 1rem;">Error: ${e.message}</div>`;
        }
    }

    elements.searchInput.addEventListener('input', (e) => {
        loadHistory(e.target.value);
    });

    function loadReport(report) {
        // Switch to main view but maybe keep history tab active? Or switch to "View Mode"
        // For simplicity, let's populate the main view
        currentImagePath = report.image_path;

        // Display Image (need to handle path correctly if it's relative)
        // Assuming image_path is relative to where server runs or accessible via static
        // Since we save full path, we might need to adjust for web access if not in static
        // But for now let's try setting src directly if it's in uploads which is not static by default in Flask unless configured
        // Actually, we need a route to serve uploaded files or move uploads to static.
        // For now, let's assume the backend serves it or we can't show it easily without a route.
        // Let's just show the text data.

        elements.reportText.textContent = '';
        typeWriter(report.report_text, elements.reportText, 1); // Fast typing

        // Parse findings
        const findings = JSON.parse(report.findings);
        displayFindings(findings);

        elements.resultsSection.style.display = 'block';
        elements.chatMessages.innerHTML = ''; // Clear chat
    }

    // File Upload Handling
    elements.dropZone.addEventListener('click', () => elements.imageInput.click());

    elements.dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        elements.dropZone.classList.add('dragover');
    });

    elements.dropZone.addEventListener('dragleave', () => {
        elements.dropZone.classList.remove('dragover');
    });

    elements.dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        elements.dropZone.classList.remove('dragover');
        handleFile(e.dataTransfer.files[0]);
    });

    elements.imageInput.addEventListener('change', (e) => {
        handleFile(e.target.files[0]);
    });

    function handleFile(file) {
        if (!file || !file.type.startsWith('image/')) return;

        currentFile = file;
        elements.fileName.textContent = file.name;
        elements.fileInfo.style.display = 'block';
        elements.analyzeBtn.disabled = false;

        const reader = new FileReader();
        reader.onload = (e) => {
            elements.previewImage.src = e.target.result;
            elements.previewImage.style.display = 'block';
        };
        reader.readAsDataURL(file);
    }

    // Analysis Logic
    elements.analyzeBtn.addEventListener('click', () => {
        if (!currentFile) return;

        // Reset UI
        elements.resultsSection.style.display = 'none';
        elements.loadingOverlay.classList.add('active');
        elements.xrayDisplay.classList.add('scanning');
        elements.analyzeBtn.disabled = true;

        const formData = new FormData();
        formData.append('file', currentFile);
        formData.append('clinical_indication', elements.clinicalIndication.value);
        formData.append('date', elements.examDate.value);
        formData.append('patient_name', elements.patientName.value || 'Anonymous');

        fetch('/upload_and_analyze', {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                if (data.error) throw new Error(data.error);
                displayResults(data);
            })
            .catch(error => {
                alert('Error: ' + error.message);
            })
            .finally(() => {
                elements.loadingOverlay.classList.remove('active');
                elements.xrayDisplay.classList.remove('scanning');
                elements.analyzeBtn.disabled = false;
            });
    });

    function displayResults(data) {
        currentImagePath = data.image_path;
        elements.resultsSection.style.display = 'block';
        displayFindings(data.cv_findings);

        // Typewriter effect for report
        elements.reportText.textContent = '';
        typeWriter(data.medical_report, elements.reportText);
    }

    function displayFindings(findingsData) {
        elements.findingsList.innerHTML = '';

        // Sort findings by probability
        const sortedFindings = Object.entries(findingsData)
            .sort(([, a], [, b]) => b.probability - a.probability);

        // Animate findings
        sortedFindings.forEach(([name, info], index) => {
            const item = document.createElement('div');
            item.className = 'finding-item';
            item.style.animation = `slideUp 0.5s ease-out forwards ${index * 0.1}s`;
            item.style.opacity = '0';

            const percentage = (info.probability * 100).toFixed(1);

            item.innerHTML = `
                <div class="finding-header">
                    <span>${name}</span>
                    <span>${percentage}%</span>
                </div>
                <div class="probability-bar">
                    <div class="probability-fill" style="width: 0%"></div>
                </div>
            `;

            elements.findingsList.appendChild(item);

            // Trigger bar animation after a small delay
            setTimeout(() => {
                item.querySelector('.probability-fill').style.width = `${percentage}%`;
            }, 100 + (index * 100));
        });
    }

    function typeWriter(text, element, speed = 10) {
        let i = 0;
        element.textContent = '';
        function type() {
            if (i < text.length) {
                element.textContent += text.charAt(i);
                i++;
                setTimeout(type, speed);
            }
        }
        type();
    }

    // Chat / Question Answering
    elements.askBtn.addEventListener('click', async () => {
        const question = elements.questionInput.value.trim();
        if (!question || !currentImagePath) return;

        // Add user message
        addMessage(question, 'user');
        elements.questionInput.value = '';
        elements.askBtn.disabled = true;

        try {
            const response = await fetch('/question', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    question: question,
                    image_path: currentImagePath
                })
            });

            const data = await response.json();

            if (data.error) throw new Error(data.error);

            addMessage(data.answer, 'ai');

        } catch (error) {
            addMessage('Error: ' + error.message, 'ai');
        } finally {
            elements.askBtn.disabled = false;
        }
    });

    function addMessage(text, type) {
        const div = document.createElement('div');
        div.className = `message ${type}`;
        div.textContent = text;
        elements.chatMessages.appendChild(div);
        elements.chatMessages.scrollTop = elements.chatMessages.scrollHeight;
    }
});
