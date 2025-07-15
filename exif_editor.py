# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import piexif
import json
import webbrowser
import http.server
import socketserver
import threading
import urllib.parse
from pathlib import Path
import os
import sys

class LocationPicker:
    def __init__(self):
        self.selected_location = None
        self.server_thread = None
        self.server = None
        
    def start_server(self):
        """Start a simple HTTP server for location picking"""
        class LocationHandler(http.server.SimpleHTTPRequestHandler):
            def do_GET(self):
                if self.path == '/':
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    
                    html = '''
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <title>Location Picker</title>
                        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
                        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
                        <style>
                            body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f0f0f0; }
                            .container { max-width: 1000px; margin: 0 auto; background: white; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); overflow: hidden; }
                            .header { padding: 20px; background: #007bff; color: white; text-align: center; }
                            .header h1 { margin: 0; font-size: 24px; }
                            .content { display: flex; min-height: 600px; }
                            .map-container { flex: 2; height: 500px; }
                            #map { height: 100%; width: 100%; }
                            .controls { flex: 1; padding: 20px; }
                            .input-group { margin: 20px 0; }
                            label { display: block; margin-bottom: 5px; font-weight: bold; color: #555; }
                            input, select { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; font-size: 14px; box-sizing: border-box; }
                            button { background: #007bff; color: white; padding: 12px 24px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; width: 100%; margin: 5px 0; }
                            button:hover { background: #0056b3; }
                            .coordinates { display: flex; gap: 10px; }
                            .coordinates input { flex: 1; }
                            .result { margin-top: 20px; padding: 15px; background: #e8f5e8; border-radius: 5px; display: none; }
                            .search-btn { background: #28a745; }
                            .search-btn:hover { background: #218838; }
                            .clear-btn { background: #6c757d; }
                            .clear-btn:hover { background: #5a6268; }
                            .error { color: red; margin-top: 10px; }
                        </style>
                    </head>
                    <body>
                        <div class="container">
                            <div class="header">
                                <h1>Interactive Location Picker</h1>
                                <p>Click on the map or search for a location</p>
                            </div>
                            
                            <div class="content">
                                <div class="map-container">
                                    <div id="map"></div>
                                </div>
                                
                                <div class="controls">
                                    <div class="input-group">
                                        <label for="search">Search Location:</label>
                                        <input type="text" id="search" placeholder="e.g., Istanbul, Turkey" />
                                        <button class="search-btn" onclick="searchLocation()">Search</button>
                                    </div>
                                    
                                    <div class="input-group">
                                        <label>Coordinates:</label>
                                        <div class="coordinates">
                                            <input type="number" id="lat" placeholder="Latitude" step="any" />
                                            <input type="number" id="lng" placeholder="Longitude" step="any" />
                                        </div>
                                    </div>
                                    
                                    <div class="input-group">
                                        <label for="location_name">Location Name:</label>
                                        <input type="text" id="location_name" placeholder="e.g., Hagia Sophia, Istanbul" />
                                    </div>
                                    
                                    <button onclick="setLocation()">Set Location</button>
                                    <button class="clear-btn" onclick="clearLocation()">Clear</button>
                                    
                                    <div id="result" class="result">
                                        <strong>Location set successfully!</strong><br>
                                        <span id="result_text"></span>
                                    </div>
                                    
                                    <div id="error" class="error" style="display: none;"></div>
                                </div>
                            </div>
                        </div>
                        
                        <script>
                            let map, marker;
                            
                            // Initialize map
                            function initMap() {
                                try {
                                    console.log('Initializing map...');
                                    map = L.map('map').setView([41.0082, 28.9784], 10); // Istanbul default
                                    
                                    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                                        attribution: '© OpenStreetMap contributors'
                                    }).addTo(map);
                                    
                                    console.log('Map initialized successfully');
                                    
                                    // Add click event to map
                                    map.on('click', function(e) {
                                        const lat = e.latlng.lat;
                                        const lng = e.latlng.lng;
                                        
                                        document.getElementById('lat').value = lat.toFixed(6);
                                        document.getElementById('lng').value = lng.toFixed(6);
                                        
                                        // Update marker
                                        if (marker) {
                                            map.removeLayer(marker);
                                        }
                                        marker = L.marker([lat, lng]).addTo(map);
                                        
                                        // Try to get location name
                                        fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}`)
                                            .then(response => response.json())
                                            .then(data => {
                                                if (data.display_name) {
                                                    const name = data.display_name.split(',')[0];
                                                    document.getElementById('location_name').value = name;
                                                }
                                            })
                                            .catch(error => console.log('Could not get location name'));
                                    });
                                } catch (error) {
                                    console.error('Error initializing map:', error);
                                    document.getElementById('error').textContent = 'Error loading map: ' + error.message;
                                    document.getElementById('error').style.display = 'block';
                                }
                            }
                            
                            function searchLocation() {
                                const search = document.getElementById('search').value;
                                if (!search) return;
                                
                                fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(search)}&limit=1`)
                                    .then(response => response.json())
                                    .then(data => {
                                        if (data.length > 0) {
                                            const location = data[0];
                                            const lat = parseFloat(location.lat);
                                            const lng = parseFloat(location.lon);
                                            
                                            document.getElementById('lat').value = lat.toFixed(6);
                                            document.getElementById('lng').value = lng.toFixed(6);
                                            document.getElementById('location_name').value = location.display_name.split(',')[0];
                                            
                                            // Update map
                                            map.setView([lat, lng], 15);
                                            
                                            if (marker) {
                                                map.removeLayer(marker);
                                            }
                                            marker = L.marker([lat, lng]).addTo(map);
                                        } else {
                                            alert('Location not found. Please try a different search term.');
                                        }
                                    })
                                    .catch(error => {
                                        alert('Search failed. Please try again.');
                                    });
                            }
                            
                            function clearLocation() {
                                document.getElementById('lat').value = '';
                                document.getElementById('lng').value = '';
                                document.getElementById('location_name').value = '';
                                document.getElementById('search').value = '';
                                
                                if (marker) {
                                    map.removeLayer(marker);
                                    marker = null;
                                }
                            }
                            
                            function setLocation() {
                                const lat = document.getElementById('lat').value;
                                const lng = document.getElementById('lng').value;
                                const locationName = document.getElementById('location_name').value;
                                
                                if (!lat || !lng) {
                                    alert('Please select a location on the map or enter coordinates');
                                    return;
                                }
                                
                                const locationData = {
                                    lat: parseFloat(lat),
                                    lng: parseFloat(lng),
                                    name: locationName || 'Custom Location'
                                };
                                
                                console.log('Sending location data:', locationData);
                                
                                // Send location data back to Python
                                fetch('/set_location', {
                                    method: 'POST',
                                    headers: {'Content-Type': 'application/json'},
                                    body: JSON.stringify(locationData)
                                }).then(response => {
                                    if (response.ok) {
                                        document.getElementById('result_text').textContent = 
                                            `${locationData.name} (${lat}, ${lng})`;
                                        document.getElementById('result').style.display = 'block';
                                        
                                        // Close window after 2 seconds
                                        setTimeout(() => {
                                            window.close();
                                        }, 2000);
                                    } else {
                                        throw new Error('Server error');
                                    }
                                }).catch(error => {
                                    console.error('Error setting location:', error);
                                    alert('Failed to set location. Please try again.');
                                });
                            }
                            
                            // Initialize map when page loads
                            window.onload = function() {
                                console.log('Page loaded, initializing map...');
                                setTimeout(initMap, 100); // Small delay to ensure DOM is ready
                            };
                            
                            // Enter key to search
                            document.getElementById('search').addEventListener('keypress', function(e) {
                                if (e.key === 'Enter') {
                                    searchLocation();
                                }
                            });
                        </script>
                    </body>
                    </html>
                    '''
                    self.wfile.write(html.encode())
                    
                elif self.path == '/set_location':
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(b'{"status": "ok"}')
                    
                else:
                    self.send_response(404)
                    self.end_headers()
                    
            def do_POST(self):
                if self.path == '/set_location':
                    try:
                        content_length = int(self.headers['Content-Length'])
                        post_data = self.rfile.read(content_length)
                        location_data = json.loads(post_data.decode('utf-8'))
                        
                        # Store the location data
                        self.server.location_picker.selected_location = location_data
                        
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.send_header('Access-Control-Allow-Origin', '*')
                        self.end_headers()
                        self.wfile.write(b'{"status": "ok"}')
                    except Exception as e:
                        print(f"Error processing POST request: {e}")
                        self.send_response(500)
                        self.end_headers()
                else:
                    self.send_response(404)
                    self.end_headers()
        
        # Create server with custom handler
        handler = LocationHandler
        
        self.server = socketserver.TCPServer(("", 0), handler)  # Use port 0 to get a random available port
        self.server.location_picker = self  # Store reference to location picker
        port = self.server.server_address[1]
        
        # Start server in a separate thread
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()
        
        return port
    
    def stop_server(self):
        """Stop the HTTP server"""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
    
    def pick_location(self):
        """Open location picker in browser and wait for selection"""
        port = self.start_server()
        url = f"http://localhost:{port}"
        
        print(f"Opening location picker at: {url}")
        webbrowser.open(url)
        
        # Wait for location selection
        while self.selected_location is None:
            import time
            time.sleep(0.1)
        
        self.stop_server()
        return self.selected_location

