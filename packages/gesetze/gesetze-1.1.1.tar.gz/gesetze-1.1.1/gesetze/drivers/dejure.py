from .driver import Driver


class DejureOnline(Driver):
    """
    Utilities for dealing with 'dejure.org'
    """

    # Individual identifier
    identifier: str = 'dejure'


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
        url = 'https://dejure.org/gesetze'

        # Set HTML file
        file = '{}.html'.format(data['norm'])

        # Combine everything
        return '{}/{}/{}'.format(url, self.library[identifier]['slug'], file)
