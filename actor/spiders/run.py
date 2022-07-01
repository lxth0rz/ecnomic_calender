import json
import re
import os
import apify
import logging
from scrapy import Spider
from urllib.parse import urljoin
from apify_client import ApifyClient
from scrapy.http.request import Request


class economic_calender(Spider):

    name = 'economic_calender'

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
               'Accept-Language': 'en-US,en;q=0.5',
               'Upgrade-Insecure-Requests': '1',
               'Sec-Fetch-Dest': 'document',
               'Sec-Fetch-Mode': 'navigate',
               'Sec-Fetch-Site': 'none',
               'Sec-Fetch-User': '?1',}

    logger = None

    directory_path = os.getcwd()

    env = os.getenv("SCRAPY_ENV")

    input_url = 'https://www.dailyfx.com/economic-calendar'

    def start_requests(self):

        self.logger = logging.getLogger()

        if self.env is None:

            # Initialize the main ApifyClient instance
            client = ApifyClient(os.environ['APIFY_TOKEN'], api_url=os.environ['APIFY_API_BASE_URL'])

            # Get the resource subclient for working with the default key-value store of the actor
            default_kv_store_client = client.key_value_store(os.environ['APIFY_DEFAULT_KEY_VALUE_STORE_ID'])

        yield Request(url=self.input_url,
                      callback=self.parse_overview_page)

    def parse_overview_page(self, response):

        data = re.findall('dataProvider,\n(\[\{.+"}])', response.text)
        if data and len(data) > 0:
            data = data[0].strip()
            data = json.loads(data)
            data = data[::-1]

            for d in data:
                yield d