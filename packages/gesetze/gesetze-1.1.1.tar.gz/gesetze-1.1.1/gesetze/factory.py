from .drivers import *


class Factory:
    """
    Utilities for creating 'Driver' instances
    """

    # List available drivers
    drivers: dict = {
        # (1) 'gesetze-im-internet.de'
        'gesetze': GesetzeImInternet,
        # (2) 'dejure.org'
        'dejure': DejureOnline,
        # (3) 'buzer.de'
        'buzer': Buzer,
        # (4) 'lexparency.de'
        'lexparency': Lexparency,
    }


    def create(self, driver: str) -> Driver:
        """
        Creates a new 'Driver' instance for the given type

        :param driver: str Driver type

        :return: Driver Driver instance
        :raises: Exception Invalid driver type
        """

        # Fail early for invalid drivers
        if driver not in self.drivers:
            raise Exception('Invalid driver type: "{}"'.format(driver))

        # Instantiate object
        return self.drivers[driver]()
