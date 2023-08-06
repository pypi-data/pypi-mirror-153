""" Event entity """
class Event:
  """
  Event entity definition

  Available attributes
  --------------------
    pk (int): Event ID
    trigger (Trigger): Trigger object that triggered the event
    asset_id (Asset): ID of the Asset owner of the event
    message (Message): Telemetry information of the event
    activated_at (datetime): Reception/triggered at
  """
  
  def __init__(self, pk, trigger, asset_id, message, activated_at):
    """ Constructor """
    self.__pk = pk
    self.__trigger = trigger
    self.__asset_id = asset_id
    self.__message = message
    self.__activated_at = activated_at
  
  @property
  def pk(self):
    """ Event ID """
    return self.__pk
  
  @property
  def trigger(self):
    """ Trigger object that triggered the event """
    return self.__trigger
  
  @property
  def asset_id(self):
    """ Asset owner of the event """
    return self.__asset_id
  
  @property
  def message(self):
    """ Telemetry information of the event """
    return self.__message
  
  @property
  def activated_at(self):
    """ Reception/triggered at """
    return self.__activated_at
  
  @property
  def __readable(self):
    """ Readable """
    return f'Event(pk={self.__pk}, trigger={self.__trigger}, asset_id={self.__asset_id}, message={self.__message}, activated_at={self.__activated_at})'
  
  def __str__(self):
    """ Readable property """
    return self.__readable
  
  def __repr__(self):
    """ Readable property """
    return self.__readable