""" Service entity """

class OutboundService:
  """
  Outbound service definition

  Available attributes
  --------------------
    pk (int): Service ID
    name (str): Service Name
  """
  def __init__(self, pk, name):
    self.__pk = pk
    self.__name = name

  @property
  def pk(self):
    """ Service ID """
    return self.__pk
  
  @property
  def name(self):
    """ Service Name """
    return self.__name

  @property
  def __readable(self):
    """ Readable """
    return f'OutboundService(pk={self.pk}, name={self.name})'

  def __repr__(self):
    """ Readable property """
    return self.__readable

  def __str__(self):
    """ Readable property """
    return self.__readable
