""" Broadcast result """

class BroadcastResult:
  """
  Broadcast result

  Available attributes
  --------------------
    service_id (int): Service ID
    asset_id (int): Asset ID
    status (BroadcastStatus): Status
    request (BroadcastRequest): Request data sent to the service
    response (BroadcastResponse): Response data came from the service
    submitted_at (datetime): Date of submission
  """
  def __init__(self, service_id, asset_id, status, request, response, submitted_at):
    self.__service_id = service_id
    self.__asset_id = asset_id
    self.__status = status
    self.__request = request
    self.__response = response
    self.__submitted_at = submitted_at

  @property
  def service_id(self):
    """ Service ID """
    return self.__service_id

  @property
  def asset_id(self):
    """ Asset ID """
    return self.__asset_id

  @property
  def status(self):
    """ Status """
    return self.__status

  @property
  def request(self):
    """ Request data sent to the service """
    return self.__request

  @property
  def response(self):
    """ Response data came from the service """
    return self.__response

  @property
  def submitted_at(self):
    """ Date of submission """
    return self.__submitted_at

  @property
  def __readable(self):
    """ Readable """
    return f'BroadcastResult(service_id={self.service_id}, asset_id={self.asset_id}, status={self.status}, request={self.request}, response={self.response}, submitted_at={self.submitted_at})'

  def __repr__(self):
    """ Readable property """
    return self.__readable

  def __str__(self):
    """ Readable property """
    return self.__readable
