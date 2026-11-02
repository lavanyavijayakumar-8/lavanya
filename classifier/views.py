import io
import os
import json
import base64
from PIL import Image

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from django.core.paginator import Paginator
from django.db.models import Avg, Count

from .models import ClassificationRecord, SampleImage
from .models_ai.taxonomy import DOMAINS, CLASS_DETAILS
from .models_ai.inference_engine import ClassificationEngine, ALL_CLASSES

# Helper to execute prediction and save database record
def run_classification_pipeline(pil_image, target_domain=None, notes="", original_filename="uploaded_image.jpg"):
    engine = ClassificationEngine.get_instance()
    
    # Run PyTorch CNN inference & Grad-CAM visualizer
    result = engine.predict(pil_image, target_domain=target_domain)
    
    # Prepare image buffers for Django ImageField storage
    img_byte_arr = io.BytesIO()
    pil_image.convert('RGB').save(img_byte_arr, format='JPEG', quality=92)
    img_byte_arr.seek(0)
    
    cam_byte_arr = io.BytesIO()
    result['overlay_cam'].save(cam_byte_arr, format='JPEG', quality=90)
    cam_byte_arr.seek(0)
    
    # Save record to database
    record = ClassificationRecord(
        domain=result['predicted_domain'],
        predicted_label=result['predicted_class'],
        confidence=result['confidence'],
        top_predictions=result['top_predictions'],
        insights={
            'details': result['details'],
            'domain_name': result['domain_name'],
            'domain_icon': result['domain_icon'],
            'domain_color': result['domain_color'],
            'domain_badge': result['domain_badge'],
            'disclaimer': result['disclaimer'],
            'features': result['features']
        },
        inference_time_ms=result['inference_time_ms'],
        notes=notes
    )
    
    clean_name = os.path.splitext(os.path.basename(original_filename))[0] or "scan"
    record.image.save(f"{clean_name}.jpg", ContentFile(img_byte_arr.getvalue()), save=False)
    record.heatmap_image.save(f"{clean_name}_cam.jpg", ContentFile(cam_byte_arr.getvalue()), save=False)
    record.save()
    
    return record, result


def index(request):
    """
    Main landing dashboard with summary stats, category highlights,
    quick classification widget, and demo test gallery.
    """
    recent_records = ClassificationRecord.objects.all()[:6]
    samples = SampleImage.objects.all()[:8]
    
    total_scans = ClassificationRecord.objects.count()
    avg_speed = ClassificationRecord.objects.aggregate(Avg('inference_time_ms'))['inference_time_ms__avg'] or 34.8
    
    context = {
        'domains': DOMAINS,
        'recent_records': recent_records,
        'samples': samples,
        'total_scans': total_scans,
        'total_classes': len(ALL_CLASSES),
        'avg_speed': round(avg_speed, 1),
        'page_title': 'Deep Learning Multi-Category Image Classifier'
    }
    return render(request, 'classifier/index.html', context)


def classify_view(request):
    """
    Dedicated interactive classification workstation supporting file upload,
    camera snapshot, sample selection, and target domain override.
    """
    selected_domain = request.GET.get('domain', 'auto')
    sample_id = request.GET.get('sample_id')
    record = None
    result_data = None
    
    # Check if a sample image was requested via query param
    if request.method == 'GET' and sample_id:
        sample = get_object_or_404(SampleImage, id=sample_id)
        try:
            pil_img = Image.open(sample.image.path)
            t_domain = sample.domain if selected_domain == 'auto' else selected_domain
            record, result_data = run_classification_pipeline(
                pil_img, 
                target_domain=t_domain, 
                notes=f"Quick test from sample: {sample.title}",
                original_filename=sample.image.name
            )
        except Exception as e:
            print(f"Error classifying sample: {e}")
            
    elif request.method == 'POST':
        target_domain = request.POST.get('domain', 'auto')
        if target_domain == 'auto':
            target_domain = None
        notes = request.POST.get('notes', '').strip()
        
        # Handle camera data (base64) or regular file upload
        camera_data = request.POST.get('camera_data', '')
        uploaded_file = request.FILES.get('image')
        
        pil_img = None
        filename = "capture.jpg"
        
        if camera_data and camera_data.startswith('data:image'):
            try:
                format_prefix, imgstr = camera_data.split(';base64,')
                image_bytes = base64.b64decode(imgstr)
                pil_img = Image.open(io.BytesIO(image_bytes))
                filename = "webcam_snapshot.jpg"
            except Exception as e:
                print(f"Error parsing webcam image: {e}")
                
        elif uploaded_file:
            try:
                pil_img = Image.open(uploaded_file)
                filename = uploaded_file.name
            except Exception as e:
                print(f"Error opening uploaded file: {e}")
                
        if pil_img:
            record, result_data = run_classification_pipeline(
                pil_img, 
                target_domain=target_domain, 
                notes=notes,
                original_filename=filename
            )

    samples = SampleImage.objects.all()
    context = {
        'domains': DOMAINS,
        'selected_domain': selected_domain,
        'record': record,
        'result_data': result_data,
        'samples': samples,
        'page_title': 'AI Classification Studio'
    }
    return render(request, 'classifier/classify.html', context)


