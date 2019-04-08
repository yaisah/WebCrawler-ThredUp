#Yaisah Granillo
##
#Don't forget to import the necessary modules
from bs4 import BeautifulSoup
from requests import get
import urllib.request, urllib.parse, urllib.error
import json
import mysql.connector

##Database connection to store the results
conn = mysql.connector.connect(host="xx.xx.xx.xx", user="xxx", password="xxx", database="xxx")
c = conn.cursor()

##website source code - I chose ThredUp filtered to my sizes
url = 'https://www.thredup.com/products/women?condition=q1_nwt&department_tags=women&include_petite=true&shop_local=false&sizing_id=551%2C765%2C778%2C781%2C774%2C791%2C788&sort=Newest+First'
response = get(url)
soup = BeautifulSoup(response.text, 'html.parser')
type(soup)

##Get a specific section of a page based on a class, in this case I want to look at the items in the grid
results = soup.find_all(class_='results-grid-item')
#print(len(results))

#menuLinks = menuNav2.find_all('a')

for container in results:
    #Name of the item brand
    brand = container.find('a', class_='_3p5eh').text
    print(brand)
    
    #Type of item
    item = container.find('div', class_='item-title').text
    print(item)

    #Size of item
    size = container.find('div', class_='size-name').text
    print(size)

    #current price in the website
    price = container.find('span', class_ = 'formatted-price').text
    print(price)

    #original price of the product in retail
    msrp = container.find('span', class_ = 'formatted-msrp').text
    print(msrp)

    #link to the product
    link = container.find('a', class_='_3p5eh')['href']
    linkurl = ("https://www.thredup.com"+ link)
    print(linkurl)

##Post the record to desired database
myquery = "INSERT INTO ygranill.ThredUp(Brand, itemtitle, size, price, MSRP, link) VALUES (%s, %s, %s, %s, %s, %s);"
arguments = (brand, item, size, price, msrp, linkurl)

##Execute the query
c.execute(myquery, arguments)
conn.commit()

print("Done!")

##close the database connections
c.close()
conn.close()
