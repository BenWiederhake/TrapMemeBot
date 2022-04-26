#!/bin/false

import hashlib
import logging
import os

logger = logging.getLogger(__name__)


def readall(filename):
    with open(filename, 'rb') as fp:
        return fp.read()


def writeall(filename, data):
    with open(filename, 'wb') as fp:
        return fp.write(data)


def check_hash(filename):
    logger.info(f'FIXME: Not actually checking {filename} D:')  # FIXME


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

        # Check that all files have valid SHA256 sums:
        logger.info(f'Found {len(self.suggested)} suggested memes. Checking consistency ...')
        for filename in self.suggested:
            check_hash(filename)
        logger.info(f'Success. Found {len(self.accepted)} accepted memes. Checking consistency ...')
        for filename in self.accepted:
            check_hash(filename)
        logger.info(f'Success. We are good to go!')
        assert len(self.accepted) > 0, 'There must be an initially-accepted meme.'

    def meme_fetch_random(self):
        raise NotImplementedError()

    def meme_suggest(self, img):
        raise NotImplementedError()

    def meme_accept(self, name):
        raise NotImplementedError()

    def meme_reject(self, meme):
        raise NotImplementedError()
