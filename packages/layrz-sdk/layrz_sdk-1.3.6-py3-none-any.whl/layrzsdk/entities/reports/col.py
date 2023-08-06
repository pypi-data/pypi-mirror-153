""" Report col """
from enum import Enum
from ..formatting.text_align import TextAlignment

class ReportDataType(Enum):
  """
  Report date type
  """
  STR = 'str'
  INT = 'int'
  FLOAT = 'float'
  DATETIME = 'datetime'
  BOOL = 'bool'
  CURRENCY = 'currency'

  @property
  def __readable(self):
    """ Readable """
    return f'ReportDataType.{self.value}'

  def __str__(self):
    """ Readable property """
    return self.__readable

  def __repr__(self):
    """ Readable property """
    return self.__readable

class ReportCol:
  """
  Report col definition

  Available attributes
  --------------------
    content (str): Display content
    color (str): Cell color
    text_color (str): Text color
    align (TextAlignment): Text Alignment
    data_type (ReportDataType): Data type
    datetime_format (str): Date time format
    currency_symbol (str): Currency symbol
  """
  def __init__(self, content, color='#ffffff', text_color='#000000', align=TextAlignment.LEFT, data_type=ReportDataType.STR, datetime_format='%Y-%m-%d %H:%M:%S', currency_symbol=''):
    self.__content = content
    self.__color = color
    self.__text_color = text_color
    self.__align = align
    self.__data_type = data_type
    self.__datetime_format = datetime_format
    self.__currency_symbol = currency_symbol

  @property
  def content(self):
    """ Display content """
    return self.__content

  @property
  def color(self):
    """ Cell color """
    return self.__color

  @property
  def text_color(self):
    """ Text color """
    return self.__text_color

  @property
  def align(self):
    """ Text Alignment """
    return self.__align

  @property
  def data_type(self):
    """ Data type """
    return self.__data_type

  @property
  def datetime_format(self):
    """ Date time format """
    return self.__datetime_format
  
  @property
  def currency_symbol(self):
    """ Currency symbol """
    return self.__currency_symbol

  @property
  def __readable(self):
    """ Readable property """
    return f'ReportCol(content={self.content}, color={self.color}, text_color={self.text_color}, align={self.align}, data_type={self.data_type}, datetime_format={self.datetime_format}, currency_symbol={self.currency_symbol})'

  def __repr__(self):
    """ Readable property """
    return self.__readable

  def __str__(self):
    """ Readable property """
    return self.__readable
