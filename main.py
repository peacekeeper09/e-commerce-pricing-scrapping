#firstly we will need to import some of the library that will help us to drive this project smoothly!
import requests [know more about the library from here](https://www.w3schools.com/python/module_requests.asp)
import smtplib [know more about the library from here](https://docs.python.org/3/library/smtplib.html)
import time [know more about the library from here](https://pypi.org/project/beautifulsoup4/)
from bs4 import BeautifulSoup [know about the library from here](https://pypi.org/project/beautifulsoup4/)


#here you will have to paste the link of the product whose price has to be scrapped. I have set it to the link of amazon, product = iPhone 14proMax
URL = 'https://www.amazon.in/iPhone-Pro-Max-256GB-Gold/dp/B0BDK63WMS?ref_=ast_sto_dp'

#here you will have to paste your "my user agent address", get yours from here http://my-user-agent.com/
headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}

# this part is for checking the price of the specified link(product link) above
def check_price():
    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    title = soup.find(id="productTitle").get_text()
    price = soup.find(id="priceblock_ourprice").get_text()
    converted_price = float(price[2:4]+price[5:8])
#here it is checking if the price of the specified product above is below than 100000 (in this case), you can choose a value of your own.
    if(converted_price < 100000):
        send_mail()
#if the condition (value of the product goes below than 100000), then it will proccess further
    print(converted_price)
    print(title.strip())

#function for sending email to the user when the prices fell for a product
def send_mail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo() # EHLO is a command sent by an email server to identify itself when connecting to another email
    server.starttls()
    server.ehlo()

    server.login('peacekeeper0907@gmail.com', 'Google app password here')
    #server.login('Your gmail account', 'Google app password here')

    subject = 'Hello PEACE, the product you were looking for is now available for 100000!'
    body = 'Hello PEACE, its been along. I have got a good news for you, the product [iPhone 14proMax is now available for 100000. Get it ASAP, before the offer goes out. Link here:- https://www.amazon.in/iPhone-Pro-Max-256GB-Gold/dp/B0BDK63WMS?ref_=ast_sto_dp]'

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail('peacekeeper0907@gmail.com', 'peacekeeper0907@gmail.com', msg)
    #server.sendmail('A mail address from where mail has to be sent', 'target mail address, where mail has to be received!', msg/ you can type a message of your own here too but we have simply made a variable above and defined the message there to make it look clean!)
    
    print("The email has been successfully to peacekeeper0907@gmail.com!")

    server.quit()

while(True):
    check_price()
    time.sleep(3600)
#time here is in seconds, please convert the time to seconds first and then fill it in here. You can use https://www.inchcalculator.com/time-to-seconds-calculator/
