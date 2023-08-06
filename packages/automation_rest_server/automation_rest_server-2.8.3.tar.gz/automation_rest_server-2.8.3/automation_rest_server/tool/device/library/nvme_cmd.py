#!/usr/bin/env python
# pylint: disable=superfluous-parens,missing-docstring,too-few-public-methods
"""
Created on Apr 19, 2019

@author: yyang
"""
from ctypes import Structure, c_uint8, c_uint16, c_uint32, c_uint64, Union, c_char, c_int, POINTER, c_wchar

class OpCode(object):
    # Opcodes for Admin Commands
    DELETE_IO_SQ = 0x00
    CREATE_IO_SQ = 0x01
    GET_LOG_PAGE = 0x02
    DELETE_IO_CQ = 0x04
    CREATE_IO_CQ = 0x05
    IDENTIFY = 0x06
    ABORT = 0x08
    SET_FEATURE = 0x09
    GET_FEATURE = 0x0A
    ASYNC_EVENT = 0x0C
    NAMESPACE_MGT = 0x0D
    FIRMWARE_COMMIT = 0x10
    FIRMWARE_DOWNLOAD = 0x11
    NAMESPACE_ATTACH = 0x15
    FORMAT_NVM = 0x80
    SECURITY_SEND = 0x81
    SECURITY_RECV = 0x82
    # Opcodes for NVM Commands
    FLUSH = 0x00
    WRITE = 0x01
    READ = 0x02
    WRITE_UNCORRECTABLE = 0x04
    COMPARE = 0x05
    WRITE_ZEROS = 0x08
    DATASET_MGT = 0x09
    RESERVATION_REGISTER = 0x0D
    RESERVATION_REPORT = 0x0E
    RESERVATION_ACQUIRE = 0x11
    RESERVATION_RELEASE = 0x12


OPCODE = OpCode()


class PassthruCmd(Union):
    """
    Take Care: different with SQE!
    cdw8 is metadata_len and cdw9 is data_len
    Add cdw16: timeout
    Add cdw17: dword0 of CQE
    """
    class Bits(Structure):
        _pack_ = 1
        _fields_ = [
            ('opcode', c_uint8),
            ('flags', c_uint8),
            ('rsvd1', c_uint16),
            ('nsid', c_uint32),
            ('cdw2', c_uint32),
            ('cdw3', c_uint32),
            ('metadata', c_uint64),
            ('addr', c_uint64),
            ('metadata_len', c_uint32),
            ('data_len', c_uint32),
            ('lba', c_uint64),
            ('cdw12', c_uint32),
            ('cdw13', c_uint32),
            ('cdw14', c_uint32),
            ('cdw15', c_uint32),
            ('timeout_ms', c_uint32),
            ('result', c_uint32),
        ]

    class Dword(Structure):
        _pack_ = 1
        _fields_ = [
            ('dword0', c_uint32),
            ('dword1', c_uint32),
            ('dword2', c_uint32),
            ('dword3', c_uint32),
            ('dword4', c_uint32),
            ('dword5', c_uint32),
            ('dword6', c_uint32),
            ('dword7', c_uint32),
            ('dword8', c_uint32),
            ('dword9', c_uint32),
            ('dword10', c_uint32),
            ('dword11', c_uint32),
            ('dword12', c_uint32),
            ('dword13', c_uint32),
            ('dword14', c_uint32),
            ('dword15', c_uint32),
            ('dword16', c_uint32),
            ('dword17', c_uint32),
        ]

    _anonymous_ = ('dword', 'bits')
    _fields_ = [
        ('dword', Dword),
        ('bits', Bits),
    ]


class FormatDword10(Union):
    """
    The Format NVM command uses the Command Dword 10 field.
    All other command specific fields are reserved.
    """
    class Bits(Structure):
        _pack_ = 1
        _fields_ = [
            ('lbaf', c_uint32, 4),      # LBA Format (LBAF)
            ('metaf', c_uint32, 1),     # Metadata Settings (MS)
            ('pif', c_uint32, 3),       # Protection Information (PI)
            ('pil', c_uint32, 1),       # Protection Information Location (PIL)
            ('ses', c_uint32, 3),       # Secure Erase Settings (SES)
            ('reserved', c_uint32, 20),
        ]

    class Dword(Structure):
        _pack_ = 1
        _fields_ = [
            ('dword', c_uint32),
        ]

    _anonymous_ = ('dword', 'bits')
    _fields_ = [
        ('dword', Dword),
        ('bits', Bits),
    ]


