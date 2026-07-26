"""
FSE Governance Runtime Status Definitions
Version: V12.00
Production Foundation
"""

from enum import Enum


class RuntimeStatus(str, Enum):
    INITIALIZED = "INITIALIZED"
    READY = "READY"
    ACTIVE = "ACTIVE"
    STOPPED = "STOPPED"
    ERROR = "ERROR"
    RECOVERING = "RECOVERING"


class DecisionStatus(str, Enum):
    ALLOW = "ALLOW"
    BLOCK = "BLOCK"


class RecoveryStatus(str, Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
