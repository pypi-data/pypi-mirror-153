"""
Options with default values
"""
from dataclasses import dataclass, field


@dataclass
class Options:
    """
    Can be changed with e.g. Options.log_level = 'INFO'
    """
    total_retries: int = field(default=10)
    timeout_seconds: int = field(default=2)
    backoff_factor: int = field(default=5)
    log_level: str = field(default='ERROR')
