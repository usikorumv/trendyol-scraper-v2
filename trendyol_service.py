import asyncio, aiohttp

from trendyol_apis import TrendyolAPIs


headers = {
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJTdGFuZGFyZFVzZXIiOiIwIiwidW5pcXVlX25hbWUiOiJ1c21hbi5vbXVyYWxpZXZAYWxhdG9vLmVkdS5rZyIsInN1YiI6InVzbWFuLm9tdXJhbGlldkBhbGF0b28uZWR1LmtnIiwicm9sZSI6InVzZXIiLCJhdHdydG1rIjoiZDMwZGMxZjYtZTRlZS0xMWVjLWJiODUtOGE1NTRiMmY1N2E3IiwidXNlcklkIjoiOTM2ODAxMDkiLCJlbWFpbCI6InVzbWFuLm9tdXJhbGlldkBhbGF0b28uZWR1LmtnIiwiYXVkIjoic2JBeXpZdFgramhlTDRpZlZXeTV0eU1PTFBKV0Jya2EiLCJleHAiOjE4MTIyMzU0OTMsImlzcyI6ImF1dGgudHJlbmR5b2wuY29tIiwibmJmIjoxNjU0NDQ3NDkzfQ.SDyHGGU41lvYWqg6w95MvEIqvs-L_R7woBaKB41Q4F0",
}


