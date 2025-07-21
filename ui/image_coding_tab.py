# ui/image_coding_tab.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import io
import os
from core.logger import get_logger

logger = get_logger(__name__)

class ImageCodingTab:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.setup_ui()
        self.current_image = None
        self.encoded_data = None
        self.current_metadata = None
        logger.info("ImageCodingTab initialized")
    
    def setup_ui(self):
        logger.debug("Setting up UI for ImageCodingTab")
        # Algorithm selection
        algo_frame = ttk.LabelFrame(self.frame, text="JPEG Settings")
        algo_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Quality setting
        quality_frame = ttk.Frame(algo_frame)
        quality_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(quality_frame, text="Quality:").pack(side=tk.LEFT, padx=5)
        self.quality_var = tk.IntVar(value=90)
        self.quality_scale = ttk.Scale(quality_frame, from_=1, to=100, 
                                     variable=self.quality_var, orient=tk.HORIZONTAL)
        self.quality_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        self.quality_label = ttk.Label(quality_frame, text="90")
        self.quality_label.pack(side=tk.LEFT, padx=5)
        
        self.quality_scale.configure(command=self.update_quality_label)
        
        # Lossless option
        self.lossless_var = tk.BooleanVar()
        self.lossless_check = ttk.Checkbutton(algo_frame, text="Lossless Compression", 
                                            variable=self.lossless_var)
        self.lossless_check.pack(anchor=tk.W, padx=5, pady=2)
        
        # Input section
        input_frame = ttk.LabelFrame(self.frame, text="Input Image")
        input_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Input controls
        input_controls = ttk.Frame(input_frame)
        input_controls.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(input_controls, text="Load Image", 
                  command=self.load_image).pack(side=tk.LEFT, padx=5)
        ttk.Button(input_controls, text="Clear", 
                  command=self.clear_image).pack(side=tk.LEFT, padx=5)
        
        # Image display
        self.image_canvas = tk.Canvas(input_frame, bg='white', height=200)
        self.image_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Control buttons
        control_frame = ttk.Frame(self.frame)
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(control_frame, text="Compress", 
                  command=self.compress_image).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Decompress", 
                  command=self.decompress_image).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Save Compressed", 
                  command=self.save_compressed).pack(side=tk.LEFT, padx=5)
        
        # Statistics
        stats_frame = ttk.LabelFrame(self.frame, text="Compression Statistics")
        stats_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.stats_text = tk.Text(stats_frame, height=4, state=tk.DISABLED)
        self.stats_text.pack(fill=tk.X, padx=5, pady=5)
    
    def update_quality_label(self, value):
        self.quality_label.config(text=str(int(float(value))))
    
    def load_image(self):
        logger.debug("Attempting to load image from file")
        filename = filedialog.askopenfilename(
            title="Select image file",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff *.gif"),
                ("JPEG files", "*.jpg *.jpeg"),
                ("PNG files", "*.png"),
                ("All files", "*.*")
            ]
        )
        if filename:
            try:
                logger.info(f"Loading image from {filename}")
                self.current_image = Image.open(filename)
                self.display_image(self.current_image)
                self.update_stats("Image loaded successfully")
                logger.info("Successfully loaded image")
            except Exception as e:
                logger.error(f"Could not load image: {str(e)}", exc_info=True)
                messagebox.showerror("Error", f"Could not load image: {str(e)}")
    
    def display_image(self, image, title=""):
        # Resize image to fit canvas while maintaining aspect ratio
        canvas_width = self.image_canvas.winfo_width()
        canvas_height = self.image_canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            canvas_width, canvas_height = 400, 200
        
        img_width, img_height = image.size
        
        # Calculate scaling factor
        scale_x = canvas_width / img_width
        scale_y = canvas_height / img_height
        scale = min(scale_x, scale_y, 1.0)  # Don't upscale
        
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)
        
        resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Convert to PhotoImage
        self.photo = ImageTk.PhotoImage(resized_image)
        
        # Clear canvas and display image
        self.image_canvas.delete("all")
        x = (canvas_width - new_width) // 2
        y = (canvas_height - new_height) // 2
        self.image_canvas.create_image(x, y, anchor=tk.NW, image=self.photo)
        
        if title:
            self.image_canvas.create_text(10, 10, anchor=tk.NW, text=title, 
                                        fill="red", font=("Arial", 12, "bold"))
    
    def compress_image(self):
        if not self.current_image:
            logger.warning("Compress attempt with no image loaded")
            messagebox.showwarning("Warning", "Please load an image first")
            return
        
        try:
            from algorithms.image.jpeg import JPEGCoder
            
            quality = self.quality_var.get()
            lossless = self.lossless_var.get()
            
            logger.info(f"Compressing image with quality={quality}, lossless={lossless}")
            coder = JPEGCoder(quality=quality, lossless=lossless)
            self.encoded_data, self.current_metadata = coder.encode(self.current_image)
            
            # Update statistics
            original_size = self.current_metadata.get('original_data_size', 0)
            compressed_size = self.current_metadata.get('compressed_size', 0)
            
            compression_ratio = original_size / compressed_size if compressed_size > 0 else 0
            
            stats = f"""Original Size: {original_size:,} bytes
Compressed Size: {compressed_size:,} bytes
Compression Ratio: {compression_ratio:.2f}:1
Quality: {quality}
Mode: {'Lossless' if lossless else 'Lossy'}"""
            
            self.update_stats(stats)
            logger.info("Image compressed successfully")
            messagebox.showinfo("Success", "Image compressed successfully!")
            
        except Exception as e:
            logger.error(f"Compression failed: {str(e)}", exc_info=True)
            messagebox.showerror("Error", f"Compression failed: {str(e)}")
    
    def decompress_image(self):
        if not self.encoded_data or not self.current_metadata:
            logger.warning("Decompress attempt with no compressed data")
            messagebox.showwarning("Warning", "No compressed data available. Please compress first.")
            return
        
        try:
            from algorithms.image.jpeg import JPEGCoder
            
            logger.info("Decompressing image")
            coder = JPEGCoder()
            decompressed_image = coder.decode(self.encoded_data, self.current_metadata)
            
            # Show decompressed image in new window
            self.show_decompressed_image(decompressed_image)
            logger.info("Image decompressed successfully")
            
        except Exception as e:
            logger.error(f"Decompression failed: {str(e)}", exc_info=True)
            messagebox.showerror("Error", f"Decompression failed: {str(e)}")
    
    def show_decompressed_image(self, image):
        # Create new window for decompressed image
        logger.debug("Showing decompressed image in popup")
        popup = tk.Toplevel(self.frame)
        popup.title("Decompressed Image")
        popup.geometry("600x500")
        
        canvas = tk.Canvas(popup, bg='white')
        canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Display image
        img_width, img_height = image.size
        canvas_width, canvas_height = 580, 480
        
        scale_x = canvas_width / img_width
        scale_y = canvas_height / img_height
        scale = min(scale_x, scale_y, 1.0)
        
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)
        
        resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(resized_image)
        
        canvas.create_image(canvas_width//2, canvas_height//2, image=photo)
        canvas.image = photo  # Keep a reference
        
        ttk.Button(popup, text="Close", command=popup.destroy).pack(pady=10)
    
    def save_compressed(self):
        if not self.encoded_data:
            logger.warning("Save attempt with no compressed data")
            messagebox.showwarning("Warning", "No compressed data to save")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Save compressed image",
            defaultextension=".jpg",
            filetypes=[
                ("JPEG files", "*.jpg"),
                ("PNG files", "*.png"),
                ("All files", "*.*")
            ]
        )
        
        if filename:
            try:
                logger.info(f"Saving compressed image to {filename}")
                with open(filename, 'wb') as f:
                    f.write(self.encoded_data)
                logger.info("Compressed image saved successfully")
                messagebox.showinfo("Success", "Compressed image saved successfully!")
            except Exception as e:
                logger.error(f"Could not save file: {str(e)}", exc_info=True)
                messagebox.showerror("Error", f"Could not save file: {str(e)}")
    
    def clear_image(self):
        logger.info("Clearing image, encoded data, and stats")
        self.current_image = None
        self.encoded_data = None
        self.current_metadata = None
        self.image_canvas.delete("all")
        self.update_stats("")
    
    def update_stats(self, text):
        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(1.0, text)
        self.stats_text.config(state=tk.DISABLED)
