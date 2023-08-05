"""


Logic Operators
***************

:func:`actuator_add`

:func:`actuator_move`

:func:`actuator_remove`

:func:`controller_add`

:func:`controller_move`

:func:`controller_remove`

:func:`custom_object_create`

:func:`custom_object_register`

:func:`custom_object_reload`

:func:`custom_object_remove`

:func:`links_cut`

:func:`properties`

:func:`python_component_create`

:func:`python_component_move_down`

:func:`python_component_move_up`

:func:`python_component_register`

:func:`python_component_reload`

:func:`python_component_remove`

:func:`region_flip`

:func:`sensor_add`

:func:`sensor_move`

:func:`sensor_remove`

:func:`view_all`

"""

import typing

def actuator_add(type: str = '', name: str = '', object: str = '') -> None:

  """

  Add an actuator to the active object

  """

  ...

def actuator_move(actuator: str = '', object: str = '', direction: str = 'UP') -> None:

  """

  Move Actuator

  """

  ...

def actuator_remove(actuator: str = '', object: str = '') -> None:

  """

  Remove an actuator from the active object

  """

  ...

def controller_add(type: str = 'LOGIC_AND', name: str = '', object: str = '') -> None:

  """

  Add a controller to the active object

  """

  ...

def controller_move(controller: str = '', object: str = '', direction: str = 'UP') -> None:

  """

  Move Controller

  """

  ...

def controller_remove(controller: str = '', object: str = '') -> None:

  """

  Remove a controller from the active object

  """

  ...

def custom_object_create(class_name: str = 'module.MyObject') -> None:

  """

  Create a KX_GameObject subclass and attach it to the selected object

  """

  ...

def custom_object_register(class_name: str = 'module.MyObject') -> None:

  """

  Use a custom KX_GameObject subclass for the selected object

  """

  ...

def custom_object_reload() -> None:

  """

  Reload custom object from the source script

  """

  ...

def custom_object_remove() -> None:

  """

  Remove this custom class from the object

  """

  ...

def links_cut(path: typing.Union[typing.Sequence[OperatorMousePath], typing.Mapping[str, OperatorMousePath], bpy.types.bpy_prop_collection] = None, cursor: int = 12) -> None:

  """

  Remove logic brick connections

  """

  ...

def properties() -> None:

  """

  Toggle the properties region visibility

  """

  ...

def python_component_create(component_name: str = 'module.Component') -> None:

  """

  Create a Python component to the selected object

  """

  ...

def python_component_move_down(index: int = 0) -> None:

  """

  Move this component down in the list

  """

  ...

def python_component_move_up(index: int = 0) -> None:

  """

  Move this component up in the list

  """

  ...

def python_component_register(component_name: str = 'module.Component') -> None:

  """

  Add a Python component to the selected object

  """

  ...

def python_component_reload(index: int = 0) -> None:

  """

  Reload component from the source script

  """

  ...

def python_component_remove(index: int = 0) -> None:

  """

  Remove this component from the object

  """

  ...

def region_flip() -> None:

  """

  Toggle the properties region's alignment (left/right)

  """

  ...

def sensor_add(type: str = '', name: str = '', object: str = '') -> None:

  """

  Add a sensor to the active object

  """

  ...

def sensor_move(sensor: str = '', object: str = '', direction: str = 'UP') -> None:

  """

  Move Sensor

  """

  ...

def sensor_remove(sensor: str = '', object: str = '') -> None:

  """

  Remove a sensor from the active object

  """

  ...

def view_all() -> None:

  """

  Resize view so you can see all logic bricks

  """

  ...
