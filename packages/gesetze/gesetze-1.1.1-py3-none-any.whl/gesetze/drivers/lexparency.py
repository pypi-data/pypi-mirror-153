from .driver import Driver


class Lexparency(Driver):
    """
    Utilities for dealing with 'lexparency.de'
    """

    # Individual identifier
    identifier: str = 'lexparency'


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
        url = 'https://lexparency.de/eu'

        # Set HTML file
        file = 'ART_{}'.format(data['norm'])

        # Combine everything
        return '{}/{}/{}'.format(url, self.library[identifier]['slug'], file)