class TrendyolService(TrendyolAPIs):
    # PRODUCTS
    all_products = []

    async def fetch_len_of_products_reviews(self, session, id):
        async with session.get(
            self.get_product_reviews_api(id, 0),
            headers=headers,
        ) as response:
            try:
                data = ujson.loads(await response.text())

                product_reviews = data["result"]["productReviews"]

                total = product_reviews["totalElements"]

                return total
            except:
                return 0

    async def fetch_product_reviews(self, session, id, get_all=True):
        size = await self.fetch_len_of_products_reviews(session, id)

        if size == 0:
            return []

        async with session.get(
            self.get_product_reviews_api(id, 0, size), headers=headers
        ) as response:
            try:
                data = ujson.loads(await response.text())

                product_reviews = data["result"]["productReviews"]

                reviews = product_reviews["content"]

                return [
                    {
                        "user": review["userFullName"],
                        "rate": review["rate"],
                        "comment": review["comment"],
                        "date": review["lastModifiedDate"],
                    }
                    for review in reviews[:20]
                ]
            except:
                return []

    # TODO: Add questions and answers
    # async def get_product_questions(self, link):
    #     "/polo-state/erkek-cok-renkli-regular-bisiklet-yaka-5-li-tisort-paketi-saks-p-115621006/saticiya-sor?merchantId=342783"

    #     async with session.get(
    #         self.get_reccomendations_api(id, "/cross"), headers=headers
    #     ) as response:
    #         try:
    #             data = ujson.loads(await response.text())

    async def fetch_cross_products_id(self, session, id):
        async with session.get(
            self.get_reccomendations_api(id, "/cross"), headers=headers
        ) as response:
            try:
                data = ujson.loads(await response.text())

                products = data["result"]["content"]

                return [product["id"] for product in products]
            except:
                return []

    async def fetch_recommendation_products_id(self, session, id):
        async with session.get(
            self.get_reccomendations_api(id, "/recommendation"), headers=headers
        ) as response:
            try:
                data = ujson.loads(await response.text())

                products = data["result"]["content"]

                return [product["id"] for product in products]
            except:
                return []

    async def fetch_product_attributes(self, session, raw_product):
        async with session.get(
            self.get_products_group_api(raw_product["productGroupId"]), headers=headers
        ) as response:
            try:
                data = ujson.loads(await response.text())

                slicing_attributes = data["result"]["slicingAttributes"][0][
                    "attributes"
                ]

                attributes = []
                for slicing_attribute in slicing_attributes:
                    attribute = slicing_attribute["contents"][0]
                    attributes.append(
                        {
                            "id": attribute["id"],
                            "name": slicing_attribute["name"],
                            "slug": slicing_attribute["beautifiedName"],
                            "link": attribute["url"],
                        }
                    )

                return attributes
            except:
                return []

    async def fetch_product_from_id(self, session, id):
        async with session.get(self.get_product_api(id), headers=headers) as response:
            try:
                data = ujson.loads(await response.text())

                product = data["result"]

                campaign = product["campaign"]
                brand = product["brand"]
                category = product["originalCategory"]
                brand = product["brand"]
                sizes = product["allVariants"]
                description = product["contentDescriptions"]

                final = {
                    "id": product["id"],
                    "name": product["name"],
                    "link": product["url"],
                    "images": [
                        self.image_api + image_link for image_link in product["images"]
                    ],
                    "price": product["price"],
                    "rating": product["ratingScore"]["averageRating"],
                    "campaign": product["merchant"]["name"],
                    "brand": {
                        "id": brand["id"],
                        "name": brand["name"],
                        "slug": brand["beautifiedName"],
                    },
                    "category": {
                        "id": category["id"],
                        "name": category["name"],
                        "slug": category["beautifiedName"],
                    },
                    "showColor": product["color"],  # REVIEW
                    # TODO: Some product have problems while getting showSize
                    "showSize": product["variants"][0]["attributeValue"],  # REVIEW
                    # TODO: Some products dont have sizes
                    "sizes": [  # REVIEW
                        {
                            "value": size["value"],
                            "inStock": size["inStock"],
                            "price": size["price"],
                            "currency": size["currency"],
                        }
                        for size in sizes
                    ],
                    "description": "\n".join(
                        [
                            description["description"]
                            for description in product["contentDescriptions"]
                        ]
                    ),
                    "reviews": await self.fetch_product_reviews(session, id),
                    "questions": [],
                    "recommendations": await self.fetch_recommendation_products_id(
                        session, id
                    ),
                    "cross": await self.fetch_cross_products_id(session, id),
                }

                return final

            except Exception as e:
                print(f"\nError: {id}\n")

    def get_product_from_id(self, id):
        async def task():
            global product
            async with aiohttp.ClientSession() as session:
                product = await self.fetch_product_from_id(session, id)

        asyncio.run(task())

        # TODO: REFACTOR
        MyUtils.create_folder("output")
        MyUtils.create_folder("output/products")
        MyUtils.create_file(f"output/products/{id}.json", ujson.dumps(product))

        return product

    async def fetch_product_from_card_data(self, session, card_data: dict):
        try:
            attributes = await self.fetch_product_attributes(session, card_data)

            product = await self.fetch_product_from_id(session, card_data["id"])

            # TODO: Make async
            product["colors"] = (
                [
                    {
                        "name": attribute["name"],
                        "slug": attribute["slug"],
                        "product": await self.fetch_product_from_id(  # STORE JUST ID`s
                            session, attribute["id"]
                        ),
                    }
                    for attribute in attributes
                ]
                if attributes != []
                else []
            )

            return product
        except:
            pass

    async def fetch_all_products_from_link(self, session, link, page):
        try:
            async with session.get(
                self.get_products_api(link, page),
                headers=headers,
                timeout=20,
            ) as response:
                data = ujson.loads(await response.text())

                raw_products = data["result"]["products"]

                for raw_product in raw_products:
                    self.all_products.append(
                        await self.fetch_product_from_card_data(session, raw_product)
                    )

                print(f"\nLink: {link}\nPage: {page + 1}")

        except asyncio.TimeoutError:
            print(f"\nFAILED TO PROCESS Link: {link}\nPage: {page + 1}")

        # except aiohttp.ClientConnectionError:
        #     # pass
        #     print(f"\nFAILED Link: {link}\nPage: {page + 1}")

        # except aiohttp.client_exceptions.ClientPayloadError:
        #     pass

        except Exception as e:
            print(f"\nFAILED Link: {link}\nPage: {page + 1}")

            # TODO: REFACTOR
            # MyUtils.create_folder("output")
            # MyUtils.create_folder("output/error")
            # MyUtils.create_file("output/error/trace_back.txt", str(e))
            # MyUtils.create_file(
            #     "output/error/products.json", ujson.dumps(self.all_products)
            # )

    # TODO: Add parameters like how much pages and categories (also check if they are valid)
    async def fetch_all_products(self):
        # TODO: OPTIMIZE
        with open("output/categories.json", "r") as f:
            categories = ujson.loads(f.read())

        end_categories = []
        for category in categories:
            parent = True
            for compare in categories:
                if compare.get("parent", "") == "":
                    continue
                if category["slug"] == compare["slug"]:
                    continue
                if category["slug"] == compare["parent"]:
                    parent = True
                    break
                parent = False

            if not parent:
                end_categories.append(category)

        self.all_products = []

        connector = aiohttp.TCPConnector(limit=50)
        async with aiohttp.ClientSession(connector=connector) as session:
            # async with aiohttp.ClientSession() as session:
            self.total = len(end_categories) * 208

            tasks = [
                self.fetch_all_products_from_link(session, category["link"], page)
                # for page in range(208 + 1)  # JUST FOR TEST
                # for category in end_categories  # JUST FOR TEST
                for page in range(1)  # JUST FOR TEST
                for category in end_categories  # JUST FOR TEST
            ]

            await asyncio.gather(*tasks)

    # TODO: Try to use in all methods where aggregation value
    # AGGREGATIONS
    # async def get_aggregations(self, session, link):
    #     async with session.get(
    #         "https://public.trendyol.com/discovery-web-searchgw-service/v2/api/aggregations"
    #         + link,
    #         headers=headers,
    #     ) as response:
    #         self.aggregations = []

    #         data = ujson.loads(await response.text())

    #         aggregations = data["result"]["aggregations"]

    #         return aggregations

    # async def get_items_from_aggregations_group(self, session, link, group):
    #     pass

    # COLORS
    all_colors = []

    async def get_colors_from_link(self, session, link):
        async with session.get(
            self.aggregations_api + link, headers=headers
        ) as response:
            data = ujson.loads(await response.text())

            aggregations = data["result"]["aggregations"]

            colors_aggregation = next(
                item for item in aggregations if item["group"] == "ATTRIBUTE"
            )
            colors = colors_aggregation["values"]

            self.all_colors += [
                {
                    "id": color["id"],
                    "name": color["text"],
                    "slug": color["beautifiedName"],
                }
                for color in colors
            ]

    async def fetch_all_colors(self):
        self.all_colors = []

        tasks = []

        async with aiohttp.ClientSession() as session:
            for category in self.categories:
                tasks.append(self.get_colors_from_link(session, category["link"]))

            await asyncio.gather(*tasks)

    # GET SIZES
    all_sizes = []

    async def get_sizes_from_link(self, session, link):
        async with session.get(
            self.aggregations_api + link, headers=headers
        ) as response:
            data = ujson.loads(await response.text())

            aggregations = data["result"]["aggregations"]

            sizes_aggregation = next(
                item for item in aggregations if item["group"] == "VARIANT"
            )
            sizes = sizes_aggregation["values"]

            self.all_sizes += [
                {
                    "name": size["text"],
                    "slug": size["beautifiedName"],
                }
                for size in sizes
            ]

    async def fetch_all_sizes(self):
        self.all_sizes = []

        tasks = []

        async with aiohttp.ClientSession() as session:
            for category in self.categories:
                tasks.append(self.get_sizes_from_link(session, category["link"]))

            await asyncio.gather(*tasks)

    # BRANDS
    all_brands = []

    async def get_brands_from_link(self, session, link):
        async with session.get(
            self.aggregations_api + link, headers=headers
        ) as response:
            data = ujson.loads(await response.text())

            aggregations = data["result"]["aggregations"]

            brands_aggregation = next(
                item for item in aggregations if item["group"] == "BRAND"
            )
            brands = brands_aggregation["values"]

            self.all_brands += [
                {
                    "id": brand["id"],
                    "name": brand["text"],
                    "slug": brand["beautifiedName"],
                }
                for brand in brands
            ]

    async def fetch_all_brands(self):
        self.all_brands = []

        tasks = []

        async with aiohttp.ClientSession() as session:
            for category in self.categories:
                tasks.append(self.get_brands_from_link(session, category["link"]))

            await asyncio.gather(*tasks)

    # CATEGORIES
    all_categories = []

    async def get_categories_from_link(self, session, link):
        async with session.get(
            self.aggregations_api + link, headers=headers
        ) as response:
            try:
                data = ujson.loads(await response.text())

                aggregations = data["result"]["aggregations"]

                category_aggregation = next(
                    item for item in aggregations if item["group"] == "CATEGORY"
                )
                categories = category_aggregation["values"]

                return categories

            except Exception as e:
                pass

    # TODO: Make full async
    async def get_categories(self, category, write2file=False):
        all_categories = [category]

        async with aiohttp.ClientSession() as session:
            i = 0
            while i < len(all_categories):
                categories = await self.get_categories_from_link(
                    session, all_categories[i]["link"]
                )

                try:
                    if len(categories) > 1:
                        print()

                        for category in categories:
                            print(category["text"])

                        all_categories += [
                            {
                                "id": category["id"],
                                "name": category["text"],
                                "slug": category["beautifiedName"],
                                "link": category["url"],
                                "count": category["count"],
                                "parent": all_categories[i]["slug"],
                            }
                            for category in categories
                        ]
                except Exception as e:  # Review
                    # print(e)
                    pass

                i += 1

        self.all_categories += all_categories

    async def fetch_all_categories(self):
        self.all_categories = []

        tasks = [self.get_categories(category) for category in self.categories_api]

        await asyncio.gather(*tasks)
