"""


Operator Type Flag Items
^^^^^^^^^^^^^^^^^^^^^^^^

:REGISTER:        
  Register.

  Display in the info window and support the redo toolbar panel.

:UNDO:            
  Undo.

  Push an undo event (needed for operator redo).

:UNDO_GROUPED:    
  Grouped Undo.

  Push a single undo event for repeated instances of this operator.

:BLOCKING:        
  Blocking.

  Block anything else from using the cursor.

:MACRO:           
  Macro.

  Use to check if an operator is a macro.

:GRAB_CURSOR:     
  Grab Pointer.

  Use so the operator grabs the mouse focus, enables wrapping when continuous grab is enabled.

:GRAB_CURSOR_X:   
  Grab Pointer X.

  Grab, only warping the X axis.

:GRAB_CURSOR_Y:   
  Grab Pointer Y.

  Grab, only warping the Y axis.

:DEPENDS_ON_CURSOR:
  Depends on Cursor.

  The initial cursor location is used, when running from a menus or buttons the user is prompted to place the cursor before beginning the operation.

:PRESET:          
  Preset.

  Display a preset button with the operators settings.

:INTERNAL:        
  Internal.

  Removes the operator from search results.

.. _rna-enum-operator-type-flag-items:

"""

import typing