class PowerStateDescriptorDataStructure(Structure):
    """Identify - Power State Descriptor Data Structure"""
    _pack_ = 1
    _fields_ = [
        ('mp', c_uint16),           # Active Power Scale
        ('reserved0', c_uint8),
        ('mps', c_uint8, 1),        # Max Power Scale
        ('non_os', c_uint8, 1),     # Non-Operational State
        ('reserved1', c_uint8, 6),
        ('entry_l', c_uint32),      # Entry Latency
        ('exit_l', c_uint32),       # Exit Latency
        ('rrt', c_uint8, 5),        # Relative Read Throughput
        ('reserved2', c_uint8, 3),
        ('rrl', c_uint8, 5),        # Relative Read Latency
        ('reserved3', c_uint8, 3),
        ('rwt', c_uint8, 5),        # Relative Write Throughput
        ('reserved4', c_uint8, 3),
        ('rwl', c_uint8, 5),        # Relative Write Latency
        ('reserved5', c_uint8, 3),
        ('ip', c_uint16),           # Idle Power
        ('reserved6', c_uint8, 6),
        ('ips', c_uint8, 2),        # Idle Power Scale
        ('reserved7', c_uint8),
        ('ap', c_uint16),           # Active Power
        ('apw', c_uint8, 3),        # Active Power Workload
        ('reserved8', c_uint8, 3),
        ('aps', c_uint8, 2),        # Active Power Scale
        ('reserved', (c_uint8 * 9)),
    ]

class ControllerDataStructure(Structure):
    """Identify - Identify Controller Data Structure"""
    _pack_ = 1
    _fields_ = [
        ('vid', c_uint16),                  # PCI Vendor ID
        ('ssvid', c_uint16),                # PCI Subsystem Vendor ID
        ('serial_num', (c_uint8 * 20)),     # Serial number
        ('model_num', (c_uint8 * 40)),      # Model number for the NVM subsystem
        ('firmware_rev', c_uint64),         # Firmware revision for the NVM subsystem
        ('rab', c_uint8),                   # Recommended Arbitration Burst size
        ('ieee', c_uint32, 24),             # IEEE OUI Identifier
        ('cmic', c_uint32, 8),              # multi-path I/O and namespace sharing capabilities
        ('mdts', c_uint8),                  # maximum data transfer size
        ('cntlid', c_uint16),               # the NVM subsystem unique controller identifier
        ('ver', c_uint32),                  # the value reported in the Version register
        ('rtd3r', c_uint32),                # RTD3 Resume Latency
        ('rtd3e', c_uint32),                # RTD3 Entry Latency
        ('oaes', c_uint32),                 # Optional Asynchronous Events Supported
        ('reserved0', (c_uint8 * 144)),
        ('NMIS', (c_uint8 * 16)),           # NVMe Management Interface Specification
        ('oacs', c_uint16),                 # Optional Admin Command Support
        ('acl', c_uint8),                   # Abort Command Limit
        ('aerl', c_uint8),                  # Asynchronous Event Request Limit
        ('fw_update', c_uint8),             # Firmware Updates
        ('lpa', c_uint8),                   # Log Page Attributes
        ('elpe', c_uint8),                  # Error Log Page Entries
        ('nopss', c_uint8),                 # Number of Power States Support
        ('avscc', c_uint8),                 # Admin Vendor Specific Command Configuration
        ('apsta', c_uint8),                 # Autonomous Power State Transition Attributes
        ('wctemp', c_uint16),               # Warning Composite Temperature Threshold
        ('cctemp', c_uint16),               # Critical Composite Temperature Threshold
        ('mtfa', c_uint16),                 # Maximum Time for Firmware Activation
        ('hmpre', c_uint32),                # Host Memory Buffer Preferred Size
        ('hmmin', c_uint32),                # Host Memory Buffer Minimum Size
        ('tnvmcap', (c_uint8 * 16)),        # Total NVM Capacity
        ('unvmcap', (c_uint8 * 16)),        # Unallocated NVM Capacity
        ('rpmbs', c_uint32),                # Replay Protected Memory Block Support
        ('reserved1', (c_uint8 * 196)),
        ('sqes', c_uint8),                  # Submission Queue Entry Size
        ('cqes', c_uint8),                  # Completion Queue Entry Size
        ('reserved2', (c_uint8 * 2)),
        ('non', c_uint32),                  # Number of Namespaces
        ('oNVMcs', c_uint16),               # Optional NVM Command Support
        ('fuses', c_uint16),                # Fused Operation Support
        ('fNVMa', c_uint8),                 # Format NVM Attributes
        ('vwc', c_uint8),                   # Volatile Write Cache
        ('awun', c_uint16),                 # Atomic Write Unit Normal
        ('awupf', c_uint16),                # Atomic Write Unit Power Fail
        ('NVM_vscc', c_uint8),              # NVM Vendor Specific Command Configuration
        ('reserved3', (c_uint8 * 1)),
        ('acwu', c_uint16),                 # Atomic Compare & Write Unit
        ('reserved4', (c_uint8 * 2)),
        ('SGLs', c_uint32),                 # SGL Support
        ('reserved5', (c_uint8 * 164)),
        ('reserved6', (c_uint8 * 1344)),
        ('psd', PowerStateDescriptorDataStructure * 32),    # Power State Descriptor
        ('vs', (c_uint8 * 1024)),                           # Vendor Specific
    ]


