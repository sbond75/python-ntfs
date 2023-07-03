from ntfs.BinaryParser import Block
from ntfs.BinaryParser import Mmap
from ntfs.FileMap import FileMap


class Volume(Block):
    """
    A volume is a logically contiguous run of bytes over which a FS is found.

    Use FlatVolume over this.
    """
    __unpackable__ = True
    def __init__(self, buf, offset, sector_size=512):
        super(Volume, self).__init__(buf, offset)
        self._sector_size = sector_size

    def __getitem__(self, index):
        if isinstance(index, slice):
            return self.__getslice__(index.start if index.start is not None else 0, index.stop if index.stop is not None else sys.maxsize)
        return self._buf[index + self._offset : index + self._offset + 1]

    def __getslice__(self, start, end):
        return self._buf[start + self._offset:end + self._offset]

    def __len__(self):
        return len(self._buf) - self._offset


class FlatVolume(Volume):
    """
    A volume found in a physically contiguous run of bytes.
    """
    def __init__(self, buf, offset, sector_size=512):
        super(FlatVolume, self).__init__(buf, offset, sector_size=sector_size)


def main():
    import sys

    # two methods
    with open(sys.argv[1], "rb") as f:
        buf = FileMap(f)
        v = FlatVolume(buf, int(sys.argv[2]))
        print(list(v[3:3+4]))

    # probably prefer this one
    with Mmap(sys.argv[1]) as buf:
        v = FlatVolume(buf, int(sys.argv[2]))
        print(list(v[3:3+4]))


if __name__ == "__main__":
    main()
