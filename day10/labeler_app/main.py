import sys
import tkinter as tk
from tkinter import messagebox
from labeler_app.controller import AppController
from labeler_app.ui.main_window import MainWindow
from labeler_app.utils.logger import app_logger

def main():
    app_logger.info("Starting Video Labeler Pro...")
    
    # 1. Initialize Controller
    controller = AppController()
    
    # 2. Initialize UI
    root = tk.Tk()
    root.title("Video Labeler Pro")
    root.geometry("1400x900")
    
    app = MainWindow(root, controller)
    app.pack(fill="both", expand=True)
    
    # 3. Handle graceful exit
    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            controller.tm.stop_task()
            root.destroy()
            
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    app_logger.info("UI Loop Starting.")
    root.mainloop()

if __name__ == "__main__":
    main()
