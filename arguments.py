from argparse import ArgumentParser


def argparse_setup() -> ArgumentParser.parse_args:
    """Setup and return argparse."""
    parser = ArgumentParser()

    parser.add_argument(
        '--all',
        dest='all',
        help='show all wishes on wishlist',
        action='store_true'
    )

    parser.add_argument(
        '-a',
        '--add',
        dest='add_wish',
        help='add a wish with link in sub_category in super_category to wishlist',
        nargs=3,
        metavar=('<super_category>', "<sub_category>", "<link>"),
        type=str
    )

    return parser.parse_args()
