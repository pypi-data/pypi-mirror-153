""" Scatter chart """
import json
from .exceptions import ChartException
from .alignment import ChartAlignment
from .serie_type import ChartDataSerieType
from .serie import ChartDataSerie

class ScatterSerieItem:
  """
  Chart Data Serie Item for Scatter Charts
  """
  def __init__(self, x, y):
    """
    Constructor

    Args
    ----
      x (any): X value of the item.
      y (any): Y value of the item.
    """
    self.__x = x
    self.__y = y

  @property
  def x(self):
    """ X value """
    return self.__x

  @property
  def y(self):
    """ Y value """
    return self.__y

class ScatterSerie:
  """
  Chart Data Serie for Timeline charts
  """
  def __init__(self, data, color, label):
    """
    Constructor

    Args
    ----
      data list(ScatterSerieItem): List of data points.
      color str: Color of the serie.
      label str: Label of the serie.
    """
    self.__data = data

    if not isinstance(color, str):
      raise ChartException('color must be an instance of str')
    self.__color = color

    if not isinstance(label, str):
      raise ChartException('label must be an instance of str')
    self.__label = label

    self.__serie_type = ChartDataSerieType.SCATTER

  @property
  def data(self):
    """ List of data points """
    return self.__data

  @property
  def color(self):
    """ Color of the serie """
    return self.__color

  @property
  def label(self):
    """ Label of the serie """
    return self.__label

  @property
  def serie_type(self):
    """ Serie type """
    return self.__serie_type

class ScatterChart:
  """
  Scatter chart configuration
  """

  def __init__(self, series, title='Chart', align=ChartAlignment.CENTER):
    """
    Constructor

    Args
    ----
      series list(ScatterSerie): Defines the series of the chart, uses the ScatterSerie class. Please read the documentation to more information.
      title (str): Title of the chart.
      align (ChartAlignment): Alignment of the chart.
    """
    for i, serie in enumerate(series):
      if not isinstance(serie, (ChartDataSerie, ScatterSerie)):
        raise ChartException(f'Y Axis serie {i} must be an instance of ScatterSerie')
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

    With less than 10.000 points (in X Axis), will return ApexCharts configuration. Else will return Google Charts
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
    colors = []

    for serie in self.__series:
      data = []

      for item in serie.data:
        data.append([item.x, item.y])

      series.append({
        'name': serie.label,
        'data': data,
        'type': serie.serie_type.value,
      })
      colors.append(serie.color)

    config = {
      'series': series,
      'colors': colors,
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
        'type': 'scatter',
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
      'dataLabels': {
        'enabled': True
      }
    }

    return config
