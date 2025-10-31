import requests
from bs4 import BeautifulSoup
import csv
import re

url = "https://www.booking.com/searchresults.html?ss=New+Delhi&ssne=New+Delhi&ssne_untouched=New+Delhi&label=gen173nr-10CAEoggI46AdIM1gEaGyIAQGYATO4ARfIAQzYAQPoAQH4AQGIAgGoAgG4AvCmkcgGwAIB0gIkNzFhN2ZmNWEtZDhhYy00NDAhLTlhMWMtYjQ3YmVkMDY2MWUx2AIB4AIB&aid=304142&lang=en-us&sb=1&src_elem=sb&src=searchresults&dest_id=-2106102&dest_type=city&checkin=2025-11-01&checkout=2025-11-02&group_adults=2&no_rooms=1&group_children=0"

r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'})

if r.status_code == 200:
    soup = BeautifulSoup(r.text, 'lxml')
    
    with open('hotel_data.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Hotel Name', 'Locality', 'Price', 'Rating', 'Score', 'Reviews', 'Link'])
        
        for hotel in soup.find_all('div', role="listitem"):
            # Extract and clean all data
            name = ' '.join(hotel.find('div', class_="b87c397a13 a3e0b4ffd1").text.strip().split()) if hotel.find('div', class_="b87c397a13 a3e0b4ffd1") else 'N/A'
            loc = ' '.join(hotel.find('span', class_="d823fbbeed f9b3563dd4").text.strip().split()) if hotel.find('span', class_="d823fbbeed f9b3563dd4") else 'N/A'
            
            price_elem = hotel.find('span', class_="b87c397a13 f2f358d1de ab607752a2")
            price = f"RS {re.sub(r'[^\d,]', '', price_elem.text.strip())}" if price_elem else 'N/A'
            
            rating = ' '.join(hotel.find('div', class_="f63b14ab7a f546354b44 becbee2f63").text.strip().split()) if hotel.find('div', class_="f63b14ab7a f546354b44 becbee2f63") else 'N/A'
            score = ' '.join(hotel.find('div', class_="f63b14ab7a dff2e52086").text.strip().split()) if hotel.find('div', class_="f63b14ab7a dff2e52086") else 'N/A'
            
            review_elem = hotel.find('div', class_="fff1944c52 fb14de7f14 eaa8455879")
            review = ''.join(re.findall(r'\d+', review_elem.text.strip())) if review_elem else 'N/A'
            
            link_elem = hotel.find('a', href=True)
            link = ('https://www.booking.com' + link_elem['href']) if link_elem and not link_elem['href'].startswith('http') else (link_elem['href'] if link_elem else 'N/A')
            
            writer.writerow([name, loc, price, rating, score, review, link])
    
    print("Data successfully saved to hotel_data.csv")
else:
    print(f"Connection Failed! {r.status_code}")