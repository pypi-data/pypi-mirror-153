from typing import Union

from .driver import Driver


class Buzer(Driver):
    """
    Utilities for dealing with 'buzer.de'
    """

    # Individual identifier
    identifier: str = 'buzer'


    def build_title(self, data: dict, mode: Union[bool, str]) -> str:
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
            return law['headings'][data['norm']['text']]

        return ''


    def build_url(self, data: dict) -> str:
        """
        Builds URL for corresponding legal norm (used as `href` attribute)

        :param data: dict Legal data

        :return: str Target URL
        :raises: Exception Invalid law
        """

        # Get lowercase identifier for current law
        identifier = data['gesetz'].lower()

        # Fail early if law is unavailable
        if identifier not in self.library:
            raise Exception('Invalid law: "{}"'.format(data['gesetz']))

        # Set base URL
        url = 'https://buzer.de'

        # Set HTML file
        file = self.library[identifier]['headings'][data['norm']]['slug']

        # Combine everything
        return '{}/{}'.format(url, file)