class PrimaryControllerCap(Structure):
    """Identify - PrimaryController Data Structure"""
    _pack_ = 1
    _fields_ = [
        ('cntlid', c_uint16),           # Number of Identifiers
        ('portid', c_uint16),
        ('crt', c_uint8),
        ('reserved0', c_uint8*27),
        ('vqfrt', c_uint32),
        ('vqrfa', c_uint32),
        ('vqrfap', c_uint16),
        ('vqprt', c_uint16),
        ('vqfrsm', c_uint16),
        ('vqgran', c_uint16),
        ('reserved1', c_uint8*16),
        ('vifrt', c_uint32),
        ('virfa', c_uint32),
        ('virfap', c_uint16),
        ('viprt', c_uint16),
        ('vifrsm', c_uint16),
        ('vigran', c_uint16),
        ('reserved2', c_uint8*4016),        # NVM Set Attributes Entry
    ]


class SecondaryControllerListEntry(Structure):
    """Identify - SecondaryControllerListEntry Data Structure"""
    _pack_ = 1
    _fields_ = [
        ('scid', c_uint16),           # Number of Identifiers
        ('pcid', c_uint16),
        ('scs', c_uint8),
        ('reserved0', c_uint8*3),
        ('vfn', c_uint16),
        ('nvq', c_uint16),
        ('nvi', c_uint16),
        ('reserved1', c_uint8*18),
    ]


class SecondaryControllerList(Structure):
    """Identify - SecondaryControllerList Data Structure"""
    _pack_ = 1
    _fields_ = [
        ('ni', c_uint8),           # Number of Identifiers
        ('reserved0', c_uint8*31),
        ('entry', SecondaryControllerListEntry*127),
    ]


class LBAFormatDataStructure(Union):
    """Identify - LBA Format Data Structure, NVM Command Set Specific"""
    class Bits(Structure):
        _pack_ = 1
        _fields_ = [
            ('metas', c_uint32, 16),    # Metadata Size
            ('lbads', c_uint32, 8),     # LBA Data Size
            ('rp', c_uint32, 2),        # Relative Performance
            ('reserved', c_uint32, 6),
        ]

    _anonymous_ = ('bits', )
    _fields_ = [
        ('dword', c_uint32),
        ('bits', Bits)]


