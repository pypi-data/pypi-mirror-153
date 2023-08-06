""" HTML chart """
from .alignment import ChartAlignment
from .exceptions import ChartException


class HTMLChart:
  """
  HTML chart configuration
  """

  def __init__(self, content='<p>N/A</p>', title='Chart', align=ChartAlignment.CENTER):
    """
    Constructor

    Args
    ----
      content (str): HTML content of the chart.
      title (str): Title of the chart.
      align (ChartAlignment): Alignment of the chart.
    """
    if not isinstance(content, str):
      raise ChartException(f'content must be an instance of str')
    self.__content = content

    if not isinstance(title, str):
      raise ChartException('title must be an instance of str')
    self.__title = title

    if not isinstance(align, ChartAlignment):
      raise ChartException('align must be an instance of ChartAlignment')
    self.__align = align

  @property
  def content(self):
    """ HTML content of the chart """
    return self.__content

  @property
  def title(self):
    """ Title of the chart """
    return self.__title

  def render(self):
    """
    Render chart to a Javascript Library.
    Currently only available for HTML.
    """
    return {
      'library': 'HTML',
      'configuration': self.__render_html()
    }

  def __render_html(self):
    """
    Converts the configuration of the chart to HTML render engine.
    """
    config = {
      'content': self.__content,
      'title': self.__title
    }

    return config