def record_detail(request, record_id):
    """
    Displays full detailed report of a historical classification.
    """
    record = get_object_or_404(ClassificationRecord, id=record_id)
    domain_info = DOMAINS.get(record.domain, {})
    class_details = CLASS_DETAILS.get(record.predicted_label, {})
    
    context = {
        'record': record,
        'domain_info': domain_info,
        'class_details': class_details,
        'domains': DOMAINS,
        'page_title': f"Report: {record.predicted_label}"
    }
    return render(request, 'classifier/record_detail.html', context)


def categories_view(request):
    """
    Taxonomy and Domain Knowledge Base Explorer for all 5 categories.
    """
    selected_domain = request.GET.get('domain', 'all')
    
    filtered_domains = {}
    if selected_domain in DOMAINS:
        filtered_domains[selected_domain] = DOMAINS[selected_domain]
    else:
        filtered_domains = DOMAINS
        
    context = {
        'domains': DOMAINS,
        'filtered_domains': filtered_domains,
        'selected_domain': selected_domain,
        'class_details': CLASS_DETAILS,
        'page_title': 'Supported Classification Domains'
    }
    return render(request, 'classifier/categories.html', context)


def cnn_explorer_view(request):
    """
    Interactive visual architectural guide to Convolutional Neural Networks,
    feature hierarchies, mathematical formulations, and Grad-CAM mechanics.
    """
    context = {
        'domains': DOMAINS,
        'total_classes': len(ALL_CLASSES),
        'page_title': 'Interactive CNN Architecture Explorer'
    }
    return render(request, 'classifier/cnn_explorer.html', context)


def history_view(request):
    """
    Prediction history view with filtering, search, and export capability.
    """
    query = request.GET.get('q', '').strip()
    domain_filter = request.GET.get('domain', 'all')
    
    records = ClassificationRecord.objects.all()
    
    if domain_filter in DOMAINS:
        records = records.filter(domain=domain_filter)
        
    if query:
        records = records.filter(predicted_label__icontains=query)
        
    paginator = Paginator(records, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'domains': DOMAINS,
        'query': query,
        'domain_filter': domain_filter,
        'total_count': records.count(),
        'page_title': 'Classification History & Audits'
    }
    return render(request, 'classifier/history.html', context)


def delete_record(request, record_id):
    """
    Deletes a specific classification record from the history.
    """
    if request.method == 'POST':
        record = get_object_or_404(ClassificationRecord, id=record_id)
        record.delete()
    return redirect('history')


def clear_history(request):
    """
    Clears all classification records.
    """
    if request.method == 'POST':
        ClassificationRecord.objects.all().delete()
    return redirect('history')


def about_view(request):
    """
    Comprehensive project documentation, objectives, methodologies,
    limitations, and ethical guidelines.
    """
    context = {
        'domains': DOMAINS,
        'total_classes': len(ALL_CLASSES),
        'page_title': 'Project Documentation & Methodology'
    }
    return render(request, 'classifier/about.html', context)


def api_docs_view(request):
    """
    REST API documentation and integration guide with code examples.
    """
    context = {
        'domains': DOMAINS,
        'page_title': 'REST API Developer Documentation'
    }
    return render(request, 'classifier/api_docs.html', context)


@csrf_exempt
def api_classify(request):
    """
    RESTful JSON API endpoint for image classification.
    Accepts:
    - Multipart Form: 'image' (file), optional 'domain'
    - JSON: 'image_base64', optional 'domain'
    - Query/Form: 'sample_id'
    """
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Only POST requests are supported.'}, status=405)
        
    target_domain = request.POST.get('domain') or request.GET.get('domain')
    if target_domain == 'auto':
        target_domain = None
        
    sample_id = request.POST.get('sample_id') or request.GET.get('sample_id')
    uploaded_file = request.FILES.get('image')
    
    pil_img = None
    filename = "api_request.jpg"
    
    if sample_id:
        sample = get_object_or_404(SampleImage, id=sample_id)
        pil_img = Image.open(sample.image.path)
        filename = sample.image.name
    elif uploaded_file:
        pil_img = Image.open(uploaded_file)
        filename = uploaded_file.name
    else:
        # Check JSON base64
        try:
            body = json.loads(request.body.decode('utf-8'))
            b64_data = body.get('image_base64', '')
            if b64_data:
                if ';base64,' in b64_data:
                    b64_data = b64_data.split(';base64,')[1]
                pil_img = Image.open(io.BytesIO(base64.b64decode(b64_data)))
            target_domain = body.get('domain', target_domain)
        except Exception:
            pass

    if not pil_img:
        return JsonResponse({'status': 'error', 'message': 'No image provided. Upload a file or provide base64/sample_id.'}, status=400)

    try:
        record, result = run_classification_pipeline(
            pil_img, 
            target_domain=target_domain, 
            notes="API Request",
            original_filename=filename
        )
        
        response_payload = {
            'status': 'success',
            'record_id': record.id,
            'prediction': {
                'class_name': result['predicted_class'],
                'domain_id': result['predicted_domain'],
                'domain_name': result['domain_name'],
                'confidence_percentage': result['confidence'],
                'inference_time_ms': result['inference_time_ms']
            },
            'top_predictions': result['top_predictions'],
            'domain_metadata': result['details'],
            'visual_features': result['features'],
            'image_urls': {
                'original': request.build_absolute_uri(record.image.url),
                'heatmap': request.build_absolute_uri(record.heatmap_image.url) if record.heatmap_image else None
            },
            'disclaimer': result['disclaimer']
        }
        return JsonResponse(response_payload)
        
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
