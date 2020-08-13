from simple_entry import SimpleEntry
from store_provider import StoreProvider
import libkeepass
from session import Session
import logging
import sys
import getpass


class KeepassStore(StoreProvider):
    def __init__(self, kee_pass_file, clear_session=False):
        self.session = Session('keepass_key', 'keepass_session')
        if clear_session:
            self.session.clear()
        self.session.load()
        self.entries = None
        self.kee_pass_file = kee_pass_file
        try:
            with open(self.kee_pass_file) as f:
                f.read()
        except IOError as ex:
            logging.error('failed to open keepass file' + str(kee_pass_file))
            raise ex

    def _session_is_established(self):
        if self.session.session is None or self.session.session == '':
            return False

        return True

    def ensure_session_and_load_cache(self):
        while not self._session_is_established():
            try:
                self.session.session = getpass.getpass(
                    'Please enter your password for file: ' + str(self.kee_pass_file) + ": ")
                with libkeepass.open(self.kee_pass_file, password=self.session.session) as kpdb:
                    self.session.write()
                    self.entries = []
                    for kpEntry in kpdb.obj_root.findall('.//Entry'):
                        simple_entry = SimpleEntry(None, [], None)
                        for s in kpEntry.findall('./String'):
                            key = s.find('./Key').text
                            val = s.find('./Value').text
                            if val is not None and val != '':
                                if key == 'URL':
                                    simple_entry.addresses.append(val)
                                elif key == 'Password':
                                    simple_entry.password = val
                                elif key == 'Title':
                                    simple_entry.name = val
                        if simple_entry.name is not None and simple_entry.password is not None:
                            self.entries.append(simple_entry)
            except CredentialsError as e:
                print 'wrong password'
                self.session.session = ''
            except:
                print "Unexpected error:", sys.exc_info()[0]
                raise

    def get_and_cache_simple_entries(self):
        self.ensure_session_and_load_cache()
        return self.entries

    def get_items(self):
        pass
