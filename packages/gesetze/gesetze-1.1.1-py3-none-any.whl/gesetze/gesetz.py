import re
from typing import Callable, Optional, Union

from .factory import Factory
from .helpers import REGEX


class Gesetz:
    """
    Utilities for dealing with german legal norms
    """

    # Available providers
    drivers: dict = {}


    # Defines HTML attribute defaults
    attributes: dict = {'target': '_blank'}


    # Controls `title` attribute
    #
    # Possible values:
    #
    # 'light'  => abbreviated law (eg 'GG')
    # 'normal' => complete law (eg 'Grundgesetz')
    # 'full'   => official heading (eg 'Art 45d Parlamentarisches Kontrollgremium')
    title: Union[bool, str] = False


    def __init__(self, order: Union[list, str] = None) -> None:
        """
        Creates 'Gesetz' instance

        :param order: list | str Single driver OR list of drivers

        :return: None
        """

        # One regEx to rule them all
        self.regex = REGEX

        # Set default order
        if order is None:
            order = [
                'gesetze',     # 'gesetze-im-internet.de'
                'dejure',      # 'dejure.org'
                'buzer',       # 'buzer.de'
                'lexparency',  # 'lexparency.de'
            ]

        # If string was passed as order ..
        if isinstance(order, str):
            # .. make it a list
            order = [order]

        # Initialize drivers
        self.drivers = {driver: Factory().create(driver) for driver in order}


    def validate(self, string: str) -> bool:
        """
        Validates a single legal norm (across all providers)

        :param string: str Legal norm

        :return: bool Whether legal norm is valid (= linkable)
        """

        # Fail early when string is empty
        if not string:
            return False

        # Iterate over drivers
        for driver, obj in self.drivers.items():
            # If legal norm checks out ..
            if obj.validate(string):
                # .. break the loop
                return True

        return False


    def extract(self, string: str) -> list:
        """
        Extracts legal norms as list of strings

        :param string: str Text

        :return: list Extracted legal norms
        """

        return [match[0] for match in self.regex.finditer(string)]


    def linkify(self, match: re.Match) -> str:
        """
        Converts matched legal reference into `a` tag

        :param match: re.Match Matched legal norm

        :return: str Converted `a` tag
        """

        # Import dependencies
        from copy import deepcopy

        # Set `a` tag attribute defaults
        attributes = deepcopy(self.attributes)

        # Fetch extracted data
        string = match.group(0)
        data = match.groupdict()

        # Iterate over drivers for each match ..
        for driver, obj in self.drivers.items():
            # .. using only valid laws & legal norms
            if obj.validate(string):
                # Build `a` tag attributes
                # (1) Determine `href` attribute
                attributes['href'] = obj.build_url(data)

                # (2) Determine `title` attribute
                attributes['title'] = obj.build_title(data, self.title)

                # Abort the loop
                break

        # If `href` attribute is undefined ..
        if 'href' not in attributes:
            # .. return original string
            return string

        # Build `a` tag
        # (1) Format key-value pairs
        attributes = ['{}="{}"'.format(key, value) for key, value in attributes.items() if value]

        # (2) Combine everything
        return '<a {}>{}</a>'.format(' '.join(attributes), string)


    def markdownify(self, match: re.Match) -> str:
        """
        Converts matched legal reference into markdown link

        :param match: re.Match Matched legal norm

        :return: str Converted markdown link
        """

        # Fetch extracted data
        string = match.group(0)
        data = match.groupdict()

        # Set fallback
        link = None

        # Iterate over drivers for each match ..
        for driver, obj in self.drivers.items():
            # .. using only valid laws & legal norms
            if obj.validate(string):
                # Determine link
                link = obj.build_url(data)

                # Abort loop
                break

        # If link is undefined ..
        if not link:
            # .. return original string
            return string

        # Build markdown link
        return '[{}]({})'.format(string, link)


    def gesetzify(self, string: str, callback: Optional[Callable] = None) -> str:
        """
        Converts legal references throughout text into `a` tags

        :param string: str Text
        :param callback: typing.Callable Callback function

        :return: str Processed text
        """

        if callback is None:
            callback = self.linkify

        return self.regex.sub(callback, string)
