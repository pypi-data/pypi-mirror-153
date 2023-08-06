""" Report header """
from ..formatting.text_align import TextAlignment

class ReportHeader:
  """
  Report header definition

  Available attributes
  --------------------
    content (str): Display name
    width (float): Column width in points (pt)
    color (str): Cell color
    text_color (str): Text color
    align (TextAlignment): Text Alignment
  """
  def __init__(self, content, width=10, color='#ffffff', text_color='#000000', align=TextAlignment.CENTER):
    self.__content = content
    self.__width = width
    self.__color = color
    self.__text_color = text_color
    self.__align = align

  @property
  def content(self):
    """ Display name """
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
  def width(self):
    """ Column width in points (pt) """
    return self.__width

  def __str__(self):
    """ Readable property """
    return f'ReportHeader(content={self.content}, width={self.width}, color={self.color}, text_color={self.text_color}, align={self.align})'

  def __repr__(self):
    """ Readable property """
    return f'ReportHeader(content={self.content}, width={self.width}, color={self.color}, text_color={self.text_color}, align={self.align})'
