import requests
from bs4 import BeautifulSoup
import smtplib
from time import sleep
import json

URL = 'https://www.amazon.it/Alesis-Recital-Principianti-Alimentazione-Altoparlanti/dp/B01DZXE9NC'

headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36 OPR/68.0.3618.63'}

def checkPrice():
    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    title = soup.find(id='productTitle').get_text().strip()
    price = soup.find(id='priceblock_ourprice').get_text().strip()
    converted_price = float(price[0:6].replace(',','.'))

    with open('lowPrice.json', 'r') as f:
        lowPrice = json.load(f)
        if(converted_price < lowPrice['price']):
            lowPrice['price'] = converted_price
            with open('lowPrice.json', 'w') as of:
                json.dump(lowPrice, of)
            sendMail(title, converted_price)
            print(f"Price went down to {price}, so the mail was sent")
        else:
            print(f"The price of {converted_price} wasn't lower than the previous lowest price {lowPrice['price']}, so no mail was sent")

def sendMail(title, price):
    global URL
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('ale56.mia@gmail.com', 'jixujmugxcabkpel')

    Subject = 'Price fell down!'
    Body = f'The price for the product {title} fell down to {price} euros, go check it out at {URL}!'

    msg = f'Subject: {Subject}\n\n{Body}'

    server.sendmail(
        'ale56.mia@gmail.com',
        'ale56.mia@gmail.com',
        msg
    )

    server.quit()

while(True):
    checkPrice()
    sleep(3600)