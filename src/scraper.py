import requests
from bs4 import BeautifulSoup
import time
import random

def get_amazon_price(url):
    """
    Fetches the price and title of a product from Amazon.
    Returns (price, title) where price is float or None, and title is str or None.
    """
    # Clean URL and force USD currency and English language
    if "/dp/" in url:
        product_id = url.split("/dp/")[1].split("/")[0].split("?")[0]
        url = f"https://www.amazon.com/dp/{product_id}?language=en_US&currency=USD"
    elif "?" in url:
        url += "&language=en_US&currency=USD"
    else:
        url += "?language=en_US&currency=USD"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    price = None
    title = None
    
    try:
        session = requests.Session()
        # Add cookie to force USD
        session.cookies.set('i18n-prefs', 'USD', domain='.amazon.com')
        session.cookies.set('lc-main', 'en_US', domain='.amazon.com')
        
        response = session.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        if "Amazon Sign-In" in response.text:
            print(f"Warning: Amazon redirected to Sign-In page for {url}")
            return None, None

        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Get Title
        title_tag = soup.select_one('#productTitle')
        if title_tag:
            title = title_tag.get_text().strip()

        # Priority order for price selectors
        selectors = [
            'span.a-price span.a-offscreen',
            'span#priceblock_ourprice',
            'span#priceblock_dealprice',
            'span.a-price-whole',
            '#corePrice_feature_div .a-offscreen',
            '#corePriceDisplay_desktop_feature_div .a-offscreen'
        ]
        
        price_text = None
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                price_text = element.get_text().strip()
                break
            
        if price_text:
            # Clean price string
            clean_price = "".join([c for c in price_text if c.isdigit() or c in '.,'])
            
            if not clean_price:
                return None, title

            # Handle European format 1.234,56 -> 1234.56 or 1,234.56 -> 1234.56
            if ',' in clean_price and '.' in clean_price:
                if clean_price.find('.') < clean_price.find(','): # 1.234,56
                    clean_price = clean_price.replace('.', '').replace(',', '.')
                else: # 1,234.56
                    clean_price = clean_price.replace(',', '')
            elif ',' in clean_price: # 1234,56
                 if len(clean_price.split(',')[-1]) <= 2: # Likely decimal
                    clean_price = clean_price.replace(',', '.')
                 else:
                    clean_price = clean_price.replace(',', '')
            
            # Final digit clean up
            final_price = ""
            dot_found = False
            for c in clean_price:
                if c.isdigit():
                    final_price += c
                elif c == '.' and not dot_found:
                    final_price += c
                    dot_found = True
                    
            if final_price:
                 try:
                    price = float(final_price)
                 except:
                    pass
        
        return price, title

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None, None


