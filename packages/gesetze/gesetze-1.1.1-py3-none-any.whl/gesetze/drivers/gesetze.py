from .driver import Driver


class GesetzeImInternet(Driver):
    """
    Utilities for dealing with 'gesetze-im-internet.de'
    """

    # Individual identifier
    identifier: str = 'gesetze'


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
        url = 'https://www.gesetze-im-internet.de'

        # Set default HTML file
        file = '__{}.html'.format(data['norm'])

        # Except for the 'Grundgesetz' ..
        if identifier == 'gg':
            # .. which is different
            file = 'art_{}.html'.format(data['norm'])

        # Combine everything
        return '{}/{}/{}'.format(url, self.library[identifier]['slug'], file)
