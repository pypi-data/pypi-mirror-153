""" Column chart """
import json
from .alignment import ChartAlignment
from .exceptions import ChartException
from .serie import ChartDataSerie
from .serie_type import ChartDataSerieType
from .scatter import ScatterSerie
from layrzsdk.helpers import convert_to_rgba

class ColumnChart:
  """
  Column chart configuration

  """

  def __init__(self, x_axis, y_axis, title='Chart', align=ChartAlignment.CENTER):
    """
    Constructor

    Args
    ----
      x_axis ChartDataSerie: Defines the X Axis of the chart, uses the ChartDataSerie class. Please read the documentation to more information.
      y_axis list(ChartDataSerie): Defines the Y Axis of the chart, uses the ChartDataSerie class. Please read the documentation to more information.
      title (str): Title of the chart
      align (ChartAlignment): Alignment of the title
    """
    for i, serie in enumerate(y_axis):
      if not isinstance(serie, (ChartDataSerie, ScatterSerie)):
        raise ChartException(f'Y Axis serie {i} must be an instance of ChartDataSerie')
    self.__x_axis = x_axis

    if not isinstance(x_axis, ChartDataSerie):
      raise ChartException('X Axis must be an instance of ChartDataSerie')
    self.__y_axis = y_axis

    if not isinstance(title, str):
      raise ChartException('title must be an instance of str')
    self.__title = title

    if not isinstance(align, ChartAlignment):
      raise ChartException('align must be an instance of ChartAlignment')
    self.__align = align

  @property
  def x_axis(self):
    """ X Axis of the chart """
    return self.__x_axis

  @property
  def y_axis(self):
    """ Y Axis of the chart """
    return self.__y_axis

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
    stroke = {
      'width': [],
      'dashArray': []
    }
    markers = []

    for serie in self.__y_axis:
      modified_serie = {
        'name': serie.label,
      }
      if serie.serie_type == ChartDataSerieType.SCATTER:
        modified_serie['data'] = [{'x': item.x, 'y': item.y} for item in serie.data]
        modified_serie['type'] = 'scatter'
        stroke['width'].append(0)
        markers.append(10)
      else:
        modified_serie['data'] = [{'x': self.__x_axis.data[i], 'y': item} for i, item in enumerate(serie.data)]

        if serie.serie_type is not ChartDataSerieType.NONE:
          modified_serie['type'] = serie.serie_type.value
        else:
          modified_serie['type'] = 'column'

        if serie.dashed and serie.serie_type == ChartDataSerieType.LINE:
          stroke['dashArray'].append(5)
        else:
          stroke['dashArray'].append(0)

        stroke['width'].append(3)
        markers.append(0)

      series.append(modified_serie)

      if serie.serie_type == ChartDataSerieType.AREA:
        color = convert_to_rgba(serie.color)
        colors.append(f'rgba({color[0]}, {color[1]}, {color[2]}, 0.5)')
      else:
        colors.append(serie.color)

    config = {
      'series': series,
      'colors': colors,
      'xaxis': {
        'type': self.__x_axis.data_type.value,
        'title': {
          'text': self.__x_axis.label,
          'style': {
            'fontFamily': 'Fira Sans Condensed',
            'fontSize': '20px',
            'fontWeight': 'normal'
          }
        }
      },
      'dataLabels': {
        'enabled': False
      },
      'title': {
        'text': self.__title,
        'align': self.__align.value,
        'style': {
          'fontFamily': 'Fira Sans Condensed',
          'fontSize': '20px',
          'fontWeight': 'normal'
        }
      },
      'markers': {
        'size': markers
      },
      'fill': {
        'type': 'solid'
      },
      'stroke': stroke,
      'chart': {
        'animations': {
          'enabled': False
        },
        'toolbar': {
          'show': False
        },
        'zoom': {
          'enabled': False
        }
      }
    }

    return config