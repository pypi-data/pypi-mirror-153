#!/usr/bin/env python
"""
Created on Apr 17, 2017

@author: yyang
"""
from ctypes import Structure, c_uint8, c_uint32, c_uint64, Union




class Arbitration(Union):
    """Arbitration"""
    class Dword(Structure):
        _pack_ = 1
        _fields_ = [
            ('dword', c_uint32),
        ]

    class Bits(Structure):
        _pack_ = 1
        _fields_ = [
            ('arb', c_uint32, 3),            # Arbitration Burst
            ('reserved0', c_uint32, 5),     # Reserved 0
            ('lpw', c_uint32, 8),           # Low Priority Weight
            ('mpw', c_uint32, 8),           # Medium Priority Weight
            ('hpw', c_uint32, 8),           # High Priority Weight
        ]

    _anonymous_ = ('dword', 'bits')
    _fields_ = [
        ('dword', Dword),
        ('bits', Bits),
    ]


class PowerManagement(Union):
    """Power Management"""
    class Dword(Structure):
        _pack_ = 1
        _fields_ = [
            ('dword', c_uint32),
        ]

    class Bits(Structure):
        _pack_ = 1
        _fields_ = [
            ('pws', c_uint32, 5),            # Power State
            ('wlh', c_uint32, 3),           # Workload Hint
            ('reserved0', c_uint32, 24),    # Reserved 0
        ]

    _anonymous_ = ('dword', 'bits')
    _fields_ = [
        ('dword', Dword),
        ('bits', Bits),
    ]

class LBARangeType(Union):
    """LBA Range - Command Dword 0/Dword 11"""
    class Dword(Structure):
        _pack_ = 1
        _fields_ = [
            ('dword', c_uint32),
        ]

    class Bits(Structure):
        _pack_ = 1
        _fields_ = [
            ('num', c_uint32, 6),           # Number of LBA Ranges
            ('rsv0', c_uint32, 24),
        ]

    _anonymous_ = ('dword', 'bits')
    _fields_ = [
        ('dword', Dword),
        ('bits', Bits),
    ]

class LBARangeTypeEntry(Union):
    """LBA Range Type - Data Structure Entry"""
    _pack_ = 1
    _fields_ = [
        ('type', c_uint8),              # Type
        ('attr', c_uint8),              # Attributes
        ('reserved0', c_uint8 * 14),    # Reserved 0
        ('slba', c_uint64),             # Starting LBA
        ('nlb', c_uint64),              # Number of Logical Blocks
        ('guid', c_uint64 * 2),         # Unique Identifier
        ('reserved1', c_uint8 * 16),    # Reserved 1
    ]


class TemperatureThreshold(Union):
    """Temperature Threshold"""
    class Dword(Structure):
        _pack_ = 1
        _fields_ = [
            ('dword', c_uint32),
        ]

    class Bits(Structure):
        _pack_ = 1
        _fields_ = [
            ('tmpth', c_uint32, 16),        # Temperature Threshold
            ('tmpsel', c_uint32, 4),        # Threshold Temperature Select
            ('thsel', c_uint32, 2),         # Threshold Type Select
            ('reserved0', c_uint32, 10),    # Reserved 0
        ]

    _anonymous_ = ('dword', 'bits')
    _fields_ = [
        ('dword', Dword),
        ('bits', Bits),
    ]


class ErrorRecovery(Union):
    """Error Recovery"""
    class Dword(Structure):
        _pack_ = 1
        _fields_ = [
            ('dword', c_uint32),
        ]

    class Bits(Structure):
        _pack_ = 1
        _fields_ = [
            ('tler', c_uint32, 16),         # Time Limited Error Recovery:
            ('dulbe', c_uint32, 1),         # Deallocated or Unwritten Logical Block Error Enable
            ('reserved0', c_uint32, 15),    # Reserved 0
        ]

    _anonymous_ = ('dword', 'bits')
    _fields_ = [
        ('dword', Dword),
        ('bits', Bits),
    ]


class VolatileWriteCache(Union):
    """Volatile Write Cache"""
    class Dword(Structure):
        _pack_ = 1
        _fields_ = [
            ('dword', c_uint32),
        ]

    class Bits(Structure):
        _pack_ = 1
        _fields_ = [
            ('wce', c_uint32, 1),           # Volatile Write Cache Enable
            ('reserved0', c_uint32, 31),    # Reserved 0
        ]

    _anonymous_ = ('dword', 'bits')
    _fields_ = [
        ('dword', Dword),
        ('bits', Bits),
    ]

