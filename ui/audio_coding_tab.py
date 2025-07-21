# ui/audio_coding_tab.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import json
import wave
import struct
from core.logger import get_logger

logger = get_logger(__name__)

class AudioCodingTab:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.setup_ui()
        self.current_audio_data = None
        self.encoded_data = None
        self.current_metadata = None
        logger.info("AudioCodingTab initialized")
    
    def setup_ui(self):
        logger.debug("Setting up UI for AudioCodingTab")
        # Algorithm selection
        algo_frame = ttk.LabelFrame(self.frame, text="Audio Coding Algorithm")
        algo_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(algo_frame, text="Algorithm:").pack(side=tk.LEFT, padx=5)
        self.algorithm_var = tk.StringVar()
        self.algorithm_combo = ttk.Combobox(algo_frame, textvariable=self.algorithm_var,
                                          values=["LPC", "MPEG-Audio"], state="readonly")
        self.algorithm_combo.pack(side=tk.LEFT, padx=5)
        self.algorithm_combo.current(0)
        
        # LPC-specific settings
        lpc_frame = ttk.LabelFrame(self.frame, text="LPC Settings")
        lpc_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(lpc_frame, text="LPC Order:").pack(side=tk.LEFT, padx=5)
        self.lpc_order_var = tk.IntVar(value=10)
        lpc_order_spin = ttk.Spinbox(lpc_frame, from_=2, to=50, 
                                   textvariable=self.lpc_order_var, width=10)
        lpc_order_spin.pack(side=tk.LEFT, padx=5)
        
        # Input section
        input_frame = ttk.LabelFrame(self.frame, text="Audio Input")
        input_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Input controls
        input_controls = ttk.Frame(input_frame)
        input_controls.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(input_controls, text="Load Audio File", 
                  command=self.load_audio_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(input_controls, text="Manual Input", 
                  command=self.show_manual_input).pack(side=tk.LEFT, padx=5)
        ttk.Button(input_controls, text="Clear", 
                  command=self.clear_input).pack(side=tk.LEFT, padx=5)
        
        # Audio data display
        data_frame = ttk.Frame(input_frame)
        data_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        ttk.Label(data_frame, text="Audio Data (first 100 samples):").pack(anchor=tk.W)
        self.audio_data_text = scrolledtext.ScrolledText(data_frame, height=6)
        self.audio_data_text.pack(fill=tk.BOTH, expand=True, pady=2)
        
        # Control buttons
        control_frame = ttk.Frame(self.frame)
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(control_frame, text="Encode", command=self.encode_audio).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Decode", command=self.decode_audio).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Save Results", command=self.save_results).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Load Encoded JSON", command=self.load_encoded_json).pack(side=tk.LEFT, padx=5)
        
        # Output section
        output_frame = ttk.LabelFrame(self.frame, text="Encoded Output")
        output_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, height=6)
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Statistics
        stats_frame = ttk.LabelFrame(self.frame, text="Encoding Statistics")
        stats_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.stats_text = tk.Text(stats_frame, height=4, state=tk.DISABLED)
        self.stats_text.pack(fill=tk.X, padx=5, pady=5)
    
    def load_audio_file(self):
        logger.debug("Attempting to load audio from file")
        filename = filedialog.askopenfilename(
            title="Select audio file",
            filetypes=[
                ("WAV files", "*.wav"),
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ]
        )
        if filename:
            try:
                logger.info(f"Loading audio from {filename}")
                if filename.lower().endswith('.wav'):
                    self.load_wav_file(filename)
                else:
                    self.load_text_file(filename)
                logger.info("Successfully loaded audio from file")
            except Exception as e:
                logger.error(f"Could not load audio file: {str(e)}", exc_info=True)
                messagebox.showerror("Error", f"Could not load audio file: {str(e)}")
    
    def load_wav_file(self, filename):
        """Load WAV file and extract audio samples"""
        with wave.open(filename, 'rb') as wav_file:
            frames = wav_file.readframes(-1)
            sample_width = wav_file.getsampwidth()
            
            if sample_width == 1:
                fmt = 'B'  # unsigned char
            elif sample_width == 2:
                fmt = 'h'  # short
            elif sample_width == 4:
                fmt = 'l'  # long
            else:
                raise ValueError(f"Unsupported sample width: {sample_width}")
            
            # Unpack audio data
            audio_samples = struct.unpack(f'{len(frames)//sample_width}{fmt}', frames)
            
            # Convert to normalized float values
            if sample_width == 1:
                self.current_audio_data = [(sample - 128) / 128.0 for sample in audio_samples]
            elif sample_width == 2:
                self.current_audio_data = [sample / 32768.0 for sample in audio_samples]
            else:
                self.current_audio_data = [sample / 2147483648.0 for sample in audio_samples]
            
            self.display_audio_data()
            self.update_stats(f"Loaded {len(self.current_audio_data)} samples from WAV file")
    
    def load_text_file(self, filename):
        """Load audio samples from text file"""
        with open(filename, 'r') as f:
            content = f.read().strip()
            try:
                # Try to parse as space-separated numbers
                self.current_audio_data = list(map(float, content.split()))
                self.display_audio_data()
                self.update_stats(f"Loaded {len(self.current_audio_data)} samples from text file")
            except ValueError:
                messagebox.showerror("Error", "Invalid audio data format in text file")
    
    def show_manual_input(self):
        """Show dialog for manual audio data input"""
        logger.debug("Showing manual audio input dialog")
        popup = tk.Toplevel(self.frame)
        popup.title("Manual Audio Input")
        popup.geometry("500x300")
        
        ttk.Label(popup, text="Enter audio samples (space-separated numbers):").pack(anchor=tk.W, padx=10, pady=5)
        
        text_widget = scrolledtext.ScrolledText(popup)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        def apply_input():
            try:
                content = text_widget.get(1.0, tk.END).strip()
                self.current_audio_data = list(map(float, content.split()))
                self.display_audio_data()
                self.update_stats(f"Loaded {len(self.current_audio_data)} samples manually")
                popup.destroy()
                logger.info("Applied manual audio input")
            except ValueError:
                logger.warning("Invalid manual audio data format")
                messagebox.showerror("Error", "Invalid audio data format")
        
        button_frame = ttk.Frame(popup)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(button_frame, text="Apply", command=apply_input).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=popup.destroy).pack(side=tk.RIGHT, padx=5)
    
    def display_audio_data(self):
        """Display first 100 audio samples"""
        if not self.current_audio_data:
            return
        
        display_data = self.current_audio_data[:100]
        formatted_data = ' '.join([f"{sample:.4f}" for sample in display_data])
        
        if len(self.current_audio_data) > 100:
            formatted_data += f"\n... and {len(self.current_audio_data) - 100} more samples"
        
        self.audio_data_text.delete(1.0, tk.END)
        self.audio_data_text.insert(1.0, formatted_data)
    
    def encode_audio(self):
        if not self.current_audio_data:
            logger.warning("Encode attempt with no audio data")
            messagebox.showwarning("Warning", "Please load audio data first")
            return
        
        try:
            algorithm = self.algorithm_var.get()
            logger.info(f"Encoding audio with algorithm: {algorithm}")
            
            if algorithm == "LPC":
                from algorithms.audio.lpc import LPCCoder
                order = self.lpc_order_var.get()
                coder = LPCCoder(order=order)
            else:
                logger.info("MPEG-Audio encoding is not implemented")
                messagebox.showinfo("Info", "MPEG-Audio encoding is not implemented in this demo")
                return
            
            self.encoded_data, self.current_metadata = coder.encode(self.current_audio_data)
            
            # Handle case where encoding returns empty coefficients
            if self.encoded_data is None or self.encoded_data.size == 0:
                logger.error("LPC encoding failed to produce valid coefficients.")
                messagebox.showerror("Error", "LPC encoding failed. The signal may be too short for the selected LPC order.")
                return
            
            # Display encoded coefficients
            if hasattr(self.encoded_data, 'tolist'):
                encoded_display = self.encoded_data.tolist()
            else:
                encoded_display = self.encoded_data
            
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(1.0, str(encoded_display))
            
            # Update statistics
            stats = f"""Algorithm: {algorithm}
Original samples: {len(self.current_audio_data)}
LPC coefficients: {len(encoded_display)}
LPC order: {self.current_metadata.get('order', 'N/A')}"""
            
            self.update_stats(stats)
            logger.info("Audio encoded successfully")
            messagebox.showinfo("Success", "Audio encoded successfully!")
            
        except Exception as e:
            logger.error(f"Encoding failed: {str(e)}", exc_info=True)
            messagebox.showerror("Error", f"Encoding failed: {str(e)}")
    
    def load_encoded_json(self):
        filename = filedialog.askopenfilename(
            title="Load encoded LPC JSON",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'r') as f:
                    data = json.load(f)
                self.current_metadata = data['metadata']
                import numpy as np
                self.encoded_data = np.array(data['encoded_data'])
                self.output_text.delete(1.0, tk.END)
                self.output_text.insert(1.0, str(self.encoded_data.tolist()))
                messagebox.showinfo("Success", "Encoded LPC data loaded. You can now decode.")
            except Exception as e:
                messagebox.showerror("Error", f"Could not load encoded JSON: {str(e)}")

    def decode_audio(self):
        if self.encoded_data is None or not self.current_metadata:
            logger.warning("Decode attempt with no encoded data")
            messagebox.showwarning("Warning", "No encoded data available. Please encode first.")
            return
        try:
            algorithm = self.algorithm_var.get()
            logger.info(f"Decoding audio with algorithm: {algorithm}")
            if algorithm == "LPC":
                from algorithms.audio.lpc import LPCCoder
                coder = LPCCoder()
                decoded_audio = coder.decode(self.encoded_data, self.current_metadata)
            else:
                logger.info("MPEG-Audio decoding is not implemented")
                messagebox.showinfo("Info", "MPEG-Audio decoding is not implemented in this demo")
                return
            # Display decoded audio in output_text instead of popup
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(1.0, ' '.join([f"{sample:.4f}" for sample in decoded_audio[:200]]))
            if len(decoded_audio) > 200:
                self.output_text.insert(tk.END, f"\n... and {len(decoded_audio) - 200} more samples")
            logger.info("Audio decoded successfully")
        except Exception as e:
            logger.error(f"Decoding failed: {str(e)}", exc_info=True)
            messagebox.showerror("Error", f"Decoding failed: {str(e)}")
    
    def show_decoded_audio(self, decoded_audio):
        """Show decoded audio data in popup window"""
        logger.debug("Showing decoded audio in popup")
        popup = tk.Toplevel(self.frame)
        popup.title("Decoded Audio")
        popup.geometry("600x400")
        
        ttk.Label(popup, text="Decoded Audio Samples:").pack(anchor=tk.W, padx=10, pady=5)
        
        text_widget = scrolledtext.ScrolledText(popup)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Display first 200 samples
        display_samples = decoded_audio[:200]
        formatted_data = ' '.join([f"{sample:.4f}" for sample in display_samples])
        
        if len(decoded_audio) > 200:
            formatted_data += f"\n\n... and {len(decoded_audio) - 200} more samples"
        
        text_widget.insert(1.0, formatted_data)
        text_widget.config(state=tk.DISABLED)
        
        ttk.Button(popup, text="Close", command=popup.destroy).pack(pady=10)
    
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
                logger.info(f"Saving results to {filename}")
                results = {
                    'algorithm': self.algorithm_var.get(),
                    'audio_data': self.current_audio_data,
                    'encoded_data': self.encoded_data.tolist() if hasattr(self.encoded_data, 'tolist') else self.encoded_data,
                    'metadata': self.current_metadata
                }
                
                with open(filename, 'w') as f:
                    json.dump(results, f, indent=2, default=str)
                
                logger.info("Results saved successfully")
                messagebox.showinfo("Success", "Results saved successfully")
            except Exception as e:
                logger.error(f"Could not save results: {str(e)}", exc_info=True)
                messagebox.showerror("Error", f"Could not save results: {str(e)}")
    
    def clear_input(self):
        logger.info("Clearing audio input, output, and stats")
        self.current_audio_data = None
        self.encoded_data = None
        self.current_metadata = None
        self.audio_data_text.delete(1.0, tk.END)
        self.output_text.delete(1.0, tk.END)
        self.update_stats("")
    
    def update_stats(self, text):
        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(1.0, text)
        self.stats_text.config(state=tk.DISABLED)
