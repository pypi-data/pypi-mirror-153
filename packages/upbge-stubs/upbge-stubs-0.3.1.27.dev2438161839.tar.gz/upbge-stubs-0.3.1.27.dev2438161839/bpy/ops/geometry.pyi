"""


Geometry Operators
******************

:func:`attribute_add`

:func:`attribute_convert`

:func:`attribute_remove`

:func:`color_attribute_add`

:func:`color_attribute_remove`

:func:`color_attribute_render_set`

"""

import typing

def attribute_add(name: str = 'Attribute', domain: str = 'POINT', data_type: str = 'FLOAT') -> None:

  """

  Add attribute to geometry

  """

  ...

def attribute_convert(mode: str = 'GENERIC', domain: str = 'POINT', data_type: str = 'FLOAT') -> None:

  """

  Change how the attribute is stored

  """

  ...

def attribute_remove() -> None:

  """

  Remove attribute from geometry

  """

  ...

def color_attribute_add(name: str = 'Color', domain: str = 'POINT', data_type: str = 'FLOAT_COLOR', color: typing.Tuple[float, float, float, float] = (0.0, 0.0, 0.0, 1.0)) -> None:

  """

  Add color attribute to geometry

  """

  ...

def color_attribute_remove() -> None:

  """

  Remove color attribute from geometry

  """

  ...

def color_attribute_render_set(name: str = 'Color') -> None:

  """

  Set default color attribute used for rendering

  """

  ...
