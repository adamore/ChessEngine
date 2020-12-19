import chess
import chess
import struct
import os
import mmap
import random
import typing


ENTRY_STRUCT = struct.Struct(">QHHI")


class _EmptyMmap(bytearray):
    def size(self) -> int:
        return 0

    def close(self) -> None:
        pass


class OpeningBookCreator:
    def __init__(self, filepath):
        self.fd = open(filepath, "wb")
        return

    def printEntry(self, entry):
        byteEntry = ENTRY_STRUCT.pack(entry.key, entry.raw_move, entry.weight, entry.learn)
        print(byteEntry)

    def addEntry(self, entry):
        byteEntry = ENTRY_STRUCT.pack(entry.key, entry.raw_move, entry.weight, entry.learn)
        self.fd.write(byteEntry)
