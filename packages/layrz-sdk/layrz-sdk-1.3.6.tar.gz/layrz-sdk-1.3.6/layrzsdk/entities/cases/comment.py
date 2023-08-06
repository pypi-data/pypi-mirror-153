""" Comment entity """

class Comment:
  """
  Case comment entity definition

  Available attributes
  --------------------
    pk (int): Comment ID
    content (str): Comment content
    user (User): Operator/User what commented the case
    submitted_at (datetime): Date of comment submission
  """

  def __init__(self, pk, content, user, submitted_at):
    """ Constructor """
    self.__pk = pk
    self.__content = content
    self.__user = user
    self.__submitted_at = submitted_at
  
  @property
  def pk(self):
    """ Comment ID """
    return self.__pk
  
  @property
  def content(self):
    """ Comment content """
    return self.__content
  
  @property
  def user(self):
    """ Operator/User who commented the case """
    return self.__user
  
  @property
  def submitted_at(self):
    """ Date of comment submission """
    return self.__submitted_at

  @property
  def __readable(self):
    """ Readable """
    return f'Comment(pk={self.__pk}, content="{self.__content}", user={self.__user}, submitted_at={self.__submitted_at})'
  
  def __str__(self):
    """ Readable property """
    return self.__readable
  
  def __repr__(self):
    """ Readable property """
    return self.__readable
