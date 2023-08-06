from typing import Any, Dict, Union
import os, json
import requests  # type: ignore

from .utils import printError, printHtml, sizeOfFmt
from .helpers import NotebookEnv, NotebookResponse


class ModelbitCore:
  version: str
  _api_host = 'https://app.modelbit.com/'
  _login_host = _api_host
  _api_url = None
  _MAX_DATA_LEN = 50_000_000

  def __init__(self, version: str, requestToken: Union[str, None]=None):
    self._state: NotebookEnv = NotebookEnv({})
    if requestToken:
      self._state.signedToken = requestToken
    self.version = version
    osApiHost = os.getenv('MB_JUPYTER_API_HOST')
    if osApiHost:
      self._api_host = osApiHost
    osLoginHost = os.getenv('MB_JUPYTER_LOGIN_HOST')
    if osLoginHost:
      self._login_host = osLoginHost
    self._api_url = f'{self._api_host}api/'

  def isAuthenticated(self, testRemote: bool = True) -> bool:
    if testRemote:
      nbResp = self.getJson("jupyter/v1/login")
      if nbResp.error:
        printError(nbResp.error)
        return False
      if nbResp.notebookEnv:
        self._state = nbResp.notebookEnv
      return self.isAuthenticated(False)
    return self._state.authenticated

  def getJson(self, path: str, body: Dict[str, Any] = {}) -> NotebookResponse:
    try:
      requestToken = self._state.signedToken
      if requestToken == None:
        requestToken = os.getenv('MB_RUNTIME_TOKEN')
      data: Dict[str, Any] = {
          "requestToken": requestToken,
          "version": self.version,
      }
      data.update(body)
      dataLen = len(json.dumps(data))
      if (dataLen > self._MAX_DATA_LEN):
        return NotebookResponse({
            "error":
                f'API Error: Request is too large. (Request is {sizeOfFmt(dataLen)} Limit is {sizeOfFmt(self._MAX_DATA_LEN)})'
        })
      with requests.post(f'{self._api_url}{path}', json=data) as url:  # type: ignore
        nbResp = NotebookResponse(url.json())  # type: ignore
        if nbResp.notebookEnv:
          self._state = nbResp.notebookEnv
        return nbResp
    except BaseException as err:
      if type(err) == requests.exceptions.JSONDecodeError:
        return NotebookResponse({"error": f'Unable to reach Modelbit. Bad response from server.'})
      else:
        return NotebookResponse({"error": f'Unable to reach Modelbit: {type(err)}'})

  def getJsonOrPrintError(self, path: str, body: Dict[str, Any] = {}):
    nbResp = self.getJson(path, body)
    if not self.isAuthenticated():
      self.performLogin()
      return False
    if nbResp.error:
      printError(nbResp.error)
      return False
    return nbResp

  def _maybeGetUpgradeMessage(self):
    if os.getenv('MB_RUNTIME_TOKEN'):
      return ""  # runtime environments don't get upgraded
    latestVer = self._state.mostRecentVersion

    def ver2ints(ver: str):
      return [int(v) for v in ver.split(".")]

    nbVer = self.version
    if latestVer and ver2ints(latestVer) > ver2ints(nbVer):
      pipCmd = '<span style="color:#E7699A; font-family: monospace;">pip install --upgrade modelbit</span>'
      return (f'<div>Please run {pipCmd} to upgrade to the latest version. ' +
              f'(Installed: <span style="font-family: monospace">{nbVer}</span>. ' +
              f' Latest: <span style="font-family: monospace">{latestVer}</span>)<div>')
    return ""

  def printAuthenticatedMsg(self):
    connectedTag = '<span style="color:green; font-weight: bold;">connected</span>'
    email = self._state.userEmail
    workspace = self._state.workspaceName
    printHtml(f'<div>You\'re {connectedTag} to Modelbit as {email} in the \'{workspace}\' workspace.</div>' +
              self._maybeGetUpgradeMessage())

  def getAuthMessage(self):
    displayUrl = f'modelbit.com/t/{self._state.uuid}'
    linkUrl = f'{self._login_host}/t/{self._state.uuid}'
    aTag = f'<a style="text-decoration:none;" href="{linkUrl}" target="_blank">{displayUrl}</a>'
    helpTag = '<a style="text-decoration:none;" href="https://doc.modelbit.com/getting-started.html" target="_blank">Learn more.</a>'
    return (
        f'<div style="font-weight: bold;">Connect to Modelbit</div><div>Open {aTag} to authenticate this kernel, then re-run this cell. {helpTag}</div>'
        + self._maybeGetUpgradeMessage())

  def performLogin(self):
    if self.isAuthenticated():
      self.printAuthenticatedMsg()
      return
    printHtml(self.getAuthMessage())