class NamespaceDataStructure(Structure):
    """Identify - Identify Namespace Data Structure, NVM Command Set Specific"""
    _pack_ = 1
    _fields_ = [
        ('ns', c_uint64),           # Namespace Size
        ('ncap', c_uint64),         # Namespace Capacity
        ('nuse', c_uint64),         # Namespace Utilization
        ('nsfeat', c_uint8),        # Namespace Features
        ('nlbaf', c_uint8),         # Number of LBA Formats
        ('flbaf', c_uint8),         # Formatted LBA Size
        ('mc', c_uint8),            # Metadata Capabilities
        ('dpc', c_uint8),           # End-to-end Data Protection Capabilities
        ('dps', c_uint8),           # End-to-end Data Protection Type Settings
        ('nmic', c_uint8),          # Namespace Multi-path I/O and Namespace Sharing Capabilities
        ('rescap', c_uint8),        # Reservation Capabilities
        ('fpi', c_uint8),           # Format Progress Indicator
        ('reserved0', c_uint8),
        ('nawun', c_uint16),        # Namespace Atomic Write Unit Normal
        ('nawupf', c_uint16),       # Namespace Atomic Write Unit Power Fail
        ('nacwu', c_uint16),        # Namespace Atomic Compare & Write Unit
        ('nabsn', c_uint16),        # Namespace Atomic Boundary Size Normal
        ('nabo', c_uint16),         # Namespace Atomic Boundary Offset
        ('nabspf', c_uint16),       # Namespace Atomic Boundary Size Power Fail
        ('reserved1', (c_uint8 * 2)),
        ('nvmecap', (c_uint8 * 16)),                # NVM Capacity:
        ('reserved2', (c_uint8 * 40)),
        ('nguid', (c_uint8 * 16)),                  # Namespace Globally Unique Identifier
        ('eui64', c_uint64),                        # IEEE Extended Unique Identifier
        ('lbaf', LBAFormatDataStructure * 16),      # LBA Format Support
        ('reserved3', (c_uint8 * 192)),
        ('vs', (c_uint8 * 3712)),                   # Vendor Specific
    ]

class IdentifyDword10(Union):

    class Bits(Structure):
        _pack_ = 1
        _fields_ = [
            ('cns', c_uint32, 8),
            ('reserved', c_uint32, 8),
            ('cntid', c_uint32, 16),
        ]

    class Dword(Structure):
        _pack_ = 1
        _fields_ = [
            ('dword', c_uint32),
        ]

    _anonymous_ = ('dword', 'bits')
    _fields_ = [
        ('dword', Dword),
        ('bits', Bits),
    ]


class GetfeaturesDword10(Union):
    class Bits(Structure):
        _pack_ = 1
        _fields_ = [
            ('fid', c_uint32, 8),
            ('sel', c_uint32, 3),
            ('reserved', c_uint32, 21),
        ]

    class Dword(Structure):
        _pack_ = 1
        _fields_ = [
            ('dword', c_uint32),
        ]

    _anonymous_ = ('dword', 'bits')
    _fields_ = [
        ('dword', Dword),
        ('bits', Bits),
    ]

class SetfeaturesDword10(Union):
    class Bits(Structure):
        _pack_ = 1
        _fields_ = [
            ('fid', c_uint32, 8),
            ('reserved', c_uint32, 23),
            ('sv', c_uint32, 1),
        ]

    class Dword(Structure):
        _pack_ = 1
        _fields_ = [
            ('dword', c_uint32),
        ]

    _anonymous_ = ('dword', 'bits')
    _fields_ = [
        ('dword', Dword),
        ('bits', Bits),
    ]

class Arbitration(Union):
    class Dword(Structure):
        _pack_ = 1
        _fields_ = [
            ('dword', c_uint32),
        ]

    class Bits(Structure):
        _pack_ = 1
        _fields_ = [
            ('arb', c_uint32, 3),
            ('res', c_uint32, 5),
            ('lpw', c_uint32, 8),
            ('mpw', c_uint32, 8),
            ('hpw', c_uint32, 8),
        ]

    _anonymous_ = ('dword', 'bits')
    _fields_ = [
        ('dword', Dword),
        ('bits', Bits),
    ]

