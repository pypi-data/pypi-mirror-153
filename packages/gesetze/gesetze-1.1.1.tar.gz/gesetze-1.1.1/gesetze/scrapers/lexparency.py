from os.path import exists
import re
import time

from .scraper import Scraper
from ..utils import dump_json


class Lexparency(Scraper):
    """
    Utilities for scraping 'lexparency.de'
    """

    # Individual identifier
    identifier: str = 'lexparency'


    def scrape(self, output_file: str, wait: int = 2) -> None:
        """
        Scrapes 'lexparency.de' for legal norms

        :param output_file: str Path to merged data file
        :param wait: int Time to wait before scraping next law

        :return: None
        """

        # Fetch overview page
        html = self.get_html('https://lexparency.de')

        # Create list of data files
        data_files = []

        # Parse their HTML & iterate over `a` tags ..
        for link in self.bs(html).select('#featured-acts')[0].select('a'):
            # .. extracting data for each law
            law = link.text.strip()

            # Determine abbreviation
            match = re.match(r'.*\((.*)\)$', law)

            # If abbreviation was found ..
            if match:
                # .. store it as shorthand for current law
                law = match.group(1)

            # Define data file for current law
            data_file = self.md5_file(self.dir, law)

            # If it already exists ..
            if exists(data_file):
                # (1) .. update list of data files
                data_files.append(data_file)

                # (2) .. skip law
                continue

            slug = link['href'][4:]

            # .. collecting its information
            node = {
                'law': law,
                'slug': slug,
                'title': '',
                'headings': {},
            }

            # Fetch index page for each law
            law_html = self.get_html('https://lexparency.de/eu/{}'.format(slug))

            # Get title
            # (1) Create empty list
            title = []

            # (2) Convert first character of second entry (= 'title essence') to lowercase
            for i, string in enumerate(list(self.bs(law_html).select('h1')[0].stripped_strings)):
                if i == 1:
                    string = string[:1].lower() + string[1:]

                title.append(string)

            # (3) Create title from strings
            node['title'] = ' '.join(title).strip()

            # Iterate over `li` tags ..
            for heading in self.bs(law_html).select('#toccordion')[0].find_all('li', attrs={'class': 'toc-leaf'}):
                # (1) .. skipping headings without `a` tag child
                if not heading.a:
                    continue

                # (2) .. skipping headings without `href` attribute in `a` tag child
                if not heading.a.get('href'):
                    continue

                string = heading.text.replace('—', '-')

                # Determine section identifier
                match = re.match(r'(?:§+|Art|Artikel)\.?\s*(\d+(?:\w\b)?)', string, re.IGNORECASE)

                # If section identifier was found ..
                if match:
                    # .. store identifier as key and heading as value
                    node['headings'][match.group(1)] = string.replace('§  ', '§ ')

                # .. otherwise ..
                else:
                    # .. store heading as both key and value
                    node['headings'][string] = string

            # Store data record
            # (1) Write data to JSON file
            dump_json(node, data_file)

            # (2) Update list of data files
            data_files.append(data_file)

            # Wait for it ..
            time.sleep(wait)

        # Merge data files
        self.build(data_files, output_file)
