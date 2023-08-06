""" Timeline chart entities """
import json
from datetime import datetime
from .alignment import ChartAlignment
from .exceptions import ChartException
from .serie_type import ChartDataSerieType

class TimelineSerieItem:
  """
  Chart Data Serie Item for Timeline Charts
  """
  def __init__(self, name, start_at, end_at, color):
    """
    Constructor

    Args
    ----
      name (str): Name of the item.
      start_at (datetime): Start date of the item.
      end_at (datetime): End date of the item.
      color (str): Color of the item.
    """
    if not isinstance(name, str):
      raise ChartException('name must be an instance of str')
    self.__name = name

    if not isinstance(start_at, datetime):
      raise ChartException('start_at must be an instance of datetime')
    self.__start_at = start_at

    if not isinstance(end_at, datetime):
      raise ChartException('end_at must be an instance of datetime')
    self.__end_at = end_at

    if not isinstance(color, str):
      raise ChartException('color must be an instance of str')
    self.__color = color

  @property
  def name(self):
    """ Name of the item """
    return self.__name

  @property
  def start_at(self):
    """ Start date of the item """
    return self.__start_at

  @property
  def end_at(self):
    """ End date of the item """
    return self.__end_at

  @property
  def color(self):
    """ Color of the item """
    return self.__color

class TimelineSerie:
  """
  Chart Data Serie for Timeline charts
  """
  def __init__(self, data, label):
    """
    Constructor

    Args
    ----
      data list(TimelineSerieItem): List of data points.
      label str: Label of the serie.
    """
    self.__data = data

    if not isinstance(label, str):
      raise ChartException('label must be an instance of str')
    self.__label = label

    self.__serie_type = ChartDataSerieType.TIMELINE

  @property
  def data(self):
    """ List of data points """
    return self.__data

  @property
  def label(self):
    """ Label of the serie """
    return self.__label

  @property
  def serie_type(self):
    """ Serie type """
    return self.__serie_type

class TimelineChart:
  """
  Timeline chart configuration
  """

  def __init__(self, series, title='Chart', align=ChartAlignment.CENTER):
    """
    Constructor

    Args
    ----
      series list(TimelineSerie): Defines the series of the chart, uses the TimelineSerie class. Please read the documentation to more information.
      title (str): Title of the chart.
      align (ChartAlignment): Alignment of the chart.
    """
    for i, serie in enumerate(series):
      if not isinstance(serie, TimelineSerie):
        raise ChartException(f'Y Axis serie {i} must be an instance of TimelineSerie')
    self.__series = series

    if not isinstance(title, str):
      raise ChartException('title must be an instance of str')
    self.__title = title

    if not isinstance(align, ChartAlignment):
      raise ChartException('align must be an instance of ChartAlignment')
    self.__align = align

  @property
  def series(self):
    """ Series of the chart """
    return self.__series

  @property
  def title(self):
    """ Title of the chart """
    return self.__title

  def render(self):
    """
    Render chart to a Javascript Library.
    Currently only available for ApexCharts.
    """
    return {
      'library': 'APEXCHARTS',
      'configuration': self.__render_apexcharts()
    }

  def __render_apexcharts(self):
    """
    Converts the configuration of the chart to Javascript library ApexCharts.
    """

    series = []

    for serie in self.__series:
      data = []

      for item in serie.data:
        data.append({
          'x': item.name,
          'y': [
            item.start_at.timestamp() * 1000,
            item.end_at.timestamp() * 1000
          ],
          'fillColor': item.color
        })

      series.append({
        'name': serie.label,
        'data': data
      })

    config = {
      'series': series,
      'title': {
        'text': self.__title,
        'align': self.__align.value,
        'style': {
          'fontFamily': 'Fira Sans Condensed',
          'fontSize': '20px',
          'fontWeight': 'normal'
        }
      },
      'chart': {
        'type': 'rangeBar',
        'animations': {
          'enabled': False
        },
        'toolbar': {
          'show': False
        },
        'zoom': {
          'enabled': False
        }
      },
      'xaxis': {
        'type': 'datetime'
      },
      'plotOptions': {
        'bar': {
          'horizontal': True,
        }
      },
      'dataLabels': {
        'enabled': True
      }
    }

    return config
