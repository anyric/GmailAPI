
from __future__ import print_function
import os
import httplib2

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
URL = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_ID = 'ClientID.json'
APP_NAME = 'Gmail API'


def get_ids():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    ids_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(ids_dir):
        os.makedirs(ids_dir)
    id_path = os.path.join(ids_dir, 'ClientID.json')

    store = Storage(id_path)
    ids = store.get()
    if not ids or ids.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_ID, URL)
        flow.user_agent = APP_NAME
        if flags:
            ids = tools.run_flow(flow, store, flags)
        else: 
            ids = tools.run(flow, store)
    return ids

def main():
    """Shows usage of the Gmail API to obtain lebels of user gmail account.

    """
    ids = get_ids()
    http = ids.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    results = service.users().labels().list(userId='me').execute()
    labelnames = results.get('labels', [])

    if not labelnames:
        print('No labels found.')
    else:
      print('Labels:')
      for name in labelnames:
        print(name['name'])


if __name__ == '__main__':
    main()