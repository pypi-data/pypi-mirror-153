"""


Keying Flag Items Api
^^^^^^^^^^^^^^^^^^^^^

:INSERTKEY_NEEDED:
  Only Needed.

  Only insert keyframes where they're needed in the relevant F-Curves.

:INSERTKEY_VISUAL:
  Visual Keying.

  Insert keyframes based on 'visual transforms'.

:INSERTKEY_XYZ_TO_RGB:
  XYZ=RGB Colors.

  Color for newly added transformation F-Curves (Location, Rotation, Scale) and also Color is based on the transform axis.

:INSERTKEY_REPLACE:
  Replace Existing.

  Only replace existing keyframes.

:INSERTKEY_AVAILABLE:
  Only Available.

  Don't create F-Curves when they don't already exist.

:INSERTKEY_CYCLE_AWARE:
  Cycle Aware Keying.

  When inserting into a curve with cyclic extrapolation, remap the keyframe inside the cycle time range, and if changing an end key, also update the other one.

.. _rna-enum-keying-flag-items-api:

"""

import typing
