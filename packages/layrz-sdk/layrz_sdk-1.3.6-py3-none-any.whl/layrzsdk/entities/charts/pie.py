""" Pie chart """
import json
from .alignment import ChartAlignment
from .exceptions import ChartException
from .serie import ChartDataSerie

class PieChart:
  """
  Pie chart configuration
  """

  def __init__(self, series, title='Chart', align=ChartAlignment.CENTER):
    """
    Constructor

    Args
    ----
      series list(ChartDataSerie): Defines the series of the chart, uses the ChartDataSerie class. Please read the documentation to more information.
      title (str): Title of the chart.
      align (ChartAlignment): Alignment of the chart.
    """
    for i, serie in enumerate(series):
      if not isinstance(serie, ChartDataSerie):
        raise ChartException(f'Y Axis serie {i} must be an instance of ChartDataSerie')
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
    colors = []
    labels = []

    for serie in self.__series:
      series.append(serie.data[0])
      colors.append(serie.color)
      labels.append(serie.label)

    config = {
      'series': series,
      'colors': colors,
      'labels': labels,
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
        'type': 'pie',
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