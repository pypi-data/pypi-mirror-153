from os import getcwd
from os.path import exists
from abc import ABC, abstractmethod
from hashlib import md5
from shutil import rmtree
from typing import Optional

from requests import get
from bs4 import BeautifulSoup

from ..utils import create_path, dump_json, load_json


class Scraper(ABC):
    """
    Utilities for scraping providers
    """

    # Individual identifier
    identifier: Optional[str] = None


    def __init__(self, path: str) -> None:
        """
        Initializes download directory

        :param path: str Path to directory

        :return: None
        """

        # Create data directory
        # (1) Define its path
        self.dir = '{}/.{}'.format(path, self.identifier)

        # (2) Create (if necessary)
        create_path(self.dir)


    def hash(self, file: str) -> str:
        """
        Creates hashed filename

        :param file: str Filename

        :return: str Hash
        """

        return md5(file.encode('utf-8')).hexdigest()


    def get_html(self, url: str) -> str:
        """
        Fetches HTML of given URL

        :param url: str Target URL

        :return: str Target HTML
        """

        file = '{}/{}.html'.format(self.dir, self.hash(url))

        if not exists(file):
            html = get(url).text

            with open(file, 'w') as html_file:
                html_file.write(html)

        else:
            with open(file, 'r') as html_file:
                html = html_file.read()

        return html


    def bs(self, html: str) -> BeautifulSoup:
        """
        Converts HTML to 'BeautifulSoup' object

        :param html: str Target HTML

        :return: bs4.BeautifulSoup 'BeautifulSoup' object
        """

        return BeautifulSoup(html, 'lxml')


    def md5_file(self, path: str, file: str) -> str:
        """
        Determines hashed JSON data file

        :param path: str Data directory
        :param file: str Filename for corresponding law

        :return: str Path to data file
        """

        return '{}/{}.json'.format(path, self.hash(file))


    def build(self, data_files: list, output_file: Optional[str] = None) -> None:
        """
        Merges JSON files & removes them afterwards

        :param data_files: list List of data files
        :param output_file: str Path to merged data file

        :return: None
        """

        # Create data buffer
        data = {}

        # Iterate over data files
        for data_file in data_files:
            # Load data & update data buffer
            node = load_json(data_file)
            data[node['law'].lower()] = node

        # if target file not specified ..
        if output_file is None:
            # .. use current working directory & identifier as fallback
            output_file = '{}/{}.json'.format(getcwd(), self.identifier)

        # Write complete dataset to JSON file
        dump_json(data, output_file)

        # Remove temporary files
        rmtree(self.dir)


    @abstractmethod
    def scrape(self, output_file: str, wait: int = 2) -> None:
        """
        Scrapes website for legal norms

        :param output_file: str Path to merged data file
        :param wait: int Time to wait before scraping next law

        :return: None
        """

        pass
