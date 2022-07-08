import asyncio

from time import time
from utils.my_utils import *

from trendyol_apis import TrendyolAPIs
from trendyol_service import TrendyolService


class TrendyolScraper(TrendyolService):
    def get_all_products(self, write2file=False):
        print("\nLooking for categories")

        if not path.exists("output/categories.json"):
            print("Starting parsing categories")

            self.get_all_categories(write2file=True)

            print("\nFinished parsing categories")
        else:
            print("Categories found")

        print("\nStarting parsing products")
        print("Processed: ")

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.fetch_all_products())

        if write2file:
            MyUtils.create_folder("output")
            MyUtils.create_file("output/products.json", ujson.dumps(self.all_products))

        print("\nFinished parsing products")

        return self.all_products

    def get_all_colors(self, write2file=False):
        asyncio.run(self.fetch_all_colors())

        if write2file:
            MyUtils.create_folder("output")
            MyUtils.create_file("output/colors.json", ujson.dumps(self.all_colors))

        return DictionaryUtils.get_unique_list_from_dicts(self.all_colors)

    def get_all_sizes(self, write2file=False):
        asyncio.run(self.fetch_all_sizes())

        if write2file:
            MyUtils.create_folder("output")
            MyUtils.create_file("output/sizes.json", ujson.dumps(self.all_sizes))

        return DictionaryUtils.get_unique_list_from_dicts(self.all_sizes)

    def get_all_brands(self, write2file=False):
        asyncio.run(self.fetch_all_brands())

        if write2file:
            MyUtils.create_folder("output")
            MyUtils.create_file("output/brands.json", ujson.dumps(self.all_brands))

        return DictionaryUtils.get_unique_list_from_dicts(self.all_brands)

    def get_all_categories(self, write2file=False):
        asyncio.run(self.fetch_all_categories())

        if write2file:
            MyUtils.create_folder("output")
            MyUtils.create_file(
                "output/categories.json", ujson.dumps(self.all_categories)
            )

        return self.all_categories


def main():
    scraper = TrendyolScraper()

    start_time = time()

    scraper.get_all_categories(write2file=True)
    # scraper.get_all_brands(write2file=True)
    # scraper.get_all_colors(write2file=True)
    # scraper.get_all_sizes(write2file=True)

    # all_products = scraper.get_all_products(write2file=True)
    # print(len(all_products))

    # print(scraper.get_product_from_id(42631817))

    print(time() - start_time)


if __name__ == "__main__":
    main()
