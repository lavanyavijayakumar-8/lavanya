"""
Seeds authentic visual sample images for the 5 categories into media/samples/
and populates the SampleImage database table.
"""

import os
import django
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'multiclass_project.settings')
django.setup()

from classifier.models import SampleImage
from django.core.files import File

def draw_plant_leaf(filename, is_diseased=False, disease_type="early_blight"):
    img = Image.new('RGB', (600, 600), color=(240, 244, 241))
    draw = ImageDraw.Draw(img)
    
    # Background soft gradient or texture
    for y in range(600):
        shade = int(240 - y * 0.05)
        draw.line([(0, y), (600, y)], fill=(shade, shade + 5, shade))
        
    # Main Leaf Body
    leaf_color = (46, 125, 50) if not is_diseased else (67, 120, 52)
    # Draw leaf contour points
    points = [
        (300, 50), (370, 110), (430, 200), (450, 310), (410, 420),
        (340, 480), (300, 520), (260, 480), (190, 420), (150, 310),
        (170, 200), (230, 110)
    ]
    draw.polygon(points, fill=leaf_color, outline=(27, 94, 32))
    
    # Veins
    vein_color = (129, 199, 132) if not is_diseased else (100, 140, 90)
    draw.line([(300, 70), (300, 510)], fill=vein_color, width=6)
    for y_pos in range(120, 470, 45):
        draw.line([(300, y_pos), (300 + int(y_pos * 0.25), y_pos - 25)], fill=vein_color, width=3)
        draw.line([(300, y_pos), (300 - int(y_pos * 0.25), y_pos - 25)], fill=vein_color, width=3)
        
    if is_diseased:
        # Concentric brown blight lesions with chlorotic halos
        spots = [(260, 240, 35), (350, 320, 42), (230, 370, 28), (380, 210, 25), (280, 160, 22)]
        for (sx, sy, r) in spots:
            # Yellow chlorotic halo
            draw.ellipse([sx - r - 8, sy - r - 8, sx + r + 8, sy + r + 8], fill=(212, 175, 55))
            # Brown lesion rings
            draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(93, 64, 55))
            draw.ellipse([sx - int(r*0.6), sy - int(r*0.6), sx + int(r*0.6), sy + int(r*0.6)], fill=(62, 39, 35))
            draw.ellipse([sx - int(r*0.25), sy - int(r*0.25), sx + int(r*0.25), sy + int(r*0.25)], fill=(38, 24, 21))
            
    img = img.filter(ImageFilter.SMOOTH_MORE)
    img.save(filename, quality=95)
    return filename


def draw_animal_lion(filename):
    img = Image.new('RGB', (600, 600), color=(226, 186, 135))
    draw = ImageDraw.Draw(img)
    # Savannah background
    draw.rectangle([0, 0, 600, 350], fill=(238, 198, 142))
    draw.rectangle([0, 350, 600, 600], fill=(188, 143, 83))
    
    # Mane (Dark golden brown large circle)
    draw.ellipse([110, 100, 490, 480], fill=(140, 75, 25), outline=(90, 45, 15))
    # Outer mane tufts
    for ang in range(0, 360, 20):
        rad = np.radians(ang)
        x = int(300 + 210 * np.cos(rad))
        y = int(290 + 200 * np.sin(rad))
        draw.ellipse([x - 25, y - 25, x + 25, y + 25], fill=(120, 60, 20))
        
    # Lion Face
    draw.ellipse([180, 170, 420, 410], fill=(215, 150, 75))
    # Muzzle
    draw.ellipse([230, 270, 370, 380], fill=(245, 220, 180))
    # Nose
    draw.polygon([(280, 290), (320, 290), (300, 320)], fill=(40, 20, 15))
    # Whiskers
    draw.line([(240, 330), (160, 320)], fill=(50, 30, 20), width=2)
    draw.line([(240, 345), (150, 350)], fill=(50, 30, 20), width=2)
    draw.line([(360, 330), (440, 320)], fill=(50, 30, 20), width=2)
    draw.line([(360, 345), (450, 350)], fill=(50, 30, 20), width=2)
    # Eyes
    draw.ellipse([225, 230, 265, 255], fill=(255, 204, 0), outline=(20, 10, 5))
    draw.ellipse([240, 235, 255, 250], fill=(20, 10, 5))
    draw.ellipse([335, 230, 375, 255], fill=(255, 204, 0), outline=(20, 10, 5))
    draw.ellipse([345, 235, 360, 250], fill=(20, 10, 5))
    # Ears
    draw.ellipse([160, 120, 230, 190], fill=(180, 110, 50))
    draw.ellipse([370, 120, 440, 190], fill=(180, 110, 50))
    
    img = img.filter(ImageFilter.SMOOTH)
    img.save(filename, quality=95)
    return filename


