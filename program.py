import questionary
import data as dt
import arguments as arg


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
    # Get user choice for super category
    user_super_category_name = questionary.select("Choose super category:", choices=[cat.name for cat in data.categories]).ask()
    # Get the class the user has chosen as super category 
    user_super_category = data.get_category(user_super_category_name)

    # Get user choice for sub category
    user_sub_category_name = questionary.select("Choose sub category:", choices=[cat.name for cat in user_super_category.sub_categories]).ask()
    # Get the class the user has chosen as sub category
    user_sub_category = user_super_category.get_sub_category(user_sub_category_name)

    # Scrape products in sub category for info
    user_sub_category.get_info_for_products()

    # Show info of the products in user chosen sub category
    show_user_choice(user_super_category, user_sub_category)


def show_user_choice(super_category: dt.SuperCategory, sub_category: dt.SubCategory):
    print(super_category.name)
    print(f"\t{sub_category.name}")
    for product in sub_category.products:
        print(f"\t\t{product.price} - {product.name}")


def main():
    args = arg.argparse_setup()
    my_data = dt.Data("wishlist.json")

    if args.add_wish:
        super_category = args.add_wish[0]
        sub_category = args.add_wish[1]
        link = args.add_wish[2]

        my_data.add_wish(super_category, sub_category, link)

    if args.all:
        show_all_data(my_data)
    else:
        get_user_choice(my_data)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Closed program")