class EXIFEditor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("EXIF Editor - Ozan's Photo Tool")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        self.current_image_path = None
        self.photo_tk = None
        self.location_picker = LocationPicker()
        self.selected_location = None
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="EXIF Editor", font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # File selection
        file_frame = ttk.LabelFrame(main_frame, text="Image Selection", padding="10")
        file_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        file_frame.columnconfigure(1, weight=1)
        
        ttk.Label(file_frame, text="Image:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.file_label = ttk.Label(file_frame, text="No file selected", foreground="gray")
        self.file_label.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        browse_btn = ttk.Button(file_frame, text="Browse", command=self.browse_file)
        browse_btn.grid(row=0, column=2)
        
        # Image preview
        preview_frame = ttk.LabelFrame(main_frame, text="Image Preview", padding="10")
        preview_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.rowconfigure(0, weight=1)
        
        self.preview_label = ttk.Label(preview_frame, text="Select an image to preview", 
                                     background="white", relief="solid", borderwidth=1)
        self.preview_label.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Location section
        location_frame = ttk.LabelFrame(main_frame, text="Location Settings", padding="10")
        location_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        location_frame.columnconfigure(1, weight=1)
        
        ttk.Label(location_frame, text="Location:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.location_label = ttk.Label(location_frame, text="No location set", foreground="gray")
        self.location_label.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        location_btn = ttk.Button(location_frame, text="Pick Location", command=self.pick_location)
        location_btn.grid(row=0, column=2)
        
        # Photographer info
        photographer_frame = ttk.LabelFrame(main_frame, text="Photographer Info", padding="10")
        photographer_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        photographer_frame.columnconfigure(1, weight=1)
        
        ttk.Label(photographer_frame, text="Photographer:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.photographer_var = tk.StringVar(value="Ozan Kaygusuz")
        photographer_entry = ttk.Entry(photographer_frame, textvariable=self.photographer_var)
        photographer_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Update button
        update_btn = ttk.Button(main_frame, text="Update EXIF Data", command=self.update_exif, 
                              style="Accent.TButton")
        update_btn.grid(row=5, column=0, columnspan=2, pady=(20, 0))
        
        # Status
        self.status_label = ttk.Label(main_frame, text="Ready", foreground="gray")
        self.status_label.grid(row=6, column=0, columnspan=2, pady=(10, 0))
        
    def browse_file(self):
        """Browse for image file"""
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff"),
                ("JPEG files", "*.jpg *.jpeg"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            self.current_image_path = file_path
            self.file_label.config(text=Path(file_path).name)
            self.load_image_preview()
            self.status_label.config(text=f"Loaded: {Path(file_path).name}")

    def load_image_preview(self):
        """Load and display image preview"""
        if not self.current_image_path:
            return
        try:
            image = Image.open(self.current_image_path)
            image.thumbnail((300, 300), Image.Resampling.LANCZOS)
            self.photo_tk = ImageTk.PhotoImage(image)
            self.preview_label.config(image=self.photo_tk, text="")
        except Exception as e:
            messagebox.showerror("Error", f"Could not load image: {str(e)}")
    
    def pick_location(self):
        """Open location picker"""
        if not self.current_image_path:
            messagebox.showwarning("Warning", "Please select an image first")
            return
        try:
            location = self.location_picker.pick_location()
            if location:
                self.selected_location = location
                self.location_label.config(
                    text=f"{location['name']} ({location['lat']:.4f}, {location['lng']:.4f})",
                    foreground="black"
                )
                self.status_label.config(text="Location selected")
        except Exception as e:
            messagebox.showerror("Error", f"Location picker error: {str(e)}")
    
    def update_exif(self):
        """Update EXIF data in the image"""
        if not self.current_image_path:
            messagebox.showwarning("Warning", "Please select an image first")
            return
        if not self.selected_location:
            messagebox.showwarning("Warning", "Please pick a location first")
            return
        try:
            image = Image.open(self.current_image_path)
            image = self.add_watermark(image, self.photographer_var.get())
            exif_dict = piexif.load(image.info.get("exif", b"")) if "exif" in image.info else {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}
            location = self.selected_location
            lat = location['lat']
            lng = location['lng']
            def decimal_to_dms(decimal):
                degrees = int(abs(decimal))
                minutes = int((abs(decimal) - degrees) * 60)
                seconds = int(((abs(decimal) - degrees - minutes/60) * 3600))
                return ((degrees, 1), (minutes, 1), (seconds, 1))
            exif_dict["GPS"][piexif.GPSIFD.GPSLatitudeRef] = b"N" if lat >= 0 else b"S"
            exif_dict["GPS"][piexif.GPSIFD.GPSLatitude] = decimal_to_dms(abs(lat))
            exif_dict["GPS"][piexif.GPSIFD.GPSLongitudeRef] = b"E" if lng >= 0 else b"W"
            exif_dict["GPS"][piexif.GPSIFD.GPSLongitude] = decimal_to_dms(abs(lng))
            photographer = self.photographer_var.get()
            if photographer:
                exif_dict["0th"][piexif.ImageIFD.Artist] = photographer.encode('utf-8')
                exif_dict["0th"][piexif.ImageIFD.Copyright] = f"© {photographer}".encode('utf-8')
            exif_bytes = piexif.dump(exif_dict)
            image.save(self.current_image_path, exif=exif_bytes)
            messagebox.showinfo("Success", "EXIF data updated successfully!")
            self.status_label.config(text="EXIF data updated")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update EXIF data: {str(e)}")
            self.status_label.config(text="Error updating EXIF data")

    def add_watermark(self, image, photographer):
        """Add a small watermark to the bottom left of the image"""
        from PIL import ImageDraw, ImageFont
        draw = ImageDraw.Draw(image)
        text = photographer if photographer else "Ozan Kaygusuz"
        font_size = max(16, image.width // 40)
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except Exception:
            font = ImageFont.load_default()
        # Get text size (use textbbox if available, else fallback to textsize)
        try:
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
        except AttributeError:
            text_width, text_height = draw.textsize(text, font=font)
        x = 10
        y = image.height - text_height - 10
        draw.text((x, y), text, font=font, fill=(255, 255, 255, 128))
        # Add a shadow for visibility
        draw.text((x+1, y+1), text, font=font, fill=(0, 0, 0, 128))
        return image
    
    def run(self):
        """Run the application"""
        try:
            self.root.mainloop()
        finally:
            # Clean up
            self.location_picker.stop_server()

if __name__ == "__main__":
    app = EXIFEditor()
    app.run() 