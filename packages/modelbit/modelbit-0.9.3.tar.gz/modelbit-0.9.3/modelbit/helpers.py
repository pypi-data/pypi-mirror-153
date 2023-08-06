from typing import Union, Any, List, Dict, cast
from enum import Enum
import uuid
from .utils import pickleObj, unpickleObj


class OwnerInfo:

  def __init__(self, data: Dict[str, Any]):
    self.id: Union[str, None] = data.get("id", None)
    self.name: Union[str, None] = data.get("name", None)
    self.imageUrl: Union[str, None] = data.get("imageUrl", None)


class DatasetDesc:

  def __init__(self, data: Dict[str, Any]):
    self.name: str = data["name"]
    self.sqlModifiedAtMs: Union[int, None] = data.get("sqlModifiedAtMs", None)
    self.query: str = data["query"]
    self.recentResultMs: Union[int, None] = data.get("recentResultMs", None)
    self.numRows: Union[int, None] = data.get("numRows", None)
    self.numBytes: Union[int, None] = data.get("numBytes", None)
    self.ownerInfo = OwnerInfo(data["ownerInfo"])


class ResultDownloadInfo:

  def __init__(self, data: Dict[str, Any]):
    self.id: str = data["id"]
    self.signedDataUrl: str = data["signedDataUrl"]
    self.key64: str = data["key64"]
    self.iv64: str = data["iv64"]


class KernelInfo:

  def __init__(self, data: Dict[str, str]):
    self.status: str = data["status"]
    self.address: Union[str, None] = data.get("address", None)
    self.sharedSecret: Union[str, None] = data.get("sharedSecret", None)
    self.error: Union[str, None] = data.get("error", None)
    self.kernelId: Union[str, None] = data.get("kernelId", None)


class WhType(Enum):
  Snowflake = 'Snowflake'
  Redshift = 'Redshift'
  Postgres = 'Postgres'


class GenericWarehouse:

  def __init__(self, data: Dict[str, Any]):
    self.type: WhType = data["type"]
    self.id: str = data["id"]
    self.displayName: str = data["displayName"]
    self.deployStatusPretty: str = data["deployStatusPretty"]
    self.createdAtMs: int = data["createdAtMs"]


class RuntimeFile:

  def __init__(self, name: str, contents: str):
    self.name = name
    self.contents = contents

  def asDict(self):
    return {"name": self.name, "contents": self.contents}


class RuntimePythonProps:
  excludeFromDict: List[str] = ['errors']

  def __init__(self):
    self.source: Union[str, None] = None
    self.name: Union[str, None] = None
    self.argNames: Union[List[str], None] = None
    self.argTypes: Union[Dict[str, str], None] = None
    self.namespaceVarsDesc: Union[Dict[str, str], None] = None
    self.namespaceFunctions: Union[Dict[str, str], None] = None
    self.namespaceImports: Union[Dict[str, str], None] = None
    self.namespaceFroms: Union[Dict[str, str], None] = None
    self.requirementsTxt: Union[str, None] = None
    self.pythonVersion: Union[str, None] = None
    self.errors: Union[List[str], None] = None
    self.namespaceVars: Union[Dict[str, Any], None] = None


class RuntimeType(Enum):
  Deployment = 'Deployment'


class EnvironmentStatus(Enum):
  Updating = 'Updating'
  Ready = 'Ready'
  Error = 'Error'
  Unknown = 'Unknown'


class RuntimeInfo:

  def __init__(self, data: Dict[str, Any]):
    self.id: str = data["id"]
    self.name: str = data["name"]
    self.version: str = data["version"]
    self.restUrl: str = data["restUrl"]
    self.snowUrl: str = data["snowUrl"]
    self.forwardLambdaArn: Union[str, None] = data.get("forwardLambdaArn", None)
    self.createdAtMs: int = data["createdAtMs"]
    self.apiAvailableAtMs: Union[int, None] = data.get("apiAvailableAtMs", None)
    self.latest: bool = data["latest"]
    self.environmentStatus: EnvironmentStatus = data["environmentStatus"]
    self.ownerInfo = OwnerInfo(data["ownerInfo"])


