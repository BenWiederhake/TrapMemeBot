#!/bin/false

import logging
import os
import secrets

logger = logging.getLogger(__name__)


def readall(filename):
    with open(filename, 'rb') as fp:
        return fp.read()


def writeall(filename, data):
    with open(filename, 'wb') as fp:
        return fp.write(data)


class Storage:
    def __init__(self):
        # Run some startup-tests:
        assert readall('trap_pics/.TRAP_PICS') == b'RIGHT HERE\n', 'Wrong working directory?'
        assert readall('trap_pics/suggested/.keep') == b'', 'Wrong working directory?'
        assert readall('trap_pics/accepted/.keep') == b'', 'Wrong working directory?'

        # Read which files exist:
        self.suggested = set(os.listdir('trap_pics/suggested/'))
        self.accepted = set(os.listdir('trap_pics/accepted/'))

        # Filter organizational files:
        self.suggested.remove('.keep')
        self.accepted.remove('.keep')

        logger.info(f'Found {len(self.suggested)} suggested and {len(self.accepted)} memes.')
        assert len(self.accepted) > 0, 'There must be an initially-accepted meme.'

    def fetch_random_suggested(self):
        raise NotImplementedError()

    def fetch_random_accepted(self):
        return f'trap_pics/accepted/{secrets.choice(list(self.accepted))}'

    def do_suggest(self, hexname):
        self.suggested.add(hexname)

    def do_accept(self, name):
        raise NotImplementedError()

    def do_reject(self, meme):
        raise NotImplementedError()

    def len_suggested(self):
        return len(self.suggested)

    def len_accepted(self):
        return len(self.accepted)
