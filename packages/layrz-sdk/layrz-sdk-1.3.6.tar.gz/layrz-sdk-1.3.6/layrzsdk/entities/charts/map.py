""" Map chart """
from enum import Enum

from .alignment import ChartAlignment
from .exceptions import ChartException


class MapCenterType(Enum):
  """
  Map Chart center type
  """
  FIXED = 'FIXED'
  CONTAIN = 'CONTAIN'

class MapPoint:
  """ Map point configuration """

  def __init__(self, latitude, longitude, label, color):
    """
    Constructor
    
    Args
    ----
      latitude (float): Latitude of the point
      longitude (float): Longitude of the point
      label (str): Label of the point
      color (str): Color of the point
    """
    if not isinstance(latitude, float):
      raise ChartException('latitude must be an instance of float')
    self.__latitude = latitude
    
    if not isinstance(longitude, float):
      raise ChartException('longitude must be an instance of float')
    self.__longitude = longitude
    
    if not isinstance(label, str):
      raise ChartException('label must be an instance of str')
    self.__label = label
    
    if not isinstance(color, str):
      raise ChartException('color must be an instance of str')
    self.__color = color

  @property
  def latitude(self):
    """ Latitude of the point """
    return self.__latitude

  @property
  def longitude(self):
    """ Longitude of the point """
    return self.__longitude

  @property
  def label(self):
    """ Label of the point """
    return self.__label

  @property
  def color(self):
    """ Color of the point """
    return self.__color

class MapChart:
  """
  Map chart configuration
  """

  def __init__(self, points, title='Chart', align=ChartAlignment.CENTER, center=MapCenterType.CONTAIN, center_latlng=None):
    """
    Constructor
    
    Args
    ----
      points list(MapPoint): Points of the chart
      title (str): Title of the chart
      align (ChartAlignment): Alignment of the title
    """
    for i, point in enumerate(points):
      if not isinstance(point, MapPoint):
        raise ChartException(f'Point {i} must be an instance of MapPoint')
    self.__points = points
    
    if not isinstance(title, str):
      raise ChartException('title must be an instance of str')
    self.__title = title
    
    if not isinstance(align, ChartAlignment):
      raise ChartException('align must be an instance of ChartAlignment')
    self.__align = align
    
    if not isinstance(center, MapCenterType):
      raise ChartException('center must be an instance of MapCenterType')
    self.__center = center

    if self.__center == MapCenterType.FIXED and not isinstance(center_latlng, (list, tuple)):
      raise ChartException('center_latlng must be an instance of list or tuple')
    self.__center_latlng = center_latlng

  @property
  def points(self):
    """ Points of the chart """
    return self.__points

  @property
  def title(self):
    """ Title of the chart """
    return self.__title
  
  @property
  def center(self):
    """ Map Center mode """
    return self.__center

  def render(self):
    """
    Converts the configuration of the chart to HTML render engine.
    """
    config = self.__render_html()
    return config

  def render(self):
    """
    Render chart to a Javascript Library.
    Currently only available for Leaflet.
    """
    return {
      'library': 'LEAFLET',
      'configuration': self.__render_leaflet()
    }

  def __render_leaflet(self):
    """
    Converts the configuration of the chart to Leaflet map engine.
    """
    points = []
    
    for point in self.__points:
      points.append({
        'label': point.label,
        'color': point.color,
        'latlng': (point.latitude, point.longitude)
      })
      
    center = 'CONTAIN'
    
    if self.__center == MapCenterType.FIXED:
      center = 'FIXED'

    config = {
      'points': points,
      'title': self.__title,
      'center': center,
    }
    
    if self.__center == MapCenterType.FIXED:
      config['centerLatLng'] = self.__center_latlng

    return config
