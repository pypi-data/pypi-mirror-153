""" Device entitiy """

class Device:
  """
  Device definition

  Available attributes
  --------------------
    pk (int): Device ID
    name (str): Name of the device
    ident (str): Unique identifier of the device.
    protocol (str): Protocol slug of the device.
    is_primary (bool): True if this device is the primary device of the asset.
  """

  def __init__(self, pk, name, ident, protocol, is_primary=False):
    """ Constructor """
    self.__pk = pk
    self.__name = name
    self.__ident = ident
    self.__protocol = protocol
    self.__is_primary = is_primary

  @property
  def pk(self):
    """ Device ID """
    return self.__pk

  @property
  def name(self):
    """ Name of the device """
    return self.__name

  @property
  def ident(self):
    """ Unique identifier of the device """
    return self.__ident

  @property
  def protocol(self):
    """ Protocol slug of the device """
    return self.__protocol

  @property
  def is_primary(self):
    """ True if this device is the primary device of the asset """
    return self.__is_primary

  @property
  def __readable(self):
    """ Readable """
    return f'Device(pk={self.__pk}, ident="{self.__ident}", name="{self.__name}", protocol="{self.__protocol}", is_primary={self.__is_primary})'

  def __str__(self):
    """ Readable property """
    return self.__readable

  def __repr__(self):
    """ Readable property """
    return self.__readable