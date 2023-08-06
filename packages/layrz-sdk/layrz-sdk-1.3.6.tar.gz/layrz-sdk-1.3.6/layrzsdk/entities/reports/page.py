""" Report page """

class ReportPage:
  """
  Report page definition

  Available attributes
  --------------------
    name (str): Name of the page. Length should be less than 60 characters
    headers (list(ReportHeader)): Headers of the page
    rows (list(ReportRow)): Rows of the page
  """
  def __init__(self, name, headers, rows):
    self.__name = name
    self.__headers = headers
    self.__rows = rows

  @property
  def name(self):
    """ Name of the page. Length should be less than 60 characters """
    return self.__name

  @property
  def headers(self):
    """ Headers of the page """
    return self.__headers

  @property
  def rows(self):
    """ Rows of the page """
    return self.__rows

  def __str__(self):
    """ Readable property """
    return f'ReportPage(name={self.name}, headers={self.headers}, rows={self.rows})'

  def __repr__(self):
    """ Readable property """
    return f'ReportPage(name={self.name}, headers={self.headers}, rows={self.rows})'
