import json
import threading
from websites import get_domain_from_link, GET_WEBSITE_METHOD


class Data:
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.data = Data.read_json(filename)
        self.categories = []
        self.format_data()

    @staticmethod
    def read_json(filename: str) -> dict:
        with open(filename, "r") as json_file:
            data = json.load(json_file)
        return data

    def format_data(self):
        # for category in self.data.keys():
        #     self.categories.update({category: []})

        #     for sub_category in self.data[category]:
        #         self.categories[category].append(SubCategory(sub_category, self.data[category][sub_category]))

        for category in self.data.keys():
            self.add_category(category, self.data[category])

    def add_category(self, name: str, info: dict):
        new_category = SuperCategory(name, info)
        self.categories.append(new_category)

    def get_category(self, cat_name):
        for cat in self.categories:
            if cat.name == cat_name:
                return cat


class SuperCategory:
    def __init__(self, name: str, info: dict) -> None:
        self.name = name
        self.info = info
        self.sub_categories = []
        self.format_info()

    def format_info(self):
        for sub_cat in self.info:
            self.add_sub_category(sub_cat, self.info[sub_cat])

    def add_sub_category(self, name: str, info: dict):
        new_sub_category = SubCategory(name, info)
        self.sub_categories.append(new_sub_category)
    
    def get_sub_category(self, sub_cat_name: str):
        for sub_cat in self.sub_categories:
            if sub_cat.name == sub_cat_name:
                return sub_cat


class SubCategory:
    def __init__(self, name: str, info: dict) -> None:
        self.name = name
        self.info = info
        self.products = []
        self.format_info()

    def format_info(self):
        for link in self.info:
            self.add_product(link)

    def add_product(self, link: str):
        new_product = Product(link)
        self.products.append(new_product)

    def get_info_for_products(self):
        # Create threads
        threads = [
            threading.Thread(
                target=product.get_info, name=f"thread_{product.domain}_{index}"
            )
            for index, product in enumerate(self.products)
        ]

        # Start all threads
        for thread in threads:
            thread.start()

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

    def __repr__(self) -> str:
        return f"SubCategory(category_name={self.name}, category_info={self.info}"

    def __str__(self) -> str:
        return f"{self.name}"


class Product:
    def __init__(self, link: str) -> None:
        self.link = link
        self.domain = get_domain_from_link(link)
        self.name = None
        self.price = None
        # self.get_info()

    def get_info(self):
        self.name, self.price = GET_WEBSITE_METHOD[self.domain](self.link)

    def __str__(self) -> str:
        return f"{self.name} - {self.price}"
