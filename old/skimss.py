import time
import json
import re
import uuid
import httpx
import requests
from selectolax.parser import HTMLParser
from bs4 import BeautifulSoup
from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager

from selectolax.parser import HTMLParser

# html_content = """
# <div>
#   <p>Hello, <b>world</b>!</p>
#   <div>
#     <p>Another paragraph.</p>
#   </div>
# </div>
# """

# # Parse HTML content
# doc = HTMLParser(html_content)

# # Use CSS selector to find all <p> elements, including nested ones
# p_elements = doc.css("div p")

# # Print text content of each <p> element
# for p_element in p_elements:
#     print(p_element.text())

# url = 'https://skims.com/collections/swim'
# url = 'https://skims.com/products/fits-everybody-t-shirt-neon-orchid'

# headers ={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}
# resp = httpx.get(url, headers=headers, timeout=30, )

# time.sleep(2)

# soup = BeautifulSoup(resp.text, features="lxml")

# print(soup.find_all('div'))

# html = HTMLParser(resp.text, detect_encoding=True, decode_errors='replace')
# body = html.body
# print(html)

# # p = html.css('div#essential > div.w-full.pt-\[10px\].pb-\[20px\].lg\:min-h-\[75vh\].lg\:max-w-\[468px\].md\:w-\[400px\].lg\:p-0.xl\:w-\[589px\].xl\:mr-\[121px\] > div > div.w-full.min-w-full.px-\[20px\].lg\:px-0 > div:nth-child(1) > fieldset')
# root = html.css('div#root')

# test = body.css('div')

# print(root[0].css_first('template').html)
# print(test)
# # p = html.xpath('//*[@id="root"]')
# # print(p)
# p = html.select('main#mainContent')
# print(p)
# print(p.any_matches)

# # p = html.select('div#collectionMain')
# # print(p)

# categories = html.select('#mainContent > div > div > div.mx-auto.max-w-1600.border-t.border-b-gray-16.lg\:mt-9.lg\:border-0.lg\:pl-\[50px\].lg\:pr-10 > div > div.min-w-0.py-1\.5.lg\:py-0 > ul')
# print(categories)



# # print(resp)

# list = html.css('ul.list-none')#mainContent > div > div > div.mx-auto.max-w-1600.border-t.border-b-gray-16.lg\:mt-9.lg\:border-0.lg\:pl-\[50px\].lg\:pr-10 > div > div.min-w-0.py-1\.5.lg\:py-0 > ul
# # list = html.css("div#collectionMain")

# print(list)

# url = "https://skims.com/collections/fits-everybody"

# Use a headless browser (invisible browser) to load the page
# options = webdriver.ChromeOptions()
# options.add_argument('--headless')
# driver = webdriver.Chrome(executable_path='chromedriver-win64\chromedriver.exe', options=options)

# try:
#     driver.get(url)

#     # Wait for a few seconds to ensure the content is loaded (you may need to adjust this)
#     time.sleep(3)

#     # Get the page source after JavaScript execution
#     page_source = driver.page_source

#     # Parse the HTML content using BeautifulSoup
#     soup = BeautifulSoup(page_source, 'html.parser')

#     # Get the 'ul.list-none' element(s)
#     ul_elements = soup.select('ul.list-none')

#     # Print the text content of each 'ul.list-none' element
#     for ul_element in ul_elements:
#         # print(ul_element.text.encode('utf-8'))

# finally:
#     # Close the browser window
#     driver.quit()

# List to store product information
products = []