class AttachnsDword10(Union):
    class Bits(Structure):
        _pack_ = 1
        _fields_ = [
            ('sel', c_uint32, 4),
            ('reserved', c_uint32, 28),
        ]

    class Dword(Structure):
        _pack_ = 1
        _fields_ = [
            ('dword', c_uint32),
        ]

    _anonymous_ = ('dword', 'bits')
    _fields_ = [
        ('dword', Dword),
        ('bits', Bits),
    ]

class CompareDword14(Union):
    class Bits(Structure):
        _pack_ = 1
        _fields_ = [
            ('eilbrt', c_uint32, 32),

        ]

    class Dword(Structure):
        _pack_ = 1
        _fields_ = [
            ('dword', c_uint32),
        ]

    _anonymous_ = ('dword', 'bits')
    _fields_ = [
        ('dword', Dword),
        ('bits', Bits),
    ]


class CompareDword15(Union):
    class Bits(Structure):
        _pack_ = 1
        _fields_ = [
            ('elbat', c_uint32, 16),
            ('elbatm', c_uint32, 16),

        ]

    class Dword(Structure):
        _pack_ = 1
        _fields_ = [
            ('dword', c_uint32),
        ]

    _anonymous_ = ('dword', 'bits')
    _fields_ = [
        ('dword', Dword),
        ('bits', Bits),
    ]

class DsmDword10(Union):
    class Bits(Structure):
        _pack_ = 1
        _fields_ = [
            ('nor', c_uint32, 8),
            ('reserved', c_uint32, 24)
        ]

    class Dword(Structure):
        _pack_ = 1
        _fields_ = [
            ('dword', c_uint32),
        ]

    _anonymous_ = ('dword', 'bits')
    _fields_ = [
        ('dword', Dword),
        ('bits', Bits),
    ]

class DsmDword11(Union):
    class Bits(Structure):
        _pack_ = 1
        _fields_ = [
            ('idr', c_uint32, 1),
            ('idw', c_uint32, 1),
            ('adc', c_uint32, 1),
            ('reserved', c_uint32, 29)
        ]

    class Dword(Structure):
        _pack_ = 1
        _fields_ = [
            ('dword', c_uint32),
        ]

    _anonymous_ = ('dword', 'bits')
    _fields_ = [
        ('dword', Dword),
        ('bits', Bits),
    ]

class SanitizeDword10(Union):
    class Bits(Structure):
        _pack_ = 1
        _fields_ = [
            ('sanact', c_uint32, 3),
            ('ause', c_uint32, 1),
            ('owpass', c_uint32, 4),
            ('oipdp', c_uint32, 1),
            ('ndas', c_uint32, 1),
            ('reserved', c_uint32, 22),
        ]

    class Dword(Structure):
        _pack_ = 1
        _fields_ = [
            ('dword', c_uint32),
        ]

    _anonymous_ = ('dword', 'bits')
    _fields_ = [
        ('dword', Dword),
        ('bits', Bits),
    ]

class SanitizeDword11(Union):
    class Bits(Structure):
        _pack_ = 1
        _fields_ = [
            ('ovrpat', c_uint32, 32),
        ]

    class Dword(Structure):
        _pack_ = 1
        _fields_ = [
            ('dword', c_uint32),
        ]

    _anonymous_ = ('dword', 'bits')
    _fields_ = [
        ('dword', Dword),
        ('bits', Bits),
    ]

class Nslist(Union):

    _pack_ = 1
    _fields_ = [
        ('identifiern', c_uint32*1024),

    ]

class Ctrllist(Structure):

    _pack_ = 1
    _fields_ = [
        ('noid', c_uint16),
        ('identifier0', c_uint16),
        ('identifier1', c_uint16),
        ('identifier2', c_uint16),
        ('identifiern', c_uint64 * 511),

    ]

class NamespaceManagement(Structure):

    _pack_ = 1
    _fields_ = [
        ('nsze', c_uint64),
        ('ncap', c_uint64),
        ('reserved0', c_uint8 * 10),
        ('flbas', c_uint8),
        ('reserved1', c_uint8 * 2),
        ('dps', c_uint8),
        ('nmic', c_uint8),
        ('reserved2', c_uint8 * 4065)

    ]

