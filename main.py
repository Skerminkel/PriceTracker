from bs4 import BeautifulSoup as BS
import requests
import smtplib


params = {
    "Accept-Encoding": "gzip, deflate",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                  "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    "Dnt": "1",
}

urls = ["https://www.amazon.com/EVGA-06G-P4-2068-KR-GeForce-Gaming-Backplate/dp/B083GGYNQ6/ref=sr_1_3?crid"
        "=9OTZ83NBJJD9&keywords=rtx+2060&qid=1640678364&sprefix=rtx+2060%2Caps%2C365&sr=8-3"]

target_card = 1000


def price_email(product_name, price):

    gmail = {"smtp": "smtp.gmail.com",
             "email": "johnathandeerathan@gmail.com",
             "pass": "}E(P)Q:k"}

    message = f"{product_name} is down to only ${price}!\n{url}"

    with smtplib.SMTP(gmail["smtp"]) as connection:
        connection.starttls()
        connection.login(user=gmail["email"], password=gmail["pass"])
        connection.sendmail(from_addr=gmail["email"], to_addrs="waynedas1@gmail.com",
                            msg=f"Subject:Price Alert!\n\n{message}")

    print("email sent")


for url in urls:
    response = requests.get(url, headers=params)

    response.raise_for_status()

    webpage = response.text

    soup = BS(webpage, 'html.parser')
    price_whole = soup.find(class_="a-price-whole").get_text()
    price_fraction = soup.find(class_="a-price-fraction").get_text()

    name = soup.find(class_="product-title-word-break").get_text().strip()

    total_price_card = float(price_whole + price_fraction.strip())
    final = f"{name}: {total_price_card}"

    if total_price_card <= target_card:
        print(f"{name} less than target amount of ${target_card}")
        price_email(name, total_price_card)

    else:
        print(f"{name} not less than target amount of ${target_card}")
