import requests
from bs4 import BeautifulSoup
from const import REQUEST_HEADER, REQUEST_COOKIES, REMOVE_FROM_DOMAIN


class Websites:
    @staticmethod
    def Komplett(link: str):
        # get name and price of product at link
        response = request_link(link)
        soup = BeautifulSoup(response.text, "html.parser")
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
        response = request_link(link)
        soup = BeautifulSoup(response.text, "html.parser")
        name = soup.find("div", class_="col-xs-12 col-sm-7").h1.text

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
        response = request_link(link)
        soup = BeautifulSoup(response.text, "html.parser")
        name = soup.find("div", class_="content-head").text.strip()
        price = soup.find("div", class_="price").text.replace(u"\xa0DKK", "")
        return name, price


GET_WEBSITE_METHOD = {
    "komplett": Websites.Komplett,
    "proshop": Websites.Proshop,
    "avxperten": Websites.AvXperten,
}


def request_link(link: str):
    response = requests.get(link, headers=REQUEST_HEADER, cookies=REQUEST_COOKIES)

    return response


def get_domain_from_link(link: str):
    # get domain with "www." and ".com"
    domain = link.split("/")[2]

    # remove "www." and ".com"
    for to_remove in REMOVE_FROM_DOMAIN:
        domain = domain.replace(to_remove, "")

    return domain
