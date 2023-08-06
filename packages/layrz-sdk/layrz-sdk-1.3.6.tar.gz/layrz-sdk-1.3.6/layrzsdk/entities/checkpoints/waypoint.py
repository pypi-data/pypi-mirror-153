""" Waypoint entity """
class Waypoint:
  """
  Checkpoint waypoint entity definition

  Available attributes
  --------------------
    pk (int): Waypoint ID
    geofence (Geofence): Related geofence
    start_at (datetime): Date of start this waypoint stage
    end_at (datetime): Date of end this waypoint stage
    sequence_real (int): Real sequence performed
    sequence_ideal (int): Ideal/defined sequence
  """
  
  def __init__(self, pk, geofence, start_at, end_at, sequence_real, sequence_ideal):
    """ Constructor """
    self.__pk = pk
    self.__geofence = geofence
    self.__start_at = start_at
    self.__end_at = end_at
    self.__sequence_real = sequence_real
    self.__sequence_ideal = sequence_ideal

  @property
  def pk(self):
    """ Waypoint ID """
    return self.__pk

  @property
  def geofence(self):
    """ Related geofence """
    return self.__geofence

  @property
  def start_at(self):
    """ Date of start this waypoint stage """
    return self.__start_at

  @property
  def end_at(self):
    """ Date of end this waypoint stage """
    return self.__end_at

  @property
  def sequence_real(self):
    """ Real sequence performed """
    return self.__sequence_real

  @property
  def sequence_ideal(self):
    """ Ideal/defined sequence """
    return self.__sequence_ideal

  @property
  def __readable(self):
    """ Readable """
    return f'Waypoint(pk={self.__pk}, geofence={self.__geofence}, start_at={self.__start_at}, end_at={self.__end_at}, sequence_real={self.__sequence_real}, sequence_ideal={self.__sequence_ideal})'

  def __str__(self):
    """ Readable property """
    return self.__readable

  def __repr__(self):
    """ Readable property """
    return self.__readable