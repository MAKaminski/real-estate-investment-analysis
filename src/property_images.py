#!/usr/bin/env python3
"""
Property Image Generator
=======================

Generates realistic property images based on property characteristics.
Uses property data to create visual representations of properties.
"""

import random
import base64
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from typing import Dict

class PropertyImageGenerator:
    def __init__(self):
        self.house_styles = {
            'modern': {'colors': ['#2c3e50', '#34495e', '#3498db'], 'shape': 'rectangular'},
            'traditional': {'colors': ['#8b4513', '#cd853f', '#daa520'], 'shape': 'gabled'},
            'colonial': {'colors': ['#f4a460', '#deb887', '#d2691e'], 'shape': 'symmetrical'},
            'ranch': {'colors': ['#556b2f', '#6b8e23', '#808080'], 'shape': 'horizontal'},
            'victorian': {'colors': ['#8b0000', '#dc143c', '#ff6347'], 'shape': 'ornate'}
        }
        
        self.property_types = {
            'Single Family': 'traditional',
            'Townhouse': 'modern',
            'Condo': 'modern',
            'Multi-Family': 'colonial'
        }
    
    def generate_property_image(self, property_data: Dict, size: tuple = (400, 300)) -> str:
        """Generate a property image based on property characteristics"""
        
        # Create base image
        img = Image.new('RGB', size, '#87CEEB')  # Sky blue background
        draw = ImageDraw.Draw(img)
        
        # Determine house style based on property type
        property_type = property_data.get('property_type', 'Single Family')
        style = self.property_types.get(property_type, 'traditional')
        style_config = self.house_styles[style]
        
        # Generate house based on price and characteristics
        self._draw_house(draw, property_data, style_config, size)
        
        # Add property details
        self._add_property_details(draw, property_data, size)
        
        # Convert to base64 for web display
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return f"data:image/png;base64,{img_str}"
    
    def _draw_house(self, draw: ImageDraw.Draw, property_data: Dict, style_config: Dict, size: tuple):
        """Draw the house based on style and characteristics"""
        
        width, height = size
        price = property_data.get('price', 200000)
        sqft = property_data.get('sqft', 1500)
        beds = property_data.get('beds', 3)
        
        # Scale house size based on square footage
        house_width = min(max(sqft / 1000 * 100, 60), 200)
        house_height = min(max(sqft / 1000 * 80, 40), 120)
        
        # Position house
        house_x = width // 2 - house_width // 2
        house_y = height - house_height - 50
        
        # Choose colors
        colors = style_config['colors']
        main_color = random.choice(colors)
        accent_color = random.choice([c for c in colors if c != main_color])
        
        # Draw main structure
        if style_config['shape'] == 'rectangular':
            self._draw_rectangular_house(draw, house_x, house_y, house_width, house_height, main_color, accent_color)
        elif style_config['shape'] == 'gabled':
            self._draw_gabled_house(draw, house_x, house_y, house_width, house_height, main_color, accent_color)
        elif style_config['shape'] == 'symmetrical':
            self._draw_symmetrical_house(draw, house_x, house_y, house_width, house_height, main_color, accent_color)
        elif style_config['shape'] == 'horizontal':
            self._draw_ranch_house(draw, house_x, house_y, house_width, house_height, main_color, accent_color)
        else:
            self._draw_ornate_house(draw, house_x, house_y, house_width, house_height, main_color, accent_color)
        
        # Add windows and doors based on bedrooms
        self._add_windows_and_doors(draw, house_x, house_y, house_width, house_height, beds)
    
    def _draw_rectangular_house(self, draw: ImageDraw.Draw, x: int, y: int, width: int, height: int, main_color: str, accent_color: str):
        """Draw a modern rectangular house"""
        # Main structure
        draw.rectangle([x, y, x + width, y + height], fill=main_color, outline='#000000', width=2)
        
        # Roof
        roof_points = [(x - 10, y), (x + width // 2, y - 20), (x + width + 10, y)]
        draw.polygon(roof_points, fill=accent_color, outline='#000000', width=2)
    
    def _draw_gabled_house(self, draw: ImageDraw.Draw, x: int, y: int, width: int, height: int, main_color: str, accent_color: str):
        """Draw a traditional gabled house"""
        # Main structure
        draw.rectangle([x, y, x + width, y + height], fill=main_color, outline='#000000', width=2)
        
        # Gabled roof
        roof_points = [(x - 10, y), (x + width // 2, y - 30), (x + width + 10, y)]
        draw.polygon(roof_points, fill=accent_color, outline='#000000', width=2)
        
        # Chimney
        chimney_x = x + width - 30
        draw.rectangle([chimney_x, y - 40, chimney_x + 15, y], fill='#696969', outline='#000000', width=1)
    
    def _draw_symmetrical_house(self, draw: ImageDraw.Draw, x: int, y: int, width: int, height: int, main_color: str, accent_color: str):
        """Draw a colonial symmetrical house"""
        # Main structure
        draw.rectangle([x, y, x + width, y + height], fill=main_color, outline='#000000', width=2)
        
        # Roof
        roof_points = [(x - 10, y), (x + width // 2, y - 25), (x + width + 10, y)]
        draw.polygon(roof_points, fill=accent_color, outline='#000000', width=2)
        
        # Columns
        col_width = 8
        col_height = height - 20
        draw.rectangle([x + 20, y + 10, x + 20 + col_width, y + 10 + col_height], fill='#f5f5dc', outline='#000000', width=1)
        draw.rectangle([x + width - 28, y + 10, x + width - 28 + col_width, y + 10 + col_height], fill='#f5f5dc', outline='#000000', width=1)
    
    def _draw_ranch_house(self, draw: ImageDraw.Draw, x: int, y: int, width: int, height: int, main_color: str, accent_color: str):
        """Draw a ranch-style house"""
        # Main structure (wider, shorter)
        ranch_width = int(width * 1.3)
        ranch_height = int(height * 0.7)
        ranch_x = x - (ranch_width - width) // 2
        
        draw.rectangle([ranch_x, y, ranch_x + ranch_width, y + ranch_height], fill=main_color, outline='#000000', width=2)
        
        # Flat roof
        draw.rectangle([ranch_x - 5, y - 5, ranch_x + ranch_width + 5, y], fill=accent_color, outline='#000000', width=2)
    
    def _draw_ornate_house(self, draw: ImageDraw.Draw, x: int, y: int, width: int, height: int, main_color: str, accent_color: str):
        """Draw a Victorian ornate house"""
        # Main structure
        draw.rectangle([x, y, x + width, y + height], fill=main_color, outline='#000000', width=2)
        
        # Complex roof
        roof_points = [(x - 15, y), (x + width // 3, y - 35), (x + width // 2, y - 25), (x + 2 * width // 3, y - 35), (x + width + 15, y)]
        draw.polygon(roof_points, fill=accent_color, outline='#000000', width=2)
        
        # Turret
        turret_x = x + width - 25
        draw.ellipse([turret_x, y - 20, turret_x + 20, y], fill=accent_color, outline='#000000', width=2)
    
    def _add_windows_and_doors(self, draw: ImageDraw.Draw, x: int, y: int, width: int, height: int, beds: int):
        """Add windows and doors based on number of bedrooms"""
        
        # Door
        door_width = 15
        door_height = height // 2
        door_x = x + width // 2 - door_width // 2
        door_y = y + height - door_height
        
        draw.rectangle([door_x, door_y, door_x + door_width, door_y + door_height], fill='#8b4513', outline='#000000', width=1)
        
        # Windows (based on bedrooms)
        window_width = 12
        window_height = 15
        
        # Front windows
        num_windows = min(beds + 1, 4)  # Max 4 windows
        window_spacing = width // (num_windows + 1)
        
        for i in range(num_windows):
            window_x = x + window_spacing * (i + 1) - window_width // 2
            window_y = y + height // 3
            
            # Window frame
            draw.rectangle([window_x, window_y, window_x + window_width, window_y + window_height], fill='#87ceeb', outline='#000000', width=1)
            
            # Window panes
            draw.line([window_x + window_width // 2, window_y, window_x + window_width // 2, window_y + window_height], fill='#000000', width=1)
            draw.line([window_x, window_y + window_height // 2, window_x + window_width, window_y + window_height // 2], fill='#000000', width=1)
    
    def _add_property_details(self, draw: ImageDraw.Draw, property_data: Dict, size: tuple):
        """Add property details as text overlay"""
        
        width, height = size
        
        # Property address (shortened)
        address = property_data.get('address', 'Unknown Address')
        address_parts = address.split(',')
        short_address = address_parts[0][:20] + "..." if len(address_parts[0]) > 20 else address_parts[0]
        
        # Price
        price = property_data.get('price', 0)
        price_text = f"${price:,.0f}"
        
        # Property details
        beds = property_data.get('beds', 0)
        baths = property_data.get('baths', 0)
        sqft = property_data.get('sqft', 0)
        details_text = f"{beds} bed, {baths} bath, {sqft:,} sqft"
        
        # Draw text with background
        self._draw_text_with_background(draw, short_address, 10, 10, width - 20)
        self._draw_text_with_background(draw, price_text, 10, 35, width - 20)
        self._draw_text_with_background(draw, details_text, 10, 60, width - 20)
    
    def _draw_text_with_background(self, draw: ImageDraw.Draw, text: str, x: int, y: int, max_width: int):
        """Draw text with a semi-transparent background"""
        
        # Try to use a default font, fallback to basic if not available
        try:
            font = ImageFont.truetype("Arial.ttf", 12)
        except:
            font = ImageFont.load_default()
        
        # Get text size
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Draw background
        bg_padding = 5
        bg_x = x - bg_padding
        bg_y = y - bg_padding
        bg_width = min(text_width + 2 * bg_padding, max_width)
        bg_height = text_height + 2 * bg_padding
        
        draw.rectangle([bg_x, bg_y, bg_x + bg_width, bg_y + bg_height], fill='rgba(0,0,0,0.7)', outline='#ffffff', width=1)
        
        # Draw text
        draw.text((x, y), text, fill='#ffffff', font=font)
    
    def generate_property_images(self, properties: list) -> Dict[str, str]:
        """Generate images for multiple properties"""
        
        property_images = {}
        
        for prop in properties:
            address = prop.get('address', 'Unknown')
            image_data = self.generate_property_image(prop)
            property_images[address] = image_data
        
        return property_images
