from os.path import dirname, exists, realpath
from abc import ABC, abstractmethod
from typing import Optional

from ..helpers import analyze
from ..utils import load_json


class Driver(ABC):
    """
    Utilities for dealing with providers
    """

    # Individual identifier
    identifier: Optional[str] = None


    def __init__(self, file: Optional[str] = None) -> None:
        """
        Creates 'Driver' instance

        :param file: str Path to (custom) data file

        :raises: Exception Invalid law
        """

        # Set default index file
        if file is None:
            file = '{}/../data/{}.json'.format(dirname(__file__), self.identifier)

        # Fail early if file does not exist
        if not exists(file):
            raise Exception('File does not exist: "{}"'.format(realpath(file)))

        # Load law library data
        self.library = load_json(file)


    def validate(self, string: str) -> bool:
        # Fail early when string is empty
        if not string:
            return False

        # Analyze legal norm
        data = analyze(string)

        # Get lowercase identifier for current law
        identifier = data['gesetz'].lower()

        # Fail early if law is unavailable
        if identifier not in self.library:
            # .. fail early
            return False

        # Return whether current law contains norm
        return data['norm'] in self.library[identifier]['headings']


    def build_title(self, data: dict, mode: str) -> str:
        """
        Builds description for corresponding legal norm (used as `title` attribute)

        :param data: dict Legal data
        :param mode: str Output mode, either 'light', 'normal' or 'full' (default: False)

        :return: str Title attribute
        :raises: Exception Invalid law
        """

        # Get lowercase identifier for current law
        identifier = data['gesetz'].lower()

        # Fail early if law is unavailable
        if identifier not in self.library:
            raise Exception('Invalid law: "{}"'.format(data['gesetz']))

        # Get data about current law
        law = self.library[identifier]

        # Determine `title` attribute
        if mode == 'light':
            return law['law']

        if mode == 'normal':
            return law['title']

        if mode == 'full':
            return law['headings'][data['norm']]

        return ''


    @abstractmethod
    def build_url(self, data: dict) -> str:
        """
        Builds URL for corresponding legal norm (used as `href` attribute)

        :param data: dict Legal data

        :return: str Target URL
        """

        pass
