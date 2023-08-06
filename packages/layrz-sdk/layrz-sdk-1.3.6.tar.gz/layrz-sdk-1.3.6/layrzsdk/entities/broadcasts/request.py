""" Broadcast Result Request data """

class BroadcastRequest:
  """
  Broadcast request data
  
  Available attributes
  --------------------
    json (dict|list): Parsed data
    raw (str): Raw data
  """
  def __init__(self, json, raw):
    self.__json = json
    self.__raw = raw
  
  @property
  def json(self):
    """ Parsed data """
    return self.__json

  @property
  def raw(self):
    """ Raw data """
    return self.__raw

  @property
  def __readable(self):
    """ Readable """
    return f'BroadcastRequest(json={self.json}, raw={self.raw})'

  def __repr__(self):
    """ Readable property """
    return self.__readable

  def __str__(self):
    """ Readable property """
    return self.__readable