class CreatnsDword10(Union):
    class Bits(Structure):
        _pack_ = 1
        _fields_ = [
            ('sel', c_uint32, 4),
            ('reserved', c_uint32, 28)
        ]

    class Dword(Structure):
        _pack_ = 1
        _fields_ = [
            ('dword', c_uint32),
        ]

    _anonymous_ = ('dword', 'bits')
    _fields_ = [
        ('dword', Dword),
        ('bits', Bits),
    ]

class SecurityReceiveDword10(Union):
    class Bits(Structure):
        _pack_ = 1
        _fields_ = [
            ('nssf', c_uint32, 8),
            ('spsp0', c_uint32, 8),
            ('spsp1', c_uint32, 8),
            ('secp', c_uint32, 8),
        ]

    class Dword(Structure):
        _pack_ = 1
        _fields_ = [
            ('dword', c_uint32),
        ]

    _anonymous_ = ('dword', 'bits')
    _fields_ = [
        ('dword', Dword),
        ('bits', Bits),
    ]

class SecurityReceiveDword11(Union):
    class Bits(Structure):
        _pack_ = 1
        _fields_ = [
            ('atl', c_uint32, 32),

        ]

    class Dword(Structure):
        _pack_ = 1
        _fields_ = [
            ('dword', c_uint32),
        ]

    _anonymous_ = ('dword', 'bits')
    _fields_ = [
        ('dword', Dword),
        ('bits', Bits),
    ]

class SecuritySendDword10(Union):
    class Bits(Structure):
        _pack_ = 1
        _fields_ = [
            ('nssf', c_uint32, 8),
            ('spsp0', c_uint32, 8),
            ('spsp1', c_uint32, 8),
            ('secp', c_uint32, 8),
        ]

    class Dword(Structure):
        _pack_ = 1
        _fields_ = [
            ('dword', c_uint32),
        ]

    _anonymous_ = ('dword', 'bits')
    _fields_ = [
        ('dword', Dword),
        ('bits', Bits),
    ]

class SecuritySendDword11(Union):
    class Bits(Structure):
        _pack_ = 1
        _fields_ = [
            ('tl', c_uint32, 32),

        ]

    class Dword(Structure):
        _pack_ = 1
        _fields_ = [
            ('dword', c_uint32),
        ]

    _anonymous_ = ('dword', 'bits')
    _fields_ = [
        ('dword', Dword),
        ('bits', Bits),
    ]


class GetlogPagDword10(Union):
    class Bits(Structure):
        _pack_ = 1
        _fields_ = [
            ('lid', c_uint32, 8),
            ('reserved0', c_uint32, 8),
            ('numd', c_uint32, 12),
            ('reserved1', c_uint32, 4)
        ]

    class Dword(Structure):
        _pack_ = 1
        _fields_ = [
            ('dword', c_uint32),
        ]

    _anonymous_ = ('dword', 'bits')
    _fields_ = [
        ('dword', Dword),
        ('bits', Bits),
    ]


class GetlogPagDword11(Union):
    class Bits(Structure):
        _pack_ = 1
        _fields_ = [
            ('numdu', c_uint32, 16),
            ('reserved', c_uint32, 16),
        ]

    class Dword(Structure):
        _pack_ = 1
        _fields_ = [
            ('dword', c_uint32),
        ]

    _anonymous_ = ('dword', 'bits')
    _fields_ = [
        ('dword', Dword),
        ('bits', Bits),
    ]



class GetlogPagDword12(Union):
    class Bits(Structure):
        _pack_ = 1
        _fields_ = [
            ('lpol', c_uint32, 32),
        ]

    class Dword(Structure):
        _pack_ = 1
        _fields_ = [
            ('dword', c_uint32),
        ]

    _anonymous_ = ('dword', 'bits')
    _fields_ = [
        ('dword', Dword),
        ('bits', Bits),
    ]

class GetlogPagDword13(Union):
    class Bits(Structure):
        _pack_ = 1
        _fields_ = [
            ('lpou', c_uint32, 32),
        ]

    class Dword(Structure):
        _pack_ = 1
        _fields_ = [
            ('dword', c_uint32),
        ]

    _anonymous_ = ('dword', 'bits')
    _fields_ = [
        ('dword', Dword),
        ('bits', Bits),
    ]