def scrape_website(url):
  options = webdriver.ChromeOptions()
  options.add_argument('--headless')
  driver = webdriver.Chrome(executable_path='chromedriver-win64\chromedriver.exe', options=options)
  
  try:
    driver.get(url)

    # Wait for a few seconds to ensure the content is loaded (you may need to adjust this)
    time.sleep(2)

    # Get the page source after JavaScript execution
    # page_source = driver.page_source

    # Parse the HTML content using BeautifulSoup
    # soup = BeautifulSoup(page_source, 'html.parser')

    # Get the 'ul.list-none' element(s)
    # ul_elements = soup.select('ul.list-none')
    # cats = driver.find_element_by_xpath('//*[@id="mainContent"]/div/div/div[3]/div/div[2]/ul').find_element_by_css_selector('li')
    # Find the parent ul element using XPath

    # Sample data retrieval for one product
    parent_data = driver.find_element_by_xpath('//*[@id="essential"]/div[3]/div/div[1]')
    # driver.find_element_by_class_name
    collection_name = parent_data.find_element_by_tag_name("a").get_attribute("innerText")
    item_name = parent_data.find_element_by_tag_name("h1").get_attribute("innerText")
    price = float(parent_data.find_element_by_tag_name("span").get_attribute("innerText").replace("$", ""))

    # Sample data retrieval for colors
    parent_color = driver.find_element_by_xpath('//*[@id="essential"]/div[3]/div/div[2]')
    color_cats = parent_color.find_elements_by_css_selector('div.pdp-translation-3')

    product_info = {
            "id": str(uuid.uuid4()),
            "collection_name": collection_name,
            "item_name": item_name,
            "price": price,
            "color_categories": [],  # List to store color categories
            "images": []
        }

    # Loop through products
    for category in color_cats:
        category_name = category.find_element_by_css_selector('header').get_attribute("innerText").split(':')[0]
        category_info = {
            "category_name": category_name,
            "colors": []  # List to store colors for the category
        }

        colors = category.find_elements_by_css_selector('ul > li')

        # Loop through colors
        for color_element in colors:
            color_name = color_element.get_attribute("innerText").split(' ')[1]
            color_code = color_element.find_element_by_tag_name('label').get_attribute('style')
            # Define a regular expression pattern to match RGB values
            bg_color_pattern = re.compile(r'background-color:\s*rgb\((\d+), (\d+), (\d+)\);')
            # Find the match in the style attribute
            match = bg_color_pattern.search(color_code)

            color = {
              "color_name": color_name,
              "color_value": {
                 "hex": "",
                 "rgba": {
                    "r": int(match.group(1)),
                    "g": int(match.group(2)),
                    "b": int(match.group(3)),
                    "a": 255
                 }
              }
            }
                        
            category_info["colors"].append(color)

        product_info["color_categories"].append(category_info)

    products.append(product_info)

    


    # parent_data = driver.find_element_by_xpath('//*[@id="essential"]/div[3]/div/div[1]')

    # collection_name = parent_data.find_element_by_tag_name("a").get_attribute("innerText")
    # item_name = parent_data.find_element_by_tag_name("h1").get_attribute("innerText")
    # price = parent_data.find_element_by_tag_name("span").get_attribute("innerText").replace("$", "")

    # print(collection_name)
    # print(item_name)
    # print(price)

    # parent_color = driver.find_element_by_xpath('//*[@id="essential"]/div[3]/div/div[2]')
    # color_cats = parent_color.find_elements_by_css_selector('div.pdp-translation-3')
    # # colors = color_cats[0]
    # for category in color_cats:
    #    category_name = category.find_element_by_css_selector('header').get_attribute("innerText").split(':')[0]
    #    print(category_name)
    #    colors = category.find_elements_by_css_selector('ul > li')
    #    for color_element in colors:
    #       color = color_element.get_attribute("innerText").split(' ')[1]
    #       print(color)


    # colors = 
    # print(colors)
    # driver.find_elements_by_css_selector
    # cats = driver.find_elements_by_xpath('//*[@id="mainContent"]/div/div/div[3]/div/div[2]/ul/li')#[3:]
    # # Find all child li elements of the parent ul
    # # cats = parent_ul.find_elements_by_xpath('./li')#[:-2]
    # list = []
    # # print(len(cats))

    # for cat in cats:
    #   print(f"Category: {cat.text}")
    #   products = cat.find_elements_by_xpath('./ul/li')[1:]
    #   # print(len(products))
    #   for product in products:
    #     anchor = product.find_element_by_xpath('./div/a').get_attribute("href")
    #     # //*[@id="mainContent"]/div/div/div[3]/div/div[2]/ul/li[1]/ul/li[2]
    #     print(f"Product: {anchor}")


    # for child_li in child_li_elements:
    #   # Find the child ul element within each li
    #   child_ul = child_li.find_elements_by_xpath('./ul')

    #   # Print the text content of the child li elements
    #   print(f"Parent LI: {child_li.text}")

    #   # Print the text content of the child ul elements, if any
    #   if child_ul:
    #     for child_ul_element in child_ul:
    #         print(f"Child UL: {child_ul_element.text}")
    # for cat in cats:
    #   cat.find_element_by_css_selector('ul')
    #   print(cat)
    # products = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/main/div/div/div[3]/div/div[2]/ul')
    # # //*[@id="mainContent"]/div/div/div[3]/div/div[2]/ul/li[1]/ul
    # print(products)
    # Print the text content of each 'ul.list-none' element
    # for ul_element in ul_elements:
        # print(ul_element.text.encode('utf-8'))
  finally:
    # Close the browser window
    driver.quit()


if __name__ == "__main__":
    # target_url = 'https://skims.com/products/fits-everybody-t-shirt-neon-orchid'
    # scrape_website(target_url)
    # Read URLs from a text file
    with open('skims.txt', 'r') as file:
        urls = file.readlines()

    # Iterate through each URL and scrape the website
    for url in urls:
        url = url.strip()
        print(url.split('/')[-1])
        scrape_website(url)
        
    # Print or save the result as JSON
    with open('skims.json', 'w') as json_file:
        json.dump(products, json_file, indent=2)


    