""" Layrz Compute Language SDK """

PATTERN_INVALID = 'Pattern should be string, received {received}'
INVALID_NUMBER_OF_PARAMS = 'Invalid number of arguments - Expected {expected} - Given {received}'
DIFFERENT_TYPES_RANGES = 'Invalid data range, value: {arg1} - Minimum: {arg2} - Maximum: {arg3}'
DIFFERENT_TYPES = 'Invalid data types - arg1: {arg1} - arg2: {arg2}'
INVALID_ARGUMENTS = 'Invalid arguments - {e}'
TIMEOUT_REACHED = 'Timeout reached - Maximum execution time: {timeout}s'

class Language:
  """
  Layrz Compute Language
  """

  def __init__(self, script='', sensors={}, previous_sensors={}, payload={}, asset_constants={}, custom_fields={}):
    """ Constructor """
    self.__sensors = sensors
    self.__previous_sensors = previous_sensors
    self.__payload = payload
    self.__asset_constants = asset_constants
    self.__custom_fields = custom_fields
    self.__script = script

  def perform(self, ignore_signal=False):
    """ Perform script using Layrz Compute Language """
    try:
      local_variables = {
        'payload': self.__payload,
        'sensors': self.__sensors,
        'custom_fields': self.__custom_fields,
        'previous_sensors': self.__previous_sensors,
        'asset_constants': self.__asset_constants,
      }

      ## Define global variables and functions
      global_functions = {
        'GET_PARAM': self.GET_PARAM,
        'GET_SENSOR': self.GET_SENSOR,
        'CONSTANT': self.CONSTANT,
        'GET_CUSTOM_FIELD': self.GET_CUSTOM_FIELD,
        'COMPARE': self.COMPARE,
        'OR_OPERATOR': self.OR_OPERATOR,
        'AND_OPERATOR': self.AND_OPERATOR,
        'SUM': self.SUM,
        'SUBSTRACT': self.SUBSTRACT,
        'MULTIPLY': self.MULTIPLY,
        'DIVIDE': self.DIVIDE,
        'TO_BOOL': self.TO_BOOL,
        'TO_STR': self.TO_STR,
        'TO_INT': self.TO_INT,
        'CEIL': self.CEIL,
        'FLOOR': self.FLOOR,
        'ROUND': self.ROUND,
        'SQRT': self.SQRT,
        'CONCAT': self.CONCAT,
        'NOW': self.NOW,
        'RANDOM': self.RANDOM,
        'RANDOM_INT': self.RANDOM_INT,
        'GREATER_THAN_OR_EQUALS_TO': self.GREATER_THAN_OR_EQUALS_TO,
        'GREATER_THAN': self.GREATER_THAN,
        'LESS_THAN_OR_EQUALS_TO': self.LESS_THAN_OR_EQUALS_TO,
        'LESS_THAN': self.LESS_THAN,
        'DIFFERENT': self.DIFFERENT,
        'HEX_TO_STR': self.HEX_TO_STR,
        'STR_TO_HEX': self.STR_TO_HEX,
        'HEX_TO_INT': self.HEX_TO_INT,
        'INT_TO_HEX': self.INT_TO_HEX,
        'TO_FLOAT': self.TO_FLOAT,
        'GET_DISTANCE_TRAVELED': self.GET_DISTANCE_TRAVELED,
        'GET_PREVIOUS_SENSOR': self.GET_PREVIOUS_SENSOR,
        'IS_PARAMETER_PRESENT': self.IS_PARAMETER_PRESENT,
        'IS_SENSOR_PRESENT': self.IS_SENSOR_PRESENT,
        'INSIDE_RANGE': self.INSIDE_RANGE,
        'OUTSIDE_RANGE': self.OUTSIDE_RANGE,
        'GET_TIME_DIFFERENCE': self.GET_TIME_DIFFERENCE,
        'IF': self.IF,
        'REGEX': self.REGEX,
        'IS_NONE': self.IS_NONE,
        'NOT': self.NOT,
        'CONTAINS': self.CONTAINS,
        'STARTS_WITH': self.STARTS_WITH,
        'ENDS_WITH': self.ENDS_WITH,
        'PRIMARY_DEVICE': self.PRIMARY_DEVICE
      }

      if not ignore_signal:
        import signal
        signal.signal(signal.SIGALRM, self.__raise_timeout)
        signal.alarm(self.timeout)

      import json
      result = json.dumps(eval(self.__script, global_functions, local_variables))

      if not ignore_signal:
        signal.signal(signal.SIGALRM, signal.SIG_IGN)

      return result
    except TimeoutError:
      return json.dumps(TIMEOUT_REACHED.format(timeout=self.timeout))
    except Exception as err:
      import json
      return json.dumps(INVALID_ARGUMENTS.format(e=err))

  @property
  def timeout(self):
    """ Timeout constant """
    return 10 # seconds

  def __raise_timeout(self, signum, frame):
    """ Raise timeout """
    raise TimeoutError

  def GET_PARAM(self, *args):
    """ GET_PARAM Function """
    if len(args) > 2:
      return INVALID_NUMBER_OF_PARAMS.format(
        expected=2,
        received=len(args)
      )

    if len(args) > 1:
      return self.__payload.get(args[0], args[1])
    return self.__payload.get(args[0], None)

  def GET_DISTANCE_TRAVELED(self, *args):
    """ GET_DISTANCE_TRAVELED Function """
    if len(args) > 0:
      return INVALID_NUMBER_OF_PARAMS.format(
        expected=0,
        received=len(args)
      )
    return self.__asset_constants.get('distanceTraveled', 0)

  def GET_PREVIOUS_SENSOR(self, *args):
    """ GET_PREVIOUS_SENSOR Function """
    if len(args) < 1:
      return INVALID_NUMBER_OF_PARAMS.format(
        expected=1,
        received=len(args)
      )

    if len(args) > 2:
      return INVALID_NUMBER_OF_PARAMS.format(
        expected=2,
        received=len(args)
      )

    if len(args) > 1:
      return self.__previous_sensors.get(args[0], args[1])
    return self.__previous_sensors.get(args[0], None)

  def GET_SENSOR(self, *args):
    """ GET_SENSOR Function """
    if len(args) < 1:
      return INVALID_NUMBER_OF_PARAMS.format(
        expected=1,
        received=len(args)
      )

    if len(args) > 2:
      return INVALID_NUMBER_OF_PARAMS.format(
        expected=2,
        received=len(args)
      )

    if len(args) > 1:
      return self.__sensors.get(args[0], args[1])
    return self.__sensors.get(args[0], None)

  def CONSTANT(self, *args):
    """ CONSTANT Function """
    if len(args) > 1:
      return INVALID_NUMBER_OF_PARAMS.format(
        expected=1,
        received=len(args)
      )
    return args[0]

  def GET_CUSTOM_FIELD(self, *args):
    """ GET_CUSTOM_FIELD Function """
    if len(args) > 1:
      return INVALID_NUMBER_OF_PARAMS.format(
        expected=1,
        received=len(args)
      )
    return self.__custom_fields.get(args[0], '')

  def COMPARE(self, *args):
    """ COMPARE Function """
    if len(args) != 2:
      return INVALID_NUMBER_OF_PARAMS.format(expected=2, received=len(args))

    if args[0] is None or args[1] is None:
      return None

    if type(args[0]) != type(args[1]):
      return DIFFERENT_TYPES.format(arg1=type(args[0]), arg2=type(args[1]))
    return args[0] == args[1]

  def OR_OPERATOR(self, *args):
    """ OR_OPERATOR Function """
    result = False

    for val in args:
      if val is None:
        return None
      if isinstance(val, bool):
        result = result or val

    return result

  def AND_OPERATOR(self, *args):
    """ AND_OPERATOR Function """
    result = False
    is_first = True

    for val in args:
      if val is None:
        return None
      if is_first:
        is_first = False
        result = val
      elif isinstance(val, bool):
        result = result and val

    return result

  def SUM(self, *args):
    """ SUM Function """
    result = 0

    for num in args:
      if num is None:
        continue
      try:
        result += float(num)
      except:
        pass

    return result

  def SUBSTRACT(self, *args):
    """ SUBSTRACT Function """
    result = 0
    is_first = True

    for num in args:
      if num is None:
        continue
      try:
        if is_first:
          result = float(num)
          is_first = False
        else:
          result -= float(num)
      except:
        pass

    return result

  def MULTIPLY(self, *args):
    """ MULTIPLY Function """
    result = 0
    is_first = True

    for num in args:
      if num is None:
        continue
      try:
        if is_first:
          is_first = False
          result = float(num)
        else:
          result *= float(num)
      except:
        pass

    return result

  def DIVIDE(self, *args):
    """ DIVIDE Function """
    result = 0
    is_first = True

    for num in args:
      if num is None:
        continue
      try:
        if is_first:
          is_first = False
          result = float(num)
        else:
          result /= float(num)
      except:
        pass

    return result

  def TO_BOOL(self, *args):
    """ TO_BOOL Function """
    if len(args) > 1:
      return INVALID_NUMBER_OF_PARAMS.format(
        expected=1,
        received=len(args)
      )
    if args[0] is None:
      return None
    return bool(args[0])

  def TO_STR(self, *args):
    """ TO_STR Function """
    if len(args) > 1:
      return INVALID_NUMBER_OF_PARAMS.format(
        expected=1,
        received=len(args)
      )

    if args[0] is None:
      return None
    return str(args[0])

  def TO_INT(self, *args):
    """ TO_INT Function """
    if len(args) > 1:
      return INVALID_NUMBER_OF_PARAMS.format(
        expected=1,
        received=len(args)
      )
    if args[0] is None:
      return None
    return int(args[0])

  def CEIL(self, *args):
    """ CEIL Function """
    if len(args) > 1:
      return INVALID_NUMBER_OF_PARAMS.format(
        expected=1,
        received=len(args)
      )
    if args[0] is None:
      return None
    import math
    return math.ceil(args[0])

  def FLOOR(self, *args):
    """ FLOOR Function """
    if len(args) > 1:
      return INVALID_NUMBER_OF_PARAMS.format(
        expected=1,
        received=len(args)
      )
    if args[0] is None:
      return None
    import math
    return math.floor(args[0])

  def ROUND(self, *args):
    """ ROUND Function """
    if len(args) > 1:
      return INVALID_NUMBER_OF_PARAMS.format(
        expected=1,
        received=len(args)
      )
    if args[0] is None:
      return None
    return round(args[0])

  def SQRT(self, *args):
    """ SQRT Function """
    if len(args) > 1:
      return INVALID_NUMBER_OF_PARAMS.format(
        expected=1,
        received=len(args)
      )
    if args[0] is None:
      return None
    import math
    return math.sqrt(args[0])

  def CONCAT(self, *args):
    """ CONCAT Function """
    for val in args:
      if val is None:
        return None
    return ''.join(map(lambda x: str(x), args))

  def RANDOM(self, *args):
    """ RANDOM Function """
    if len(args) > 2:
      return INVALID_NUMBER_OF_PARAMS.format(
        expected=2,
        received=len(args)
      )
    if len(args) < 2:
      return INVALID_NUMBER_OF_PARAMS.format(
        expected=2,
        received=len(args)
      )

    import random
    return random.random() * (float(args[1]) - float(args[0])) + float(args[0])

  def RANDOM_INT(self, *args):
    """ RANDOM_INT Function """
    if len(args) != 2:
      return INVALID_NUMBER_OF_PARAMS.format(
        expected=2,
        received=len(args)
      )

    import random
    return random.randint(int(args[0]), int(args[1]))

  def GREATER_THAN_OR_EQUALS_TO(self, *args):
    """ GREATER_THAN_OR_EQUALS_TO Function """
    if len(args) > 2:
      return INVALID_NUMBER_OF_PARAMS.format(
        expected=1,
        received=len(args)
      )
    if len(args) < 2:
      return INVALID_NUMBER_OF_PARAMS.format(
        expected=1,
        received=len(args)
      )

    if args[0] is None or args[1] is None:
      return None

    if type(args[0]) != type(args[1]):
      return DIFFERENT_TYPES.format(
        arg1=type(args[0]),
        arg2=type(args[1])
      )
    return args[0] >= args[1]

  def GREATER_THAN(self, *args):
    """ GREATER_THAN Function """
    if len(args) > 2:
      return INVALID_NUMBER_OF_PARAMS.format(
        expected=1,
        received=len(args)
      )
    if len(args) < 2:
      return INVALID_NUMBER_OF_PARAMS.format(
        expected=1,
        received=len(args)
      )

    if args[0] is None or args[1] is None:
      return None

    if type(args[0]) != type(args[1]):
      return DIFFERENT_TYPES.format(
        arg1=type(args[0]),
        arg2=type(args[1])
      )
    return args[0] > args[1]

  def LESS_THAN_OR_EQUALS_TO(self, *args):
    """ LESS_THAN_OR_EQUALS_TO Function """
    if len(args) > 2:
      return INVALID_NUMBER_OF_PARAMS.format(
        expected=1,
        received=len(args)
      )
    if len(args) < 2:
      return INVALID_NUMBER_OF_PARAMS.format(
        expected=1,
        received=len(args)
      )

    if args[0] is None or args[1] is None:
      return None

    if type(args[0]) != type(args[1]):
      return DIFFERENT_TYPES.format(
        arg1=type(args[0]),
        arg2=type(args[1])
      )
    return args[0] <= args[1]

  def LESS_THAN(self, *args):
    """ LESS_THAN Function """
    if len(args) > 2:
      return INVALID_NUMBER_OF_PARAMS.format(
        expected=1,
        received=len(args)
      )
    if len(args) < 2:
      return INVALID_NUMBER_OF_PARAMS.format(
        expected=1,
        received=len(args)
      )

    if args[0] is None or args[1] is None:
      return None

    if type(args[0]) != type(args[1]):
      return DIFFERENT_TYPES.format(
        arg1=type(args[0]),
        arg2=type(args[1])
      )
    return args[0] < args[1]

  def DIFFERENT(self, *args):
    """ DIFFERENT Function """
    if len(args) > 2:
      return INVALID_NUMBER_OF_PARAMS.format(
        expected=1,
        received=len(args)
      )
    if len(args) < 2:
      return INVALID_NUMBER_OF_PARAMS.format(
        expected=1,
        received=len(args)
      )

    if args[0] is None or args[1] is None:
      return None

    if type(args[0]) != type(args[1]):
      return DIFFERENT_TYPES.format(
        arg1=type(args[0]),
        arg2=type(args[1])
      )
    return args[0] != args[1]

  def HEX_TO_STR(self, *args):
    """ HEX_TO_STR Function """
    if len(args) > 1:
      return INVALID_NUMBER_OF_PARAMS.format(
        expected=1,
        received=len(args)
      )

    if args[0] is None:
      return None
    byte_array = bytes.fromhex(args[0])
    return byte_array.decode('ASCII')

  def STR_TO_HEX(self, *args):
    """ STR_TO_HEX Function """
    if len(args) > 1:
      return INVALID_NUMBER_OF_PARAMS.format(
        expected=1,
        received=len(args)
      )
    if args[0] is None:
      return None
    return str(args[0]).encode('ASCII').hex()

  def HEX_TO_INT(self, *args):
    """ HEX_TO_INT Function """
    if len(args) > 1:
      return INVALID_NUMBER_OF_PARAMS.format(
        expected=1,
        received=len(args)
      )
    if args[0] is None:
      return None
    return int(int(args[0], 16))

  def INT_TO_HEX(self, *args):
    """ INT_TO_HEX Function """
    if len(args) > 1:
      return INVALID_NUMBER_OF_PARAMS.format(
        expected=1,
        received=len(args)
      )
    if args[0] is None:
      return None
    return hex(int(args[0]))[2:]

  def TO_FLOAT(self, *args):
    """ TO_FLOAT Function """
    if len(args) > 1:
      return INVALID_NUMBER_OF_PARAMS.format(
        expected=1,
        received=len(args)
      )
    if args[0] is None:
      return None
    return float(args[0])

  def IS_PARAMETER_PRESENT(self, *args):
    """ IS_PARAMETER_PRESENT Function """
    if len(args) > 1:
      return INVALID_NUMBER_OF_PARAMS.format(
        expected=1,
        received=len(args)
      )

    return args[0] in self.__payload

  def IS_SENSOR_PRESENT(self, *args):
    """ IS_SENSOR_PRESENT Function """
    if len(args) > 1:
      return INVALID_NUMBER_OF_PARAMS.format(
        expected=1,
        received=len(args)
      )

    return args[0] in self.__sensors

  def INSIDE_RANGE(self, *args):
    """ INSIDE_RANGE Function """
    if len(args) != 3:
      return INVALID_NUMBER_OF_PARAMS.format(
        expected=3,
        received=len(args)
      )

    if args[0] is None or args[1] is None or args[2] is None:
      return None
    if type(args[0]) != type(args[1]) or type(args[0]) != type(args[2]):
      return DIFFERENT_TYPES_RANGES.format(
        arg1=type(args[0]),
        arg2=type(args[1]),
        arg3=type(args[2])
      )

    return args[1] <= args[0] <= args[2]

  def OUTSIDE_RANGE(self, *args):
    """ OUTSIDE_RANGE Function """
    if len(args) != 3:
      return INVALID_NUMBER_OF_PARAMS.format(
        expected=3,
        received=len(args)
      )

    if args[0] is None or args[1] is None or args[2] is None:
      return None
    if type(args[0]) != type(args[1]) or type(args[0]) != type(args[2]):
      return DIFFERENT_TYPES_RANGES.format(
        arg1=type(args[0]),
        arg2=type(args[1]),
        arg3=type(args[2])
      )

    return not (args[1] <= args[0] <= args[2])

  def GET_TIME_DIFFERENCE(self, *args):
    """ GET_TIME_DIFFERENCE Function """
    if len(args) > 0:
      return INVALID_NUMBER_OF_PARAMS.format(
        expected=0,
        received=len(args)
      )
    return self.__asset_constants.get('timeElapsed', 0)

  def IF(self, *args):
    """ IF Function """
    if len(args) != 3:
      return INVALID_NUMBER_OF_PARAMS.format(
        expected=3,
        received=len(args)
      )

    return args[1] if args[0] else args[2]

  def NOW(self, *args):
    """ NOW Function """
    from datetime import datetime
    import pytz
    return datetime.now(tz=pytz.utc).timestamp()

  def REGEX(self, *args):
    """ REGEX Function """
    if len(args) != 2:
      return INVALID_NUMBER_OF_PARAMS.format(
        expected=2,
        received=len(args)
      )

    if args[0] is None or args[1] is None:
      return None

    if type(args[0]) != str:
      return PATTERN_INVALID.format(received=type(args[0]))

    import re
    pattern = re.compile(args[1])
    return bool(pattern.match(args[0]))

  def IS_NONE(self, *args):
    """ IS_NONE Function """
    if len(args) != 1:
      return INVALID_NUMBER_OF_PARAMS.format(
        expected=1,
        received=len(args)
      )

    return args[0] is None

  def NOT(self, *args):
    """ NOT Function """
    if len(args) != 1:
      return INVALID_NUMBER_OF_PARAMS.format(
        expected=1,
        received=len(args)
      )

    return not args[0]

  def CONTAINS(self, *args):
    """ CONTAINS function """
    if len(args) != 2:
      return INVALID_NUMBER_OF_PARAMS.format(
        expected=2,
        received=len(args)
      )

    return str(args[0]) in str(args[1])

  def STARTS_WITH(self, *args):
    """ STARTS_WITH function """
    if len(args) != 2:
      return INVALID_NUMBER_OF_PARAMS.format(
        expected=2,
        received=len(args)
      )

    return str(args[1]).startswith(str(args[0]))

  def ENDS_WITH(self, *args):
    """ ENDS_WITH function """
    if len(args) != 2:
      return INVALID_NUMBER_OF_PARAMS.format(
        expected=2,
        received=len(args)
      )

    return str(args[1]).endswith(str(args[0]))

  def PRIMARY_DEVICE(self, *args):
    """ PRIMARY_DEVICE function """
    if len(args) > 0:
      return INVALID_NUMBER_OF_PARAMS.format(
        expected=0,
        received=len(args)
      )

    return self.__asset_constants.get('primaryDevice', None)