class FirmwareLog(Structure):

    _pack_ = 1
    _fields_ = [
        ('afi', c_uint8),
        ('reserved0', c_uint8 * 7),
        ('frs1', c_uint64),
        ('frs2', c_uint64),
        ('frs3', c_uint64),
        ('frs4', c_uint64),
        ('frs5', c_uint64),
        ('frs6', c_uint64),
        ('frs7', c_uint64),
        ('reserved1', c_uint8 * 4032)

    ]


class VirtualizationManagemenDword10(Union):
    class Bits(Structure):
        _pack_ = 1
        _fields_ = [
            ('act', c_uint32, 4),
            ('reserved1', c_uint32, 4),
            ('resource_type', c_uint32, 3),
            ('reserved0', c_uint32, 5),
            ('cntlid', c_uint32, 16),

        ]

    class Dword(Structure):
        _pack_ = 1
        _fields_ = [
            ('dword', c_uint32),
        ]

    _anonymous_ = ('dword', 'bits')
    _fields_ = [
        ('dword', Dword),
        ('bits', Bits),
    ]


class VirtualizationManagemenDword11(Union):
    class Bits(Structure):
        _pack_ = 1
        _fields_ = [
            ('num_resource', c_uint32, 16),
            ('reserved0', c_uint32, 16),
        ]

    class Dword(Structure):
        _pack_ = 1
        _fields_ = [
            ('dword', c_uint32),
        ]

    _anonymous_ = ('dword', 'bits')
    _fields_ = [
        ('dword', Dword),
        ('bits', Bits),
    ]


class SmartHealth(Structure):
    """Get Log Page - SMART/Health Information (Log Identifier 02h)"""
    _pack_ = 1
    _fields_ = [
        ('cw', c_uint8),            # Critical Warning
        ('ct', c_uint16),           # Composite Temperature
        ('aspare', c_uint8),        # Available Spare
        ('asparet', c_uint8),       # Available Spare Threshold
        ('prctu', c_uint8),         # Percentage Used
        ('egcws', c_uint8),         # Endurance Group Critical Warning Summary
        ('rsv0', c_uint8 * 25),     # Reserve field 0
        ('dur', c_uint64 * 2),      # Data Units Read
        ('duw', c_uint64 * 2),      # Data Units Write
        ('hrc', c_uint64 * 2),      # Host Read Commands
        ('hwc', c_uint64 * 2),      # Host Write Commands
        ('cbt', c_uint64 * 2),      # Controller Busy Time
        ('pc', c_uint64 * 2),       # Power Cycles
        ('ponh', c_uint64 * 2),     # Power On Hours
        ('ussd', c_uint64 * 2),     # Unsafe Shutdowns
        ('mdie', c_uint64 * 2),     # Number of Error Information Log Entries
        ('neile', c_uint64 * 2),    # Media and Data Integrity Errors
        ('wctt', c_uint32),         # Warning Composite Temperature Time
        ('cctt', c_uint32),         # Critical Composite Temperature Time
        ('ts1', c_uint16),          # Temperature Sensor 1
        ('ts2', c_uint16),          # Temperature Sensor 2
        ('ts3', c_uint16),          # Temperature Sensor 3
        ('ts4', c_uint16),          # Temperature Sensor 4
        ('ts5', c_uint16),          # Temperature Sensor 5
        ('ts6', c_uint16),          # Temperature Sensor 6
        ('ts7', c_uint16),          # Temperature Sensor 7
        ('ts8', c_uint16),          # Temperature Sensor 8
        ('rsv1', c_uint8 * 296),    # Reserve field 1
    ]


class DevName(Structure):
    _pack_ = 1
    _fields_ = [
        ("name", c_char * 100)
    ]


class DevIndex(Structure):
    _pack_ = 1
    _fields_ = [
        ("index", c_int)
    ]


class DevList(Structure):
    """get dev list from dll"""
    _pack_ = 1
    _fields_ = [
        ('number', c_int),
        ('name', c_char * 100),
        ('index',c_int),

    ]
