from dataclasses import dataclass
from typing import Dict


@dataclass
class WorkerMetadata:
    module_name: str
    args: Dict
    interval_seconds: int
    error_resiliency: int
