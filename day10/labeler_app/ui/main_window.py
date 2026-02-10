import tkinter as tk
from tkinter import ttk, filedialog
from .toolbox import Toolbox
from .timeline import Timeline
from .canvas import ZoomCanvas

class MainWindow(tk.Frame):
    """Root application window layout."""
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.controller.bind_ui(self)
        
        # --- Menu Bar ---
        self.create_menu(parent)
        
        # --- Layout ---
        # Left: Toolbox
        # Right: Canvas (Center) + Timeline (Bottom)
        
        self.paned = tk.PanedWindow(self, orient="horizontal")
        self.paned.pack(fill="both", expand=True)
        
        self.toolbox = Toolbox(self.paned, controller)
        self.paned.add(self.toolbox, minsize=200)
        
        self.right_panel = tk.Frame(self.paned)
        self.paned.add(self.right_panel)
        
        self.canvas = ZoomCanvas(self.right_panel, controller, bg="#333")
        self.canvas.pack(fill="both", expand=True)
        
        self.timeline = Timeline(self.right_panel, controller)
        self.timeline.pack(fill="x", side="bottom")

        # --- Status Bar ---
        self.status_var = tk.StringVar(value="Ready.")
        self.status_bar = ttk.Label(self.right_panel, textvariable=self.status_var, relief="sunken", anchor="w")
        self.status_bar.pack(fill="x", side="bottom")

        # Hook up controller
        self.controller.on_status_update = self.update_status
        
    def create_menu(self, root):
        menubar = tk.Menu(root)
        
        # File
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New Project...", command=self.on_new_project)
        file_menu.add_command(label="Open Project...", command=self.on_open_project)
        file_menu.add_separator()
        file_menu.add_command(label="Save (Ctrl+S)", command=self.controller.save)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # Edit
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Undo (Ctrl+Z)", command=self.controller.undo)
        edit_menu.add_command(label="Redo (Ctrl+Y)", command=self.controller.redo)
        menubar.add_cascade(label="Edit", menu=edit_menu)

        # View
        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_command(label="Reset Zoom", command=lambda: setattr(self.canvas, 'zoom_scale', 1.0) or self.canvas.redraw())
        menubar.add_cascade(label="View", menu=view_menu)
        
        root.config(menu=menubar)
        
    def on_new_project(self):
        video_path = filedialog.askopenfilename(title="Select Video", filetypes=[("Video Files", "*.mp4 *.avi *.mkv")])
        if not video_path: return
        
        project_name = tk.simpledialog.askstring("New Project", "Enter Project Name:", initialvalue="MyProject")
        if not project_name: return
        
        self.controller.initialize_project(project_name, video_path, ["object"])
             # Show loading...
             
    def on_open_project(self):
        project_dir = filedialog.askdirectory(title="Select Project Directory")
        if project_dir:
            self.controller.open_project(project_dir)
        
    def update_status(self, msg):
        self.status_var.set(msg)
