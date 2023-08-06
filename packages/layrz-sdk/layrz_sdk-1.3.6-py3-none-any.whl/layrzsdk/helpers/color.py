"""
Color helpers
"""
def convert_to_rgba(hex_color):
  """
  Convert Hex (or Hexa) color to RGB (or RGBA) color
  
  Arguments
  ---------
    hex_color (str): Hex (or Hexa) color
  Returns
  -------
    tuple(r,g,b,a): Combination of colors. When the argument (hex_color) is Hex, the alpha channel is set to 1.
	"""

  if not hex_color.startswith('#'):
    raise Exception('Invalid color, must starts with #')

  hex_color = hex_color.replace('#', '')
  if len(hex_color) == 6:
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4)) + (1,)

  return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4, 6))

def use_black(color):
  """
  Use black
  Will return when the background color works well with black text color.
  Note: This method is not 100% accurate and will not work with alpha channel (Hexa color)

  Arguments
  ---------
    color (str): Hex color

  Returns
  -------
    boolean: True if use black
  """
  rgb = convert_to_rgba(color)
  a = 1 - (0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]) / 255
  return (a < 0.5)

