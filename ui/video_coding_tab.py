# ui/video_coding_tab.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
import os
from threading import Thread
import json
from core.logger import get_logger

logger = get_logger(__name__)

class VideoCodingTab:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.setup_ui()
        self.current_video_path = None
        self.encoded_data = None
        self.current_metadata = None
        self.processing = False
        logger.info("VideoCodingTab initialized")
    
    def setup_ui(self):
        logger.debug("Setting up UI for VideoCodingTab")
        # Algorithm settings
        algo_frame = ttk.LabelFrame(self.frame, text="H.261 Settings")
        algo_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Block size setting
        block_frame = ttk.Frame(algo_frame)
        block_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(block_frame, text="Block Size:").pack(side=tk.LEFT, padx=5)
        self.block_size_var = tk.IntVar(value=16)
        block_combo = ttk.Combobox(block_frame, textvariable=self.block_size_var,
                                 values=[8, 16, 32], state="readonly", width=10)
        block_combo.pack(side=tk.LEFT, padx=5)
        block_combo.current(1)
        
        # Search range setting
        ttk.Label(block_frame, text="Search Range:").pack(side=tk.LEFT, padx=10)
        self.search_range_var = tk.IntVar(value=8)
        search_spin = ttk.Spinbox(block_frame, from_=4, to=32, 
                                textvariable=self.search_range_var, width=10)
        search_spin.pack(side=tk.LEFT, padx=5)
        
        # Input section
        input_frame = ttk.LabelFrame(self.frame, text="Video Input")
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Input controls
        input_controls = ttk.Frame(input_frame)
        input_controls.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(input_controls, text="Load Video", 
                  command=self.load_video).pack(side=tk.LEFT, padx=5)
        ttk.Button(input_controls, text="Clear", 
                  command=self.clear_video).pack(side=tk.LEFT, padx=5)
        
        # Video info display
        self.video_info_text = tk.Text(input_frame, height=4, state=tk.DISABLED)
        self.video_info_text.pack(fill=tk.X, padx=5, pady=5)
        
        # Control buttons
        control_frame = ttk.Frame(self.frame)
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(control_frame, text="Encode Video", 
                  command=self.encode_video).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Decode Video", 
                  command=self.decode_video).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Save Results", 
                  command=self.save_results).pack(side=tk.LEFT, padx=5)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.frame, variable=self.progress_var, 
                                          maximum=100, mode='determinate')
        self.progress_bar.pack(fill=tk.X, padx=5, pady=5)
        
        # Status label
        self.status_label = ttk.Label(self.frame, text="Ready")
        self.status_label.pack(anchor=tk.W, padx=5, pady=2)
        
        # Output section
        output_frame = ttk.LabelFrame(self.frame, text="Encoding Results")
        output_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Results display
        self.results_text = tk.Text(output_frame, state=tk.DISABLED)
        results_scrollbar = ttk.Scrollbar(output_frame, orient=tk.VERTICAL, 
                                        command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=results_scrollbar.set)
        
        self.results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        results_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
        
        # Statistics
        stats_frame = ttk.LabelFrame(self.frame, text="Video Statistics")
        stats_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.stats_text = tk.Text(stats_frame, height=4, state=tk.DISABLED)
        self.stats_text.pack(fill=tk.X, padx=5, pady=5)
    
    def load_video(self):
        logger.debug("Attempting to load video from file")
        filename = filedialog.askopenfilename(
            title="Select video file",
            filetypes=[
                ("Video files", "*.mp4 *.avi *.mov *.mkv *.flv"),
                ("AVI files", "*.avi"),
                ("MP4 files", "*.mp4"),
                ("All files", "*.*")
            ]
        )
        if filename:
            try:
                # Validate video file
                logger.info(f"Loading video from {filename}")
                cap = cv2.VideoCapture(filename)
                if not cap.isOpened():
                    raise ValueError("Cannot open video file")
                
                # Get video properties
                frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                fps = cap.get(cv2.CAP_PROP_FPS)
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                
                cap.release()
                
                self.current_video_path = filename
                
                # Display video info
                video_info = f"""Video File: {os.path.basename(filename)}
Resolution: {width}x{height}
Frame Rate: {fps:.2f} FPS
Total Frames: {frame_count}
Duration: {frame_count/fps:.2f} seconds"""
                
                self.update_video_info(video_info)
                self.update_status("Video loaded successfully")
                logger.info("Successfully loaded video")
                
            except Exception as e:
                logger.error(f"Could not load video: {str(e)}", exc_info=True)
                messagebox.showerror("Error", f"Could not load video: {str(e)}")
    
    def encode_video(self):
        if not self.current_video_path:
            logger.warning("Encode attempt with no video loaded")
            messagebox.showwarning("Warning", "Please load a video file first")
            return
        
        if self.processing:
            logger.warning("Encode attempt while already processing")
            messagebox.showwarning("Warning", "Processing already in progress")
            return
        
        # Start encoding in separate thread
        logger.info("Starting video encoding thread")
        thread = Thread(target=self._encode_video_thread)
        thread.daemon = True
        thread.start()
    
    def _encode_video_thread(self):
        try:
            self.processing = True
            self.update_status("Encoding video...")
            self.progress_var.set(0)
            
            from algorithms.video.h261 import H261Coder
            
            block_size = self.block_size_var.get()
            search_range = self.search_range_var.get()
            
            logger.info(f"Encoding video with block_size={block_size}, search_range={search_range}")
            coder = H261Coder(block_size=block_size, search_range=search_range)
            
            # Update progress callback
            def progress_callback(current, total):
                progress = (current / total) * 100
                self.progress_var.set(progress)
                self.update_status(f"Processing frame {current}/{total}")
            
            self.encoded_data, self.current_metadata = coder.encode(self.current_video_path)
            
            self.progress_var.set(100)
            self.update_status("Encoding completed successfully")
            
            # Display results
            results = f"""Encoding Results:
Algorithm: H.261 with Motion Estimation & Compensation
Block Size: {block_size}x{block_size}
Search Range: ±{search_range}
Total Frames: {self.current_metadata['frame_count']}
Frame Shape: {self.current_metadata['frame_shape']}

Motion Vector Statistics:
- I-frames: 1
- P-frames: {self.current_metadata['frame_count'] - 1}
"""
            
            self.update_results(results)
            
            # Update statistics
            stats = f"""Input: {os.path.basename(self.current_video_path)}
Frames Processed: {self.current_metadata['frame_count']}
Frame Dimensions: {self.current_metadata['frame_shape']}
Block Size: {block_size}x{block_size}"""
            
            self.update_stats(stats)
            
        except Exception as e:
            logger.error(f"Encoding failed: {str(e)}", exc_info=True)
            self.update_status(f"Encoding failed: {str(e)}")
            messagebox.showerror("Error", f"Encoding failed: {str(e)}")
        finally:
            self.processing = False
            self.progress_var.set(0)
    
    def decode_video(self):
        if not self.encoded_data or not self.current_metadata:
            logger.warning("Decode attempt with no encoded data")
            messagebox.showwarning("Warning", "No encoded data available. Please encode first.")
            return
        
        if self.processing:
            logger.warning("Decode attempt while already processing")
            messagebox.showwarning("Warning", "Processing already in progress")
            return
        
        # Ask for output filename
        output_path = filedialog.asksaveasfilename(
            title="Save decoded video",
            defaultextension=".avi",
            filetypes=[("AVI files", "*.avi"), ("MP4 files", "*.mp4")]
        )
        
        if not output_path:
            return
        
        # Start decoding in separate thread
        logger.info("Starting video decoding thread")
        thread = Thread(target=self._decode_video_thread, args=(output_path,))
        thread.daemon = True
        thread.start()
    
    def _decode_video_thread(self, output_path):
        try:
            self.processing = True
            self.update_status("Decoding video...")
            self.progress_var.set(0)
            
            from algorithms.video.h261 import H261Coder
            
            logger.info(f"Decoding video to {output_path}")
            coder = H261Coder()
            decoded_frames = coder.decode(self.encoded_data, self.current_metadata)
            
            # Save decoded video
            if decoded_frames:
                height, width = decoded_frames[0].shape
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                out = cv2.VideoWriter(output_path, fourcc, 30.0, (width, height), isColor=False)
                
                for i, frame in enumerate(decoded_frames):
                    out.write(frame)
                    progress = ((i + 1) / len(decoded_frames)) * 100
                    self.progress_var.set(progress)
                    self.update_status(f"Writing frame {i + 1}/{len(decoded_frames)}")
                
                out.release()
                
                self.update_status(f"Video decoded and saved to {output_path}")
                logger.info(f"Video decoded and saved to {output_path}")
                messagebox.showinfo("Success", f"Video decoded successfully!\nSaved to: {output_path}")
            
        except Exception as e:
            logger.error(f"Decoding failed: {str(e)}", exc_info=True)
            self.update_status(f"Decoding failed: {str(e)}")
            messagebox.showerror("Error", f"Decoding failed: {str(e)}")
        finally:
            self.processing = False
            self.progress_var.set(0)
    
    def save_results(self):
        if not self.current_metadata:
            logger.warning("Save results attempt with no metadata")
            messagebox.showwarning("Warning", "No results to save")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Save results",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                # Prepare serializable results (exclude actual frame data)
                logger.info(f"Saving results to {filename}")
                results = {
                    'algorithm': 'H.261',
                    'video_file': self.current_video_path,
                    'settings': {
                        'block_size': self.block_size_var.get(),
                        'search_range': self.search_range_var.get()
                    },
                    'metadata': {
                        'frame_count': self.current_metadata['frame_count'],
                        'frame_shape': self.current_metadata['frame_shape'],
                        'block_size': self.current_metadata['block_size'],
                        'search_range': self.current_metadata['search_range']
                    }
                }
                
                with open(filename, 'w') as f:
                    json.dump(results, f, indent=2, default=str)
                
                logger.info("Results saved successfully")
                messagebox.showinfo("Success", "Results saved successfully")
            except Exception as e:
                logger.error(f"Could not save results: {str(e)}", exc_info=True)
                messagebox.showerror("Error", f"Could not save results: {str(e)}")
    
    def clear_video(self):
        logger.info("Clearing video, encoded data, and stats")
        self.current_video_path = None
        self.encoded_data = None
        self.current_metadata = None
        self.update_video_info("")
        self.update_results("")
        self.update_stats("")
        self.update_status("Ready")
        self.progress_var.set(0)
    
    def update_video_info(self, text):
        self.video_info_text.config(state=tk.NORMAL)
        self.video_info_text.delete(1.0, tk.END)
        self.video_info_text.insert(1.0, text)
        self.video_info_text.config(state=tk.DISABLED)
    
    def update_results(self, text):
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(1.0, text)
        self.results_text.config(state=tk.DISABLED)
    
    def update_stats(self, text):
        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(1.0, text)
        self.stats_text.config(state=tk.DISABLED)
    
    def update_status(self, text):
        self.status_label.config(text=text)
        self.frame.update_idletasks()
