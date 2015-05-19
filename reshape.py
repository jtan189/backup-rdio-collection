#!/usr/bin/env python

# (c) 2011 Rdio Inc
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# include the parent directory in the Python path

from __future__ import unicode_literals

import sys,os.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import sh

from rdio import Rdio
from rdio_consumer_credentials import RDIO_CREDENTIALS, RDIO_TOKEN, GIT_REPO_PATH
try:
    from urllib.error import HTTPError
except ImportError:
    from urllib2 import HTTPError

# Fix for Python 2.X
try:
    input = raw_input
except NameError:
    pass

def update_collection(rdio):

    # get all tracks
    tracks = rdio.call('getTracksInCollection')['result']

    # save json as file
    tracks_path = os.path.join(GIT_REPO_PATH, 'tracks.json')
    with open(tracks_path, 'w') as json_file:
        json.dump(tracks, json_file, indent=4)

    git = sh.git.bake(_cwd=GIT_REPO_PATH)
    print git.add(tracks_path)
    print git.commit(m='Updating rdio collection.')
    print git.push()

if __name__ == "__main__":

    try:
        if '' in RDIO_TOKEN:

            # create an instance of the Rdio object with our consumer credentials
            rdio = Rdio(RDIO_CREDENTIALS)

            # authenticate against the Rdio service
            url = rdio.begin_authentication('oob')
            print('Go to: ' + url)
            verifier = input('Then enter the code: ').strip()
            rdio.complete_authentication(verifier)

        else:
            rdio = Rdio(RDIO_CREDENTIALS, RDIO_TOKEN)

    except HTTPError as e:
        # if we have a protocol error, print it
        print(e.read())
    
    update_collection(rdio)
