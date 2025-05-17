from pathlib import Path

import scrapy
from urllib.parse import urlparse
import html2text # For markdown conversion

class ShopSpider(scrapy.Spider):
    name = "shop_spider"

    # You can provide start_urls here, or pass them via command line:
    # scrapy crawl shop_spider -a urls="http://example.com/product,http://another.com/item"
    # Example URLs for testing different parsers:
    # start_urls = [
    #     "https://www.mouser.com/ProductDetail/Texas-Instruments/LM358ADR?qs=sGAEpiMZZMtQ4%2FzC62gV75V9Nq2hCj2B",
    #     "https://www.digikey.com/en/products/detail/texas-instruments/LM358DR/277374",
    #     "https://www.ti.com/product/LM358" # Example for 'other'
    # ]

    def __init__(self, urls=None, *args, **kwargs):
        super(ShopSpider, self).__init__(*args, **kwargs)
        if urls:
            self.start_urls = urls.split(',')
        elif not getattr(self, 'start_urls', None):
            # Fallback if no URLs are provided via CLI or in the class
            self.start_urls = [] 
            self.logger.warning("No start_urls provided for the spider.")


    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        domain = urlparse(response.url).netloc.lower()
        """
        Mouser scraping is currently not working, so we skip it for now and only rely on digikey

        if "mouser.com" in domain:
            return self.parse_mouser(response)"""

        if "digikey.com" in domain:
            return self.parse_digikey(response)
        else:
            return self.parse_other(response)

    def parse_mouser(self, response):
        self.logger.info(f"Parsing Mouser URL: {response.url}")
        item = {'url': response.url, 'source': 'mouser'}

        # Pricing Information from table: //*[@id="pdpPricingAvailability"]/div[2]/div[3]
        # This usually contains a table with id "pdp-pricing-table"
        pricing_data = []
        pricing_rows = response.xpath('//table[@id="pdp-pricing-table"]/tbody/tr')
        for row in pricing_rows:
            quantity = "".join(row.xpath('./td[1]//text()').getall()).strip()
            unit_price = "".join(row.xpath('./td[2]//text()').getall()).strip()
            if quantity and unit_price:
                pricing_data.append({"quantity": quantity, "unit_price": unit_price})
        item['pricing'] = pricing_data

        # Specification Information from table: //*[@id="formProductSpecs"]
        # This form contains a div with id="specs" which has the table
        specifications = {}
        spec_rows = response.xpath('//div[@id="specs"]//table/tbody/tr')
        for row in spec_rows:
            key_elements = row.xpath('./th//text() | ./td[1]//text()').getall()
            value_elements = row.xpath('./td[last()]//text()').getall()
            key = "".join(key_elements).strip().replace(':', '')
            value = "".join(value_elements).strip()
            if key and value:
                specifications[key] = value
        item['specifications'] = specifications

        # Datasheet link: //*[@id="collapseDocuments"]/div/div[2]/div[2]/div/ul/li/a
        datasheet_url = response.xpath('//*[@id="collapseDocuments"]//a[contains(translate(@href, "DATASHEET", "datasheet"), "datasheet") or contains(translate(@href, ".PDF", ".pdf"), ".pdf")]/@href').get()
        if datasheet_url:
            item['datasheet_link'] = response.urljoin(datasheet_url)
        else: # Fallback if specific XPath fails
            doc_links = response.xpath('//*[@id="collapseDocuments"]//a/@href').getall()
            for link in doc_links:
                if 'datasheet' in link.lower() or link.lower().endswith('.pdf'):
                    item['datasheet_link'] = response.urljoin(link)
                    break
        
        yield item

    def parse_digikey(self, response):
        self.logger.info(f"Parsing Digi-Key URL: {response.url}")
        item = {'url': response.url, 'source': 'digikey'}

        # Attributes from table: <table class="MuiTable-root mui-css-1ssfo" id="product-attributes">
        attributes = {}
        # Debug: Print the HTML elements found by xpath
        attribute_rows = response.xpath('//table[@id="product-attributes"]/tbody/tr')
        self.logger.debug(f"Found attribute rows HTML: {attribute_rows.get()}")
        for row in attribute_rows:
            key = "".join(row.xpath('./th//text()').getall()).strip()
            value = "".join(row.xpath('./td//text()').getall()).strip()
            if key and value:
                attributes[key] = value
        item['attributes'] = attributes

        # In-stock information
        # Try to find "Quantity Available" or "In Stock" text.
        # This is an estimate, Digikey's structure can vary.
        quantity_available_text = response.xpath('//td[contains(text(),"Quantity Available")]/following-sibling::td/span/text()').get()
        if not quantity_available_text: # Fallback
            quantity_available_text = response.xpath('//div[contains(@class, "pdp-product-availability")]//span[contains(text(), "In Stock")]/text()').get()
        if not quantity_available_text and "Quantity Available" in attributes:
             quantity_available_text = attributes["Quantity Available"]

        item['in_stock'] = quantity_available_text.strip() if quantity_available_text else "Not found"
        
        # Pricing information: //*[@id="__next"]/div/main/div/div/div[1]/div[2]/div/div/div[4]
        # This div contains the pricing table.
        pricing_data = []
        # Look for a table within the pricing section; class names might vary.
        pricing_rows = response.xpath('//div[contains(@class,"PriceAndAvailability")]//table/tbody/tr[td[2]] | //div[contains(@data-testid, "price-and-procure")]//table/tbody/tr[td[2]]')
        for row in pricing_rows:
            quantity = "".join(row.xpath('./td[1]//text()').getall()).strip()
            unit_price = "".join(row.xpath('./td[2]//text()').getall()).strip()
            # Filter out header or non-price rows
            if quantity and unit_price and quantity.replace(',','').isdigit():
                pricing_data.append({"quantity": quantity, "unit_price": unit_price})
        item['pricing'] = pricing_data

        # Datasheet: //*[@id="__next"]/div/main/div/div/div[1]/div[4]/div/div[2]/table/tbody/tr[1]/td[2]/a
        # Make it more robust by looking for "Datasheets" text in the table row.
        datasheet_url = response.xpath('//table[contains(@class, "MuiTable-root")]//tr[contains(./td[1]//text(), "Datasheets")]/td[2]//a/@href').get()
        if not datasheet_url: # Fallback
            datasheet_url = response.xpath('//a[.//span[contains(text(),"Datasheet")] or contains(text(),"Datasheet")][@href]/@href').get()
        if datasheet_url:
            item['datasheet_link'] = response.urljoin(datasheet_url)
        
        yield item

    def parse_other(self, response):
        pass 
        """
        self.logger.info(f"Parsing other URL: {response.url}")
        item = {'url': response.url, 'source': 'other'}

        # Convert content to Markdown
        h = html2text.HTML2Text()
        h.ignore_links = False # Keep links to find datasheets
        h.ignore_images = True
        h.body_width = 0 # No wrap
        try:
            markdown_content = h.handle(response.text)
        except Exception as e:
            self.logger.error(f"Error converting HTML to Markdown for {response.url}: {e}")
            markdown_content = "Error converting content."
        item['markdown_content'] = markdown_content

        # Search for datasheet links
        datasheet_links_found = []
        for link_tag in response.css('a[href]'):
            href = link_tag.attrib.get('href', '')
            link_text = "".join(link_tag.css('::text').getall()).lower()
            
            if href and (
                ".pdf" in href.lower() or 
                "datasheet" in href.lower() or 
                "data-sheet" in href.lower() or
                "datasheet" in link_text or
                "data-sheet" in link_text
            ):
                datasheet_links_found.append(response.urljoin(href))
        
        item['datasheet_links'] = list(set(datasheet_links_found)) # Unique links
        
        yield item"""
        