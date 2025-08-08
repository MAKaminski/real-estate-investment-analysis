#!/usr/bin/env python3
"""
Georgia Property Data Scraper
=============================

A dedicated scraper for collecting real property data from Georgia.
Uses multiple sources to gather comprehensive property information.
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

class GeorgiaPropertyScraper:
    def __init__(self):
        self.ua = UserAgent()
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': self.ua.random})
        self.properties = []
        
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
    
    def scrape_realtor_georgia(self, city: str = "Atlanta") -> List[Dict]:
        """Scrape property data from Realtor.com for Georgia cities"""
        properties = []
        
        try:
            driver = self.setup_selenium_driver()
            
            # Search for properties in Georgia
            search_url = f"https://www.realtor.com/realestateandhomes-search/{city}_GA"
            logger.info(f"Scraping Realtor.com for {city}, GA")
            
            driver.get(search_url)
            time.sleep(3)
            
            # Wait for properties to load
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='property-card']"))
                )
            except:
                logger.warning("Property cards not found, trying alternative selectors")
            
            # Scroll to load more properties
            for _ in range(3):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
            
            # Try multiple selectors for property cards
            selectors = [
                "[data-testid='property-card']",
                ".component_property-card",
                ".property-card",
                "[data-testid='property']",
                ".srp-list-card"
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
            for card in property_cards[:50]:  # Limit to 50 properties per city
                try:
                    property_data = self._parse_realtor_property_card(card)
                    if property_data:
                        properties.append(property_data)
                except Exception as e:
                    logger.debug(f"Error parsing property card: {e}")
                    continue
            
            driver.quit()
            
        except Exception as e:
            logger.error(f"Error scraping Realtor.com for {city}: {e}")
        
        return properties
    
    def _parse_realtor_property_card(self, card) -> Optional[Dict]:
        """Parse property data from Realtor.com property card"""
        try:
            # Extract price
            price_elem = card.find_element(By.CSS_SELECTOR, "[data-testid='property-price'], .price, .list-price")
            price_text = price_elem.text.replace('$', '').replace(',', '').replace('K', '000').replace('M', '000000')
            price = int(re.sub(r'[^\d]', '', price_text)) if price_text else 0
            
            # Extract address
            address_elem = card.find_element(By.CSS_SELECTOR, "[data-testid='property-address'], .address, .property-address")
            address = address_elem.text
            
            # Extract beds/baths/sqft
            beds = 0
            baths = 0
            sqft = 0
            
            try:
                details_elem = card.find_element(By.CSS_SELECTOR, "[data-testid='property-details'], .property-details, .details")
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
                'source': 'realtor_georgia',
                'listing_id': f"realtor_{hash(address)}"
            }
            
        except Exception as e:
            logger.debug(f"Error parsing Realtor property card: {e}")
            return None
    
    def scrape_zillow_georgia(self, city: str = "Atlanta") -> List[Dict]:
        """Scrape property data from Zillow for Georgia cities"""
        properties = []
        
        try:
            driver = self.setup_selenium_driver()
            
            # Search for properties in Georgia
            search_url = f"https://www.zillow.com/homes/for_sale/{city}-GA"
            logger.info(f"Scraping Zillow for {city}, GA")
            
            driver.get(search_url)
            time.sleep(3)
            
            # Wait for properties to load
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='property-card']"))
                )
            except:
                logger.warning("Property cards not found, trying alternative selectors")
            
            # Scroll to load more properties
            for _ in range(3):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
            
            # Try multiple selectors for property cards
            selectors = [
                "[data-testid='property-card']",
                ".property-card",
                ".list-card",
                ".property-card-container"
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
            for card in property_cards[:50]:  # Limit to 50 properties per city
                try:
                    property_data = self._parse_zillow_property_card(card)
                    if property_data:
                        properties.append(property_data)
                except Exception as e:
                    logger.debug(f"Error parsing Zillow property card: {e}")
                    continue
            
            driver.quit()
            
        except Exception as e:
            logger.error(f"Error scraping Zillow for {city}: {e}")
        
        return properties
    
    def _parse_zillow_property_card(self, card) -> Optional[Dict]:
        """Parse property data from Zillow property card"""
        try:
            # Extract price
            price_elem = card.find_element(By.CSS_SELECTOR, "[data-testid='property-price'], .price, .list-price")
            price_text = price_elem.text.replace('$', '').replace(',', '').replace('K', '000').replace('M', '000000')
            price = int(re.sub(r'[^\d]', '', price_text)) if price_text else 0
            
            # Extract address
            address_elem = card.find_element(By.CSS_SELECTOR, "[data-testid='property-address'], .address, .property-address")
            address = address_elem.text
            
            # Extract beds/baths/sqft
            beds = 0
            baths = 0
            sqft = 0
            
            try:
                details_elem = card.find_element(By.CSS_SELECTOR, "[data-testid='property-details'], .property-details, .details")
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
                'source': 'zillow_georgia',
                'listing_id': f"zillow_{hash(address)}"
            }
            
        except Exception as e:
            logger.debug(f"Error parsing Zillow property card: {e}")
            return None
    
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
    
    def scrape_georgia_properties(self, cities: List[str] = None, target_count: int = 200) -> List[Dict]:
        """Scrape property data from multiple sources for Georgia cities"""
        if cities is None:
            cities = ["Atlanta", "Savannah", "Athens", "Augusta", "Macon", "Columbus", "Albany"]
        
        all_properties = []
        
        for city in cities:
            logger.info(f"Scraping properties for {city}, GA")
            
            # Scrape from Realtor.com
            realtor_properties = self.scrape_realtor_georgia(city)
            all_properties.extend(realtor_properties)
            
            # Scrape from Zillow
            zillow_properties = self.scrape_zillow_georgia(city)
            all_properties.extend(zillow_properties)
            
            # Add delay between cities
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
        
        return filtered_properties[:target_count]
