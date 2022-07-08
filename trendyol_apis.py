class TrendyolAPIs:
    api = "https://www.trendyol.com"
    image_api = "https://cdn.dsmcdn.com"

    aggregations_api = (
        "https://public.trendyol.com/discovery-web-searchgw-service/v2/api/aggregations"
    )

    categories_api = [
        {
            "name": "Kadın Giyim",
            "slug": "kadın-giyim",
            "link": "/kadin-giyim-x-g1-c82",
        },
        {
            "name": "Erkek Giyim",
            "slug": "erkek-giyim",
            "link": "/erkek-giyim-x-g2-c82",
        },
        {
            "name": "Çocuk Giyim",
            "slug": "cocuk-giyim",
            "link": "/cocuk-giyim-x-g3-c82",
        },
    ]

    def get_products_api(self, link, page=0):
        url = (
            "https://public.trendyol.com/discovery-web-searchgw-service/v2/api/infinite-scroll"
            + link
        )
        if page != 0:
            return url + f"?pi={page}"
        return url

    def get_products_group_api(self, id):
        return f"https://public.trendyol.com/discovery-web-websfxproductgroups-santral/api/v1/product-groups/{id}"

    def get_product_api(self, id):
        return f"https://public.trendyol.com/discovery-web-productgw-service/api/productDetail/{id}?linearVariants=true"

    def get_reccomendations_api(self, id, link):
        return f"https://public-mdc.trendyol.com/discovery-web-websfxproductrecommendation-santral/api/v1/product/{id}{link}?size=20&version=1&page=0"

    def get_product_reviews_api(self, id, page, size=10):
        return f"https://public-mdc.trendyol.com/discovery-web-socialgw-service/api/review/{id}?pageSize={size}&page={page}"