class NumberOfQueues(Union):
    """Number of Queues"""
    class Dword(Structure):
        _pack_ = 1
        _fields_ = [
            ('dword', c_uint32),
        ]

    class Bits(Structure):
        _pack_ = 1
        _fields_ = [
            ('nsqr', c_uint32, 16),  # Number of I/O Submission Queues Requested
            ('ncqr', c_uint32, 16),  # Number of I/O Completion Queues Requested
        ]

    _anonymous_ = ('dword', 'bits')
    _fields_ = [
        ('dword', Dword),
        ('bits', Bits),
    ]

class NumberOfQueuesEntry(Union):
    """Number of Queues - command queue entry"""
    _pack_ = 1
    _fields_ = [
        ('nsqa', c_uint32, 16),  # Number of I/O Submission Queues Allocated
        ('ncqa', c_uint32, 16),  # Number of I/O Completion Queues Allocated
    ]


class InterruptCoalescing(Union):
    """Interrupt Coalescing"""
    class Dword(Structure):
        _pack_ = 1
        _fields_ = [
            ('dword', c_uint32),
        ]

    class Bits(Structure):
        _pack_ = 1
        _fields_ = [
            ('athr', c_uint32, 8),          # Aggregation Threshold
            ('atime', c_uint32, 8),         # Aggregation Time
            ('reserved0', c_uint32, 16),    # Reserved 0
        ]

    _anonymous_ = ('dword', 'bits')
    _fields_ = [
        ('dword', Dword),
        ('bits', Bits),
    ]


class InterruptVectorConfiguration(Union):
    """Interrupt Vector Configuration"""
    class Dword(Structure):
        _pack_ = 1
        _fields_ = [
            ('dword', c_uint32),
        ]

    class Bits(Structure):
        _pack_ = 1
        _fields_ = [
            ('itv', c_uint32, 16),           # Interrupt Vector
            ('cgd', c_uint32, 1),            # Coalescing Disable
            ('reserved0', c_uint32, 15),    # Reserved 0
        ]

    _anonymous_ = ('dword', 'bits')
    _fields_ = [
        ('dword', Dword),
        ('bits', Bits),
    ]


class WriteAtomicityNormal(Union):
    """Write Atomicity Normal"""
    class Dword(Structure):
        _pack_ = 1
        _fields_ = [
            ('dword', c_uint32),
        ]

    class Bits(Structure):
        _pack_ = 1
        _fields_ = [
            ('den', c_uint32, 1),            # Disable Normal
            ('reserved0', c_uint32, 31),    # Reserved 0
        ]

    _anonymous_ = ('dword', 'bits')
    _fields_ = [
        ('dword', Dword),
        ('bits', Bits),
    ]


class AsynchronousEventConfiguration(Union):
    """Asynchronous Event Configuration"""
    class Dword(Structure):
        _pack_ = 1
        _fields_ = [
            ('dword', c_uint32),
        ]

    class Bits(Structure):
        _pack_ = 1
        _fields_ = [
            ('shcw', c_uint32, 8),          # SMART / Health Critical Warnings
            ('nsan', c_uint32, 1),          # Namespace Attribute Notices
            ('fwan', c_uint32, 1),          # Firmware Activation Notices
            ('tln', c_uint32, 1),
            ('anacn', c_uint32, 1),
            ('plealcn', c_uint32, 1),
            ('lsin', c_uint32, 1),
            ('egealcn', c_uint32, 1),
            ('rsv0', c_uint32, 13),    # Reserved 0
            ('nvmof', c_uint32, 4)
        ]

    _anonymous_ = ('dword', 'bits')
    _fields_ = [
        ('dword', Dword),
        ('bits', Bits),
    ]


class AutonomousPowerStateTransition(Union):
    """Autonomous Power State Transition"""
    class Dword(Structure):
        _pack_ = 1
        _fields_ = [
            ('dword', c_uint32),
        ]

    class Bits(Structure):
        _pack_ = 1
        _fields_ = [
            ('apste', c_uint32, 1),         # Autonomous Power State Transition Enable
            ('reserved0', c_uint32, 31),    # Reserved 0
        ]

    _anonymous_ = ('dword', 'bits')
    _fields_ = [
        ('dword', Dword),
        ('bits', Bits),
    ]


class AutonomousPowerStateTransitionEntry(Union):
    """Autonomous Power State Transition Entry"""
    _pack_ = 1
    _fields_ = [
        ('reserved0', c_uint32, 3),     # Reserved 0
        ('itps', c_uint32, 5),          # Idle Transition Power State
        ('itpt', c_uint32, 24),         # Idle Time Prior to Transition
        ('reserved1', c_uint32, 32),    # Reserved 1
    ]


