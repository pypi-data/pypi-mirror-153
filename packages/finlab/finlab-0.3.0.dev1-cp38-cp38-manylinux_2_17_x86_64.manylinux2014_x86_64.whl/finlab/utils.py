import os
import re
import sys
import json
import logging
import finlab
from finlab.utils_core import str_to_bytearray

# Get an instance of a logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def requests_module_factory():

    """Creates a requests module

    The function returns requests module if it is installed.
    If requests module is not installed, raise error to inform user.
    If the python version is pyodide, try to create a custom requests module.

    Returns:
        requests module

    """

    # check requests is installed and return the module
    if "pyodide" not in sys.modules:
        import requests
        return requests

    # raise error if not install requests and not in pyodide env
    from js import XMLHttpRequest, Blob, FormData
    import urllib.parse
    import pyodide

    # in pyodide env, make fake requests
    class Response:
        text = ''
        json_ = ''
        content = ''
        ok = True

        def json(self):
            return self.json_

    class requests:

        def getBytes(url):
            req = XMLHttpRequest.new()
            req.open("GET", auth_url.text, False)
            req.overrideMimeType('text/plain; charset=x-user-defined')
            req.send(None)
            return str_to_bytearray(req.response)

        def get(url, params=None):

            if params == None:
                params = {}


            complete_url = url + '?' + '&'.join([
                urllib.parse.quote_plus(k)
                + '=' + urllib.parse.quote_plus(v)
                for k, v in params.items()])

            str_io = pyodide.http.open_url(complete_url)

            res = Response()
            res.text = str_io.read()
            res.json_ = requests.parse_json(res.text)
            res.status_code = 200

            return res

        def post(url, data, asyn=False):

            if data == None:
                data = {}


            req = XMLHttpRequest.new()
            form = FormData.new()

            for k, v in data.items():
                form.append(k, v)

            req.open("POST", url, asyn)
            req.send(form)

            res = Response()
            res.content = req.response
            res.text = str(req.response)
            res.json_ = requests.parse_json(res.text)
            res.status_code = 200

            return res

        def parse_json(text):

            if len(text) == 0:
                return {}

            if text[-1] == '\n':
                text = text[:-1]

            if text[0] != '{' or text[-1] != '}':
                return {}

            try:
                return json.loads(text)
            except:
                return {}

    return requests


def check_version_function_factory():

    """ Check finlab package version is the latest or not

    if the package version is out of date, info user to update.

    Returns
        None

    """

    latest_package_version = None

    def ret():

        nonlocal latest_package_version

        if latest_package_version is None:
            res = requests.get('https://pypi.org/project/finlab/')
            res.encoding = 'utf-8'

            m = re.findall("finlab\s([a-z0-9.]*)\s*</h1>", res.text)
            latest_package_version =  m[0] if m else None

            if latest_package_version != finlab.__version__:
                logger.warning(f'Your version is {finlab.__version__}, please install a newer version.\n Use "pip install finlab=={latest_package_version}" to update the latest version.')

    return ret


def futureDateFactory():
  """  get future date factory

  Returns
      function of get_future_date

  """
  latest = None
  date = None

  def ret(d):

    nonlocal latest
    nonlocal date

    if latest == d:
      return date

    latest = d

    if pd.to_datetime(d) > datetime.datetime(2022,1,1):

      url = "https://asia-east1-fdata-299302.cloudfunctions.net/future_date"
      res = requests.get(url, {'datestr': str(pd.to_datetime(d).date())})
      date = res.text

      return date

    else:
      return d

  return ret

def global_object_getter_setter_factory():
    _finlab_global_objects = {}

    def get_global(name):
        nonlocal _finlab_global_objects
        if name in _finlab_global_objects:
            return _finlab_global_objects[name]
        else:
            return None

    def set_global(name, obj):
        nonlocal _finlab_global_objects
        _finlab_global_objects[name] = obj
        if "pyodide" in sys.modules:
            import js
            js.postMessage(pyodide.to_js({'content': name, 'finish': False, 'type': 'py_global_update', 'id': js._pyodide_execution_id}))


    return get_global, set_global

get_global, set_global = global_object_getter_setter_factory()

requests = requests_module_factory()
check_version = check_version_function_factory()
get_future_date = futureDateFactory()

