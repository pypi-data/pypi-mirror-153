"""A module responsible for Masterful code deployment."""

import atexit
import json
import os
import time
import sys
import types
import uuid
from datetime import datetime
import re

import memory_tempfile
import requests
from requests import auth

from masterful import constants
from masterful import version


try:
  memory_tempfile = memory_tempfile.MemoryTempfile(fallback=True)
  _DOWNLOAD_FOLDER = memory_tempfile.gettempdir()
except AttributeError:
  import tempfile
  _DOWNLOAD_FOLDER = tempfile.gettempdir()
except RuntimeError:
  import tempfile
  _DOWNLOAD_FOLDER = tempfile.gettempdir()

# Seconds to sleep the register call after 30 days of trial period
_NAGWARE_SLEEP_SECONDS = 30
# Number of trial days where an user can use masterful freely
_MASTERFUL_TRIAL_DAYS = 45
# Number of to filter the nagging message sent to clients
_MASTERFUL_REMINDER_DAYS = 30

_MASTERFUL_TRIAL_ACCOUNT_ID = '631d9db2-39cd-420c-a6aa-4c7c7f81464d'
_MASTERFUL_TRIAL_AUTHORIZATION_KEY = '6cef878d-fc77-4f1f-a2c5-2f3db6b6258a'

_MASTERFUL_REMINDER_DAYS_MESSAGE = (
  'Loaded Masterful version {}. This software is distributed free of charge for\n'
  'personal use. Register in the next {} days to continue using Masterful.\n'
  'Visit http://www.masterfulai.com/register for more details.\n'
)

_MASTERFUL_REMINDER_SIGN_UP_NOW = (
  'Loaded Masterful version {}. This software is distributed free of charge for\n'
  'personal use. Register now to continue using Masterful.\n'
  'Visit http://www.masterfulai.com/register for more details.\n'
)

_MASTERFUL_REMINDER_TRIAL_VERSION_FINISHED = (
  'Unable to load Masterful. Registration required. Register now to continue using\n'
  'Masterful. Visit http://www.masterfulai.com/register for more details.\n'
)


def _pretty_error_message(response, account_id) -> str:
  status_code = response.status_code
  account_status = response.json().get('context', {}).get('account_status', '')
  pretty_messages = {
      400:
          f"The Masterful account id '{account_id}' or authorization key is in a bad format. Please register for a new account at https://www.masterfulai.com/try-free.",
      401:
          f"The authorization key for Masterful account id '{account_id}' is incorrect. Please check your key and try again.",
      403:
          f"The Masterful account id '{account_id}' has hit its free usage limits ({account_status}). Please contact your Masterful representative to get a new key.",
      404:
          f"The Masterful account id '{account_id}' does not exist. Please check your key and try again.",
  }
  if status_code in pretty_messages:
    print(ValueError(pretty_messages[status_code]))
  else:
    print(
        f'Failed to register Masterful package. (Internal Server Error: {response.status_code}){os.linesep}'
        f'{json.dumps(response.json(), indent=2)}')



def _print_success_message(version: str) -> None:
  """Prints a user friendly message to confirm the success of register.

  Args:
    version: The package version to include in the message.
  """
  print(
    "MASTERFUL: Your account has been successfully registered."
    f" Masterful v{version} is loaded."
  )


def _get_nagware_message(current_date: datetime,
                         masterful_home_creation_date: datetime,
                         masterful_version: str) -> str:
  """Gets a nagware message given date constraints.

  Returns a nagware message given the current date and the date where the
  ~/.masterful folder was created.

  Args:
    current_date: The current time in datetime format.
    masterful_home_creation_date: The date in which the masterful folder was created.
    masterful_version: The package version to include in the message.

  Returns:
    The message to be printed into the console.
  """
  delta = current_date - masterful_home_creation_date
  message = None
  if delta.days <= _MASTERFUL_REMINDER_DAYS:
    days_to_sign = _MASTERFUL_TRIAL_DAYS - delta.days
    message = _MASTERFUL_REMINDER_DAYS_MESSAGE.format(masterful_version, days_to_sign)

  elif delta.days > _MASTERFUL_REMINDER_DAYS and delta.days <= _MASTERFUL_TRIAL_DAYS:
    message = _MASTERFUL_REMINDER_SIGN_UP_NOW.format(masterful_version)

  elif delta.days > _MASTERFUL_TRIAL_DAYS:
    message = _MASTERFUL_REMINDER_TRIAL_VERSION_FINISHED.format(masterful_version)

  return message


