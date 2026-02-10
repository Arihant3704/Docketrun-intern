import tkinter as tk
from tkinter import ttk

class Timeline(tk.Frame):
    """Timeline with slider and frame controls."""
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.total_frames = 100 # Default
        self.current_frame = 0
        
        # Controls
        self.btn_prev = ttk.Button(self, text="<", width=3, command=self.on_prev)
        self.btn_play = ttk.Button(self, text="Play", width=5, command=self.on_play)
        self.btn_next = ttk.Button(self, text=">", width=3, command=self.on_next)
        
        self.slider = ttk.Scale(self, from_=0, to=100, orient="horizontal", command=self.on_slide)
        self.lbl_frame = ttk.Label(self, text="Frame: 0 / 100")
        
        # Layout
        self.btn_prev.pack(side="left", padx=2)
        self.btn_play.pack(side="left", padx=2)
        self.btn_next.pack(side="left", padx=2)
        self.lbl_frame.pack(side="right", padx=10)
        self.slider.pack(side="left", fill="x", expand=True, padx=10)
        
    def set_total_frames(self, total):
        self.total_frames = total
        self.slider.config(to=total-1)
        self.update_label()
        
    def set_current_frame(self, frame):
        self.current_frame = frame
        self.slider.set(frame)
        self.update_label()
        
    def update_label(self):
        self.lbl_frame.config(text=f"Frame: {self.current_frame} / {self.total_frames}")
        
    def on_prev(self):
        self.controller.change_frame(-1)
        
    def on_next(self):
         self.controller.change_frame(1)
    
    def on_play(self):
        self.controller.toggle_play()
        
    def update_play_button(self, is_playing):
        self.btn_play.config(text="Pause" if is_playing else "Play")
        
    def on_slide(self, val):
        frame = int(float(val))
        if frame != self.current_frame:
             if self.controller.backend:
                 self.controller.load_frame(frame)
