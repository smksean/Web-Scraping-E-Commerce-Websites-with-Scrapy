from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import os
from csv import writer

class BeveragesScraper(CrawlSpider):
    name = "beverages_scraper"
    start_urls = ["https://healthplusnigeria.com/collections/beverages"]

    rules = (
        Rule(LinkExtractor(restrict_css='a.product-item__title'), callback='parse_product', follow=True),
    )

    def parse_product(self, response):
        # Extract product data
        product_item = {
            "image_url": response.urljoin(response.css("img.product-gallery__image::attr(src)").get()),
            "title": response.css("h1.product-meta__title::text").get(),
            "price": self.extract_price(response),
            "url": response.url
        }
        
        # Save the data to CSV
        self.save_to_file(product_item["image_url"], product_item["title"], product_item["price"], product_item["url"])
        return product_item

    def extract_price(self, response):
        # Extract price after "Price:" label
        price_label = response.css("span.product-form__info-title.text--strong::text").get()
        if price_label and "Price:" in price_label:
            price = response.css("span.price::text").get()
            return price.strip().replace('₦', '').replace(' NGN', '') if price else None
        return None

    def save_to_file(self, image_url, title, price, url):
        # Save the scraped data to a CSV file
        file_exists = os.path.isfile("beverages_data.csv")
        with open("beverages_data.csv", "a" if file_exists else "w", newline='', encoding="utf-8") as f_object:
            writer_object = writer(f_object)
            if not file_exists:
                writer_object.writerow(["Image URL", "Title", "Price", "URL"])  # Add header if file doesn't exist
            writer_object.writerow([image_url, title, price, url])

