""" Chart exceptions """
class ChartException(BaseException):
  """
  Chart Exception
  """
  def __init__(self, message):
    """ Constructor """
    self.__message = message

  @property
  def __readable(self):
    """ Readable """
    return f'ChartException: {self.__message}'

  def __str__(self):
    """ Readable property """
    return self.__readable

  def __repr__(self):
    """ Readable property """
    return self.__readable
