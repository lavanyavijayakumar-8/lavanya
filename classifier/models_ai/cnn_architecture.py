"""
Deep Learning CNN Architectures & Class Activation Mapping (Grad-CAM) Visualizer.
Implements custom CNN blocks, Feature Extraction, and visual heatmaps.
"""

import math
import numpy as np
from PIL import Image
import torch
import torch.nn as nn
import torch.nn.functional as F

class ConvBlock(nn.Module):
    """
    Standard Convolutional Block:
    Conv2D -> BatchNorm2D -> LeakyReLU -> MaxPool2D
    """
    def __init__(self, in_channels, out_channels, pool=True):
        super(ConvBlock, self).__init__()
        self.conv = nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1, bias=False)
        self.bn = nn.BatchNorm2d(out_channels)
        self.act = nn.LeakyReLU(0.1, inplace=True)
        self.pool = nn.MaxPool2d(2, 2) if pool else nn.Identity()

    def forward(self, x):
        return self.pool(self.act(self.bn(self.conv(x))))


class MultiCategoryCNN(nn.Module):
    """
    Modular Convolutional Neural Network for Multi-Category Image Classification.
    Extracts multi-scale hierarchical spatial features (edges, textures, object parts).
    """
    def __init__(self, num_classes=33, in_channels=3):
        super(MultiCategoryCNN, self).__init__()
        
        # Feature Extraction Backbone
        self.block1 = ConvBlock(in_channels, 32)    # 224x224 -> 112x112
        self.block2 = ConvBlock(32, 64)            # 112x112 -> 56x56
        self.block3 = ConvBlock(64, 128)           # 56x56 -> 28x28
        self.block4 = ConvBlock(128, 256)          # 28x28 -> 14x14
        self.block5 = ConvBlock(256, 512, pool=False) # 14x14 -> 14x14
        
        self.global_pool = nn.AdaptiveAvgPool2d((1, 1))
        
        # Fully Connected Classifier Head
        self.classifier = nn.Sequential(
            nn.Dropout(0.35),
            nn.Linear(512, 256),
            nn.BatchNorm1d(256),
            nn.ReLU(inplace=True),
            nn.Dropout(0.25),
            nn.Linear(256, num_classes)
        )
        
        # Hook holders for Grad-CAM activation mapping
        self.gradients = None
        self.activations = None

    def activations_hook(self, grad):
        self.gradients = grad

    def forward(self, x):
        x = self.block1(x)
        x = self.block2(x)
        x = self.block3(x)
        x = self.block4(x)
        
        # Target layer for Grad-CAM
        x = self.block5(x)
        if x.requires_grad:
            h = x.register_hook(self.activations_hook)
        self.activations = x
        
        pooled = self.global_pool(x)
        flattened = torch.flatten(pooled, 1)
        out = self.classifier(flattened)
        return out


def generate_gradcam_heatmap(model, input_tensor, original_pil_image, target_class_idx=None):
    """
    Generates a Class Activation Map (CAM) heatmap visualization.
    Shows the spatial image regions that the CNN's convolutional filters focused on.
    """
    try:
        model.eval()
        input_tensor = input_tensor.clone().detach().requires_grad_(True)
        
        # Forward pass
        output = model(input_tensor)
        
        if target_class_idx is None:
            target_class_idx = output.argmax(dim=1).item()
            
        target_score = output[0, target_class_idx]
        
        # Zero grads and backward pass
        model.zero_grad()
        target_score.backward(retain_graph=True)
        
        # Pull saved activations and gradients
        activations = model.activations.detach() # [1, 512, H, W]
        if model.gradients is not None:
            gradients = model.gradients.detach() # [1, 512, H, W]
            weights = torch.mean(gradients, dim=(2, 3), keepdim=True)
            cam = torch.sum(weights * activations, dim=1, keepdim=True)
        else:
            # Fallback to direct channel activation mean
            cam = torch.mean(activations, dim=1, keepdim=True)
            
        cam = F.relu(cam) # Only positive activations
        cam = cam.squeeze().cpu().numpy()
        
        # Normalize between 0 and 1
        cam_min, cam_max = np.min(cam), np.max(cam)
        if cam_max > cam_min:
            cam = (cam - cam_min) / (cam_max - cam_min)
        else:
            cam = np.zeros_like(cam)
            
        # Resize CAM to match original image dimensions
        orig_w, orig_h = original_pil_image.size
        cam_img = Image.fromarray((cam * 255).astype(np.uint8)).resize((orig_w, orig_h), resample=Image.BILINEAR)
        cam_np = np.array(cam_img) / 255.0
        
        # Apply Jet / Turbo-style colormap (Blue -> Cyan -> Green -> Yellow -> Red)
        heatmap = apply_colormap(cam_np)
        
        # Blend original image and heatmap
        orig_np = np.array(original_pil_image.convert('RGB'))
        overlay = (0.55 * orig_np + 0.45 * heatmap).clip(0, 255).astype(np.uint8)
        
        return Image.fromarray(overlay), Image.fromarray(heatmap.astype(np.uint8))
        
    except Exception as e:
        print(f"CAM generation error: {e}")
        # Return fallback with subtle highlight
        return original_pil_image, original_pil_image


def apply_colormap(cam_norm):
    """
    Generates a vibrant jet/spectral RGB colormap from normalized [0, 1] 2D array.
    Implemented without external cv2 dependency for maximum portability.
    """
    h, w = cam_norm.shape
    r = np.clip(1.5 - np.abs(4.0 * cam_norm - 3.0), 0.0, 1.0)
    g = np.clip(1.5 - np.abs(4.0 * cam_norm - 2.0), 0.0, 1.0)
    b = np.clip(1.5 - np.abs(4.0 * cam_norm - 1.0), 0.0, 1.0)
    
    rgb = np.stack([r, g, b], axis=-1) * 255.0
    return rgb
