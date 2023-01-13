import logging
import os
import sys
from advisor import __version__
from advisor.helpers.version_comparer import VersionComparer
from zipfile import ZipFile

# Temp test bucket
DOWNLOAD_URL = ''
LATEST_VERSION_URL = ''

def main(argv=sys.argv[1:]):
    check_for_updates()


def check_for_updates():
    """Checks for latest version. Displays a message if new message is available.
    """
    if (is_newer_version_available()):
        print(f'New version of Porting Advisor for Graviton is available. Please download it at: {DOWNLOAD_URL}')

def is_newer_version_available():
    current_version = __version__
    latest_version = get_latest_version()
    return VersionComparer.is_valid(latest_version) and VersionComparer.compare(current_version, latest_version) == -1

def get_latest_version():
    """Gets latest version available

    Returns:
        str: The latest published version. Empty if it failed to get the latest version available.
    """
    try:
        return do_request(LATEST_VERSION_URL).decode('utf-8')
    except:
        logging.debug('Error while getting latest version.', exc_info=True)
        return ''

def do_request(request_url):
    """Executes an https request
    Returns:
        bytes: The latest version of the tool. None if it fails.
    """
    try:
        # if running as a binary, need to specify the path to the cacert.pem for requests to succeed
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            import certifi.core
            certifi.core.where = _get_cacert_pem()
            import requests.utils
            import requests.adapters
            requests.utils.DEFAULT_CA_BUNDLE_PATH = _get_cacert_pem()
            requests.adapters.DEFAULT_CA_BUNDLE_PATH = _get_cacert_pem()
        else:
            import certifi.core
            import requests.utils
            import requests.adapters
        
        return requests.get(request_url).content
    except:
        logging.debug('Error while executing https request.', exc_info=True)
        return None

def _get_cacert_pem():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), 'certifi', 'cacert.pem'))

if __name__ == '__main__':
    main()