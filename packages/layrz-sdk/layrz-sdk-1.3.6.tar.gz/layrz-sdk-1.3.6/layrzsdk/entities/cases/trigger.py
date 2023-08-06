""" Trigger entity """
class Trigger:
  """
  Trigger entity definition
  
  Available attributes
  --------------------
    pk (int): Trigger ID
    name (str): Trigger name
    code (str): Trigger code
  """
  
  def __init__(self, pk, name, code):
    """ Constructor """
    self.__pk = pk
    self.__name = name
    self.__code = code
  
  @property
  def pk(self):
    """ Trigger ID """
    return self.__pk
  
  @property
  def name(self):
    """ Trigger name """
    return self.__name
  
  @property
  def code(self):
    """ Trigger code """
    return self.__code
  
  @property
  def __readable(self):
    """ Readable """
    return f'Trigger(pk={self.__pk}, name="{self.__name}", code="{self.__code}")'
  
  def __str__(self):
    """ Readable property """
    return self.__readable
  
  def __repr__(self):
    """ Readable property """
    return self.__readable