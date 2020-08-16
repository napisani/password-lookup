from provider.simple_entry import SimpleEntry
from provider.store_provider import StoreProvider
import subprocess
import json
import logging
import os
from provider.session import Session
import getpass

SESSION_KEY = 'BW_SESSION'


def get_session():
    """
    Function to return a valid Bitwarden session
    """
    # Check for an existing, user-supplied Bitwarden session
    try:
        if os.environ[SESSION_KEY]:
            logging.debug('Existing Bitwarden session found')
            return os.environ[SESSION_KEY]
    except KeyError:
        pass

    # Check if we're already logged in
    proc = subprocess.Popen(
        [
            'bw',
            'login',
            '--check',
            '--quiet'
        ]
    )
    proc.wait()

    if proc.returncode:
        logging.debug('Not logged into Bitwarden')
        operation = 'login'
        credentials = ["{}".format(input('Bitwarden user: '))]
    else:
        logging.debug('Bitwarden vault is locked')
        operation = 'unlock'
        credentials = []

    # Ask for the password
    pw = getpass.getpass('Bitwarden Vault password: ')
    credentials.append("{}".format(pw))

    logging.debug(list(filter(None, [
        'bw',
        '--raw',
        '--nointeraction',
        operation
    ] + credentials)))

    proc = subprocess.Popen(
        list(filter(None, [
            'bw',
            '--raw',
            '--nointeraction',
            operation
        ] + credentials)),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    (stdout, stderr) = proc.communicate()

    if proc.returncode:
        logging.error(stderr.decode('utf-8'))
        return None

    return stdout.decode('utf-8')


def run_bw_command(args):
    cmd = ['bw']
    cmd.extend(args)
    logging.debug('full cmd {}'.format(cmd))
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE
    )

    (stdout, _) = proc.communicate()

    if proc.returncode:
        raise RuntimeError('Unable to exec Bitwarden CLI ')

    return stdout.decode('utf-8')


def get_bw_status(session_id):
    return json.loads(run_bw_command(['status', '--session', session_id]))['status']


def build_simple_entries(items):
    entries = []
    for item in items:
        se = SimpleEntry(item['name'], [], '')
        try:
            se.addresses = list(filter(lambda x: x is not None, map(lambda entry: entry['uri'], item['login']['uris'])))
        except:
            se.addresses = []
        try:
            se.password = item['login']['password']
        except:
            continue

        entries.append(se)
    return entries


class BitwardenStore(StoreProvider):
    def __init__(self, clear_session=False):
        self.session = Session('bw_key', 'bw_session')
        if clear_session:
            self.session.clear()
        self.session.load()
        self.entries = None

    def get_and_cache_simple_entries(self):
        if self.entries:
            return self.entries
        self.entries = build_simple_entries(self.get_items())
        return self.entries

    def ensure_session(self):
        try:
            if get_bw_status(self.session.session) == 'unlocked':
                return
        except:
            pass
        session_id = get_session()
        while not session_id:
            logging.error('session id could not be established please try again')
            session_id = get_session()
        logging.debug('setting up session')
        self.session.set(session_id)
        self.session.write()

    def get_bw_version(self):
        print(run_bw_command(['--version']))

    def get_items(self):
        self.ensure_session()
        return json.loads(run_bw_command(['list', 'items', '--session', self.session.session]))
