from typing import List, Dict

from .utils import formatImageTag, timeago
from .helpers import RuntimeInfo
from .modelbit_core import ModelbitCore
from .ux import makeHtmlTable, TableHeader


class Deployments:

  def __init__(self, mbMain: ModelbitCore):
    self._mbMain = mbMain
    self._deployments: List[RuntimeInfo] = []
    resp = self._mbMain.getJsonOrPrintError("jupyter/v1/runtimes/list?runtimeType=Deployment")
    if resp and resp.deployments:
      self._deployments = resp.deployments

  def _repr_html_(self):
    return self._makeDeploymentsHtmlTable()

  def _makeDeploymentsHtmlTable(self):
    from collections import defaultdict

    if len(self._deployments) == 0:
      return "There are no deployments to show."
    deploymentsByName: Dict[str, List[RuntimeInfo]] = defaultdict(lambda: [])
    for d in self._deployments:
      deploymentsByName[d.name].append(d)

    headers = [
        TableHeader("Name", TableHeader.LEFT),
        TableHeader("Owner", TableHeader.CENTER, skipEscaping=True),
        TableHeader("Status", TableHeader.LEFT),
        TableHeader("Version", TableHeader.RIGHT),
        TableHeader("Deployed", TableHeader.LEFT),
    ]
    rows: List[List[str]] = []
    for dList in deploymentsByName.values():
      ld = dList[0]
      versionCount = len(dList)
      connectedAgo = timeago(ld.createdAtMs)
      ownerImageTag = formatImageTag(ld.ownerInfo.imageUrl, ld.ownerInfo.name)
      rows.append([ld.name, ownerImageTag, str(ld.environmentStatus), str(versionCount), connectedAgo])
    return makeHtmlTable(headers, rows)
