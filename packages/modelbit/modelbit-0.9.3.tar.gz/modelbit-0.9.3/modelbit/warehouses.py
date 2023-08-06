from typing import List

from .helpers import GenericWarehouse
from .modelbit_core import ModelbitCore
from .utils import timeago
from .ux import makeHtmlTable, TableHeader


class Warehouses:

  def __init__(self, mbMain: ModelbitCore):
    self._mbMain = mbMain
    self._warehouses: List[GenericWarehouse] = []
    resp = self._mbMain.getJsonOrPrintError("jupyter/v1/warehouses/list")
    if resp and resp.warehouses:
      self._warehouses = resp.warehouses

  def _repr_html_(self):
    return self._makeWarehousesHtmlTable()

  def _makeWarehousesHtmlTable(self):
    if len(self._warehouses) == 0:
      return ""
    headers = [
        TableHeader("Name", TableHeader.LEFT),
        TableHeader("Type", TableHeader.LEFT),
        TableHeader("Connected", TableHeader.LEFT),
        TableHeader("Deploy Status", TableHeader.LEFT),
    ]
    rows: List[List[str]] = []
    for w in self._warehouses:
      connectedAgo = timeago(w.createdAtMs)
      rows.append([w.displayName, str(w.type), connectedAgo, w.deployStatusPretty])
    return makeHtmlTable(headers, rows)
