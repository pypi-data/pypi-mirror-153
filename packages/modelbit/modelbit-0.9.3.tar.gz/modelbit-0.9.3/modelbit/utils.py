from typing import Union, Any, cast
import os, io, re, html, pickle, codecs
from IPython import display
from html.parser import HTMLParser
import time


# From https://stackoverflow.com/questions/753052/strip-html-from-strings-in-python
class MLStripper(HTMLParser):

  def __init__(self):
    super().__init__()
    self.reset()
    self.strict = False
    self.convert_charrefs = True
    self.text = io.StringIO()

  def handle_data(self, data: str):
    self.text.write(data)

  def get_data(self):
    return self.text.getvalue()


def _strip_tags(html: str):
  s = MLStripper()
  s.feed(html)
  return s.get_data()


def printHtml(txt: str):
  txtMode = os.getenv('MB_TXT_MODE')
  if txtMode:
    dispText = _strip_tags(txt.replace("<br/>", "\n"))
    display.display(display.TextDisplayObject(dispText))  # type: ignore
  else:
    display.display(display.HTML(f'<div>{txt}</div>'))  # type: ignore


def printError(txt: str):
  printHtml(f'<span style="font-weight: bold; color: #E2548A;">Error:</span> {html.escape(txt)}')


# From https://stackoverflow.com/questions/1094841/get-human-readable-version-of-file-size
def sizeOfFmt(num: Union[int, Any]):
  if type(num) != int:
    return ""
  numLeft: float = num
  for unit in ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB"]:
    if abs(numLeft) < 1000.0:
      return f"{numLeft:3.0f} {unit}"
    numLeft /= 1000.0
  return f"{numLeft:.1f} YB"


def formatImageTag(imageUrl: Union[str, None], imageAltText: Union[str, None]):
  imageUrl = imageUrl if imageUrl else "https://app.modelbit.com/images/profile-placeholder.png"
  return (
      f'<img src="{ imageUrl }" '
      f'alt="{ imageAltText }" '
      f'referrerPolicy="no-referrer" '
      f'height="32" width="32" '  # for hex.tech, they strip style tags
      f'style="display:inline-block;border-radius:9999px;width:2rem;height:2rem;background-color: rgb(229 231 235);" />'
  )


def pandasTypeToPythonType(pandasType: str):
  if pandasType in ['float32', 'float64']:
    return 'float'
  if pandasType in ['int32', 'int64']:
    return 'int'
  if pandasType == 'bool':
    return 'bool'
  return 'Any'


def simplifyArgName(argName: str):
  scrubbed = re.sub("\\W+", "_", argName.lower())
  scrubbed = re.sub('^(\\d+)', "c\\1", scrubbed)
  if scrubbed.endswith("_"):
    scrubbed = scrubbed[:-1]
  return scrubbed


def unindent(source: str) -> str:
  leadingWhitespaces = len(source) - len(source.lstrip())
  if leadingWhitespaces == 0:
    return source
  newLines = [line[leadingWhitespaces:] for line in source.split("\n")]
  return "\n".join(newLines)


def timeago(pastDateMs: int):
  nowMs = time.time() * 1000
  options = [
      {
          "name": "second",
          "divide": 1000
      },
      {
          "name": "minute",
          "divide": 60
      },
      {
          "name": "hour",
          "divide": 60
      },
      {
          "name": "day",
          "divide": 24
      },
      {
          "name": "month",
          "divide": 30.5
      },
  ]
  currentDiff = nowMs - pastDateMs
  if currentDiff < 0:
    raise Exception("The future is NYI")
  resp = "Just now"
  for opt in options:
    currentDiff = round(currentDiff / cast(Union[float, int], opt["divide"]))
    if currentDiff <= 0:
      return resp
    pluralS = ""
    if currentDiff != 1:
      pluralS = "s"
    resp = f"{currentDiff} {opt['name']}{pluralS} ago"
  return resp


def unpickleObj(str64: str):
  return pickle.loads(codecs.decode(str64.encode(), "base64"))


def pickleObj(obj: Any):
  return codecs.encode(pickle.dumps(obj), "base64").decode()
