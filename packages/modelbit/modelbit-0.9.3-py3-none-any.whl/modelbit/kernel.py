from ipykernel.kernelbase import Kernel
from typing import Dict, Any, Union, cast, Iterator
import json, time
import logging
import os

from . import modelbit_core
from .helpers import NotebookResponse, KernelInfo
from . import __version__
from .ipython_pb2 import JupyterMessage, CodeRequest, ShutdownRequest, EmptyMessage
from .ipython_pb2_grpc import KernelWrapperStub

PROD_CA_CERT = """
-----BEGIN CERTIFICATE-----
MIIFZzCCA0+gAwIBAgIUeOrlZfltFm6S/4Iz36QRntCW8CkwDQYJKoZIhvcNAQEL
BQAwQzELMAkGA1UEBhMCVVMxCzAJBgNVBAgMAkNBMREwDwYDVQQKDAhNb2RlbGJp
dDEUMBIGA1UECwwLTW9kZWxiaXQgQ0EwHhcNMjIwNDI1MjIxODM3WhcNMzIwNDIy
MjIxODM3WjBDMQswCQYDVQQGEwJVUzELMAkGA1UECAwCQ0ExETAPBgNVBAoMCE1v
ZGVsYml0MRQwEgYDVQQLDAtNb2RlbGJpdCBDQTCCAiIwDQYJKoZIhvcNAQEBBQAD
ggIPADCCAgoCggIBAMLzsnSOG2pCA1wdk1kuJp7JtKzEdi618x5SNOSUE7+X9U17
j0grGXLI8xSLWW5PY3g6h9NNPps7mjO3TDxYqO8RvvCb9oouOvkW7wYPcfEZAS6K
0fjufmNPL9FX50vmb1eCFxuP8wcaWTDLBdbRYPr12alUnQ/DePctzMhnAr3bQQ/e
lQcjJJFwT6aa1ag12oW+SAWs/RH6kC5mgMXJYUHp5MKnkebEfuuZOTZD1wA/wAmX
Er71dLuPnRxIo8JNgVNeMXcGFGVfINTg8+30FBU02CHD0vLmOXdXWLOFntMTtMCq
vnVpmsOMECpfbleiClJQZJSQXsKxN56jQRf3E/0R/qN1xeU68qVPQ/0Hj+bejfoS
hGlpKtEHMddEwzI7JWVq67PtT29+Mk7dJm+kx7IqfOvsOKqvE94iFYSwFAgOv2sM
uoPdEnzRUDXrpzO7SEcK0NryMbrBlMr+j2nbH/oLklqlc3A7XL/tooV24ei80Hak
K1LPPbwSHmCYVvhjDxXyzqP4ehjZ3KQjwQcPUlyyGxOU/8NIVSEm9w1Voe46glzK
RlLc4tXHgQ3oae89PqpemixRTOUxk/Y46GfvDQ4BhwnMcGEygpPn2IUgS3snEvCb
tmwjFsLwGMiCH8CB7NjxQWO0KyMcbK1PYiGx1NE/mQpLqhySWPy1d0HMI8G/AgMB
AAGjUzBRMB0GA1UdDgQWBBSkKGYAm8qZY3ttTLCMMIEO1qMH2DAfBgNVHSMEGDAW
gBSkKGYAm8qZY3ttTLCMMIEO1qMH2DAPBgNVHRMBAf8EBTADAQH/MA0GCSqGSIb3
DQEBCwUAA4ICAQCuxnnBGLLJB6La4s0/DEL4dXGXTXgSxM9I9YoCbWHL2HZ+B0z4
OauIeDQXDs1cQIkRjRHs3Id9lMXLJA23WjbCSqqAXyPVqLhCch84H2beEuDhs+fU
1rk8v7a/dDxtyQxTnYXp/yOvC26cw8SjC6/nsWi8Wj7mnSuyaObcHv3AM7XDBCew
mF3saFgpMjvwg2OXys2SRx5YLQ5FaCBBYMYRNp3pzpC+7s5TFnxxUPz+LYuph8VJ
2MUawNxpWoU2gUWg1cb03sQVp5LIFKqGXWbOiL+TY5R/6MlGevEtdv3s0Rik/m8S
5I51ii7lHdxLmeXIvx3W5QWkH7yzi0pjt73yhFmM2vNm5jYXqRodWUhPoWCnbsqm
/n7WEVLvmDfiAhgaE4+HDXKW2EpYZev3JfTQ9/Wuop9GD1TfkawQFw2VLdB8ZZ4i
aU6MIGqe0l6+XHIXH8fanOrEQKpf4RhRCPTd9qBn4NVOC/hfE/WHeJo1hCftvZ98
icbIAiz9IJToB30/kNXvZsCGKngO3Z5/+ab5OSkDnMnap9zfWWEaug7QkQ0slWGF
l31eh5lyIV51a9/qWPvR8NCkDnaGdiOq8EIjrDsnUIHu4NWQL0UsE3EJA2inqksf
qwQn1TahV1l6EzhjM/ryga+vBniKxVePwc4ZZKtvWnwuOPPu9q57ZFGiKg==
-----END CERTIFICATE-----"""


