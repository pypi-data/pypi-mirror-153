# Masterful only supports tensorflow 2.4.0


def _check_tensorflow_version():
  from packaging import version
  try:
    import tensorflow as tf
    assert version.parse(tf.__version__) >= version.parse(
        '2.4.0'
    ), "Masterful only supports Tensorflow versions 2.4.0 and greater."
  except ImportError:
    print(
        "Masterful requires Tensorflow 2.4+. Please install Tensorflow before installing Masterful."
    )
    exit()


def _log_masterful_import():
  """Logs an import event to datalake."""

  from masterful.proto import log_pb2
  import os

  MASTERFUL_STUB_ACCOUNT_ID = 'bb8c34ca-2abb-4e74-83c6-595d8da8b50e'
  MASTERFUL_STUB_AUTHORIZATION_KEY = '3eb905df-69a0-4b34-91e4-56a6dba893ca'

  def _environment_override(env_variable: str, default: str, type=None) -> str:
    if type is not None:
      return (type(os.environ[env_variable])
              if env_variable in os.environ else default)
    else:
      return (os.environ[env_variable]
              if env_variable in os.environ else default)

  MASTERFUL_ACCOUNT_ID = _environment_override('MASTERFUL_ACCOUNT_ID',
                                               MASTERFUL_STUB_ACCOUNT_ID)
  MASTERFUL_AUTHORIZATION_KEY = _environment_override(
      'MASTERFUL_AUTHORIZATION_KEY', MASTERFUL_STUB_AUTHORIZATION_KEY)

  def _create_base_log_entry():
    import uuid
    from masterful.version import __version__ as masterful_version

    log_entry = log_pb2.LogEntry()
    log_entry.customer_id = MASTERFUL_ACCOUNT_ID
    log_entry.mac_address = str(uuid.getnode())
    log_entry.client_version = masterful_version
    return log_entry

  def _send_log_entry(log_entry: log_pb2.LogEntry):
    """Sends a log request to the server carrying a log entry payload.

    Request exceptions are intercepted and printed to console.

    Args:
      log_entry: The log entry payload.
    """
    import requests
    from requests import auth
    from masterful import constants

    headers = {'Content-Type': 'application/octet-stream'}
    http_auth = auth.HTTPBasicAuth(MASTERFUL_ACCOUNT_ID,
                                   MASTERFUL_AUTHORIZATION_KEY)
    try:
      response = requests.post(constants.MASTERFUL_LOG_ENTRY,
                               headers=headers,
                               data=log_entry.SerializeToString(),
                               auth=http_auth)
      # TODO(MAS-1301): Retrieve global logger for reporting
      if response.status_code not in [200, 201]:
        print(
            f'Log {log_pb2.EventType.keys()[log_pb2.EventType.values().index(log_entry.event_type)]} ({response.status_code}): {response.json()}'
        )
    except requests.exceptions.RequestException as request_exception:
      print(request_exception)

  log_entry = _create_base_log_entry()
  log_entry.event_type = log_pb2.EventType.API_EVENT
  log_entry.api_event_data.type = log_pb2.ApiEventType.IMPORT_MASTERFUL
  log_entry.api_event_data.version = 2

  _send_log_entry(log_entry)

  # Now log the environment we are running ine
  log_entry = _create_base_log_entry()
  log_entry.event_type = log_pb2.EventType.ENVIRONMENT_EVENT

  import platform
  log_entry.environment_event_data.platform_system = platform.system()
  log_entry.environment_event_data.platform_release = platform.release()

  import sys
  log_entry.environment_event_data.python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

  try:
    import tensorflow as tf
    log_entry.environment_event_data.tensorflow_version = tf.__version__
  except ImportError:
    pass

  try:
    import torch
    log_entry.environment_event_data.pytorch_version = torch.__version__
  except ImportError:
    pass

  import os
  gpu_usage_query = os.popen(
      "nvidia-smi --query-gpu=gpu_name,memory.total --format=csv")
  gpu_usage = gpu_usage_query.read()
  log_entry.environment_event_data.gpu_info = gpu_usage

  def shell_type():
    try:
      shell_type = get_ipython().__class__.__name__
      return shell_type
    except NameError:
      return "standard"  # Probably standard Python interpreter

  log_entry.environment_event_data.shell_type = shell_type()
  _send_log_entry(log_entry)


_check_tensorflow_version()

# Catch all errors on import logging
# so that its not fatal.
try:
  _log_masterful_import()
except:
  pass

# Bring package level classes into the top level namespace
from masterful.version import __version__
from masterful.utils.register import register

# Pre-import the core packages.
import masterful.enums
import masterful.data
import masterful.architecture
import masterful.optimization
import masterful.regularization
import masterful.ssl
import masterful.training

# Import the convenience functions
from masterful.utils.helpers import learn_architecture_and_data_params
