# ui/text_coding_tab.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from core.factory import coder_factory
import json
from core.logger import get_logger
from decimal import Decimal

logger = get_logger(__name__)

class TextCodingTab:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.setup_ui()
        self.current_metadata = None
        logger.info("TextCodingTab initialized")
    
    def setup_ui(self):
        logger.debug("Setting up UI for TextCodingTab")
        # Algorithm selection
        algo_frame = ttk.LabelFrame(self.frame, text="Algorithm Selection")
        algo_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(algo_frame, text="Algorithm:").pack(side=tk.LEFT, padx=5)
        self.algorithm_var = tk.StringVar()
        self.algorithm_combo = ttk.Combobox(algo_frame, textvariable=self.algorithm_var,
                                          values=["Shannon-Fano", "Huffman", "Arithmetic", 
                                                "Run Length Encoding", "LZW"], state="readonly")
        self.algorithm_combo.pack(side=tk.LEFT, padx=5)
        self.algorithm_combo.current(0)
        
        # Input section
        input_frame = ttk.LabelFrame(self.frame, text="Input")
        input_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Input options
        input_options_frame = ttk.Frame(input_frame)
        input_options_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(input_options_frame, text="Load from File", 
                  command=self.load_from_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(input_options_frame, text="Clear", 
                  command=self.clear_input).pack(side=tk.LEFT, padx=5)
        
        # Text input
        self.input_text = scrolledtext.ScrolledText(input_frame, height=8)
        self.input_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Control buttons
        control_frame = ttk.Frame(self.frame)
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(control_frame, text="Encode", command=self.encode_text).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Decode", command=self.decode_text).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Save Results", command=self.save_results).pack(side=tk.LEFT, padx=5)
        
        # Output section
        output_frame = ttk.LabelFrame(self.frame, text="Output")
        output_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, height=8)
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Statistics section
        stats_frame = ttk.LabelFrame(self.frame, text="Statistics")
        stats_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.stats_text = tk.Text(stats_frame, height=4, state=tk.DISABLED)
        self.stats_text.pack(fill=tk.X, padx=5, pady=5)
    
    def load_from_file(self):
        logger.debug("Attempting to load text from file")
        filename = filedialog.askopenfilename(
            title="Select text file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            try:
                logger.info(f"Loading text from {filename}")
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.input_text.delete(1.0, tk.END)
                self.input_text.insert(1.0, content)
                logger.info("Successfully loaded text from file")
            except Exception as e:
                logger.error(f"Could not load file: {str(e)}", exc_info=True)
                messagebox.showerror("Error", f"Could not load file: {str(e)}")
    
    def clear_input(self):
        logger.info("Clearing text input, output, and stats")
        self.input_text.delete(1.0, tk.END)
        self.output_text.delete(1.0, tk.END)
        self.update_stats("")
    
    def encode_text(self):
        try:
            text = self.input_text.get(1.0, tk.END).strip()
            if not text:
                logger.warning("Encode attempt with no input text")
                messagebox.showwarning("Warning", "Please enter text to encode")
                return
            
            algorithm = self.algorithm_var.get()
            logger.info(f"Encoding text with algorithm: {algorithm}")
            coder = self._get_coder(algorithm)
            
            encoded_data, metadata = coder.encode(text)
            self.current_metadata = metadata
            
            # For Arithmetic coding, store the Decimal object directly
            if algorithm == "Arithmetic":
                self.encoded_decimal = encoded_data

            # Display results
            if isinstance(encoded_data, list):
                result = ' '.join(map(str, encoded_data))
            else:
                result = str(encoded_data)
            
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(1.0, result)
            
            # Update statistics
            self.update_stats(self.format_stats(metadata, True))
            logger.info("Text successfully encoded and results displayed")
            
        except Exception as e:
            logger.error(f"Encoding failed: {str(e)}", exc_info=True)
            messagebox.showerror("Error", f"Encoding failed: {str(e)}")
    
    def decode_text(self):
        try:
            if not self.current_metadata:
                logger.warning("Decode attempt with no metadata")
                messagebox.showwarning("Warning", "No encoding metadata available. Please encode first.")
                return
            
            encoded_text = self.output_text.get(1.0, tk.END).strip()
            if not encoded_text:
                logger.warning("Decode attempt with no encoded data")
                messagebox.showwarning("Warning", "No encoded data to decode")
                return
            
            algorithm = self.algorithm_var.get()
            logger.info(f"Decoding text with algorithm: {algorithm}")
            coder = self._get_coder(algorithm)
            
            # Convert encoded data back to appropriate format
            if algorithm == "LZW":
                encoded_data = list(map(int, encoded_text.split()))
            elif algorithm == "Arithmetic":
                # Use the stored Decimal object for decoding
                if hasattr(self, 'encoded_decimal'):
                    encoded_data = self.encoded_decimal
                else:
                    # Fallback for manual input or other cases
                    encoded_data = Decimal(encoded_text)
            else:
                encoded_data = encoded_text
            
            decoded_text = coder.decode(encoded_data, self.current_metadata)
            
            # Show decoded result in a popup
            self.show_decode_result(decoded_text)
            logger.info("Text successfully decoded")
            
        except Exception as e:
            logger.error(f"Decoding failed: {str(e)}", exc_info=True)
            messagebox.showerror("Error", f"Decoding failed: {str(e)}")
    
    def _get_coder(self, algorithm):
        from algorithms.text.shannon_fano import ShannonFanoCoder
        from algorithms.text.huffman import HuffmanCoder
        from algorithms.text.arithmetic import ArithmeticCoder
        from algorithms.text.run_length import RunLengthCoder
        from algorithms.text.lzw import LZWCoder
        
        coders = {
            "Shannon-Fano": ShannonFanoCoder(),
            "Huffman": HuffmanCoder(),
            "Arithmetic": ArithmeticCoder(),
            "Run Length Encoding": RunLengthCoder(),
            "LZW": LZWCoder()
        }
        logger.debug(f"Retrieved coder for algorithm: {algorithm}")
        return coders[algorithm]
    
    def format_stats(self, metadata, is_encoding=True):
        stats = []
        if 'original_length' in metadata:
            stats.append(f"Original length: {metadata['original_length']}")
        if 'encoded_length' in metadata:
            stats.append(f"Encoded length: {metadata['encoded_length']}")
        if 'compression_ratio' in metadata:
            stats.append(f"Compression ratio: {metadata['compression_ratio']:.2f}")
        elif 'original_length' in metadata and 'encoded_length' in metadata:
            if metadata['encoded_length'] > 0:
                ratio = metadata['original_length'] / metadata['encoded_length']
                stats.append(f"Compression ratio: {ratio:.2f}")
        
        return '\n'.join(stats)
    
    def update_stats(self, text):
        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(1.0, text)
        self.stats_text.config(state=tk.DISABLED)
    
    def show_decode_result(self, decoded_text):
        # Create popup window for decoded result
        logger.debug("Showing decoded text in popup")
        popup = tk.Toplevel(self.frame)
        popup.title("Decoded Result")
        popup.geometry("600x400")
        
        ttk.Label(popup, text="Decoded Text:").pack(anchor=tk.W, padx=10, pady=5)
        
        text_widget = scrolledtext.ScrolledText(popup)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        text_widget.insert(1.0, decoded_text)
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
                
                encoded_output = self.output_text.get(1.0, tk.END).strip()
                # For Arithmetic, ensure the high-precision string is saved
                if self.algorithm_var.get() == "Arithmetic" and hasattr(self, 'encoded_decimal'):
                    encoded_output = str(self.encoded_decimal)

                results = {
                    'algorithm': self.algorithm_var.get(),
                    'input_text': self.input_text.get(1.0, tk.END).strip(),
                    'encoded_data': encoded_output,
                    'metadata': self.current_metadata
                }
                
                with open(filename, 'w') as f:
                    json.dump(results, f, indent=2, default=str)
                
                logger.info("Results saved successfully")
                messagebox.showinfo("Success", "Results saved successfully")
            except Exception as e:
                logger.error(f"Could not save results: {str(e)}", exc_info=True)
                messagebox.showerror("Error", f"Could not save results: {str(e)}")