class SoftwareProgressMarker(Structure):
    """Software Progress Marker"""
    _pack_ = 1
    _fields_ = [
        ('pbslc', c_uint32, 8),         # Pre-boot Software Load Count
        ('reserved0', c_uint32, 24),    # Reserved 0
    ]


class HostIdentifier(Structure):
    """Host Identifier, ONLY 8 bytes data structure"""
    _pack_ = 1
    _fields_ = [
        ('exhid', c_uint32, 1),         # Pre-boot Software Load Count
        ('reserved0', c_uint32, 31),    # Reserved 0
    ]


class HostIdentifierEntry(Structure):
    """Host Identifier, ONLY 8 bytes data structure"""
    _pack_ = 1
    _fields_ = [
        ('hostidl', c_uint64),
        ('hostidh', c_uint64),
    ]


class ReservationNotificationMask(Structure):
    """Reservation Notification Mask"""
    _pack_ = 1
    _fields_ = [
        ('reserved0', c_uint32, 1),     # Reserved 0
        ('regpre', c_uint32, 1),        # Mask Registration Preempted Notification
        ('resrel', c_uint32, 1),        # Mask Reservation Released Notification
        ('respre', c_uint32, 1),        # Mask Reservation Preempted Notification
        ('reserved1', c_uint32, 28),    # Reserved 1
    ]


class ReservationPersistence(Structure):
    """Reservation Persistence Configuration"""
    _pack_ = 1
    _fields_ = [
        ('ptpl', c_uint32, 1),          # Persist Through Power Loss
        ('reserved0', c_uint32, 31),    # Reserved 0
    ]

class Timestamp(Structure):
    """Reservation Persistence Configuration"""
    _pack_ = 1
    _fields_ = [
        ('timestamp', c_uint64, 48),          # Persist Through Power Loss
        ('synch', c_uint64, 1),
        ('to', c_uint64, 3),
        ('rsv0', c_uint64, 4),
        ('rsv1', c_uint64, 8),
    ]

class KeepAliveTimer(Structure):
    """Reservation Persistence Configuration"""
    _pack_ = 1
    _fields_ = [
        ('kato', c_uint32),          # Persist Through Power Loss
    ]

class HostControlledThermalManagement(Structure):
    """Reservation Persistence Configuration"""
    _pack_ = 1
    _fields_ = [
        ('tmt2', c_uint32, 16),          # Persist Through Power Loss
        ('tmt1', c_uint32, 16),
    ]

class NonOperationalPowerStateConfig(Structure):
    """Reservation Persistence Configuration"""
    _pack_ = 1
    _fields_ = [
        ('noppme', c_uint32, 1),          # Persist Through Power Loss
        ('rsv0', c_uint32, 31),
    ]

class ReadRecoveryLevelConfig(Structure):
    """Reservation Persistence Configuration"""
    _pack_ = 1
    _fields_ = [
        ('rrl', c_uint32, 4),          # Persist Through Power Loss
        ('rsv0', c_uint32, 28),
    ]

class SanitizeConfig(Structure):
    """Reservation Persistence Configuration"""
    _pack_ = 1
    _fields_ = [
        ('nodrm', c_uint32, 1),          # Persist Through Power Loss
        ('rsv0', c_uint32, 31),
    ]

class FeatureIdentifier(object):
    """Get Feature/Set Feature - Feature Identifier"""
    Arbitration = 0x1
    PowerManagement = 0x2
    LBARangeType = 0x3
    TemperatureThreshold = 0x4
    ErrorRecovery = 0x5
    VolatileWriteCache = 0x6
    NumberOfQueues = 0x7
    InterruptCoalescing = 0x8
    InterruptVectorConfiguration = 0x9
    WriteAtomicityNormal = 0xa
    AsynchronousEventConfiguration = 0xb
    AutonomousPowerStateTransition = 0xc
    HostMemoryBuffer = 0xd
    Timestamp = 0xe
    KeepAliveTimer = 0xf
    HostControlledThermalManagement = 0x10
    NonOperationalPowerStateConfig = 0x11
    ReadRecoveryLevelConfig = 0x12
    PredictableLatencyModeConfig = 0x13
    PredictableLatencyModeWindow = 0x14
    LBAStatusInfoReportInterval = 0x15
    HostBehaviorSupport = 0x16
    SanitizeConfig = 0x17
    EnduranceGroupEventConfig = 0x18
    SoftwareProgressMarker = 0x80
    HostIdentifier = 0x81
    ReservationNotificationMask = 0x82
    ReservationPersistence = 0x83
    NamespaceWriteProtectionConfig = 0x84
