""" Charts entities """
class ChartConfiguration:
  """
  Chart configuration
  """

  def __init__(self, name, description):
    """ Constructor """
    self.__name = name
    self.__description = description

  @property
  def name(self):
    """ Name of the chart """
    return self.__name

  @property
  def description(self):
    """ Description of the chart """
    return self.__description

  @property
  def __readable(self):
    """ Readable """
    return f'ChartConfiguration(name="{self.__name}")'

  def __str__(self):
    """ Readable property """
    return self.__readable

  def __repr__(self):
    """ Readable property """
    return self.__readable