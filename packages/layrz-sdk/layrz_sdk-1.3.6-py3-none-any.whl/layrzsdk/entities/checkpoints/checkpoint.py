""" Checkpoints entitites """

class Checkpoint:
  """
  Checkpoint entity definition

  Available attributes
  --------------------
    pk (int): Checkpoint activation ID
    asset_id (int): Asset ID
    waypoints (list(Waypoint)): List of waypoints of the checkpoint
    start_at (datetime): Start date
    end_at (datetime): End date
  """

  def __init__(self, pk, asset_id, waypoints, start_at, end_at):
    """ Constructor """
    self.__pk = pk
    self.__asset_id = asset_id
    self.__waypoints = waypoints
    self.__start_at = start_at
    self.__end_at = end_at

  @property
  def pk(self):
    """ Checkpoint activation ID """
    return self.__pk

  @property
  def asset_id(self):
    """ Asset ID """
    return self.__asset_id

  @property
  def waypoints(self):
    """ List of waypoints of the checkpoint """
    return self.__waypoints

  @property
  def start_at(self):
    """ Start date """
    return self.__start_at

  @property
  def end_at(self):
    """ End date """
    return self.__end_at

  @property
  def __readable(self):
    """ Readable """
    return f'Checkpoint(pk={self.__pk}, asset_id={self.__asset_id}, waypoints={self.__waypoints}, start_at={self.__start_at}, end_at={self.__end_at})'

  def __str__(self):
    """ Readable property """
    return self.__readable

  def __repr__(self):
    """ Readable property """
    return self.__readable
