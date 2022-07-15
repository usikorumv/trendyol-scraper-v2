import ujson
import asyncio
from time import time

from utils.my_utils import *

from trendyol_apis import TrendyolAPIs
from trendyol_service import TrendyolService


class TrendyolScraper(TrendyolService):
    # TODO: Finish
    def get_product_from_id(self, id):
        pass

    def get_all_products(self, write2file=False):
        print("\nSearching for categories.json")

        if not FolderAndFileUtils.path_exist("output/categories.json"):
            print("Starting parsing categories")

            self.get_all_categories(write2file=True)

            print("\nFinished parsing categories")
            print("\nCategories saved to categories.json")
        else:
            print("categories.json found")

        print("\nStarting parsing products")
        print("Processed: ")
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.fetch_all_products())
        loop.close()

        if write2file:
            FolderAndFileUtils.create_file(
                "output/products.json", ujson.dumps(self.all_products)
            )

        print("\nFinished parsing products")

        return self.all_products

    def get_all_colors(self, write2file=False):
        asyncio.run(self.fetch_all_colors())

        if write2file:
            FolderAndFileUtils.create_file(
                "output/colors.json", ujson.dumps(self.all_colors)
            )

        return DictionaryUtils.get_unique_list_from_dicts(self.all_colors)

    def get_all_sizes(self, write2file=False):
        asyncio.run(self.fetch_all_sizes())

        if write2file:
            FolderAndFileUtils.create_file(
                "output/sizes.json", ujson.dumps(self.all_sizes)
            )

        return DictionaryUtils.get_unique_list(self.all_sizes)

    def get_all_brands(self, write2file=False):
        asyncio.run(self.fetch_all_brands())

        if write2file:
            FolderAndFileUtils.create_file(
                "output/brands.json", ujson.dumps(self.all_brands)
            )

        return DictionaryUtils.get_unique_list_from_dicts(self.all_brands)

    def get_all_categories(self, write2file=False):
        asyncio.run(self.fetch_all_categories())

        if write2file:
            FolderAndFileUtils.create_file(
                "output/categories.json", ujson.dumps(self.all_categories)
            )

        return self.all_categories


def main():
    scraper = TrendyolScraper()

    start_time = time()

    products = scraper.get_all_products()
    
    print(len(products))
    
    for product in products:
        if product["colors"]:
            FolderAndFileUtils.create_file("output/products/with_key.json", ujson.dumps(product))
            break

    print(time() - start_time)


if __name__ == "__main__":
    main()

# /erkek-hastane-cikisi-x-g2-c104159