class ModelbitKernel(Kernel):
  implementation = "Modelbit"
  implementation_version = "1.0"
  language = "python"
  language_version = "3"
  language_info = {
      "codemirror_mode": {
          "name": "ipython",
          "version": 3
      },
      "name": "python",
      "nbconvert_exporter": "python",
      "file_extension": ".py",
      "mimetype": "text/x-python",
      "pygments_lexer": "ipython3",
      "version": "3",
  }
  banner = "Modelbit Kernel"
  kernelId = ""

  def __init__(self, **kwargs: Any):
    super().__init__(**kwargs)  # type: ignore
    self._mbCore = modelbit_core.ModelbitCore(__version__)

  # using warning so messages show up by default
  def logMsg(self, msg: Any):
    self.log.warning(msg)  # type: ignore

  def send_io_response(self, mode: str, content: Dict[str, Any]):
    super().send_response(self.iopub_socket, mode, content)  # type: ignore

  def sendText(self, msg: str, pipe: str = "stdout"):
    self.send_io_response("stream", {"name": pipe, "text": msg})

  def sendHtml(self, html: str, id: Union[str, None] = None):
    mode = "update_display_data" if id != None else "display_data"
    id = str(time.time()) if id == None else id
    self.send_io_response(
        mode,
        {
            "data": {
                "text/html": html
            },
            "metadata": {},
            "transient": {
                "display_id": id
            },
        },
    )
    return id

  def clearOutput(self):
    self.send_io_response("clear_output", {"wait": False})

  def callWeb(self, path: str, data: Dict[str, Any]):
    try:
      return self._mbCore.getJson(f"jupyter/v1/kernel/{path}", data)
    except Exception as err:
      return NotebookResponse({"error": str(err)})

  def start(self):
    super().start()
    self.logMsg("NYI: starting remote kernel")


  def _waitForAuth(self):
    self.logMsg("Started polling")
    maxAttempts = 120
    self.pollingOkay = True
    while self.pollingOkay and maxAttempts > 0 and not self._mbCore.isAuthenticated(True):
        self.logMsg("Not yet authed")
        time.sleep(1)
        maxAttempts -= 1

    self.logMsg("Authed!" if self.pollingOkay and maxAttempts > 0 else "Auth timed out")

  def do_execute(
      self,
      code: str,
      silent: bool,
      store_history: bool = True,
      user_expressions: Union[Dict[str, Any], None] = None,
      allow_stdin: bool = False,
      *,
      cell_id: Union[str, None] = None,
  ) -> Any:
    kernelInfo = self._waitForKernelInfo(silent)
    if kernelInfo is not None and kernelInfo.status == "ready":
      try:
        client = self.authenticatedClient(kernelInfo)
        req = CodeRequest()
        req.code = code
        respStream = cast(Iterator[JupyterMessage], client.ExecuteCode(req))
        return self.remoteExecute(respStream)
      except Exception as err:
        logging.error("Error executing code: %s", err)
        self.sendText(
            "Error getting connection details: %s" % (err),
            "stderr",
        )

    return {
        "status": "error",
        "error": "Failed to connect to the cloud.",
        "execution_count": self.execution_count,
        "payload": [],
        "user_expressions": {},
    }


  def do_complete(
      self,
      code: str,
      cursor_pos: int,
  ) -> Any:
    kernelInfo = self._waitForKernelInfo()
    if not self._mbCore.isAuthenticated(True):
      return
    if kernelInfo is not None and kernelInfo.status == "ready":
      try:
        client = self.authenticatedClient(kernelInfo)
        req = CodeRequest()
        req.code = code
        req.cursor_pos = cursor_pos
        respStream = cast(Iterator[JupyterMessage], client.CompleteCode(req))
        return self.remoteExecute(respStream)
      except Exception as err:
        logging.error("Error completing code: %s", err)
        self.sendText(
            "Error getting connection details: %s" % (err),
            "stderr",
        )
    return {
        "status": "error",
        "error": "Failed to connect to the cloud.",
        "execution_count": self.execution_count,
        "payload": [],
        "user_expressions": {},
    }


  def do_inspect(
      self,
      code: str,
      cursor_pos: int,
      detail_level: int = 0,
      omit_sections = (),
  ) -> Any:
    if not self._mbCore.isAuthenticated(True):
      return
    kernelInfo = self._waitForKernelInfo()
    if kernelInfo is not None and kernelInfo.status == "ready":
      try:
        client = self.authenticatedClient(kernelInfo)
        req = CodeRequest()
        req.code = code
        req.cursor_pos = cursor_pos
        req.detail_level = detail_level
        respStream = cast(Iterator[JupyterMessage], client.InspectCode(req))
        return self.remoteExecute(respStream)
      except Exception as err:
        logging.error("Error completing code: %s", err)
        self.sendText(
            "Error getting connection details: %s" % (err),
            "stderr",
        )
    return {
        "status": "error",
        "error": "Failed to connect to the cloud.",
        "execution_count": self.execution_count,
        "payload": [],
        "user_expressions": {},
    }


  def _waitForKernelInfo(self, silent=False):
    dispId = None
    if not self._mbCore.isAuthenticated(True):
      dispId = self.sendHtml(self._mbCore.getAuthMessage())
      self._waitForAuth()
      self.sendHtml("<div>Preparing kernel...</div>", dispId)

    kernelInfo = self.waitForConnectionInfo(dispId)
    if not silent:
      if kernelInfo is None:
        self.sendText("Failed getting connection details", "stderr")
      elif kernelInfo.error:
        self.sendText(
            "Error getting connection details: %s" % (kernelInfo.error),
            "stderr",
        )
      elif kernelInfo.status != "ready":
        self.sendText("Unknown response: %s" % (json.dumps(kernelInfo.__dict__)), "stderr")
    return kernelInfo


  def do_shutdown(self, restart: bool):
    kernelInfo = self.connectionInfo(forShutdown=True)
    if kernelInfo:
      client = self.authenticatedClient(kernelInfo)
      req = ShutdownRequest()
      req.restart = restart
      client.ShutdownKernel(req)
    return super().do_shutdown(restart)  # type: ignore

  async def interrupt_request(self, stream, ident, parent):
    self.logMsg("Got interrupt")
    self.pollingOkay = False
    kernelInfo = self.connectionInfo(forShutdown=True)
    if kernelInfo:
      client = self.authenticatedClient(kernelInfo)
      client.InterruptKernel(EmptyMessage())
    return super().interrupt_request(stream, ident, parent)


  def caCert(self):
    cert = bytes(os.environ.get("MODELBIT_CA_CERT", PROD_CA_CERT), 'utf-8')
    if cert == "":
        cert = PROD_CA_CERT
    return cert

  def authenticatedClient(self, kernelInfo: KernelInfo) -> KernelWrapperStub:
    import grpc
    class GrpcAuth(grpc.AuthMetadataPlugin):
      """Used to pass JWT and runtime token via channel credentials."""
      def __init__(self, key: str, token: str):
        self._key = key
        self._token = token

      def __call__(self, context: grpc.AuthMetadataContext, callback: grpc.AuthMetadataPluginCallback):
        callback((("rpc-auth-header", self._key),("mb-runtime-token-header", self._token)), None)

    sslCreds = grpc.ssl_channel_credentials(self.caCert())  # type: ignore
    authCreds = grpc.metadata_call_credentials(GrpcAuth(kernelInfo.sharedSecret, self._mbCore._state.signedToken))  # type: ignore
    creds = grpc.composite_channel_credentials(sslCreds, authCreds)  # type: ignore
    channel = grpc.secure_channel(  # type: ignore
        kernelInfo.address,
        creds,
        (("grpc.ssl_target_name_override", "km.modelbit.com"),),
    )
    stub = KernelWrapperStub(channel)
    return stub

  def connectionInfo(self, forShutdown: bool = False) -> Union[KernelInfo, None]:
    args = {"requestedKernelId": self.kernelId}
    if forShutdown:
      args["forShutdown"] = "true"
    resp = self.callWeb("kernel_info", args)

    if resp.kernelInfo and resp.kernelInfo.kernelId is not None:
      if resp.kernelInfo.kernelId != self.kernelId:
        logging.info("New remote kernel_id=%s", resp.kernelInfo.kernelId)
        self.kernelId = resp.kernelInfo.kernelId
      if resp.kernelInfo.address != "":
        logging.info("Connecting to kernel_id=%s address=%s", resp.kernelInfo.kernelId, resp.kernelInfo.address)
    return resp.kernelInfo

  def waitForConnectionInfo(self, dispId:Union[str, None]) -> Union[KernelInfo, None]:
    kernelInfo = self.connectionInfo()

    if kernelInfo is None:
      return None

    if kernelInfo.status == "preparing":
      start = time.time()
      dispId = self.sendHtml("<div>Preparing kernel...</div>", dispId)
      while kernelInfo is not None and kernelInfo.status == "preparing":
        time.sleep(1)
        kernelInfo = self.connectionInfo()
        self.sendHtml(
            f"<div>Preparing kernel... {round(time.time() - start)}s</div>",
            dispId,
        )
      self.clearOutput()
    return kernelInfo

  def remoteExecute(self, replyStream:Iterator[JupyterMessage]) -> Dict[str, Any]:
    reply: Dict[str, Any] = {}
    for resp in replyStream:
      if resp.channel == JupyterMessage.Channel.SHELL:
        reply = json.loads(resp.content)
      elif resp.channel == JupyterMessage.Channel.IOPUB:
        self.send_io_response(resp.msg_type, json.loads(resp.content))
    return reply


if __name__ == "__main__":
  from ipykernel.kernelapp import IPKernelApp

  logging.basicConfig(level=logging.DEBUG)
  IPKernelApp.launch_instance(kernel_class=ModelbitKernel)  # type: ignore
