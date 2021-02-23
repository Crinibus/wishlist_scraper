import requests
from bs4 import BeautifulSoup
from const import REQUEST_HEADER, REQUEST_COOKIES, REMOVE_FROM_DOMAIN


class Websites:
    @staticmethod
    def Komplett(link: str):
        # get name and price of product at link
        soup = request_link(link)
        name = soup.find("div", class_="product-main-info__info").h1.span.text
        price = (
            soup.find("span", class_="product-price-now")
            .text.strip(",-")
            .replace(".", "")
        )
        return name, price

    @staticmethod
    def Proshop(link: str):
        # get name and price of product at link
        soup = request_link(link)
        name = soup.find("meta", property="og:title")["content"]

        try:
            # find normal price
            price = (
                soup.find("span", class_="site-currency-attention")
                .text.split(",")[0]
                .replace(".", "")
            )
        except AttributeError:
            try:
                # find discount price
                price = (
                    soup.find(
                        "div", class_="site-currency-attention site-currency-campaign"
                    )
                    .text.split(",")[0]
                    .replace(".", "")
                )
            except AttributeError:
                # if campaign is sold out (udsolgt)
                price = (
                    soup.find("div", class_="site-currency-attention")
                    .text.split(",")[0]
                    .replace(".", "")
                )
        return name, price

    @staticmethod
    def AvXperten(link: str):
        # get name and price of product at link
        soup = request_link(link)
        name = soup.find("meta", property="og:title")['content']
        price = soup.find("div", class_="price").text.replace(u"\xa0DKK", "")
        return name, price

    @staticmethod
    def Computersalg(link: str):
        # get name and price of product at link
        soup = request_link(link)
        name = soup.findAll('td', class_='specLine')[1].text
        price = soup.find('span', itemprop='price').text.strip().split(',')[0].replace('.', '')
        return name, price

    @staticmethod
    def Elgiganten(link: str):
        # get name and price of product at link
        soup = request_link(link)
        name = soup.find('h1', class_='product-title').text
        price = soup.find('div', class_='product-price-container').text.strip().replace(u'\xa0', '')
        return name, price

    @staticmethod
    def Amazon(link: str):
        # get name and price of product at link
        soup = request_link(link)
        name = soup.find('span', id='productTitle').text.strip().lower()
        price = soup.find('span', id='priceblock_ourprice').text.replace('$', '').split('.')[0].replace(',', '')
        return name, price

    @staticmethod
    def eBay(link: str):
        # get name and price of product at link
        soup = request_link(link)
        if link.split('/')[3] == 'itm':
            name = link.split('/')[4].replace('-', ' ')
            price = soup.find('span', id='convbinPrice').text.replace('(including shipping)', '').replace('DKK ', '').replace(',', '')
        else:
            name = soup.find('h1', class_='product-title').text
            price = soup.find('div', class_='display-price').text.replace('DKK ', '').replace(',', '')
        return name, price


GET_WEBSITE_METHOD = {
    "komplett": Websites.Komplett,
    "proshop": Websites.Proshop,
    "avxperten": Websites.AvXperten,
    "computersalg": Websites.Computersalg,
    "elgiganten": Websites.Elgiganten,
    "amazon": Websites.Amazon,
    "ebay": Websites.eBay,
}


def request_link(link: str) -> BeautifulSoup:
    response = requests.get(link, headers=REQUEST_HEADER, cookies=REQUEST_COOKIES)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup


def get_domain_from_link(link: str) -> str:
    # get domain with "www." and ".com"
    domain = link.split("/")[2]

    # remove "www." and ".com"
    for to_remove in REMOVE_FROM_DOMAIN:
        domain = domain.replace(to_remove, "")

    return domain
