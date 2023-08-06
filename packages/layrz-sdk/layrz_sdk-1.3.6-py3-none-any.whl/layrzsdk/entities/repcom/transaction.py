""" Transaction entity """
class Transaction:
  """
  Transaction definition

  Available attributes
  --------------------
    pk (int): Transaction ID
    asset (Asset): Asset related to the transaction
    amount (float): Amount of the transaction
    quantity (float): Quantity of the transaction
    mileage (float): Mileage in kilometers
    distance (float): Distance traveled in kilometers
    engine_time (timedelta): Time with the engine on
    idle_time (timedelta): Time with the engine on without movement
    in_geofence (bool): Flag to indicate if transaction occurred inside a geofence
    geofence_name (str): Name of the geofence where transaction occurred
    received_at (datetime(tzinfo=pytz.UTC)): Transaction reception date and time
    is_wildcard (bool): Wildcard indicator for transaction
  """

  def __init__(self, pk, asset, amount, quantity, mileage, distance, engine_time, idle_time, in_geofence, geofence_name, received_at, is_wildcard):
    """ Constructor """
    self.__pk = pk
    self.__asset = asset
    self.__amount = amount
    self.__quantity = quantity
    self.__mileage = mileage
    self.__distance = distance
    self.__engine_time = engine_time
    self.__idle_time = idle_time
    self.__in_geofence = in_geofence
    self.__geofence_name = geofence_name
    self.__received_at = received_at
    self.__is_wildcard = is_wildcard

  @property
  def pk(self):
    """ Transaction ID """
    return self.__pk

  @property
  def asset(self):
    """ Asset ID """
    return self.__asset

  @property
  def amount(self):
    """ Amount of the transaction """
    return self.__amount

  @property
  def quantity(self):
    """ Quantity of the transaction """
    return self.__quantity

  @property
  def mileage(self):
    """ Mileage in kilometers """
    return self.__mileage

  @property
  def distance(self):
    """ Distance traveled in kilometers """
    return self.__distance

  @property
  def engine_time(self):
    """ Time with the engine on """
    return self.__engine_time

  @property
  def idle_time(self):
    """ Time with the engine on without movement """
    return self.__idle_time

  @property
  def in_geofence(self):
    """ Flag to indicate if transaction occurred inside a geofence """
    return self.__in_geofence

  @property
  def geofence_name(self):
    """ Name of the geofence where transaction occurred """
    return self.__geofence_name

  @property
  def received_at(self):
    """ Transaction reception date and time """
    return self.__received_at

  @property
  def is_wildcard(self):
    """ Wildcard indicator for transaction """
    return self.__is_wildcard
