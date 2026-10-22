/**
 * Interactive Client-Side Controller for Deep Learning Image Classifier.
 * Handles drag & drop, camera capture, Grad-CAM toggle, and UI states.
 */

document.addEventListener('DOMContentLoaded', () => {
    initDropzone();
    initViewerToggle();
    initCameraModal();
    initDomainPills();
});

/**
 * Drag and Drop & File Upload Preview Handler
 */
function initDropzone() {
    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('imageInput');
    const previewContainer = document.getElementById('previewContainer');
    const previewImg = document.getElementById('imagePreview');
    const dropzoneContent = document.getElementById('dropzoneContent');

    if (!dropzone || !fileInput) return;

    // Trigger file dialog on dropzone click
    dropzone.addEventListener('click', (e) => {
        if (e.target.closest('.camera-btn') || e.target.closest('.clear-btn')) return;
        fileInput.click();
    });

    // Drag-over styling
    ['dragenter', 'dragover'].forEach(eventName => {
        dropzone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropzone.classList.add('dragover');
        });
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropzone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropzone.classList.remove('dragover');
        });
    });

    // File dropped
    dropzone.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        const files = dt.files;
        if (files.length > 0) {
            fileInput.files = files;
            showFilePreview(files[0]);
        }
    });

    // File selected via dialog
    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            showFilePreview(fileInput.files[0]);
        }
    });

    function showFilePreview(file) {
        if (!file.type.startsWith('image/')) {
            alert('Please select a valid image file (JPEG, PNG, WebP).');
            return;
        }

        const reader = new FileReader();
        reader.onload = (e) => {
            if (previewImg) {
                previewImg.src = e.target.result;
            }
            if (previewContainer) {
                previewContainer.style.display = 'block';
            }
            if (dropzoneContent) {
                dropzoneContent.style.display = 'none';
            }
            const submitBtn = document.getElementById('submitBtn');
            if (submitBtn) {
                submitBtn.disabled = false;
                submitBtn.classList.add('pulse');
            }
        };
        reader.readAsDataURL(file);
    }
}

/**
 * Toggle between Original Image and Grad-CAM Activation Heatmap
 */
function initViewerToggle() {
    const toggleBtns = document.querySelectorAll('.viewer-toggle-btn');
    const originalImg = document.getElementById('displayOriginal');
    const heatmapImg = document.getElementById('displayHeatmap');

    if (!toggleBtns.length || !originalImg || !heatmapImg) return;

    toggleBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            toggleBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const viewMode = btn.dataset.view;
            if (viewMode === 'heatmap') {
                originalImg.style.display = 'none';
                heatmapImg.style.display = 'block';
            } else {
                originalImg.style.display = 'block';
                heatmapImg.style.display = 'none';
            }
        });
    });
}

/**
 * Domain Pill Radio Selector
 */
function initDomainPills() {
    const pills = document.querySelectorAll('.domain-pill');
    const domainInput = document.getElementById('targetDomainInput');

    if (!pills.length || !domainInput) return;

    pills.forEach(pill => {
        pill.addEventListener('click', () => {
            pills.forEach(p => p.classList.remove('active'));
            pill.classList.add('active');
            domainInput.value = pill.dataset.domain;
        });
    });
}

/**
 * Web Camera Snapshot Capture
 */
let cameraStream = null;

function initCameraModal() {
    const cameraBtn = document.getElementById('openCameraBtn');
    const modal = document.getElementById('cameraModal');
    const video = document.getElementById('cameraVideo');
    const captureBtn = document.getElementById('capturePhotoBtn');
    const closeBtn = document.getElementById('closeCameraBtn');
    const cameraDataInput = document.getElementById('cameraDataInput');
    const previewImg = document.getElementById('imagePreview');
    const previewContainer = document.getElementById('previewContainer');
    const dropzoneContent = document.getElementById('dropzoneContent');

    if (!cameraBtn || !modal || !video) return;

    cameraBtn.addEventListener('click', async (e) => {
        e.stopPropagation();
        modal.classList.add('active');
        try {
            cameraStream = await navigator.mediaDevices.getUserMedia({ 
                video: { width: { ideal: 1280 }, height: { ideal: 720 }, facingMode: 'environment' } 
            });
            video.srcObject = cameraStream;
            video.play();
        } catch (err) {
            console.error('Camera access error:', err);
            alert('Could not access camera. Please allow camera permissions or upload an image file.');
            modal.classList.remove('active');
        }
    });

    function stopCamera() {
        if (cameraStream) {
            cameraStream.getTracks().forEach(track => track.stop());
            cameraStream = null;
        }
        modal.classList.remove('active');
    }

    if (closeBtn) closeBtn.addEventListener('click', stopCamera);
    modal.addEventListener('click', (e) => {
        if (e.target === modal) stopCamera();
    });

    if (captureBtn) {
        captureBtn.addEventListener('click', () => {
            const canvas = document.createElement('canvas');
            canvas.width = video.videoWidth || 640;
            canvas.height = video.videoHeight || 480;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
            
            const dataUrl = canvas.toDataURL('image/jpeg', 0.92);
            if (cameraDataInput) cameraDataInput.value = dataUrl;
            if (previewImg) previewImg.src = dataUrl;
            if (previewContainer) previewContainer.style.display = 'block';
            if (dropzoneContent) dropzoneContent.style.display = 'none';

            const submitBtn = document.getElementById('submitBtn');
            if (submitBtn) submitBtn.disabled = false;

            stopCamera();
        });
    }
}
