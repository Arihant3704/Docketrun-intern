import tkinter as tk
from tkinter import ttk, simpledialog

class Toolbox(tk.Frame):
    """Left sidebar with modes and object list."""
    
    def __init__(self, parent, controller):
        super().__init__(parent, width=250)
        self.controller = controller
        self.pack_propagate(False)
        
        # Modes
        lbl_mode = ttk.Label(self, text="MODES", font=("Arial", 10, "bold"))
        lbl_mode.pack(pady=(10, 5))
        
        self.mode_var = tk.StringVar(value="detect")
        modes = [("Detect (SAM)", "detect"), ("Track", "track"), ("Edit", "edit")]
        for text, val in modes:
            rb = ttk.Radiobutton(self, text=text, variable=self.mode_var, value=val, command=self.on_mode_change)
            rb.pack(anchor="w", padx=10)
            
        # Class List
        ttk.Separator(self, orient="horizontal").pack(fill="x", pady=10)
        ttk.Label(self, text="OBJECTS", font=("Arial", 10, "bold")).pack()
        
        self.tree = ttk.Treeview(self, columns=("ID", "Class"), show="headings", height=15)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Class", text="Class")
        self.tree.column("ID", width=40)
        self.tree.column("Class", width=100)
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(fill="x", padx=5)
        ttk.Button(btn_frame, text="Add", command=self.on_add).pack(side="left", expand=True)
        ttk.Button(btn_frame, text="Rename", command=self.on_rename).pack(side="left", expand=True)
        ttk.Button(btn_frame, text="Del", command=self.on_delete).pack(side="left", expand=True)
        
        # Export
        ttk.Separator(self, orient="horizontal").pack(fill="x", pady=10)
        
        # Track Control
        ttk.Button(self, text="▶ Propagate...", command=self.on_propagate).pack(fill="x", padx=10, pady=2)
        ttk.Button(self, text="⏹ Stop Tracking", command=lambda: self.controller.stop_propagation()).pack(fill="x", padx=10, pady=2)
        
        ttk.Separator(self, orient="horizontal").pack(fill="x", pady=5)
        ttk.Button(self, text="Export YOLO", command=lambda: self.controller.export()).pack(fill="x", padx=10, pady=10)
        
    def on_mode_change(self):
        new_mode = self.mode_var.get()
        self.controller.set_mode(new_mode)
        
    def on_add(self):
        new_name = simpledialog.askstring("New Object", "Enter Class Name:")
        if new_name:
            next_id = max(self.controller.am.objects.keys(), default=0) + 1
            # Random color generator could be nice here
            self.controller.am.add_object(next_id, new_name, (0, 255, 0))
            self.controller.active_obj_id = next_id
            self.update_object_list(self.controller.am.objects)
            
    def on_rename(self):
        sel = self.tree.selection()
        if sel:
            item = self.tree.item(sel[0])
            obj_id = item['values'][0]
            current_name = item['values'][1]
            new_name = simpledialog.askstring("Rename Object", "Enter New Name:", initialvalue=current_name)
            if new_name:
                self.controller.rename_object(obj_id, new_name)
            
    def on_delete(self):
        sel = self.tree.selection()
        if sel:
            item = self.tree.item(sel[0])
            obj_id = item['values'][0]
            self.controller.am.delete_object(obj_id)
            self.update_object_list(self.controller.am.objects)
            self.controller.load_frame(self.controller.current_frame_idx) # Refresh view

    def on_propagate(self):
         # Ask for number of frames
         # 0 or Empty or Cancel?
         # askinteger returns None on Cancel.
         # We want to allow user to specify "All".
         # Let's say: "Enter max frames (0 for all):"
         frames = simpledialog.askinteger("Propagate", "Max Frames (0 for All):", initialvalue=0, minvalue=0)
         if frames is not None:
             # Treat 0 as None (All)
             max_f = frames if frames > 0 else None
             self.controller.propagate(max_frames=max_f)
        
    def update_object_list(self, objects):
        self.tree.delete(*self.tree.get_children())
        for obj in objects.values():
            self.tree.insert("", "end", values=(obj.obj_id, obj.class_name))
