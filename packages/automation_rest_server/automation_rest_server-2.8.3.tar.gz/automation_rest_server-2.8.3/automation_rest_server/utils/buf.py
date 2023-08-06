#!/usr/bin/env python
"""
Created on 2017/3/3

@author: yyang
"""
import os
import sys
import zlib
import platform
from ctypes import c_uint8, c_uint16, c_uint32, c_uint64, Array, Union, Structure, CDLL
from ctypes import POINTER, cast, sizeof, addressof, memmove, memset, pointer
from .system import ROOT_PATH


def get_string(content, little_endian=True):
    """Get string"""
    content_list = ["{:#04x}".format(x) for x in content]
    if little_endian:
        content_list.reverse()
    return "".join(content_list)


def dump_line(name, data, indent=0):
    """Dump line"""
    if data == "-":
        if name == "-":
            print("-" * 132)
        else:
            print("| {:<128} |".format(name))
    else:
        line = list()
        line.append("{:<15}".format("{}{}".format(" " * indent, name)))
        if data == "HEAD":
            line.append("{:<18}".format("HEX"))
            line.append("{:<22}".format("DEC"))
            line.append("{:<64}".format("BIN"))
        elif isinstance(data, (bool, int, float, type(sys.maxsize + 1))):
            line.append("{:<#18x}".format(data))
            line.append("{:<22}".format(data))
            line.append("{:<64}".format(bin(data)[2:]))
        else:
            line.append("{:<18}".format(data))
            line.append("{:<22}".format(data))
            line.append("{:<64}".format(data))

        print("| {} |".format(" | ".join(line)))


def dump(buf, indent, skip):
    """Dump UnionType/StructType to STDOUT"""
    if not isinstance(type(buf), (type(Union), type(Structure))):
        raise RuntimeError("Error type({})".format(type(buf)))

    skip = skip if isinstance(skip, list) else [skip]

    for field in getattr(buf, '_fields_'):
        name, types = field[0], field[1]
        for item in skip:
            if item in name and item:
                break
        else:
            value = getattr(buf, name)

            if isinstance(types, (type(Union), type(Structure))):
                dump_line(name, "", indent)
                dump(value, indent + 2, skip)
            elif isinstance(types, type(Array)):
                for i, item in enumerate(value):
                    if isinstance(type(item), (type(Union), type(Structure))):
                        dump_line("{}[{}]".format(name, i), "", indent)
                        dump(item, indent + 2, skip)
                    else:
                        dump_line("{}[{}]".format(name, i), item, indent)
            else:
                dump_line(name, value, indent)


