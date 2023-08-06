from typing import Union, List, Dict, Any, cast, Callable
import inspect, re, html

from .modelbit_core import ModelbitCore
from .utils import printHtml, printError, unindent, pickleObj
from .session import anyAuthenticatedSession as untypedAnyAuthenticatedSession
from .helpers import RuntimeFile, RuntimePythonProps, RuntimeType
from .ux import makeHtmlTable, TableHeader, codeStyle


def anyAuthedModelbitCore():
  clientSession = cast(Union[Any, None], untypedAnyAuthenticatedSession())
  if clientSession:
    return cast(ModelbitCore, clientSession._mbCore)
  return None


class RuntimeStatusNotes:

  def __init__(self, deployable: bool, notes: List[str]):
    self.deployable = deployable
    self.notes = notes

  def statusMsg(self):
    if self.deployable:
      return 'Ready'
    return 'Not Ready'

  def statusStyle(self):
    if self.deployable:
      return "color:green; font-weight: bold;"
    return "color:gray; font-weight: bold;"


class NamespaceCollection:

  def __init__(self):
    self.functions: Dict[str, str] = {}
    self.vars: Dict[str, Any] = {}
    self.imports: Dict[str, str] = {}
    self.froms: Dict[str, str] = {"*": "typing"}


class Runtime:
  _runtimeTypeName = "runtime"
  ALLOWED_PY_VERSIONS = ['3.6', '3.7', '3.8', '3.9']

  MAX_REQUIREMENTS_TXT = 20_000
  LAMBDA_RAM_MAX_MB = 10_240
  LAMBDA_RAM_MIN_MB = 128

  def __init__(self,
               rtType: RuntimeType,
               name: Union[str, None] = None,
               main_function: Union[Callable[..., Any], None] = None,
               python_version: Union[str, None] = None,
               requirements_txt_filepath: Union[str, None] = None,
               requirements_txt_contents: Union[List[str], None] = None,
               source_override: Union[str, None] = None):
    self._requirementsTxt: Union[str, None] = None
    self._deployName: Union[str, None] = None
    self._deployFunc: Union[Callable[..., Any], None] = None
    self._pythonVersion = '3.8'  # Default version
    self.rtType: RuntimeType = rtType
    self._sourceOverride = source_override
    if name:
      self.set_name(name)
    if main_function:
      self._set_main_function(main_function)
    if python_version:
      self.set_python_version(python_version)
    if requirements_txt_filepath:
      self.set_requirements_txt(filepath=requirements_txt_filepath)
    if requirements_txt_contents:
      self.set_requirements_txt(contents=requirements_txt_contents)

  def _repr_html_(self):
    return self._describeHtml()

  def set_name(self, name: str):
    if not re.match('^[a-zA-Z0-9_]+$', name):
      raise Exception("Names should be alphanumeric with underscores.")
    self._deployName = name
    return self

  def set_python_version(self, version: str):
    if version not in self.ALLOWED_PY_VERSIONS:
      return self._selfError(f'Python version should be one of {self.ALLOWED_PY_VERSIONS}.')
    self._pythonVersion = version
    return self

  # Doesn't work in VSCode. Need to resolve that before re-enabling this path.
  # def _filepicker_requirements_txt(self):
  #   upload = ipywidgets.FileUpload(accept='.txt', multiple=False)
  #   out = ipywidgets.Output()
  #   display(out)
  #   out.append_display_data(upload) # type: ignore
  #   def onUploadChange(change: Dict[str, str]):
  #     updatedRequirementsTxt = False
  #     if not hasattr(change, 'new') or type(change['new']) is not dict: return
  #     newContent = cast(Dict[str, Any], change['new'])
  #     for v in newContent.values():
  #       if type(v) is not dict: continue
  #       rawContent: bytes = v['content']
  #       if type(rawContent) != bytes: continue
  #       content = rawContent.decode('utf-8')
  #       if len(content) < self.MAX_REQUIREMENTS_TXT:
  #         updatedRequirementsTxt = True
  #         self._requirementsTxt = content
  #       else:
  #         out.append_display_data(Markdown("The requirements.txt file is too large.")) # type: ignore
  #     if updatedRequirementsTxt:
  #       upload.add_class("lm-mod-hidden") # type: ignore
  #       out.append_display_data(Markdown(self._describe())) # type: ignore
  #   upload.observe(onUploadChange) # type: ignore
  #   return None

  def set_requirements_txt(self, filepath: Union[str, None] = None, contents: Union[List[str], None] = None):
    # if filepath == None and contents == None:
    # return self._filepicker_requirements_txt()
    lines: List[str] = []
    if filepath != None and type(filepath) == str:
      f = open(filepath, "r")
      lines = [n.strip() for n in f.readlines()]
    elif contents != None:
      if type(contents) != list:
        printError("The contents parameter must be list of strings.")
        return
      lines = contents
    requirementsTxt = "\n".join(lines)
    if len(requirementsTxt) > self.MAX_REQUIREMENTS_TXT:
      printError("The requirements list is too large.")
      return
    self._requirementsTxt = requirementsTxt
    mbMain = anyAuthedModelbitCore()
    if mbMain:
      mbMain.getJson(
          "jupyter/v1/runtimes/prep_environment",
          {"environment": {
              "requirementsTxt": self._requirementsTxt,
              "pythonVersion": self._pythonVersion
          }})
    return self

  def _set_main_function(self, func: Callable[..., Any]):
    self._deployFunc = func
    if callable(func) and self._deployName == None:
      self.set_name(func.__name__)
    return self

  def train(self, mbMain: Union[ModelbitCore, None] = None):
    self.deploy(mbMain)

  def deploy(self, mbMain: Union[ModelbitCore, None] = None):
    if not mbMain:
      mbMain = anyAuthedModelbitCore()
    if not mbMain:
      printError("Unable to continue because session isn't authenticated.")
      return self

    status = self._getStatusNotes()
    rtProps, errors = self._getFuncProps()
    if not status.deployable or len(errors) > 0:
      printError("Unable to continue because errors are present.")
      return self

    sourceFile = self._makeSourceFile(rtProps)
    valueFiles = self._makeValueFiles(rtProps, mbMain)
    printHtml(f"Sending {self._runtimeTypeName}...")
    resp = mbMain.getJsonOrPrintError(
        "jupyter/v1/runtimes/create", {
            "runtime": {
                "name": self._deployName,
                "type": self.rtType.value,
                "pyState": {
                    "sourceFile": sourceFile.asDict(),
                    "valueFiles": [vf.asDict() for vf in valueFiles],
                    "name": rtProps.name,
                    "module": self._sourceFileName(),
                    "argNames": rtProps.argNames,
                    "argTypes": rtProps.argTypes,
                    "requirementsTxt": self._requirementsTxt,
                    "pythonVersion": self._pythonVersion
                }
            }
        })
    if not resp:
      printHtml(f'Error processing request: no response from server.')
    elif resp.error:
      printHtml(f'Error processing request: {html.escape(resp.error)}')
    elif resp.runtimeOverviewUrl:
      if resp.message:
        printHtml(html.escape(resp.message))
      message = "View status and integration options."
      printHtml(f'<a href="{resp.runtimeOverviewUrl}" target="_blank">{message}</a>')
    else:
      printHtml(f"Unknown error while processing request (server response in unexpected format).")
    return None

  def _sourceFileName(self):
    return "source"

  def _makeSourceFile(self, pyProps: RuntimePythonProps):

    def addSpacer(strList: List[str]):
      if len(strList) > 0 and strList[-1] != "":
        strList.append("")

    sourceParts: List[str] = ["import modelbit, sys"]

    if pyProps.namespaceFroms:
      for iAs, iModule in pyProps.namespaceFroms.items():
        sourceParts.append(f"from {iModule} import {iAs}")
    if pyProps.namespaceImports:
      for iAs, iModule in pyProps.namespaceImports.items():
        sourceParts.append(f"import {iModule} as {iAs}")
    addSpacer(sourceParts)

    if pyProps.namespaceVars and pyProps.namespaceVarsDesc:
      for nName, _ in pyProps.namespaceVars.items():
        sourceParts.append(f'{nName} = modelbit.load_value("{nName}") # {pyProps.namespaceVarsDesc[nName]}')

    addSpacer(sourceParts)
    if pyProps.namespaceFunctions:
      for _, fSource in pyProps.namespaceFunctions.items():
        sourceParts.append(fSource)
        addSpacer(sourceParts)

    addSpacer(sourceParts)
    if pyProps.source:
      sourceParts.append("# main function")
      sourceParts.append(pyProps.source)

    sourceParts.append("# to run locally via git & terminal")
    sourceParts.append('if __name__ == "__main__":')
    sourceParts.append(f"  print({pyProps.name}(*sys.argv[1:]))")
    return RuntimeFile(f"{self._sourceFileName()}.py", "\n".join(sourceParts))

  def _makeValueFiles(self, pyState: RuntimePythonProps, mbMain: ModelbitCore):
    valueFiles: List[RuntimeFile] = []
    if pyState.namespaceVars and pyState.namespaceVarsDesc:
      for nName, nVal in pyState.namespaceVars.items():
        # TODO: handle nVal that are too big
        valueFiles.append(RuntimeFile(f"{nName}.pkl", pickleObj(nVal)))
    return valueFiles

  def _selfError(self, txt: str):
    printError(txt)
    return None

  def _describeHtml(self):
    nonStr = '(None)'

    def codeWrap(txt: str):
      if txt == nonStr:
        return nonStr
      return self._wrapStyle(html.escape(txt), codeStyle())

    status = self._getStatusNotes()
    statusWithStyle = self._wrapStyle(status.statusMsg(), status.statusStyle())
    funcProps, _ = self._getFuncProps()

    headerLines: List[str] = []
    if self._deployName != None:
      headerLines.append(f'<div style="font-weight: bold;">{html.escape(self._deployName)}</div>')
    headerLines.append(f'<div>Status: {statusWithStyle}</div>')
    if len(status.notes) > 0:
      headerLines.append('<ul>')
      for note in status.notes:
        headerLines.append(f'<li>{note}</li>')
      headerLines.append('</ul>')

    headers = [
        TableHeader("Property", TableHeader.LEFT),
        TableHeader("Value", TableHeader.LEFT, skipEscaping=True),
    ]
    rows: List[List[str]] = []

    funcSig = nonStr
    if funcProps.name and funcProps.argNames:
      funcSig = f"{funcProps.name}({', '.join(funcProps.argNames)})"
    rows.append(["Function", codeWrap(funcSig)])

    if funcProps.namespaceFunctions and len(funcProps.namespaceFunctions) > 0:
      nsFuncs = "<br/>".join([codeWrap(k) for k, _ in funcProps.namespaceFunctions.items()])
      rows.append(["Helpers", nsFuncs])

    if funcProps.namespaceVarsDesc and len(funcProps.namespaceVarsDesc) > 0:
      nsVars = "<br/>".join([codeWrap(f'{k}: {v}') for k, v in funcProps.namespaceVarsDesc.items()])
      rows.append(["Values", nsVars])

    nsImports: List[str] = []
    if funcProps.namespaceFroms and len(funcProps.namespaceFroms) > 0:
      for k, v in funcProps.namespaceFroms.items():
        nsImports.append(codeWrap(f'from {v} import {k}'))
    if funcProps.namespaceImports and len(funcProps.namespaceImports) > 0:
      for k, v in funcProps.namespaceImports.items():
        nsImports.append(codeWrap(f'import {v} as {k}'))
    if len(nsImports) > 0:
      rows.append(["Imports", '<br/>'.join(nsImports)])

    rows.append(["Python Version", codeWrap(self._pythonVersion)])

    if self._requirementsTxt and len(self._requirementsTxt) > 0:
      depsList = self._requirementsTxt.splitlines()
      maxDepsShown = 7
      if len(depsList) > maxDepsShown:
        deps = "<br/>".join([codeWrap(d) for d in depsList[:maxDepsShown]])
        numLeft = len(depsList) - maxDepsShown
        deps += f'<br/><span style="font-style: italic;">...and {numLeft} more.</span>'
      else:
        deps = "<br/>".join([codeWrap(d) for d in depsList])
      rows.append(["requirements.txt", deps])

    return "".join(headerLines) + makeHtmlTable(headers, rows)

  def _getFuncProps(self):
    errors: List[str] = []
    props: RuntimePythonProps = RuntimePythonProps()
    if not callable(self._deployFunc):
      errors.append('The main_function parameter does not appear to be a function.')
    else:
      props.name = self._deployFunc.__name__
      props.source = self.getFuncSource()
      props.argNames = self.getFuncArgNames()
      props.argTypes = self._annotationsToTypeStr(self._deployFunc.__annotations__)
      nsCollection = NamespaceCollection()
      self._collectNamespaceDeps(self._deployFunc, nsCollection)
      props.namespaceFunctions = nsCollection.functions
      props.namespaceVars = nsCollection.vars
      props.namespaceVarsDesc = self._strValues(nsCollection.vars)
      props.namespaceImports = nsCollection.imports
      props.namespaceFroms = nsCollection.froms
    return (props, errors)

  def getFuncSource(self):
    if self._sourceOverride:
      return self._sourceOverride
    if not callable(self._deployFunc):
      return None
    return unindent(inspect.getsource(self._deployFunc))

  def getFuncArgNames(self):
    argSpec = inspect.getfullargspec(self._deployFunc)
    if argSpec.varargs:
      return ['...']
    if argSpec.args:
      return argSpec.args
    noArgs: List[str] = []
    return noArgs

  def _annotationsToTypeStr(self, annotations: Dict[str, Any]):
    annoStrs: Dict[str, str] = {}
    for name, tClass in annotations.items():
      try:
        if tClass == Any:
          annoStrs[name] = "Any"
        else:
          annoStrs[name] = tClass.__name__
      except:
        pass
    return annoStrs

  def _collectNamespaceDeps(self, func: Callable[..., Any], collection: NamespaceCollection):
    if not callable(func):
      return collection
    globalsDict = func.__globals__  # type: ignore
    allNames = func.__code__.co_names + func.__code__.co_freevars
    for maybeFuncVarName in allNames:
      if maybeFuncVarName in globalsDict:
        maybeFuncVar = globalsDict[maybeFuncVarName]
        if "__module__" in dir(maybeFuncVar):
          if maybeFuncVar.__module__ == "__main__":  # the user's functions
            argNames = list(maybeFuncVar.__code__.co_varnames or [])
            funcSig = f"{maybeFuncVar.__name__}({', '.join(argNames)})"
            if funcSig not in collection.functions:
              collection.functions[funcSig] = inspect.getsource(maybeFuncVar)
              self._collectNamespaceDeps(maybeFuncVar, collection)
          else:  # functions imported by the user from elsewhere
            if inspect.isclass(maybeFuncVar):
              collection.froms[maybeFuncVarName] = maybeFuncVar.__module__
            elif callable(maybeFuncVar):
              collection.froms[maybeFuncVarName] = maybeFuncVar.__module__
            elif isinstance(maybeFuncVar, object):
              collection.froms[maybeFuncVar.__class__.__name__] = maybeFuncVar.__module__
              collection.vars[maybeFuncVarName] = maybeFuncVar
            else:
              collection.froms[maybeFuncVarName] = f"NYI: {maybeFuncVar.__module__}"
        elif str(maybeFuncVar).startswith('<module'):
          collection.imports[maybeFuncVarName] = maybeFuncVar.__name__
        else:
          collection.vars[maybeFuncVarName] = maybeFuncVar

  def _getStatusNotes(self):
    notes: List[str] = []
    if not self._deployName:
      cmd = self._wrapStyle(".set_name('name')", codeStyle())
      notes.append(f'Run {cmd} to specify the {self._runtimeTypeName}\'s name.')
    if not self._deployFunc:
      funcName = "set_deploy_function"
      cmd = self._wrapStyle("." + funcName + "(func, args = {\"arg1\": value1, ...})", codeStyle())
      notes.append(f'Run {cmd} to specify the {self._runtimeTypeName}\'s runtime.')
    else:
      _, errors = self._getFuncProps()
      if len(errors) > 0:
        notes.extend(errors)
    if len(notes) > 0:
      return RuntimeStatusNotes(False, notes)
    else:
      cmd = self._wrapStyle("mb.deploy(...)", codeStyle())
      notes.append(f'Run {cmd} to send this function to Modelbit.')
      return RuntimeStatusNotes(True, notes)

  def _wrapStyle(self, text: str, style: str):
    return f'<span style="{style}">{html.escape(text)}</span>'

  def _strValues(self, args: Dict[str, Any]):
    newDict: Dict[str, str] = {}
    for k, v in args.items():
      newDict[k] = re.sub(r'\s+', " ", str(v))
    return newDict


class Deployment(Runtime):
  _runtimeTypeName = "deployment"

  def __init__(self,
               name: Union[str, None] = None,
               deploy_function: Union[Callable[..., Any], None] = None,
               python_version: Union[str, None] = None,
               requirements_txt_filepath: Union[str, None] = None,
               requirements_txt_contents: Union[List[str], None] = None,
               source_override: Union[str, None] = None):
    Runtime.__init__(self,
                     RuntimeType.Deployment,
                     name=name,
                     main_function=deploy_function,
                     python_version=python_version,
                     requirements_txt_filepath=requirements_txt_filepath,
                     requirements_txt_contents=requirements_txt_contents,
                     source_override=source_override)

  def set_deploy_function(self, func: Callable[..., Any]):
    self._set_main_function(func)
