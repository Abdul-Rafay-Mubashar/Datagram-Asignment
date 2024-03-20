import requests
from bs4 import BeautifulSoup
import os
import re
import json
import hashlib



URL='https://www.pascalcoste-shopping.com/esthetique/fond-de-teint.html?'
CRAWLER_DIR = './crawler'

# Get SCRAPER API KEY By Sign Up On Scraper Api
SCRAPER_API_KEY='2f73d36161caedc5202721d58e8d7f8c'
href=[]


def md5(data):
    md5_hash = hashlib.md5()
    md5_hash.update(data.encode('utf-8'))
    return md5_hash.hexdigest()


#  scrape brand name and price


def scrape_brand_name_price(item:BeautifulSoup):
        card_container=item.find('div',class_='uk-visible-product uk-text-center')
        brand_name_div=card_container.find('div',class_='uk-grid uk-grid-small small-label uk-grid-divider uk-flex-center')
        if brand_name_div:
            brand_name=slice_until_numeric(brand_name_div.text)
        else :
            brand_name=None
        h3_tag=card_container.find('h3')
        if h3_tag:
            product_name=h3_tag.text
        else:
            product_name=None
        for_price=card_container.find('div',class_='uk-grid uk-grid-small uk-prix-final uk-margin-remove-top uk-flex-center')
        if for_price:
            price_tag=for_price.find('span',class_='uk-price')
            if for_price:
                price=price_tag.text
            else:
                price=None
        else:
            price=None
        return {"brand": brand_name, "name": product_name, "price": price}


# When Scrape Brand Name It Also Have ML Info With It For That To Slice Upto Numaric


def slice_until_numeric(string):
    for i, char in enumerate(string):
        if char.isdigit():
            return string[:i]
    return string


# load page and return BeautifulSoup Also Contain Cache Logic


def load_page(url:str,retry=0):
    file_name = os.path.join(CRAWLER_DIR, f"{re.sub(r'[^a-zA-Z0-9]', '', url.split('/')[-1])}.html")
    if len(file_name) > 260:
        file_name = os.path.join(CRAWLER_DIR, f'{md5(file_name)}.html')
    print(f'file name generated: {file_name}')
    if os.path.exists(file_name):
        print('cached file found')
        with open(file_name, 'r', encoding='utf-8') as f:
            html_content = f.read()
        return BeautifulSoup(html_content, "html.parser")
    else:

        while(retry<3):
            payload = { 'api_key':SCRAPER_API_KEY , 'url': url } 
            r = requests.get('https://api.scraperapi.com/', params=payload)
            print(f'Status code for ({url}): {r.status_code}')
            html = r.text
            soup = BeautifulSoup(html, 'html.parser') 

            if(r.status_code==200):
                with open(file_name, 'w', encoding='utf-8') as f:
                    f.write(html)
                return soup
            retry=retry+1
    return None


# Scrape Links Of All Items


def scrape_links(soup:BeautifulSoup):
    Headings=soup.find('div',id='narrow-by-list')
    sub_heading=headings=Headings.find_all('ol')
    for heading in sub_heading:
        a_tag=heading.find_all('a')
        for i in a_tag:
            href.append(i['href'])
    return href



# Scrape Img Url and Product_Url 


def get_data(doc:BeautifulSoup):
    if doc is None:
        print('No HTML Recived')
        return None
    items=doc.find_all('div',class_='uk-panel uk-position-relative')
    if len(items)==0:
        return 'END'
    print(len(items))
    products=[]
    for item in items:
        img_div=item.find('div',class_='uk-photo-product')
        img_tag=img_div.find('img',class_='product-image-photo')
        a_tag=item.find('a',class_='product photo product-item-photo uk-text-center')
        img_url=img_tag['data-amsrc']
        product_url=a_tag['href']
        data=scrape_brand_name_price(item)
        products.append({"name": data["name"], "brand": data["brand"], "price": data["price"], "productUrl": product_url, "imgUrl": img_url})
    return products



# Main Function 

def main():
    if not os.path.exists(CRAWLER_DIR):
        os.makedirs(CRAWLER_DIR)
    Output_File="Output.json"
    with open(Output_File, 'w', encoding='utf-8') as json_file:
        Doc_For_Links=load_page(URL)
        Links=scrape_links(Doc_For_Links)
        all_products = []
        for Link in Links:
            page=load_page(Link)
            if page is None:
                continue
            Num=2
            while True:
                your_data=get_data(page)
                if your_data=='END':
                    print("Last Page")
                    break
                else:
                    for products in your_data:
                        all_products.append(products)         
                if '?' in Link:
                    new_url = f"{Link}&p={Num}"
                else:
                    new_url = f"{Link}?p={Num}"
                Num=Num+1
                page=load_page(new_url)
                if page is None:
                    if '?' in new_url:
                        new_url = f"{Link}&p={Num}"
                    else:
                        new_url = f"{Link}?p={Num}"
                    Num=Num+1
        json.dump(all_products, json_file, ensure_ascii=False, indent=4)



if __name__ == "__main__":
    
    URL='https://www.pascalcoste-shopping.com/esthetique/fond-de-teint.html?'
    CRAWLER_DIR = './crawler'
    href=[]
    main()