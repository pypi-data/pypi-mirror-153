""" Report row """
from ..formatting.text_align import TextAlignment

class ReportRow:
  """
  Report row definition

  Available attributes
  --------------------
    content (list(ReportCol)): Cols to display
    height (float): Height of the cell, in points (pt)
    compact (bool): Compact mode
  """
  def __init__(self, content, height=14, compact=False):
    self.__content = content
    self.__height = height
    self.__compact = compact

  @property
  def content(self):
    """ Cols """
    return self.__content

  @property
  def height(self):
    """ Height of the cell, in points (pt) """
    return self.__height

  @property
  def compact(self):
    """ Compact mode """
    return self.__compact

  def __str__(self):
    """ Readable property """
    return f'ReportRow(content={self.content}, height={self.height}, compact={self.compact})'

  def __repr__(self):
    """ Readable property """
    return f'ReportRow(content={self.content}, height={self.height}, compact={self.compact})'