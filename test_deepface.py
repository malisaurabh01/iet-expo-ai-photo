#!/usr/bin/env python3
import os
import sys
import json
import sqlite3
from pathlib import Path

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

try:
    from deepface import DeepFace
    print("✓ DeepFace imported successfully")
    print(f"  Version: {DeepFace.__version__}")
except ImportError as e:
    print(f"✗ DeepFace import failed: {e}")
    sys.exit(1)

# Test with a sample photo
upload_folder = os.path.join(os.path.dirname(__file__), 'backend', 'uploads')
sample_photos = [f for f in os.listdir(upload_folder) 
                 if os.path.isfile(os.path.join(upload_folder, f)) 
                 and f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.bmp'))]

if sample_photos:
    test_photo = os.path.join(upload_folder, sample_photos[0])
    print(f"\n Testing with: {sample_photos[0]}")
    
    try:
        result = DeepFace.represent(
            img_path=test_photo,
            model_name="Facenet",
            enforce_detection=False,
            detector_backend="opencv"
        )
        print(f"✓ Face detection works! Found {len(result)} face(s)")
        if result:
            print(f"  Embedding dimension: {len(result[0]['embedding'])}")
    except Exception as e:
        print(f"✗ Face detection failed: {e}")
        print(f"  (This might be a model download issue on first run)")
else:
    print("✗ No photos found to test with")

# Check database
db_path = os.path.join(os.path.dirname(__file__), 'backend', 'data', 'expo.db')
if os.path.exists(db_path):
    print(f"\n Database: {db_path}")
    db = sqlite3.connect(db_path)
    cursor = db.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM photos")
    photo_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM face_encodings")
    encoding_count = cursor.fetchone()[0]
    
    print(f"  Photos: {photo_count}")
    print(f"  Face encodings: {encoding_count}")
    
    if photo_count > 0 and encoding_count == 0:
        print("  ⚠ Photos exist but no face encodings! Need to re-process.")
    
    db.close()
