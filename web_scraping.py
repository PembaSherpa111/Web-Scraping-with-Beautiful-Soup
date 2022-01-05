from bs4 import BeautifulSoup
import requests
import csv

Books = []
for x in range(1,51):

    html = requests.get("http://books.toscrape.com/catalogue/page-" + f'{x}' + ".html").text

    soup = BeautifulSoup(html,"html.parser")

    list = soup.find("ol",attrs = {"class":"row"})

    for dict in list.find_all("li"): # dict has all the data of a book  
        
        Book = {}

        for line in dict.find_all("div",attrs = {"class":"product_price"}):  
            price = line.find_all("p")
            price_amount = price[0].string
            price_amount = "".join(c for c in price_amount if ord(c)<128) #removes non ascii

            instock_availability = price[1].text
            if instock_availability.strip() == "In stock":
                
                title = dict.find("h3").find("a").attrs["title"]
                Book["Title"] = (f"{title}")
                
                Book["Price"] = price_amount

                rating_tag = (dict.find("p", attrs ="star-rating")).attrs # .attrs provides the name of tag
                star_rating = rating_tag["class"]
                Book["Rating"] = star_rating[1]

            Books.append(Book)

keys = Books[0].keys()
with open("Books.csv", "w", encoding="utf-8") as csvfile: 
    csvwriter = csv.DictWriter(csvfile,keys)     #creating a csv writer object 
    csvwriter.writeheader()
    csvwriter.writerows(Books)
