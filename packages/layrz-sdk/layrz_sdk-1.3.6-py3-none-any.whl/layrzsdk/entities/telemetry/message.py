""" Message entity """
class Message:
  """
  Message definition

  Available attributes
  --------------------
    pk (int): Message ID
    asset_id (int): Asset ID
    position (Position): Geographic position
    payload (dict): Message raw payload
    sensors (dict): Calculated sensor values
    received_at (datetime(tzinfo=pytz.UTC)): Message reception date and time
  """

  def __init__(self, pk, asset_id, position, payload, sensors, received_at):
    """ Constructor """
    self.__pk = pk
    self.__asset_id = asset_id
    self.__position = position
    self.__payload = payload
    self.__sensors = sensors
    self.__received_at = received_at

  @property
  def pk(self):
    """ Message ID """
    return self.__pk

  @property
  def asset_id(self):
    """ Asset ID """
    return self.__asset_id

  @property
  def position(self):
    """ Geographic position """
    return self.__position

  @property
  def payload(self):
    """ Message raw payload """
    return self.__payload

  @property
  def sensors(self):
    """ Calculated sensor values """
    return self.__sensors

  @property
  def received_at(self):
    """ Message reception date and time """
    return self.__received_at
