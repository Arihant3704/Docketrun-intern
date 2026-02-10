import tkinter as tk
from PIL import Image, ImageTk

class ZoomCanvas(tk.Canvas):
    """Canvas with Zoom and Pan capabilities."""
    
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, **kwargs)
        self.controller = controller
        self.image = None # Original PIL Image
        self.tk_image = None
        self.zoom_scale = 1.0
        self.pan_x = 0
        self.pan_y = 0
        
        # Bindings
        self.bind("<ButtonPress-1>", self.on_click)
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<MouseWheel>", self.on_zoom) # Windows
        self.bind("<Button-4>", self.on_zoom)   # Linux Scroll Up
        self.bind("<Button-5>", self.on_zoom)   # Linux Scroll Down
        self.bind("<Button-3>", self.on_right_click) # Right Click Context Menu
        
        # Pan state
        self._drag_data = {"x": 0, "y": 0}

    def set_image(self, pil_image):
        self.image = pil_image
        self.redraw()
        
    def redraw(self):
        if not self.image: return
        
        # Resize
        w, h = self.image.size
        new_w = int(w * self.zoom_scale)
        new_h = int(h * self.zoom_scale)
        
        resized = self.image.resize((new_w, new_h), Image.Resampling.NEAREST)
        self.tk_image = ImageTk.PhotoImage(resized)
        
        self.delete("all")
        # Center or use pan offset
        # For simplicity, just centering + pan
        cx = (self.winfo_width() // 2) + self.pan_x
        cy = (self.winfo_height() // 2) + self.pan_y
        
        self.create_image(cx, cy, image=self.tk_image, anchor="center")
        
    def on_click(self, event):
        # Calculate Image Coordinates taking Zoom/Pan into account
        # screen_x = event.x, screen_y = event.y
        # image_x = (screen_x - center_x) / zoom + center_x ... roughly
        
        if not self.image: return
        
        cx = (self.winfo_width() // 2) + self.pan_x
        cy = (self.winfo_height() // 2) + self.pan_y
        
        # Inverse transform
        img_x = int((event.x - cx) / self.zoom_scale + (self.image.width * self.zoom_scale / 2) / self.zoom_scale) 
        # Wait, simple math:
        # drawn_x = cx - (w*z)/2 ... NO.
        # Let's use the anchor center logic:
        # Center of image is at (cx, cy) on screen.
        # TopLeft of image on screen is (cx - w*z/2, cy - h*z/2)
        
        w, h = self.image.size
        tl_x = cx - (w * self.zoom_scale) / 2
        tl_y = cy - (h * self.zoom_scale) / 2
        
        rel_x = int((event.x - tl_x) / self.zoom_scale)
        rel_y = int((event.y - tl_y) / self.zoom_scale)
        
        if 0 <= rel_x < w and 0 <= rel_y < h:
            self.controller.handle_canvas_click(rel_x, rel_y, event.num, w, h)
        else:
             self._drag_data["x"] = event.x
             self._drag_data["y"] = event.y
             
    def on_drag(self, event):
        # Only drag if NOT in detect mode? Or middle click?
        # For now constant drag
        dx = event.x - self._drag_data["x"]
        dy = event.y - self._drag_data["y"]
        self.pan_x += dx
        self.pan_y += dy
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y
        self.redraw()
        
    def on_zoom(self, event):
        if event.num == 5 or event.delta < 0:
            self.zoom_scale *= 0.9
        else:
            self.zoom_scale *= 1.1
        self.redraw()

    def on_right_click(self, event):
        import tkinter as tk
        if not self.image: return
        
        # Calculate Image Coordinates (Same logic as on_click)
        cx = (self.winfo_width() // 2) + self.pan_x
        cy = (self.winfo_height() // 2) + self.pan_y
        
        w, h = self.image.size
        tl_x = cx - (w * self.zoom_scale) / 2
        tl_y = cy - (h * self.zoom_scale) / 2
        
        # Avoid division by zero if zoom_scale is weird
        if self.zoom_scale == 0: return

        img_x = int((event.x - tl_x) / self.zoom_scale)
        img_y = int((event.y - tl_y) / self.zoom_scale)
        
        if 0 <= img_x < w and 0 <= img_y < h:
            obj_id = self.controller.get_object_at(img_x, img_y)
            if obj_id:
                obj = self.controller.am.objects.get(obj_id)
                if obj:
                    menu = tk.Menu(self, tearoff=0)
                    
                    # Per-Frame Actions
                    menu.add_command(label=f"Rename (This Frame Only)", command=lambda: self.reassign_mask(obj_id, obj.class_name))
                    menu.add_command(label=f"Delete (This Frame Only)", command=lambda: self.controller.delete_mask_on_frame(obj_id))
                    
                    menu.add_separator()
                    
                    # Global Actions
                    menu.add_command(label=f"Delete Object (All Frames)", command=lambda: self.controller.delete_object_global(obj_id))
                    
                    menu.add_separator()
                    menu.add_command(label="Add Point (Refine)", command=lambda: self.start_refinement(obj_id))
                    
                    menu.tk_popup(event.x_root, event.y_root)

    def reassign_mask(self, obj_id, current_name):
        from tkinter import simpledialog
        new_name = simpledialog.askstring("Rename (Frame)", "Enter New Name for this frame:", initialvalue=current_name)
        if new_name:
            self.controller.reassign_mask_on_frame(obj_id, new_name)

    def start_refinement(self, obj_id):
        self.controller.set_mode("detect")
        self.controller.active_obj_id = obj_id
        if self.controller.ui:
             self.controller.ui.update_status(f"Refining Object {obj_id}. Click to add points.")
