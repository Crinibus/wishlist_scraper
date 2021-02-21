import json
import questionary
import data as dt


def read_wishlist(filename: str) -> dict:
    with open(filename, "r") as json_file:
        data = json.load(json_file)
    return data


def get_super_categories(data: dict) -> list:
    temp = []
    for super_cat in data.keys():
        temp.append(super_cat)
    return temp


def get_sub_categories(data: dict, super_category: str) -> list:
    temp = []
    for sub_cat in data[super_category]:
        temp.append(sub_cat)
    return temp


def get_links(data: dict, super_category: str, sub_category: str) -> list:
    temp = []
    for link in data[super_category][sub_category]:
        temp.append(link)
    return temp


# if __name__ == '__main__':
#     data = read_wishlist('wishlist.json')
#     super_cat = questionary.select("Select a category:", choices=get_super_categories(data)).ask()
#     sub_cat = questionary.select("Select a sub category:", choices=get_sub_categories(data, super_cat)).ask()

#     print()
#     for index, link in enumerate(get_links(data, super_cat, sub_cat)):
#         print(f"{index + 1} > {link}")


def show_all_data(data: dt.Data):
    for superCategory in data.categories:
        print(f"\nSuper category: {superCategory.name}")
        for subCategory in superCategory.sub_categories:
            print(f"\tSub category: {subCategory.name}")
            subCategory.get_info_for_products()
            for product in subCategory.products:
                # product.get_info_link()
                print(f"\t\t{product.price} - {product.name}")


def get_user_choice(data: dt.Data):
    user_super_category_name = questionary.select("Choose super category:", choices=[cat.name for cat in data.categories]).ask()
    user_super_category = data.get_category(user_super_category_name)
    # user_super_category = questionary.select("Choose super category:", choices=data.categories).ask()
    user_sub_category_name = questionary.select("Choose sub category:", choices=[cat.name for cat in user_super_category.sub_categories]).ask()
    user_sub_category = user_super_category.get_sub_category(user_sub_category_name)
    user_sub_category.get_info_for_products()
    
    show_user_choice(user_super_category, user_sub_category)


def show_user_choice(super_category: dt.SuperCategory, sub_category: dt.SubCategory):
    print(super_category.name)
    print(f"\t{sub_category.name}")
    for product in sub_category.products:
        print(f"\t\t{product.price} - {product.name}")


def main():
    my_data = dt.Data("wishlist.json")

    show_all_data(my_data)
    # get_user_choice(my_data)


if __name__ == "__main__":
    main()
