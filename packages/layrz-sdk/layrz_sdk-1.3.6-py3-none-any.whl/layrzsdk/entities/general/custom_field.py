""" Custom Field entitiy """

class CustomField:
  """
  Custom field definition

  Available attributes
  --------------------
    name (str): Name of the custom field
    value (str): Value of the custom field
  """

  def __init__(self, name, value):
    """ Constructor """
    self.__name = name
    self.__value = value

  @property
  def name(self):
    """ Name of the custom field """
    return self.__name

  @property
  def value(self):
    """ Value of the custom field """
    return self.__value

  @property
  def __readable(self):
    """ Readable """
    return f'CustomField(name="{self.name}", value="{self.value}")'

  def __str__(self):
    """ Readable property """
    return self.__readable

  def __repr__(self):
    """ Readable property """
    return self.__readable