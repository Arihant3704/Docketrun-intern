from fastapi import FastAPI, File, UploadFile, HTTPException, Form, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse, StreamingResponse
from ultralytics import YOLO
import cv2
import numpy as np
import shutil
import os
import uuid
import time
from pathlib import Path
from typing import List

app = FastAPI(title="YOLO Segmentation API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
MODELS_DIR = "model"
UPLOAD_DIR = "uploads"
RESULTS_DIR = "results"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

# Global model cache to avoid reloading if selected model hasn't changed
current_model = None
current_model_name = ""

def get_available_models():
    return [f.name for f in Path(MODELS_DIR).glob("*.pt")]

def load_model(model_name: str):
    global current_model, current_model_name
    
    if current_model_name == model_name and current_model is not None:
        return current_model
        
    model_path = os.path.join(MODELS_DIR, model_name)
    if not os.path.exists(model_path):
        raise HTTPException(status_code=404, detail=f"Model {model_name} not found")
        
    print(f"Loading model from {model_path}...")
    try:
        current_model = YOLO(model_path)
        current_model_name = model_name
        print(f"Model {model_name} loaded successfully.")
        return current_model
    except Exception as e:
        print(f"Error loading model: {e}")
        raise HTTPException(status_code=500, detail=f"Error loading model: {e}")

@app.get("/models")
async def list_models():
    models = get_available_models()
    return {"models": models}

@app.get("/")
async def root():
    return {"message": "YOLO Segmentation API is running", "models_available": get_available_models()}

@app.post("/predict/image")
async def predict_image(file: UploadFile = File(...), model_name: str = Form(...), threshold: float = Form(0.25)):
    print(f"Predicting image: model={model_name}, threshold={threshold}")
    model = load_model(model_name)
    
    try:
        # Save uploaded file
        file_id = str(uuid.uuid4())
        file_ext = os.path.splitext(file.filename)[1]
        input_path = os.path.join(UPLOAD_DIR, f"{file_id}{file_ext}")
        
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Run inference
        results = model(input_path, conf=threshold)
        
        # Process results
        result = results[0]
        output_filename = f"{file_id}_pred.jpg"
        output_path = os.path.join(RESULTS_DIR, output_filename)
        
        # Save plotted image
        result_img = result.plot()
        cv2.imwrite(output_path, result_img)
        
        return {
            "file_id": file_id,
            "filename": output_filename,
            "image_url": f"/results/{output_filename}"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict/video")
async def predict_video(file: UploadFile = File(...), model_name: str = Form(...), threshold: float = Form(0.25)):
    model = load_model(model_name)
    
    try:
        # Save uploaded file
        file_id = str(uuid.uuid4())
        file_ext = os.path.splitext(file.filename)[1]
        original_filename = f"{file_id}{file_ext}"
        input_path = os.path.join(UPLOAD_DIR, original_filename)
        
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Process video
        cap = cv2.VideoCapture(input_path)
        if not cap.isOpened():
            raise HTTPException(status_code=400, detail="Could not open video")
            
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        output_filename = f"{file_id}_pred.mp4"
        output_path = os.path.join(RESULTS_DIR, output_filename)
        
        # Define codec and create VideoWriter
        # Use 'mp4v' or 'avc1' for browser compatibility
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            results = model(frame, conf=threshold)
            annotated_frame = results[0].plot()
            out.write(annotated_frame)
            
        cap.release()
        out.release()
        
        return {
            "file_id": file_id,
            "filename": output_filename,
            "processed_video_url": f"/results/{output_filename}",
            "original_video_url": f"/uploads/{original_filename}"
        }
        
    except Exception as e:
        print(f"Error processing video: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/uploads/{filename}")
async def get_upload_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path)

@app.post("/predict/url")
async def predict_url(url: str = Query(...), model_name: str = Query(...), threshold: float = Query(0.25)):
    print(f"Predicting URL: {url}, model={model_name}, threshold={threshold}")
    import requests
    model = load_model(model_name)
        
    try:
        # Download image
        response = requests.get(url, stream=True)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Could not download image from URL")
            
        file_id = str(uuid.uuid4())
        input_path = os.path.join(UPLOAD_DIR, f"{file_id}.jpg")
        
        with open(input_path, "wb") as out_file:
            shutil.copyfileobj(response.raw, out_file)
            
        # Run inference
        results = model(input_path, conf=threshold)
        result = results[0]
        
        output_filename = f"{file_id}_pred.jpg"
        output_path = os.path.join(RESULTS_DIR, output_filename)
        
        result_img = result.plot()
        cv2.imwrite(output_path, result_img)
        
        return {
            "file_id": file_id,
            "filename": output_filename,
            "image_url": f"/results/{output_filename}"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/results/{filename}")
async def get_result_image(filename: str):
    file_path = os.path.join(RESULTS_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
