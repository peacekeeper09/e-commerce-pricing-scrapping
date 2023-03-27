import os
import time
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from configparser import ConfigParser
from bs4 import BeautifulSoup


# Load configuration file
config = ConfigParser()
config.read('config.ini')

# Load product URLs from configuration file
product_urls = config.get('PRODUCTS', 'urls').split(',')
# Load threshold prices from configuration file
threshold_prices = [float(p) for p in config.get('PRODUCTS', 'threshold_prices').split(',')]

# Load email configuration from environment variables
email_address = os.environ.get('EMAIL_ADDRESS')
email_password = os.environ.get('EMAIL_PASSWORD')
smtp_server = os.environ.get('SMTP_SERVER')
smtp_port = os.environ.get('SMTP_PORT')

# Set user agent string
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'

def check_prices():
    for i, url in enumerate(product_urls):
        # Make request to product URL with user agent string
        response = requests.get(url, headers={'User-Agent': user_agent})
        # Parse response with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        # Get product title
        title = soup.find(id="productTitle").get_text().strip()
        # Get product price and convert to float
        price_str = soup.find(id="priceblock_ourprice").get_text().strip()
        price = float(price_str[2:].replace(',', ''))
        # Check if product price is below threshold
        if price < threshold_prices[i]:
            # Send email notification
            send_email(title, url, price)

def send_email(title, url, price):
    # Create message object
    message = MIMEMultipart()
    message['From'] = email_address
    message['To'] = email_address
    message['Subject'] = 'Price Alert: {} - {:.2f}'.format(title, price)
    # Create message body
    body = 'The price of {} is now below the threshold price of {:.2f}. You can buy it here: {}'.format(title, threshold_prices[i], url)
    message.attach(MIMEText(body, 'plain'))
    # Connect to SMTP server and send email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(email_address, email_password)
        server.sendmail(email_address, email_address, message.as_string())
    print('Email sent for product: {}'.format(title))

# Schedule check_prices() function to run every hour
while True:
    check_prices()
    time.sleep(3600)
