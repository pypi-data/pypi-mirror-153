""" Chart Data Serie """
from .serie_type import ChartDataSerieType
from .data_type import ChartDataType
from .exceptions import ChartException

class ChartDataSerie:
  """
  Chart Serie
  """

  def __init__(self, data, color='#000000', label='', dashed=False, serie_type=ChartDataSerieType.NONE, data_type=ChartDataType.NUMBER):
    """
    Constructor

    Args
    ----
      data (list((float|int|bool))): List of data points.
      color (str): Color of the serie.
      label (str): Label of the serie.
      serie_type (ChartDataSerieType): Type of the serie. Only used for mixed range charts.
      data_type (ChartDataType): Type of the data.
      dashed (bool): If the serie should be dashed.
    """
    self.__data = data

    if not isinstance(color, str):
      raise ChartException('color must be an instance of str')
    self.__color = color

    if not isinstance(label, str):
      raise ChartException('label must be an instance of str')
    self.__label = label

    if not isinstance(data_type, ChartDataType):
      raise ChartException('data_type must be an instance of ChartDataType')
    self.__data_type = data_type

    if not isinstance(serie_type, ChartDataSerieType):
      raise ChartException('serie_type must be an instance of ChartDataSerieType')
    self.__serie_type = serie_type or ChartDataSerieType.NONE

    if not isinstance(dashed, bool):
      raise ChartException('dashed must be an instance of bool')
    self.__dashed = dashed

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
  def data_type(self):
    """ Data type of the serie """
    return self.__data_type

  @property
  def serie_type(self):
    """ Serie type """
    return self.__serie_type

  @property
  def dashed(self):
    """ If the serie should be dashed """
    return self.__dashed