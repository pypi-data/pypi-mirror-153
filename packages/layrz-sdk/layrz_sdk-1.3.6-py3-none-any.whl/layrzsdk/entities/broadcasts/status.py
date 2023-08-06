""" Broadcast result Status """
from enum import Enum
from http.client import UNAUTHORIZED

class BroadcastStatus(Enum):
  """ Broadcast result status """
  OK = 'OK'
  BADREQUEST = 'BADREQUEST'
  INTERNALERROR = 'INTERNALERROR'
  UNAUTHORIZED = 'UNAUTHORIZED'
  UNPROCESSABLE = 'UNPROCESSABLE'

  @property
  def __readable(self):
    """ Readable """
    return f'BroadcastStatus.{self.value}'

  def __str__(self):
    """ Readable property """
    return self.__readable

  def __repr__(self):
    """ Readable property """
    return self.__readable