class Malloc(object):
    """
    Malloc memory
    """

    def __init__(self, length=1, types=c_uint8):
        self.m_types = types  # types of item
        self.m_len = length  # count of items
        self.m_sizeof = sizeof(self.m_types)  # size of item
        self.m_size = self.m_len * self.m_sizeof  # count of bytes
        # noinspection PyTypeChecker,PyCallingNonCallable
        self.m_buf = (self.m_types * self.m_len)()  # buffer instance

    def __getitem__(self, key):
        return self.m_buf[key]

    def __setitem__(self, key, val):
        self.m_buf[key] = val

    def realloc(self, length=sys.maxsize, types=c_uint8):
        """Realloc memory to other types"""
        self.m_types = types
        self.m_len = min(length, self.m_size // sizeof(types))
        self.m_sizeof = sizeof(self.m_types)
        self.m_size = self.m_len * self.m_sizeof
        self.m_buf = cast(self.m_buf, POINTER(types))
        return self

    def len(self):
        """Get length"""
        return self.m_len

    def size(self):
        """Get total size"""
        return self.m_size

    def sizeof(self):
        return self.m_sizeof

    def types(self):
        """Get type"""
        return self.m_types

    def buffer(self):
        """Get instance"""
        return self.m_buf

    def addressof(self):
        """Get address of"""
        return addressof(self.m_buf)

    def pointer(self):
        """Get pointer"""
        return pointer(self.m_buf)

    def cast(self, types):
        """Cast buffer to type lp"""
        return cast(self.m_buf, POINTER(types))

    def convert(self, types, index=0):
        """Cast buffer to type lp and return buf[index]"""
        return cast(self.m_buf, POINTER(types))[index]

    def memset(self, value):
        """Set memory"""
        memset(self.m_buf, value, self.m_size)

    def memmove(self, offset, source, start, length):
        """Copy memory"""
        memmove(self.addressof() + offset, source.addressof() + start, length)

    def memcopy(self, stream, offset=0, length=sys.maxsize):
        """Set buffer by stream"""
        data = [i for i in list(stream)]
        size = min(length, len(data), self.m_size)
        for i in range(size):
            self.set_uint8(offset + i, data[i])

    def dump(self, offset=0, length=sys.maxsize, skip=""):
        """Dump buffer"""
        length = min(length, self.m_len)
        print("")
        if "ctypes" in str(self.m_types):
            self.dump_uint8(offset, length * self.m_sizeof)
        else:
            dump_line(str(self.m_types), "-")
            for i in range(offset, offset + length):
                print("")
                dump_line("BUFFER[{}]:".format(i), "HEAD")
                dump_line("-", "-")
                dump(self.m_buf[i], 0, skip)
                dump_line("-", "-")
        print("")

    def translate(self, start, size, types=c_uint8):
        length = min(self.m_size - (start // sizeof(types)) * sizeof(types), size) // sizeof(types)
        offset = start // sizeof(types)
        memory = cast(self.m_buf, POINTER(types))
        return memory, offset, length

    def dump_diff(self, dest, src_start=0, src_size=sys.maxsize, dst_start=None, dst_size=None):
        dst_start = dst_start if dst_start is not None else src_start
        dst_size = dst_size if dst_size is not None else src_size

        src_buf, src_off, src_len = self.translate(src_start, src_size, c_uint32)
        dst_buf, dst_off, dst_len = dest.translate(dst_start, dst_size, c_uint32)
        print("")

        print("          ADDR_A  /  ADDR_B   :   DATA_A     DATA_B")
        print("-----------------------------------------------------")
        for i in range(min(src_len, dst_len)):
            src_index = i + src_off
            dst_index = i + dst_off
            if src_buf[src_index] != dst_buf[dst_index]:
                print("ADDRESS {:#010x}/{:#010x} : {:#010x} {:#010x}".format(
                    src_index * 4, dst_index * 4, src_buf[src_index], dst_buf[dst_index]))

    def dump_uint8(self, start=0, size=sys.maxsize):
        """Dump with uint8"""
        print("          0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f")
        print("---------------------------------------------------------")

        memory, offset, length = self.translate(start, size, c_uint8)

        for i in range(offset, offset + length, 0x10):
            data = ["{:02x}".format(d) for d in memory[i:min(i + 0x10, offset + length)]]
            print("{:#08x}: {}".format(i, " ".join(data)))

    def dump_uint32(self, start=0, size=sys.maxsize):
        """Dump with uint32"""
        print("         0        1        2        3       ")
        print("--------------------------------------------")

        memory, offset, length = self.translate(start, size, c_uint32)

        for i in range(offset, offset + length, 0x4):
            data = ["{:08x}".format(d) for d in memory[i:min(i + 0x4, offset + length)]]
            print("{:#08x}: {}".format(i, " ".join(data)))

    def dump_uint8_uart(self, start=0, size=sys.maxsize):
        """Dump with uint32"""
        memory, offset, length = self.translate(start, size, c_uint8)

        for i in range(offset, offset + length, 0x10):
            data = ["{:02x}".format(d) for d in memory[i:min(i + 0x10, offset + length)]]
            print("{}".format(" ".join(data)))

    def set_sub_buffer(self, offset, size):
        """Set sub buffer"""
        p_buff = cast(self.m_buf, POINTER(c_uint8))
        d_list = Malloc(size)
        if (offset + size) > self.m_len:
            raise RuntimeError("[ERR] out of range(offset: {}, size: {})".format(offset, size))
        for off in range(offset, offset + size):
            d_list.set_uint8(off - offset, p_buff[off])
        return d_list

    def mask(self, buff):
        """Mask data"""
        for i in range(buff.size()):
            mask = buff.get_uint8(i)
            if mask == 1:
                self.set_uint8(i, 0)

    def get_string(self, offset, length):
        """Get string of buffer"""
        dat_list = list()
        p_buff = cast(self.m_buf, POINTER(c_uint8))
        for i in range(length):
            off = offset + i
            ret = "{:#04x}".format(p_buff[off])
            dat_list.append(ret)
        dat_list.reverse()
        ret = "".join(dat_list)
        return ret

    def ascii_to_string(self, offset, length):
        dat_list = list()
        p_buff = cast(self.m_buf, POINTER(c_uint8))
        for i in range(length):
            off = offset + i
            ret = "{}".format(chr(p_buff[off]))
            dat_list.append(ret)
        ret = "".join(dat_list)
        return ret

    def get(self, types, index):
        if not 0 <= index < self.m_size // sizeof(types):
            raise RuntimeError("[ERR] out of range(types: {}, index: {})".format(types, index))

        return cast(self.m_buf, POINTER(types))[index]

    def set(self, types, index, value):
        if not 0 <= index < self.m_size // sizeof(types):
            raise RuntimeError("[ERR] out of range(types: {}, index: {})".format(types, index))

        cast(self.m_buf, POINTER(types))[index] = value

    def get_uint8(self, offset):
        return self.get(c_uint8, offset)

    def get_uint16(self, offset):
        return self.get(c_uint16, offset // 2)

    def get_uint32(self, offset):
        return self.get(c_uint32, offset // 4)

    def get_uint64(self, offset):
        return self.get(c_uint64, offset // 8)

    def set_uint8(self, offset, value):
        self.set(c_uint8, offset, value)

    def set_uint16(self, offset, value):
        self.set(c_uint16, offset // 2, value)

    def set_uint32(self, offset, value):
        self.set(c_uint32, offset // 4, value)

    def set_uint64(self, offset, value):
        self.set(c_uint64, offset // 8, value)

    def set_multi_bytes(self, offset, length, buff):
        """Set multiple bytes"""
        for i in range(length):
            self.set_uint8(offset + i, buff.get_uint8(i))

    def set_multi_bytes_fix(self, offset, length, val):
        """Set multiple bytes with fixed data"""
        for i in range(length):
            self.set_uint8(offset + i, val)

    def set_multi_dword(self, stream, offset=0, length=1):
        """Set buffer with multi-dword"""
        # data = map(ord, list(stream))
        for i in range(length):
            self.set_uint32(offset + i * 4, stream[i])

    def set_multi_qword(self, stream, offset=0, length=1):
        """Set buffer with multi-qword"""
        # data = map(ord, list(stream))
        for i in range(length):
            self.set_uint64(offset + i * 8, stream[i])

    def write(self, path, offset=0, mode='wb'):
        """Write buffer to file"""
        with open(path, mode) as fpath:
            fpath.seek(offset, 0)
            fpath.write(self.m_buf)

    def read(self, path):
        """Read from file to buffer"""
        with open(path, "rb") as fpath:
            memmove(self.m_buf, fpath.read(), self.m_size)

    def write_string(self, path, offset=0, mode='wb'):
        """Write buffer to file with string"""
        with open(path, mode) as fpath:
            fpath.seek(offset, 2)
            string = "".join([chr(i) for i in list(self.m_buf)])
            fpath.write(string)

    def copy_value(self, value):
        """Copy value"""
        memmove(self.m_buf, value, self.m_size)

    def crc32(self):
        """Get crc32"""
        return zlib.crc32(self.m_buf) & 0xffffffff
