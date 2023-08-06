""" User entity """
class User:
  """
  User entity definition
  
  Available attributes
  --------------------
    pk (int): User ID
    name (str): User name
  """
  
  def __init__(self, pk, name):
    """ Constructor """
    self.__pk = pk
    self.__name = name
  
  @property
  def pk(self):
    """ User ID """
    return self.__pk
  
  @property
  def name(self):
    """ User name """
    return self.__name

  @property
  def __readable(self):
    """ Readable """
    return f'User(pk={self.__pk}, name="{self.__name}")'
  
  def __str__(self):
    """ Readable property """
    return self.__readable
  
  def __repr__(self):
    """ Readable property """
    return self.__readable