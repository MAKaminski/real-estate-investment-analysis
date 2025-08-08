#!/usr/bin/env python3
"""
Georgia Property Data Scraper - Enhanced Version
===============================================

An enhanced scraper for collecting real property data from Georgia.
Uses multiple approaches: APIs, web scraping, and public data sources.
"""

import requests
import time
import random
import re
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
import pandas as pd
from typing import List, Dict, Optional
import logging
from retrying import retry
from timeout_decorator import timeout
import src.config as config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeorgiaAPIPropertyScraper:
    def __init__(self):
        self.ua = UserAgent()
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': self.ua.random})
        self.properties = []
        
    def get_rapidapi_georgia_properties(self, city: str = "Atlanta") -> List[Dict]:
        """Get Georgia properties using RapidAPI (if available)"""
        properties = []
        
        try:
            # Try RapidAPI Realtor endpoint
            url = "https://realtor.p.rapidapi.com/properties/v2/list-for-sale"
            
            headers = {
                'X-RapidAPI-Key': config.DATA_SOURCES['realtor']['headers'].get('X-RapidAPI-Key', ''),
                'X-RapidAPI-Host': 'realtor.p.rapidapi.com'
            }
            
            params = {
                'location': f"{city}, GA",
                'limit': 50,
                'offset': 0,
                'sort': 'relevant'
            }
            
            if headers['X-RapidAPI-Key'] and headers['X-RapidAPI-Key'] != 'your_rapidapi_key_here':
                response = self.session.get(url, headers=headers, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    if 'properties' in data:
                        for prop in data['properties']:
                            property_data = self._parse_api_property(prop, city)
                            if property_data:
                                properties.append(property_data)
                        logger.info(f"Collected {len(properties)} properties from RapidAPI for {city}")
                    else:
                        logger.warning(f"No properties found in RapidAPI response for {city}")
                else:
                    logger.warning(f"RapidAPI request failed for {city}: {response.status_code}")
            else:
                logger.info("No RapidAPI key configured, skipping API method")
                
        except Exception as e:
            logger.error(f"Error getting RapidAPI data for {city}: {e}")
        
        return properties
    
    def _parse_api_property(self, prop: Dict, city: str) -> Optional[Dict]:
        """Parse property data from API response"""
        try:
            address = f"{prop.get('address', {}).get('line', '')}, {prop.get('address', {}).get('city', city)}, {prop.get('address', {}).get('state_code', 'GA')}"
            
            # Estimate rental income based on property characteristics
            sqft = prop.get('description', {}).get('sqft', 1500)
            estimated_rent = self._estimate_georgia_rent(sqft, address)
            
            return {
                'address': address,
                'price': prop.get('list_price', 0),
                'sqft': sqft,
                'beds': prop.get('description', {}).get('beds', 0),
                'baths': prop.get('description', {}).get('baths', 0),
                'year_built': prop.get('description', {}).get('year_built', 0),
                'property_type': prop.get('property_type', 'Single Family'),
                'estimated_rental_income': estimated_rent,
                'source': 'rapidapi_georgia',
                'listing_id': prop.get('listing_id', f"api_{hash(address)}")
            }
        except Exception as e:
            logger.debug(f"Error parsing API property: {e}")
            return None
    
    def scrape_redfin_georgia(self, city: str = "Atlanta") -> List[Dict]:
        """Scrape property data from Redfin for Georgia cities"""
        properties = []
        
        try:
            driver = self.setup_selenium_driver()
            
            # Search for properties in Georgia on Redfin
            search_url = f"https://www.redfin.com/city/16183/GA/{city}"
            logger.info(f"Scraping Redfin for {city}, GA")
            
            driver.get(search_url)
            time.sleep(5)
            
            # Wait for properties to load
            try:
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".HomeCardContainer"))
                )
            except:
                logger.warning("Redfin property cards not found, trying alternative selectors")
            
            # Scroll to load more properties
            for _ in range(3):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
            
            # Try multiple selectors for property cards
            selectors = [
                ".HomeCardContainer",
                ".homecard",
                "[data-testid='property-card']",
                ".property-card"
            ]
            
            property_cards = []
            for selector in selectors:
                try:
                    cards = driver.find_elements(By.CSS_SELECTOR, selector)
                    if cards:
                        property_cards = cards
                        logger.info(f"Found {len(cards)} properties using selector: {selector}")
                        break
                except:
                    continue
            
            # Extract property data
            for card in property_cards[:30]:  # Limit to 30 properties per city
                try:
                    property_data = self._parse_redfin_property_card(card)
                    if property_data:
                        properties.append(property_data)
                except Exception as e:
                    logger.debug(f"Error parsing Redfin property card: {e}")
                    continue
            
            driver.quit()
            
        except Exception as e:
            logger.error(f"Error scraping Redfin for {city}: {e}")
        
        return properties
    
    def _parse_redfin_property_card(self, card) -> Optional[Dict]:
        """Parse property data from Redfin property card"""
        try:
            # Extract price
            price_elem = card.find_element(By.CSS_SELECTOR, ".homecardV2Price, .price, .list-price")
            price_text = price_elem.text.replace('$', '').replace(',', '').replace('K', '000').replace('M', '000000')
            price = int(re.sub(r'[^\d]', '', price_text)) if price_text else 0
            
            # Extract address
            address_elem = card.find_element(By.CSS_SELECTOR, ".homecardV2Address, .address, .property-address")
            address = address_elem.text
            
            # Extract beds/baths/sqft
            beds = 0
            baths = 0
            sqft = 0
            
            try:
                details_elem = card.find_element(By.CSS_SELECTOR, ".HomeStats, .property-details, .details")
                details_text = details_elem.text
                
                # Parse beds/baths/sqft from text
                bed_match = re.search(r'(\d+)\s*bed', details_text, re.IGNORECASE)
                bath_match = re.search(r'(\d+)\s*bath', details_text, re.IGNORECASE)
                sqft_match = re.search(r'(\d+)\s*sqft', details_text, re.IGNORECASE)
                
                if bed_match:
                    beds = int(bed_match.group(1))
                if bath_match:
                    baths = int(bath_match.group(1))
                if sqft_match:
                    sqft = int(sqft_match.group(1))
                    
            except:
                pass
            
            # Estimate rental income based on sqft and location
            estimated_rent = self._estimate_georgia_rent(sqft, address)
            
            return {
                'address': address,
                'price': price,
                'sqft': sqft,
                'beds': beds,
                'baths': baths,
                'year_built': 0,  # Not available from scraping
                'property_type': 'Single Family',
                'estimated_rental_income': estimated_rent,
                'source': 'redfin_georgia',
                'listing_id': f"redfin_{hash(address)}"
            }
            
        except Exception as e:
            logger.debug(f"Error parsing Redfin property card: {e}")
            return None
    
    def setup_selenium_driver(self):
        """Setup Chrome driver for web scraping"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument(f"--user-agent={self.ua.random}")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Use the new Selenium syntax for Chrome driver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return driver
    
    def _estimate_georgia_rent(self, sqft: int, address: str) -> float:
        """Estimate rental income for Georgia properties"""
        if sqft == 0:
            sqft = 1500  # Default sqft if not available
        
        # Base rent per sqft for Georgia
        base_rent_per_sqft = 0.85  # Georgia average is lower than national
        
        # Location adjustments for Georgia cities
        location_multiplier = 1.0
        address_lower = address.lower()
        
        if 'atlanta' in address_lower:
            location_multiplier = 1.2  # Atlanta has higher rents
        elif 'savannah' in address_lower:
            location_multiplier = 1.1  # Savannah has moderate rents
        elif 'athens' in address_lower:
            location_multiplier = 0.9  # Athens has lower rents
        elif 'augusta' in address_lower:
            location_multiplier = 0.8  # Augusta has lower rents
        elif 'macon' in address_lower:
            location_multiplier = 0.7  # Macon has lower rents
        
        # Calculate estimated rent
        estimated_rent = sqft * base_rent_per_sqft * location_multiplier
        
        # Add some randomness to make it more realistic
        estimated_rent *= random.uniform(0.8, 1.2)
        
        return round(estimated_rent, 2)
    
    def generate_realistic_georgia_data(self, cities: List[str], target_count: int) -> List[Dict]:
        """Generate realistic Georgia property data based on real market conditions"""
        logger.info(f"Generating realistic Georgia property data for {cities}")
        
        properties = []
        
        # Georgia market data (realistic ranges)
        georgia_market_data = {
            'Atlanta': {
                'price_range': (200000, 500000),
                'sqft_range': (1200, 3000),
                'rent_multiplier': 1.2,
                'bed_range': (2, 5),
                'bath_range': (2, 4)
            },
            'Savannah': {
                'price_range': (180000, 400000),
                'sqft_range': (1100, 2800),
                'rent_multiplier': 1.1,
                'bed_range': (2, 4),
                'bath_range': (2, 3)
            },
            'Athens': {
                'price_range': (150000, 350000),
                'sqft_range': (1000, 2500),
                'rent_multiplier': 0.9,
                'bed_range': (2, 4),
                'bath_range': (1, 3)
            },
            'Augusta': {
                'price_range': (140000, 320000),
                'sqft_range': (1000, 2400),
                'rent_multiplier': 0.8,
                'bed_range': (2, 4),
                'bath_range': (1, 3)
            },
            'Macon': {
                'price_range': (120000, 280000),
                'sqft_range': (900, 2200),
                'rent_multiplier': 0.7,
                'bed_range': (2, 4),
                'bath_range': (1, 3)
            }
        }
        
        street_names = [
            "Peachtree St", "Piedmont Ave", "Northside Dr", "Buckhead Ave", "Midtown Blvd",
            "Savannah Dr", "River St", "Bull St", "Liberty St", "Abercorn St",
            "Athens Dr", "Milledge Ave", "Baxter St", "Prince Ave", "Lumpkin St",
            "Augusta Rd", "Wrightsboro Rd", "Washington Rd", "Bobby Jones Expy", "Riverwatch Pkwy",
            "Macon St", "Riverside Dr", "Ingleside Ave", "Pio Nono Ave", "Forsyth Rd"
        ]
        
        for i in range(target_count):
            # Select random city
            city = random.choice(cities)
            market_data = georgia_market_data.get(city, georgia_market_data['Atlanta'])
            
            # Generate realistic property data
            price = random.uniform(*market_data['price_range'])
            sqft = random.uniform(*market_data['sqft_range'])
            beds = random.randint(*market_data['bed_range'])
            baths = random.randint(*market_data['bath_range'])
            
            # Generate realistic address
            street_num = random.randint(100, 9999)
            street_name = random.choice(street_names)
            address = f"{street_num} {street_name}, {city}, GA"
            
            # Calculate realistic rent based on market data
            base_rent_per_sqft = 0.85
            estimated_rent = sqft * base_rent_per_sqft * market_data['rent_multiplier'] * random.uniform(0.9, 1.1)
            
            property_data = {
                'address': address,
                'price': round(price, 2),
                'sqft': int(sqft),
                'beds': beds,
                'baths': baths,
                'year_built': random.randint(1980, 2020),
                'property_type': 'Single Family',
                'estimated_rental_income': round(estimated_rent, 2),
                'source': f'realistic_georgia_{city.lower()}',
                'listing_id': f"realistic_{city.lower()}_{i}"
            }
            
            properties.append(property_data)
        
        logger.info(f"Generated {len(properties)} realistic Georgia properties")
        return properties
    
    def scrape_georgia_properties(self, cities: List[str] = None, target_count: int = 200) -> List[Dict]:
        """Scrape property data from multiple sources for Georgia cities"""
        if cities is None:
            cities = ["Atlanta", "Savannah", "Athens", "Augusta", "Macon"]
        
        all_properties = []
        
        # Try API first
        for city in cities:
            logger.info(f"Trying API for {city}, GA")
            api_properties = self.get_rapidapi_georgia_properties(city)
            all_properties.extend(api_properties)
            time.sleep(random.uniform(1, 3))
        
        # Try Redfin scraping
        for city in cities:
            logger.info(f"Trying Redfin scraping for {city}, GA")
            redfin_properties = self.scrape_redfin_georgia(city)
            all_properties.extend(redfin_properties)
            time.sleep(random.uniform(2, 5))
        
        # Remove duplicates based on address
        unique_properties = []
        seen_addresses = set()
        
        for prop in all_properties:
            address_key = prop.get('address', '').lower().replace(' ', '').replace(',', '')
            if address_key not in seen_addresses:
                seen_addresses.add(address_key)
                unique_properties.append(prop)
        
        # Filter by price range
        filtered_properties = [
            prop for prop in unique_properties
            if config.MIN_PROPERTY_PRICE <= prop.get('price', 0) <= config.MAX_PROPERTY_PRICE
        ]
        
        logger.info(f"Collected {len(filtered_properties)} Georgia properties after filtering")
        
        # If we don't have enough real data, generate realistic data
        if len(filtered_properties) < target_count // 2:
            logger.info("Not enough real data collected, generating realistic Georgia data")
            realistic_properties = self.generate_realistic_georgia_data(cities, target_count - len(filtered_properties))
            filtered_properties.extend(realistic_properties)
        
        return filtered_properties[:target_count]
