import time
import os
from scraper import get_amazon_price
from notifier import send_telegram_alert

PRODUCTS_FILE = 'products.txt'
CHECK_INTERVAL = 3600  # Check every hour (in seconds)

def load_products():
    """
    Reads products from products.txt
    Returns a list of tuples: (url, target_price)
    """
    products = []
    if not os.path.exists(PRODUCTS_FILE):
        print(f"{PRODUCTS_FILE} not found!")
        return products

    with open(PRODUCTS_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            try:
                parts = line.split(',')
                url = parts[0].strip()
                target_price = float(parts[1].strip())
                products.append((url, target_price))
            except ValueError:
                print(f"Skipping invalid line: {line}")
    
    return products

def main():
    print("Starting...")
    
    # Verify .env is loaded (it's loaded in notifier, but good to check here or just rely on notifier)
    
    while True:
        products = load_products()
        if not products:
            print("No products to check. Waiting...")
        
        for url, target_price in products:
            current_price, title = get_amazon_price(url)
            display_name = title if title else url
            print(f"Checking: {display_name}...")
            
            if current_price is not None:
                print(f"Current price: {current_price}, Target: {target_price}")
                
                if current_price <= target_price:
                    product_display_name = title if title else "Producto Amazon"
                    
                    msg = (
                        "📉 <b>¡BAJA DE PRECIO DETECTADA!</b>\n\n"
                        f"📦 <b>Producto:</b> {product_display_name}\n"
                        f"💰 <b>Precio Actual:</b> ${current_price}\n"
                        f"🎯 <b>Tu Objetivo:</b> ${target_price}\n\n"
                        f"<a href='{url}'>🔗 Ver en Amazon</a>"
                    )
                    send_telegram_alert(msg)
            else:
                print("Could not fetch price.")
            
            # Sleep a bit between requests to avoid bot detection
            time.sleep(5) 
            
        print(f"Cycle complete. Waiting {CHECK_INTERVAL} seconds...")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
