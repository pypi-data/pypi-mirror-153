#   -*- coding: utf-8 -*-
import re
import logging
from queue import Empty
from time import sleep

from mpmq import MPmq

from .terminal import Terminal

logger = logging.getLogger(__name__)


class MP4ansi(MPmq):
    """ a subclass of MPmq providing multi-processing (MP) capabilities for a simple ANSI terminal
        setup simple ANSI terminal for all processes to be executed
        write log messages from executing functions to respective lines on ANSI terminal
        add ability to represent execution using progress bar
    """
    def __init__(self, *args, **kwargs):
        logger.debug('executing MP4ansi constructor')
        config = kwargs.pop('config', None)
        # call parent constructor
        super(MP4ansi, self).__init__(*args, **kwargs)
        self.terminal = Terminal(len(self.process_data), config=config, durations=self.finished_processes)

    def get_message(self):
        """ return message from top of message queue
            override parent class method
        """
        message = super(MP4ansi, self).get_message()
        if message['offset'] is None:
            # parse offset from the message
            match = re.match(r'^#(?P<offset>\d+)-(?P<message>.*)$', message['message'], re.M)
            if match:
                return {
                    'offset': int(match.group('offset')),
                    'control': None,
                    'message': match.group('message')
                }
            else:
                logger.debug(f'unable to match offset in message {message}')
        return message

    def process_non_control_message(self, offset, message):
        """ write message to terminal at offset
            override parent class method
        """
        if offset is None:
            logger.warn(f'unable to write {message} line to terminal because offset is None')
            return
        if message == 'RESET':
            # implement ability to reset index
            self.terminal.reset(offset)
        else:
            self.terminal.write_line(offset, message)

    def execute_run(self):
        """ write data to terminal and hide cursor
            override parent class method
        """
        logger.debug('executing run task wrapper')
        self.terminal.hide_cursor()
        self.terminal.write_lines()
        # call parent method
        super(MP4ansi, self).execute_run()

    def final(self):
        """ write data to terminal and show cursor
            override parent class method
        """
        logger.debug('executing final task')
        self.terminal.write_lines(add_duration=True, force=True)
        self.terminal.show_cursor()
