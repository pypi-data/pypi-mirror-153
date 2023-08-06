""" Geofence entity """
class Geofence:
  """
  Geofence entity definition

  Available attributes
  --------------------
    pk (int): Geofence ID
    name (str): Geofence name
    color (str): Geofence color in Hex format
  """

  def __init__(self, pk, name, color):
    """ Constructor """
    self.__pk = pk
    self.__name = name
    self.__color = color

  @property
  def pk(self):
    """ Geofence ID """
    return self.__pk

  @property
  def name(self):
    """ Geofence name """
    return self.__name

  @property
  def color(self):
    """ Geofence color in Hex format """
    return self.__color

  @property
  def __readable(self):
    """ Readable """
    return f'Geofence(pk={self.__pk}, name="{self.__name}", color="{self.__color}")'

  def __str__(self):
    """ Readable property """
    return self.__readable

  def __repr__(self):
    """ Readable property """
    return self.__readable