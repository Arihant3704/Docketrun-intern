# YOLO Segmentation App

A modern web application for real-time image and video segmentation using YOLO models. This project features a FastAPI backend and a React/Vite frontend, providing a seamless interface for object detection and segmentation.

## 🚀 Features

- **Image Inference**: Upload an image to perform instant segmentation.
- **Video Inference**: Upload a video to process and visualize segmentation results side-by-side.
- **URL Inference**: Provide an image URL for remote inference.
- **Model Selection**: Choose from various available YOLO models (`.pt` files).
- **Adjustable Threshold**: Fine-tune the confidence threshold for detections.
- **Real-time Results**: Instant visualization of annotated images and videos.

## 🛠 Tech Stack

- **Backend**: Python, FastAPI, Ultralytics YOLO, OpenCV, Uvicorn.
- **Frontend**: React, Vite, Lucide React, Tailwind CSS.
- **Automation**: Bash script for unified startup.

## 📋 Prerequisites

- **Python**: 3.8 or higher.
- **Node.js**: v18 or higher.
- **npm**: v9 or higher.

## ⚙️ Installation & Setup

### 1. Clone the repository
```bash
git clone <repository-url>
cd yolo_segmentation_app
```

### 2. Backend Setup
Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r backend/requirements.txt
```

### 3. Frontend Setup
Install npm packages:
```bash
cd frontend
npm install
cd ..
```

### 4. Models
Ensure your YOLO model files (`.pt`) are placed in the `backend/model/` directory.

## 🏃 Running the Application

You can start both the backend and frontend simultaneously using the provided `run.sh` script:

```bash
chmod +x run.sh
./run.sh
```

- **Frontend**: Accessible at `http://localhost:5173`
- **Backend API**: Accessible at `http://localhost:8000`
- **API Documentation**: `http://localhost:8000/docs`

## 📂 Project Structure

```text
yolo_segmentation_app/
├── backend/            # FastAPI application
│   ├── main.py         # Primary API entry point
│   ├── model/          # YOLO weights (.pt files)
│   ├── uploads/        # Temporary storage for uploaded files
│   └── results/        # Storage for processed images/videos
├── frontend/           # React/Vite application
│   ├── src/            # Component and logic source
│   │   ├── components/ # UI Components
│   │   └── App.jsx     # Main application layout
│   └── package.json    # Frontend dependencies
├── run.sh              # Unified startup script
└── README.md           # Project documentation
```

## 📝 License

This project is open-source and available under the MIT License.