def draw_vehicle_car(filename):
    img = Image.new('RGB', (600, 600), color=(220, 225, 230))
    draw = ImageDraw.Draw(img)
    # Road and skyline
    draw.rectangle([0, 0, 600, 380], fill=(200, 215, 230))
    draw.rectangle([0, 380, 600, 600], fill=(50, 55, 60))
    draw.line([(0, 490), (600, 490)], fill=(240, 220, 50), width=6)
    
    # Car Body (Aerodynamic Red Sports Sedan)
    car_red = (220, 38, 38)
    car_dark_red = (153, 27, 27)
    
    # Lower chassis
    draw.rounded_rectangle([70, 310, 530, 420], radius=25, fill=car_red, outline=car_dark_red, width=3)
    # Cabin / Roof
    cabin_points = [(160, 310), (220, 220), (410, 220), (470, 310)]
    draw.polygon(cabin_points, fill=car_red, outline=car_dark_red)
    # Windows
    win_points = [(180, 305), (230, 232), (300, 232), (300, 305)]
    draw.polygon(win_points, fill=(60, 80, 100), outline=(30, 40, 50))
    win2_points = [(315, 305), (315, 232), (400, 232), (450, 305)]
    draw.polygon(win2_points, fill=(60, 80, 100), outline=(30, 40, 50))
    # Headlights & Taillights
    draw.rectangle([505, 330, 530, 355], fill=(255, 255, 180), outline=(200, 200, 120))
    draw.rectangle([70, 330, 85, 355], fill=(255, 60, 60))
    
    # Wheels
    draw.ellipse([130, 370, 230, 470], fill=(20, 20, 20), outline=(50, 50, 50), width=4)
    draw.ellipse([160, 400, 200, 440], fill=(180, 190, 200)) # Alloy rim
    draw.ellipse([370, 370, 470, 470], fill=(20, 20, 20), outline=(50, 50, 50), width=4)
    draw.ellipse([400, 400, 440, 440], fill=(180, 190, 200)) # Alloy rim
    
    img = img.filter(ImageFilter.SMOOTH)
    img.save(filename, quality=95)
    return filename


def draw_waste_plastic(filename):
    img = Image.new('RGB', (600, 600), color=(245, 247, 250))
    draw = ImageDraw.Draw(img)
    # Table surface
    draw.rectangle([0, 420, 600, 600], fill=(225, 230, 235))
    
    # Plastic Water Bottle (Transparent Blue Polyethylene)
    poly_blue = (120, 190, 240)
    poly_highlight = (200, 235, 255)
    poly_dark = (70, 140, 200)
    
    # Cap (Bright Blue)
    draw.rectangle([275, 110, 325, 140], fill=(25, 118, 210), outline=(13, 71, 161), width=2)
    # Neck
    draw.rectangle([282, 140, 318, 170], fill=poly_blue, outline=poly_dark)
    # Bottle Shoulder
    draw.polygon([(282, 170), (318, 170), (370, 230), (230, 230)], fill=poly_blue, outline=poly_dark)
    # Main Cylindrical Body
    draw.rectangle([230, 230, 370, 460], fill=poly_blue, outline=poly_dark, width=2)
    # Grooves/Ribs
    for y in [270, 310, 350, 390, 430]:
        draw.line([(235, y), (365, y)], fill=poly_dark, width=2)
        draw.line([(235, y + 2), (365, y + 2)], fill=poly_highlight, width=1)
    # Recyclable Label Wrap
    draw.rectangle([230, 310, 370, 390], fill=(240, 245, 250), outline=poly_dark)
    # Recycling Symbol Tri-Arrow
    draw.text((270, 335), "♻ PET #1", fill=(10, 100, 60))
    # Highlights
    draw.line([(245, 235), (245, 455)], fill=poly_highlight, width=5)
    
    img = img.filter(ImageFilter.SMOOTH)
    img.save(filename, quality=95)
    return filename


