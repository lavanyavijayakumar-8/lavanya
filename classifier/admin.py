from django.contrib import admin
from .models import ClassificationRecord, SampleImage

@admin.register(ClassificationRecord)
class ClassificationRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'domain', 'predicted_label', 'confidence', 'inference_time_ms', 'created_at')
    list_filter = ('domain', 'created_at')
    search_fields = ('predicted_label', 'notes')
    readonly_fields = ('created_at', 'inference_time_ms')

@admin.register(SampleImage)
class SampleImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'domain', 'expected_label', 'created_at')
    list_filter = ('domain',)
    search_fields = ('title', 'expected_label')
