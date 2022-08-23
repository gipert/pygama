"""
This subpackage overloads decoding utilities defined in :mod:`pygama.raw` to
read files produced by the FlashCam acquisition system.
"""

import logging

log = logging.getLogger(__name__)

try:
    import fcutils  # noqa: F401

except ModuleNotFoundError as msg:
    raise ModuleNotFoundError(
        f"No module named '{msg.name}'. Hint: fcutils is needed for decoding "
        "FlashCam files. See https://github.com/legend-exp/pyfcutils for "
        "install instructions."
    )
