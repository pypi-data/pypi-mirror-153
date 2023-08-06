""" Sensor entity """

class Sensor:
  """
  Sensor entity

  Available attributes
  --------------------
    pk (int): Sensor ID
    name (str): Name of the sensor
    slug (str): Slug of the sensor
  """

  def __init__(self, pk, name, slug):
    """ Constructor """
    self.__pk = pk
    self.__name = name
    self.__slug = slug

  @property
  def pk(self):
    """ Sensor ID """
    return self.__pk

  @property
  def name(self):
    """ Name of the sensor """
    return self.__name

  @property
  def slug(self):
    """ Slug of the sensor """
    return self.__slug

  @property
  def __readable(self):
    """ Readable """
    return f'Sensor(pk={self.__pk}, name="{self.__name}", slug="{self.__slug}")'

  def __str__(self):
    """ Readable property """
    return self.__readable

  def __repr__(self):
    """ Readable property """
    return self.__readable
