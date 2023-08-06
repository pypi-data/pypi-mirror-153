from os.path import exists
import re
import time

from .scraper import Scraper
from ..utils import dump_json


class Buzer(Scraper):
    """
    Utilities for scraping 'buzer.de'
    """

    # Individual identifier
    identifier: str = 'buzer'


    def scrape(self, output_file: str, wait: int = 2) -> None:
        """
        Scrapes 'buzer.de' for legal norms

        :param output_file: str Path to merged data file
        :param wait: int Time to wait before scraping next law

        :return: None
        """

        # Fetch overview page
        html = self.get_html('https://www.buzer.de')

        # Create list of data files
        data_files = []

        # Parse their HTML & iterate over `a` tags ..
        for link in self.bs(html).select('.table1')[0].select('a'):
            # .. extracting data for each law
            law = link.text.strip()

            # Define data file for current law
            data_file = self.md5_file(self.dir, law)

            # If it already exists ..
            if exists(data_file):
                # (1) .. update list of data files
                data_files.append(data_file)

                # (2) .. skip law
                continue

            slug = link['href']

            # .. collecting its information
            node = {
                'law': law,
                'slug': slug,
                'title': '',
                'headings': {},
            }

            # Fetch index page for each law
            law_html = self.get_html(slug)

            # Get title
            title = self.bs(law_html).select('h1')[0].text

            # Strip shorthand from title (if present)
            match = re.match(r'(.*)\s\(.*\)$', title)

            # If heading was found ..
            if match:
                # .. store it as title for current law
                title = match.group(1)

            node['title'] = title

            # Iterate over `li` tags ..
            for heading in self.bs(law_html).find_all('a', attrs={'class': 'preview'}):
                # .. skipping headings without `title` attribute
                if not heading.get('title'):
                    continue

                heading = {
                    'slug': heading['href'][1:],
                    'text': heading.text.replace('§  ', '§ '),
                }

                # Determine section identifier
                match = re.match(r'(?:§+|Art|Artikel)\.?\s*(\d+(?:\w\b)?)', heading['text'], re.IGNORECASE)

                # If section identifier was found ..
                if match:
                    # .. store identifier as key and heading as value
                    node['headings'][match.group(1)] = heading

                # .. otherwise ..
                else:
                    # .. store heading as both key and value
                    node['headings'][heading['text']] = heading

            # Store data record
            # (1) Write data to JSON file
            dump_json(node, data_file)

            # (2) Update list of data files
            data_files.append(data_file)

            # Wait for it ..
            time.sleep(wait)

        # Merge data files
        self.build(data_files, output_file)
