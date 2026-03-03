#!/usr/bin/env python3
import os
import sys
import cv2

# Test OpenCV face detection
upload_folder = os.path.join(os.path.dirname(__file__), 'backend', 'uploads')
sample_photos = [f for f in os.listdir(upload_folder) 
                 if os.path.isfile(os.path.join(upload_folder, f)) 
                 and f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.bmp'))]

print("Testing OpenCV Face Detection")
print("=" * 50)

if sample_photos:
    test_photo = os.path.join(upload_folder, sample_photos[0])
    print(f"Testing with: {sample_photos[0]}")
    
    # Load cascade
    cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    print(f"Cascade path: {cascade_path}")
    print(f"Cascade exists: {os.path.exists(cascade_path)}")
    
    face_cascade = cv2.CascadeClassifier(cascade_path)
    
    # Load image
    image = cv2.imread(test_photo)
    if image is None:
        print(f"✗ Failed to load image: {test_photo}")
    else:
        print(f"✓ Image loaded: {image.shape}")
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        print(f"✓ Faces detected: {len(faces)}")
        for i, (x, y, w, h) in enumerate(faces):
            print(f"  Face {i+1}: position=({x},{y}) size=({w}x{h})")
else:
    print("✗ No photos found in uploads folder")
