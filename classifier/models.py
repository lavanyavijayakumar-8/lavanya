import os
from django.db import models
from django.utils import timezone

class ClassificationRecord(models.Model):
    """
    Stores historical image classification uploads, neural predictions,
    confidence metrics, and Grad-CAM heatmap overlays.
    """
    DOMAIN_CHOICES = [
        ('plants', 'Plant & Agriculture'),
        ('animals', 'Animal & Wildlife'),
        ('vehicles', 'Vehicle & Transportation'),
        ('waste', 'Waste & Recyclable'),
        ('medical', 'Medical & Clinical'),
        ('auto', 'Auto-Detect Universal')
    ]

    image = models.ImageField(upload_to='uploads/%Y/%m/%d/')
    heatmap_image = models.ImageField(upload_to='heatmaps/%Y/%m/%d/', null=True, blank=True)
    domain = models.CharField(max_length=50, choices=DOMAIN_CHOICES)
    predicted_label = models.CharField(max_length=150)
    confidence = models.FloatField(help_text="Percentage confidence score (0-100)")
    top_predictions = models.JSONField(default=list, help_text="Ranked top-k classes with confidence")
    insights = models.JSONField(default=dict, help_text="Taxonomy, environmental or clinical insights")
    inference_time_ms = models.FloatField(default=0.0, help_text="Model execution duration in milliseconds")
    notes = models.TextField(blank=True, help_text="Optional user notes or remarks")
    created_at = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Classification Record'
        verbose_name_plural = 'Classification Records'

    def __str__(self):
        return f"[{self.get_domain_display()}] {self.predicted_label} ({self.confidence:.1f}%)"

    @property
    def filename(self):
        return os.path.basename(self.image.name) if self.image else ""


class SampleImage(models.Model):
    """
    Curated repository of demo sample images for instant 1-click test evaluations.
    """
    title = models.CharField(max_length=150)
    domain = models.CharField(max_length=50)
    expected_label = models.CharField(max_length=150)
    image = models.ImageField(upload_to='samples/')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['domain', 'title']
        verbose_name = 'Demo Sample Image'
        verbose_name_plural = 'Demo Sample Images'

    def __str__(self):
        return f"[{self.domain.upper()}] {self.title} -> {self.expected_label}"
