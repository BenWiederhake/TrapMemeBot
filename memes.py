#!/bin/false

import logging
import os
import secrets

logger = logging.getLogger(__name__)


def readall(filename):
    with open(filename, 'rb') as fp:
        return fp.read()


def strip_extension(filename):
    if filename.endswith('.jpg'):
        filename = filename[:-len('.jpg')]
    return filename


class Storage:
    def __init__(self):
        # Run some startup-tests:
        assert readall('trap_pics/.TRAP_PICS') == b'RIGHT HERE\n', 'Wrong working directory?'
        assert readall('trap_pics/suggested/.keep') == b'', 'Wrong working directory?'
        assert readall('trap_pics/accepted/.keep') == b'', 'Wrong working directory?'

        # Read which files exist:
        self.suggested = set(strip_extension(e) for e in os.listdir('trap_pics/suggested/'))
        self.accepted = set(os.listdir('trap_pics/accepted/'))

        # Filter organizational files:
        self.suggested.remove('.keep')
        self.accepted.remove('.keep')

        logger.info(f'Found {len(self.suggested)} suggested and {len(self.accepted)} memes.')
        assert len(self.accepted) > 0, 'There must be an initially-accepted meme.'

    def fetch_random_suggested(self):
        raise NotImplementedError()  # FIXME

    def fetch_random_accepted(self):
        return f'trap_pics/accepted/{secrets.choice(list(self.accepted))}'

    def do_suggest(self, hexname):
        self.suggested.add(hexname)

    def do_accept(self, name):
        if name not in self.suggested:
            return 'Not in suggested anymore'
        try:
            os.rename(f'trap_pics/suggested/{name}.jpg', f'trap_pics/accepted/{name}.jpg')
        except FileNotFoundError:
            return f'File not found: trap_pics/suggested/{name}.jpg'

        self.suggested.remove(name)
        self.accepted.add(f'{name}.jpg')

    def do_reject(self, name):
        if name not in self.suggested:
            return 'Not in suggested anymore'
        try:
            os.remove(f'trap_pics/suggested/{name}.jpg')
        except FileNotFoundError:
            return f'File not found: trap_pics/suggested/{name}.jpg'

        self.suggested.remove(name)

    def len_suggested(self):
        return len(self.suggested)

    def len_accepted(self):
        return len(self.accepted)
