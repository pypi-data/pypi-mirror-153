from typing import List
import html


def codeStyle():
  return "font-family: monospace; font-size: 0.95em; font-weight: medium; color: #714488;"


class TableHeader:
  LEFT = 'left'
  CENTER = 'center'
  RIGHT = 'right'

  def __init__(self, name: str, alignment: str = LEFT, skipEscaping: bool = False):
    self.name = name
    self.alignment = alignment
    self.skipEscaping = skipEscaping
    if self.alignment not in [self.LEFT, self.CENTER, self.RIGHT]:
      raise Exception(f'Unrecognized alignment: {self.alignment}')

  def alignStyle(self):
    return f'text-align:{self.alignment};'

  def maybeEscape(self, val: str):
    return (val if self.skipEscaping else html.escape(val))


def makeHtmlTable(headers: List[TableHeader], rows: List[List[str]]) -> str:
  lines: List[str] = []
  lines.append('<table>')

  lines.append('<thead>')
  for header in headers:
    lines.append(f'<th style="{header.alignStyle()}">{html.escape(header.name)}</th>')
  lines.append('</thead>')

  lines.append('<tbody>')
  for row in rows:
    lines.append('<tr>')
    for i in range(len(row)):
      lines.append(f'<td style="{headers[i].alignStyle()}">{headers[i].maybeEscape(row[i])}</td>')
    lines.append('</tr>')
  lines.append('</tbody>')

  lines.append('</table>')
  return "".join(lines)
