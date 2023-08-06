import re
import logging

from colorama import init as colorama_init
from colorama import Style
from colorama import Fore
from colorama import Back
from colorama import Cursor

logger = logging.getLogger(__name__)

MAX_CHARS = 120
FILL = 2


class StatusLine(object):
    """ Status Line implementation
    """

    def __init__(self, index, fill=None, regex=None):
        """ class constructor
        """
        logger.debug('executing StatusLine constructor')
        colorama_init()
        self.fill = StatusLine._get_fill(fill)
        if not regex:
            regex = {}
        self.text = ''
        self.regex = regex
        self.index = index
        self.duration = None

    def __str__(self):
        """ return string interpretation of class instance
        """
        index_fill = self.fill['index']
        bright_yellow = Style.BRIGHT + Fore.YELLOW + Back.BLACK
        index = f"{bright_yellow}{str(self.index).zfill(index_fill)}{Style.RESET_ALL}"
        text = self.text
        if self.duration:
            text = f'{text.strip()} - {self.duration}'
        return f"{index}: {text}"

    def reset(self):
        """ reset status line
        """
        pass

    def match(self, text):
        """ call match functions and return on first success
        """
        regex = self.regex.get('text')
        if regex:
            match = re.match(regex, text)
            if match:
                self.text = StatusLine._sanitize(text)
        else:
            self.text = StatusLine._sanitize(text)

    @staticmethod
    def _sanitize(text):
        """ sanitize text
        """
        if text:
            text = text.splitlines()[0]
            if len(text) > MAX_CHARS:
                text = f'{text[0:MAX_CHARS - 3]}...'
            else:
                text = text.ljust(MAX_CHARS)
        return text

    @staticmethod
    def _get_fill(data):
        """ return fill dictionary derived from data values
        """
        fill = {}
        if not data:
            fill['index'] = FILL
        else:
            fill['index'] = len(str(data.get('max_index', FILL * '-')))
        return fill