def _print_nagware_reminder(masterful_version: str) -> None:
  """Prints to the console a nagware message.

  Prints Messages to the users indicating when they need to sign up in masterful's
  webpage in order to get a key.

  Args:
    version: The package version to include in the message.
  """
  masterful_home = f'{os.path.expanduser("~")}/.masterful'
  masterful_stats_file = '.stats'
  stats_file_path = os.path.join(masterful_home, masterful_stats_file)

  if os.path.exists(stats_file_path):
    with open(stats_file_path, 'r') as f:
      masterful_home_creation_timestamp = f.read()

    masterful_home_creation_date = datetime.fromtimestamp(float(masterful_home_creation_timestamp))

  else:
    if not os.path.exists(masterful_home):
      os.mkdir(masterful_home)

    with open(stats_file_path, 'w') as f:
      masterful_home_creation_date = datetime.utcnow()
      f.write(str(datetime.timestamp(masterful_home_creation_date)))

  current_date = datetime.utcnow()
  delta = current_date - masterful_home_creation_date
  nagware_message = _get_nagware_message(current_date, masterful_home_creation_date, masterful_version)

  print(nagware_message)
  delta = current_date - masterful_home_creation_date
  if delta.days > _MASTERFUL_REMINDER_DAYS and delta.days <= _MASTERFUL_TRIAL_DAYS:
    print(f"[Pausing for {_NAGWARE_SLEEP_SECONDS} seconds]")
    time.sleep(_NAGWARE_SLEEP_SECONDS)

  if delta.days > _MASTERFUL_TRIAL_DAYS:
    sys.exit('Masterful Library not loaded')



def register(account_id: str = '',
             authorization_key: str = '') -> types.ModuleType:
  """Authorizes the Masterful library and prepares the system for its use.

  This function authorizes usage of the Masterful library, and loads it into
  memory for use. This function *must* be called before using or importing
  any other Masterful packages.

  Note this function returns a new Masterful module instance, so you must
  replace the existing instance like so::

    import masterful
    masterful = masterful.register(...)

  If you need an account_id and authorization_key, register an account  
  `here <https://www.masterfulai.com/register>`_

  Args:
    account_id: The account credentials that were assigned by Masterful.
    authorization_key: The authorization key assigned by Masterful for the provided account.

  Returns:
    Module containing the latest implementation of the Masterful API.
  """

  def remove_file(file_path: str):
    if os.path.exists(file_path):
      os.remove(file_path)

  # Download zip file of Masterful package
  if not account_id:
    account_id = account_id if account_id else constants.MASTERFUL_ACCOUNT_ID
    if account_id == '':
      account_id = _MASTERFUL_TRIAL_ACCOUNT_ID

  if not authorization_key:
    authorization_key = (authorization_key if authorization_key else
                         constants.MASTERFUL_AUTHORIZATION_KEY)
    if authorization_key == '':
      authorization_key = _MASTERFUL_TRIAL_AUTHORIZATION_KEY

  zip_path = f'{_DOWNLOAD_FOLDER}/masterful-{version.__version__}.zip'
  if not f'{zip_path}/masterful-{version.__version__}/' in sys.path:
    response = requests.get(
        constants.MASTERFUL_LOAD + f'?version={version.__version__}',
        auth=auth.HTTPBasicAuth(account_id, authorization_key),
        stream=True)

    if response.status_code != 200:
      _pretty_error_message(response, account_id)
      sys.exit()

    with open(zip_path, 'wb') as zip_file:
      zip_file.write(response.raw.read())
    atexit.register(lambda: remove_file(zip_path))

    # Prepend zip file to system path
    if zip_path not in sys.path:
      sys.path.insert(0, f'{zip_path}/masterful-{version.__version__}/')

    # Remove masterful from the global modules list
    masterful_module_names = []
    for module_name in sys.modules:
      if 'masterful' in module_name:
        masterful_module_names.append(module_name)

    for module_name in masterful_module_names:
      del sys.modules[module_name]

    # Re-import the new masterful
    globals()['masterful'] = __import__('masterful')

  import masterful

  # Update the constants so the rest of the package
  # can use them
  import masterful.constants
  masterful.constants.MASTERFUL_ACCOUNT_ID = account_id
  masterful.constants.MASTERFUL_AUTHORIZATION_KEY = authorization_key
  masterful.constants.MASTERFUL_SESSION_ID = str(uuid.uuid4())
  # uuid.get_node gets the mac address of the device as a 48-bit positive integer
  masterful.constants.MASTERFUL_USER_MAC_ADDRESS = str(uuid.getnode())

  if account_id != _MASTERFUL_TRIAL_ACCOUNT_ID:
    _print_success_message(version.__version__)

  if account_id == _MASTERFUL_TRIAL_ACCOUNT_ID:
    _print_nagware_reminder(version.__version__)

  import masterful.proto.log_pb2
  import masterful.utils.logging

  masterful.utils.logging.log_api_event2(masterful.proto.log_pb2.ApiEventType.REGISTER)

  return masterful
