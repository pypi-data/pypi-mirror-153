"""


Sculpt Curves Operators
***********************

:func:`brush_stroke`

:func:`select_all`

"""

import typing

def brush_stroke(stroke: typing.Union[typing.Sequence[OperatorStrokeElement], typing.Mapping[str, OperatorStrokeElement], bpy.types.bpy_prop_collection] = None, mode: str = 'NORMAL') -> None:

  """

  Sculpt curves using a brush

  """

  ...

def select_all(action: str = 'TOGGLE') -> None:

  """

  (De)select all control points

  """

  ...
