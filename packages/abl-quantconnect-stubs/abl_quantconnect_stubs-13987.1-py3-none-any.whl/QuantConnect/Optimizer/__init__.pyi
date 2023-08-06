from typing import overload
import QuantConnect.Optimizer
import System


class OptimizationStatus(System.Enum):
    """The different optimization status"""

    New = 0
    """Just created and not running optimization"""

    Aborted = 1
    """We failed or we were aborted"""

    Running = 2
    """We are running"""

    Completed = 3
    """Optimization job has completed"""


