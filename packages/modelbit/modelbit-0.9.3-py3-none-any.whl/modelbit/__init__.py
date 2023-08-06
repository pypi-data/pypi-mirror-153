__version__ = "0.9.3"
__author__ = 'Modelbit'

import os, sys, zipimport
from typing import cast, Union, Callable, Any, Dict, List

from . import modelbit_core
from . import datasets
from . import warehouses
from . import runtime
from . import model
from . import deployments
from . import secure_storage
from . import utils
from . import ux
from . import helpers
from . import session
from . import model_wrappers


# Nicer UX for customers: from modelbit import Deployment
class Deployment(runtime.Deployment):
  ...


class Model(model.Model):
  ...


class _ClientSession:

  def _resetState(self, runtimeToken: Union[str, None] = None):
    self._mbCore = modelbit_core.ModelbitCore(__version__, runtimeToken)
    self._mbCore.performLogin()
    session.rememberSession(self)

  def __init__(self, runtimeToken: Union[str, None] = None):
    self._resetState(runtimeToken)

  # Interface for pickle. We don't currently _need_ to save anything, and explicitly don't want to save auth state
  def __getstate__(self):
    pickleState: Dict[str, str] = {}
    return pickleState  # need to return something. Returning None won't call setstate

  def __setstate__(self, pickledState: Dict[str, str]):
    self._resetState()

  def __str__(self):
    return "modelbit.login()"

  def _objIsDeployment(self, obj: Any):
    try:
      if type(obj) in [Deployment, runtime.Deployment]:
        return True
      # catch modelbit._reload() class differences
      if obj.__class__.__name__ in ['Deployment']:
        return True
    except:
      return False
    return False

  # Public mb.* API
  def isAuthenticated(self):
    return self._mbCore.isAuthenticated(True)

  def printAuthenticatedMsg(self):
    return self._mbCore.printAuthenticatedMsg()

  def datasets(self):
    return datasets.Datasets(self._mbCore)

  def get_dataset(self, dataset_name: str):
    return datasets.Datasets(self._mbCore).get(dataset_name)

  def warehouses(self):
    return warehouses.Warehouses(self._mbCore)

  def Deployment(self,
                 name: Union[str, None] = None,
                 deploy_function: Union[Callable[..., Any], None] = None,
                 python_version: Union[str, None] = None,
                 requirements_txt_filepath: Union[str, None] = None,
                 requirements_txt_contents: Union[List[str], None] = None):
    return Deployment(name=name,
                      deploy_function=deploy_function,
                      python_version=python_version,
                      requirements_txt_filepath=requirements_txt_filepath,
                      requirements_txt_contents=requirements_txt_contents)

  def Model(self,
            modelObj: Any,
            name: Union[str, None] = None,
            properties: Union[Dict[str, Any], None] = None,
            helpers: Union[Dict[str, Any], None] = None):
    return Model(modelObj, name=name, properties=properties, helpers=helpers)

  def deployments(self):
    return deployments.Deployments(self._mbCore)

  def models(self):
    return model.ModelList(self._mbCore)

  def _createRuntime(self,
                     rtType: helpers.RuntimeType,
                     deployableObj: Union[Callable[..., Any], runtime.Runtime, None],
                     name: Union[str, None] = None,
                     python_version: Union[str, None] = None):
    if not self.isAuthenticated():
      self._mbCore.performLogin()
      return
    if self._objIsDeployment(deployableObj):
      deployableObj = cast(runtime.Runtime, deployableObj)
      return deployableObj.deploy(self._mbCore)
    if callable(deployableObj):
      if rtType == helpers.RuntimeType.Deployment:
        dep = self.Deployment(name=name, deploy_function=deployableObj, python_version=python_version)
        return dep.deploy(self._mbCore)
    if hasattr(deployableObj, "__module__") and "sklearn" in deployableObj.__module__ and hasattr(
        deployableObj, "predict"):
      return model_wrappers.SklearnPredictor(deployableObj, name=name,
                                             python_version=python_version).makeDeployment().deploy()

    print("First argument doesn't looks like a deployable object.")

  def deploy(self,
             deployableObj: Union[Callable[..., Any], runtime.Deployment, None] = None,
             name: Union[str, None] = None,
             python_version: Union[str, None] = None,
             pycaret_classifier_name: Union[str, None] = None):
    if pycaret_classifier_name:
      return model_wrappers.PyCaretClassification(pycaret_classifier_name).makeDeployment(name=name).deploy()
    return self._createRuntime(helpers.RuntimeType.Deployment,
                               deployableObj,
                               name=name,
                               python_version=python_version)

  def save_model(self,
                 modelObj: Any,
                 name: Union[str, None] = None,
                 properties: Union[Dict[str, Any], None] = None,
                 helpers: Union[Dict[str, Any], None] = None):
    if type(modelObj) in [Model, model.Model]:
      modelObjM = cast(Model, modelObj)
      return modelObjM.save(self._mbCore)
    return Model(modelObj, name=name, properties=properties, helpers=helpers).save(self._mbCore)

  def load_model(self, name: str):
    return Model.load(self._mbCore, name)


def login():
  existingSession = cast(Union[_ClientSession, None], session.anyAuthenticatedSession())
  if existingSession:
    existingSession.printAuthenticatedMsg()
    return existingSession
  return _ClientSession()


def loginWithToken(runtimeToken: str):
  existingSession = cast(Union[_ClientSession, None], session.anyAuthenticatedSession())
  if existingSession:
    existingSession.printAuthenticatedMsg()
    return existingSession
  return _ClientSession(runtimeToken)


def load_value(name: str):
  if "snowparkZip" in os.environ:
    zipPath = [p for p in sys.path if p.endswith(os.environ["snowparkZip"])][0]
    importer = zipimport.zipimporter(zipPath)
    # Typing thinks the response is a string, but we get bytes
    val64 = cast(bytes, importer.get_data(f"{name}.pkl")).decode()
    return utils.unpickleObj(val64)
  extractPath = ""
  if 'MB_EXTRACT_PATH' in os.environ:
    extractPath = os.environ['MB_EXTRACT_PATH']
  f = open(f"{extractPath}/{name}.pkl", "r")
  val64 = f.read()
  f.close()
  return utils.unpickleObj(val64)


def _reload():  # type: ignore
  import importlib
  importlib.reload(modelbit_core)
  importlib.reload(datasets)
  importlib.reload(warehouses)
  importlib.reload(runtime)
  importlib.reload(model)
  importlib.reload(deployments)
  importlib.reload(secure_storage)
  importlib.reload(utils)
  importlib.reload(ux)
  importlib.reload(helpers)
  importlib.reload(model_wrappers)
  importlib.reload(importlib.import_module("modelbit"))
  print("All modules reloaded, except session.")
