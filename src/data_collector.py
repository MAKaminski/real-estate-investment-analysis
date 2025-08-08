import requests
import time
import random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

class PropertyDataCollector:
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
        
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return driver
    
    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    @timeout(30)
    def get_realtor_data(self, location: str, limit: int = 100) -> List[Dict]:
        """Get property data from Realtor.com API"""
        properties = []
        
        try:
            # Use Realtor.com API through RapidAPI
            url = f"{config.DATA_SOURCES['realtor']['base_url']}/properties/v2/list-for-sale"
            
            params = {
                'location': location,
                'limit': min(limit, 200),  # API limit
                'offset': 0,
                'sort': 'relevant'
            }
            
            response = self.session.get(
                url, 
                headers=config.DATA_SOURCES['realtor']['headers'],
                params=params
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'properties' in data:
                    for prop in data['properties']:
                        property_data = self._parse_realtor_property(prop)
                        if property_data:
                            properties.append(property_data)
                            
        except Exception as e:
            logger.error(f"Error fetching Realtor data: {e}")
            
        return properties
    
    def _parse_realtor_property(self, prop: Dict) -> Optional[Dict]:
        """Parse property data from Realtor API response"""
        try:
            return {
                'address': f"{prop.get('address', {}).get('line', '')}, {prop.get('address', {}).get('city', '')}, {prop.get('address', {}).get('state_code', '')}",
                'price': prop.get('list_price', 0),
                'sqft': prop.get('description', {}).get('sqft', 0),
                'beds': prop.get('description', {}).get('beds', 0),
                'baths': prop.get('description', {}).get('baths', 0),
                'year_built': prop.get('description', {}).get('year_built', 0),
                'property_type': prop.get('property_type', ''),
                'listing_id': prop.get('listing_id', ''),
                'source': 'realtor'
            }
        except Exception as e:
            logger.error(f"Error parsing Realtor property: {e}")
            return None
    
    def scrape_zillow_data(self, location: str, limit: int = 100) -> List[Dict]:
        """Scrape property data from Zillow"""
        properties = []
        
        try:
            driver = self.setup_selenium_driver()
            
            # Search for properties in the location
            search_url = f"https://www.zillow.com/homes/for_sale/{location.replace(' ', '-')}"
            driver.get(search_url)
            
            # Wait for page to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "property-card"))
            )
            
            # Scroll to load more properties
            for _ in range(limit // 20):  # Load properties in batches
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.uniform(1, 3))
            
            # Extract property data
            property_cards = driver.find_elements(By.CLASS_NAME, "property-card")
            
            for card in property_cards[:limit]:
                try:
                    property_data = self._parse_zillow_property(card)
                    if property_data:
                        properties.append(property_data)
                except Exception as e:
                    logger.error(f"Error parsing Zillow property: {e}")
                    continue
                    
            driver.quit()
            
        except Exception as e:
            logger.error(f"Error scraping Zillow data: {e}")
            
        return properties
    
    def _parse_zillow_property(self, card) -> Optional[Dict]:
        """Parse property data from Zillow property card"""
        try:
            # Extract price
            price_elem = card.find_element(By.CSS_SELECTOR, "[data-testid='property-price']")
            price_text = price_elem.text.replace('$', '').replace(',', '')
            price = int(price_text) if price_text.isdigit() else 0
            
            # Extract address
            address_elem = card.find_element(By.CSS_SELECTOR, "[data-testid='property-address']")
            address = address_elem.text
            
            # Extract beds/baths/sqft
            beds = 0
            baths = 0
            sqft = 0
            
            try:
                details_elem = card.find_element(By.CSS_SELECTOR, "[data-testid='property-details']")
                details_text = details_elem.text
                
                # Parse beds/baths/sqft from text
                import re
                bed_match = re.search(r'(\d+)\s*bed', details_text)
                bath_match = re.search(r'(\d+)\s*bath', details_text)
                sqft_match = re.search(r'(\d+)\s*sqft', details_text)
                
                if bed_match:
                    beds = int(bed_match.group(1))
                if bath_match:
                    baths = int(bath_match.group(1))
                if sqft_match:
                    sqft = int(sqft_match.group(1))
                    
            except:
                pass
            
            return {
                'address': address,
                'price': price,
                'sqft': sqft,
                'beds': beds,
                'baths': baths,
                'property_type': 'Single Family',
                'listing_id': f"zillow_{hash(address)}",
                'source': 'zillow'
            }
            
        except Exception as e:
            logger.error(f"Error parsing Zillow property card: {e}")
            return None
    
    def get_rental_estimates(self, properties: List[Dict]) -> List[Dict]:
        """Get rental estimates for properties"""
        for prop in properties:
            try:
                # Estimate rental income based on property characteristics
                rental_estimate = self._estimate_rental_income(prop)
                prop['estimated_rental_income'] = rental_estimate
                
                # Add some delay to avoid rate limiting
                time.sleep(random.uniform(0.1, 0.5))
                
            except Exception as e:
                logger.error(f"Error estimating rental income: {e}")
                prop['estimated_rental_income'] = 0
                
        return properties
    
    def _estimate_rental_income(self, prop: Dict) -> float:
        """Estimate monthly rental income based on property characteristics"""
        base_rent_per_sqft = 1.0  # $1 per sqft as base
        
        # Adjust based on location (simplified)
        location_multiplier = 1.0
        if prop.get('address', '').lower().find('california') != -1:
            location_multiplier = 1.5
        elif prop.get('address', '').lower().find('new york') != -1:
            location_multiplier = 1.8
        elif prop.get('address', '').lower().find('texas') != -1:
            location_multiplier = 0.8
        
        # Adjust based on property type
        type_multiplier = 1.0
        if 'condo' in prop.get('property_type', '').lower():
            type_multiplier = 0.9
        elif 'townhouse' in prop.get('property_type', '').lower():
            type_multiplier = 0.95
        
        # Calculate estimated rent
        sqft = prop.get('sqft', 1000)
        estimated_rent = sqft * base_rent_per_sqft * location_multiplier * type_multiplier
        
        # Add some randomness to make it more realistic
        estimated_rent *= random.uniform(0.8, 1.2)
        
        return round(estimated_rent, 2)
    
    def collect_property_data(self, locations: List[str], target_count: int = 1000) -> List[Dict]:
        """Collect property data from multiple sources"""
        all_properties = []
        
        for location in locations:
            logger.info(f"Collecting data for location: {location}")
            
            # Get data from Realtor API
            realtor_properties = self.get_realtor_data(location, limit=200)
            all_properties.extend(realtor_properties)
            
            # Get data from Zillow scraping
            zillow_properties = self.scrape_zillow_data(location, limit=200)
            all_properties.extend(zillow_properties)
            
            # Add delay between locations
            time.sleep(random.uniform(2, 5))
        
        # Remove duplicates based on address
        unique_properties = []
        seen_addresses = set()
        
        for prop in all_properties:
            address_key = prop.get('address', '').lower().replace(' ', '').replace(',', '')
            if address_key not in seen_addresses:
                seen_addresses.add(address_key)
                unique_properties.append(prop)
        
        # Get rental estimates
        properties_with_rentals = self.get_rental_estimates(unique_properties)
        
        # Filter by price range
        filtered_properties = [
            prop for prop in properties_with_rentals
            if config.MIN_PROPERTY_PRICE <= prop.get('price', 0) <= config.MAX_PROPERTY_PRICE
        ]
        
        logger.info(f"Collected {len(filtered_properties)} properties after filtering")
        
        return filtered_properties[:target_count]
