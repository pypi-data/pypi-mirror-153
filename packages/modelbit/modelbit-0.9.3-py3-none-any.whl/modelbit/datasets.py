from typing import Union, Any, List, cast
import pandas
from urllib.parse import quote_plus

from .utils import formatImageTag, sizeOfFmt, timeago
from .helpers import DatasetDesc
from .modelbit_core import ModelbitCore
from .secure_storage import getSecureData
from .ux import makeHtmlTable, TableHeader


class Datasets:

  def __init__(self, mbMain: ModelbitCore):
    self._mbMain = mbMain
    self._datasets: List[DatasetDesc] = []
    self._iter_current = -1
    resp = self._mbMain.getJsonOrPrintError("jupyter/v1/datasets/list")
    if resp and resp.datasets:
      self._datasets = resp.datasets

  def _repr_html_(self):
    return self._makeDatasetsHtmlTable()

  def __iter__(self):
    return self

  def __next__(self) -> str:
    self._iter_current += 1
    if self._iter_current < len(self._datasets):
      return self._datasets[self._iter_current].name
    raise StopIteration

  def _makeDatasetsHtmlTable(self):
    if len(self._datasets) == 0:
      return "There are no datasets to show."
    headers = [
        TableHeader("Name", TableHeader.LEFT),
        TableHeader("Owner", TableHeader.CENTER, skipEscaping=True),
        TableHeader("Data Refreshed", TableHeader.RIGHT),
        TableHeader("SQL Updated", TableHeader.RIGHT),
        TableHeader("Rows", TableHeader.RIGHT),
        TableHeader("Bytes", TableHeader.RIGHT),
    ]
    rows: List[List[str]] = []
    for d in self._datasets:
      rows.append([
          d.name,
          formatImageTag(d.ownerInfo.imageUrl, d.ownerInfo.name),
          timeago(d.recentResultMs) if d.recentResultMs != None else '',
          timeago(d.sqlModifiedAtMs) if d.sqlModifiedAtMs != None else '',
          self._fmt_num(d.numRows),
          sizeOfFmt(d.numBytes)
      ])
    return makeHtmlTable(headers, rows)

  def get(self, dsName: str):
    data = self._mbMain.getJsonOrPrintError(f'jupyter/v1/datasets/get?dsName={quote_plus(dsName)}')
    if data and data.dsrDownloadInfo:
      stStream = getSecureData(data.dsrDownloadInfo, dsName)
      df = cast(pandas.DataFrame,
                pandas.read_csv(stStream, sep='|', low_memory=False, na_values=['\\N',
                                                                                '\\\\N']))  # type: ignore
      return df

  def _fmt_num(self, num: Union[int, Any]):
    if type(num) != int:
      return ""
    return format(num, ",")
