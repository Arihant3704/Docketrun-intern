# Internship Project Portfolio

Welcome to my internship project repository. This directory contains the work completed over three days, focusing on **AI Development**, **Computer Vision**, and **Full-stack Web Applications**.

## 📁 Project Structure

### [Day 1: AI Foundations & Automated Annotation](./day1)
- **AI Development Lifecycle**: Documentation on the lifecycle of AI projects.
- **Automated Labeling**: Jupyter notebooks for automated dataset annotation using **Grounding DINO** and **SAM (Segment Anything Model)**.
- **Resources**: Research papers and documentation relevant to the initial phase.

### [Day 2: Data Science Hub](./day2)
- **Python Data Stack**: Resources and guides for the essential Python data science libraries.
- **[Python DS Hub](./day2/python-ds-hub)**: A React-based dashboard for exploring data science tools and workflows.
- **Visual Assets**: Screencasts and diagrams detailing project workflows.

### [Day 3: YOLO Segmentation App](./day3)
- **[YOLO Segmentation App](./day3/yolo_segmentation_app)**: A complete full-stack application featuring:
  - **Backend**: FastAPI with Ultralytics YOLO integration.
  - **Frontend**: React/Vite with real-time video/image segmentation visualization.
- **Model Training**: Jupyter notebooks for training custom YOLO models on unique datasets.
- **Dataset**: Custom `.pt` model weights and training results.

---

## 🛠 Tech Stack

| Component | Technologies |
| :--- | :--- |
| **Backend** | Python, FastAPI, Ultralytics YOLO, OpenCV, Uvicorn |
| **Frontend** | React, Vite, Tailwind CSS, Lucide React, Axios |
| **Data Science** | Jupyter Notebook, Grounding DINO, SAM |
| **Automation** | Bash Shell Scripting |

---

## 🚀 Quick Start

To run the primary application (YOLO Segmentation App):

1. **Navigate to the app directory**:
   ```bash
   cd day3/yolo_segmentation_app
   ```
2. **Execute the startup script**:
   ```bash
   chmod +x run.sh
   ./run.sh
   ```
3. **Access the Application**:
   - Frontend: `http://localhost:5173`
   - API Docs: `http://localhost:8000/docs`

---

## 📝 License

This project is open-source and available under the [MIT License](LICENSE).