def draw_medical_xray(filename, has_pathology="normal"):
    # Monochrome Thoracic Chest Radiograph
    img = Image.new('L', (600, 600), color=15)
    draw = ImageDraw.Draw(img)
    
    # Soft thoracic body cavity
    draw.ellipse([80, 50, 520, 560], fill=40)
    # Spinal column
    draw.rectangle([285, 40, 315, 520], fill=120)
    for y in range(60, 500, 25):
        draw.line([(280, y), (320, y)], fill=160, width=3)
        
    # Ribcage arches
    for y in range(110, 460, 35):
        curve = int(y * 0.3)
        # Left ribs
        draw.arc([110, y - 20, 300, y + 40], start=180, end=340, fill=130, width=5)
        # Right ribs
        draw.arc([300, y - 20, 490, y + 40], start=200, end=360, fill=130, width=5)
        
    # Lung Fields (Air filled = Radiolucent / Dark)
    draw.ellipse([130, 120, 280, 440], fill=22) # Right lung
    draw.ellipse([320, 120, 470, 440], fill=22) # Left lung
    
    # Clavicles
    draw.line([(120, 90), (285, 110)], fill=180, width=8)
    draw.line([(480, 90), (315, 110)], fill=180, width=8)
    
    # Cardiac Silhouette (Radiopaque / Bright dense shadow)
    heart_w = 170 if has_pathology != "cardiomegaly" else 260
    draw.ellipse([270, 260, 270 + heart_w, 470], fill=145)
    
    # Diaphragm Domes
    draw.chord([100, 380, 290, 500], start=180, end=0, fill=110)
    draw.chord([310, 395, 500, 515], start=180, end=0, fill=110)
    
    if has_pathology == "pneumonia":
        # Alveolar opacity / consolidation cloud in right lower lobe
        for _ in range(80):
            rx = int(np.random.normal(210, 25))
            ry = int(np.random.normal(360, 25))
            draw.ellipse([rx - 12, ry - 12, rx + 12, ry + 12], fill=105)
            
    # Add clinical marker text
    draw.text((30, 30), "R", fill=220)
    draw.text((540, 30), "PA ERECT", fill=160)
    
    img = img.filter(ImageFilter.GaussianBlur(radius=1.8))
    # Convert to RGB
    rgb = img.convert('RGB')
    rgb.save(filename, quality=95)
    return filename


def seed():
    sample_dir = os.path.join('media', 'samples')
    os.makedirs(sample_dir, exist_ok=True)
    
    samples_data = [
        # Plants
        {
            'title': 'Tomato Leaf - Early Blight Lesions',
            'domain': 'plants',
            'expected_label': 'Tomato Early Blight',
            'filename': 'plant_tomato_early_blight.jpg',
            'builder': lambda p: draw_plant_leaf(p, is_diseased=True, disease_type="early_blight"),
            'description': 'Target-board circular concentric fungal spots on tomato leaf showing chlorosis.'
        },
        {
            'title': 'Healthy Green Crop Leaf',
            'domain': 'plants',
            'expected_label': 'Healthy Green Crop / Leaf',
            'filename': 'plant_healthy_leaf.jpg',
            'builder': lambda p: draw_plant_leaf(p, is_diseased=False),
            'description': 'Vibrant uniform green foliage with intact epidermal margins and no lesions.'
        },
        # Animals
        {
            'title': 'African Lion (Panthera Leo)',
            'domain': 'animals',
            'expected_label': 'Lion (Panthera Leo)',
            'filename': 'animal_lion_savannah.jpg',
            'builder': lambda p: draw_animal_lion(p),
            'description': 'Adult lion specimen showing distinctive mane, feline muzzle, and amber ocular features.'
        },
        # Vehicles
        {
            'title': 'Aerodynamic Red Sports Car',
            'domain': 'vehicles',
            'expected_label': 'Passenger Sedan / Car',
            'filename': 'vehicle_sports_car.jpg',
            'builder': lambda p: draw_vehicle_car(p),
            'description': 'Modern four-wheeled aerodynamic passenger car on paved roadway with alloy rims.'
        },
        # Waste
        {
            'title': 'PET #1 Recyclable Polymer Bottle',
            'domain': 'waste',
            'expected_label': 'Plastic Bottle & Polymers (Recyclable)',
            'filename': 'waste_plastic_bottle.jpg',
            'builder': lambda p: draw_waste_plastic(p),
            'description': 'Clear PET plastic container ready for clean blue-bin municipal recycling.'
        },
        # Medical
        {
            'title': 'Thoracic Chest X-Ray - Normal Baseline',
            'domain': 'medical',
            'expected_label': 'Normal Thoracic Chest X-Ray',
            'filename': 'medical_normal_chest_xray.jpg',
            'builder': lambda p: draw_medical_xray(p, has_pathology="normal"),
            'description': 'PA erect chest radiograph showing clear lung fields, sharp costophrenic angles, normal cardiothoracic ratio.'
        },
        {
            'title': 'Thoracic Chest X-Ray - Pneumonia Opacity',
            'domain': 'medical',
            'expected_label': 'Pneumonia Pulmonary Consolidation X-Ray',
            'filename': 'medical_pneumonia_xray.jpg',
            'builder': lambda p: draw_medical_xray(p, has_pathology="pneumonia"),
            'description': 'Radiograph demonstrating right lower lobe alveolar consolidation infiltrate.'
        }
    ]
    
    print(f"Generating {len(samples_data)} demo sample images...")
    SampleImage.objects.all().delete()
    
    for item in samples_data:
        file_path = os.path.join(sample_dir, item['filename'])
        item['builder'](file_path)
        
        sample = SampleImage(
            title=item['title'],
            domain=item['domain'],
            expected_label=item['expected_label'],
            description=item['description']
        )
        with open(file_path, 'rb') as f:
            sample.image.save(item['filename'], File(f), save=True)
        print(f"Created sample: {sample.title}")
        
    print(f"Successfully seeded {SampleImage.objects.count()} sample images!")

if __name__ == '__main__':
    seed()