class PickledObj:

  def __init__(self, obj: Any = None, jDict: Union[Dict[str, Any], None] = None):
    self.pkl: Union[str, None] = None
    self.desc: Union[str, None] = None
    self.kind: Union[str, None] = None
    self.size: Union[int, None] = None
    if obj:
      self.pkl = pickleObj(obj)
      self.desc = str(obj)
      self.kind = self._getClassName(obj)
      self.size = len(self.pkl)
    elif jDict:
      self.pkl = jDict.get("pkl", None)
      self.desc = jDict.get("desc", None)
      self.kind = jDict.get("kind", None)
      self.size = jDict.get("size", None)

  def unpickle(self):
    if self.pkl:
      return unpickleObj(self.pkl)
    else:
      return None

  def asDict(self):
    return self.__dict__

  def _getClassName(self, obj: Any):
    try:
      return f"{obj.__module__}.{obj.__class__.__name__}"
    except:
      return ""


class ModelPackage:

  def __init__(self, data: Dict[str, Any]):
    self.uuid: str = data.get("uuid", str(uuid.uuid4()))
    self.name: Union[str, None] = data.get("name", None)
    self.ownerInfo: Union[OwnerInfo, None] = None
    if "ownerInfo" in data:
      self.ownerInfo = OwnerInfo(data["ownerInfo"])
    self.model: Union[PickledObj, None] = None
    if "model" in data:
      self.model = PickledObj(jDict=data["model"])
    self.helpers: Dict[str, PickledObj] = {}
    if "helpers" in data:
      helpers = cast(Dict[str, Any], data["helpers"])
      for hName, hVal in helpers.items():
        self.helpers[hName] = PickledObj(jDict=hVal)
    self.properties: Dict[str, Any] = data.get("properties", {})
    self.requirementsTxt: Union[str, None] = data.get("requirementsTxt", None)
    self.pythonVersion: Union[str, None] = data.get("pythonVersion", None)
    self.createdAtMs: Union[int, None] = data.get("createdAtMs", None)

  def asDict(self):
    d = self.__dict__.copy()
    if self.model:
      d["model"] = self.model.asDict()
    d["helpers"] = {}
    for hName, hPkl in self.helpers.items():
      d["helpers"][hName] = hPkl.asDict()
    del d["ownerInfo"]
    return d


class NotebookEnv:

  def __init__(self, data: Dict[str, Any]):
    self.userEmail: Union[str, None] = data.get("userEmail", None)
    self.signedToken: Union[str, None] = data.get("signedToken")
    self.uuid: Union[str, None] = data.get("uuid", None)
    self.authenticated: bool = data.get("authenticated", False)
    self.workspaceName: Union[str, None] = data.get("workspaceName", None)
    self.mostRecentVersion: Union[str, None] = data.get("mostRecentVersion", None)


class NotebookResponse:

  def __init__(self, data: Dict[str, Any]):
    self.error: Union[str, None] = data.get("error", None)
    self.message: Union[str, None] = data.get("message", None)

    self.notebookEnv: Union[NotebookEnv, None] = None
    if "notebookEnv" in data:
      self.notebookEnv = NotebookEnv(data["notebookEnv"])

    self.datasets: Union[List[DatasetDesc], None] = None
    if "datasets" in data:
      self.datasets = [DatasetDesc(d) for d in data["datasets"]]

    self.dsrDownloadInfo: Union[ResultDownloadInfo, None] = None
    if "dsrDownloadInfo" in data:
      self.dsrDownloadInfo = ResultDownloadInfo(data["dsrDownloadInfo"])

    self.warehouses: Union[List[GenericWarehouse], None] = None
    if "warehouses" in data:
      self.warehouses = [GenericWarehouse(w) for w in data["warehouses"]]

    self.runtimeOverviewUrl: Union[str, None] = None
    if "runtimeOverviewUrl" in data:
      self.runtimeOverviewUrl = data["runtimeOverviewUrl"]

    self.deployments: Union[List[RuntimeInfo], None] = None
    if "deployments" in data:
      self.deployments = [RuntimeInfo(d) for d in data["deployments"]]

    self.modelOverviewUrl: Union[str, None] = None
    if "modelOverviewUrl" in data:
      self.modelOverviewUrl = data["modelOverviewUrl"]

    self.models: Union[List[ModelPackage], None] = None
    if "models" in data:
      self.models = [ModelPackage(m) for m in data["models"]]

    self.modelDownloadInfo: Union[ResultDownloadInfo, None] = None
    if "modelDownloadInfo" in data:
      self.modelDownloadInfo = ResultDownloadInfo(data["modelDownloadInfo"])

    self.kernelInfo: Union[KernelInfo, None] = None
    if "kernelInfo" in data:
      self.kernelInfo = KernelInfo(data["kernelInfo"])
