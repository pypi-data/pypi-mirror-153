""" Report formats """
from enum import Enum

class ReportFormat(Enum):
  """
  Report format definition.
  """
  MICROSOFT_EXCEL = 'MICROSOFT_EXCEL'

  @property
  def __readable(self):
    """ Readable """
    return f'ReportFormat.{self.value}'

  def __str__(self):
    """ Readable property """
    return self.__readable

  def __repr__(self):
    """ Readable property """
    return self.__readable
