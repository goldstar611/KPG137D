#!/usr/bin/python3

import sys


def main():
    if len(sys.argv) < 2:
        print("Usage:\n       {} [infile1] [infile2] [infile...]\n".format(sys.argv[0]))
        return None

    for arg in sys.argv[1:]:
        with open (arg, "r+b") as f:
            data = f.read()
            data_ba = bytearray(data)
            # ASSUMPTION: First 0x40 bytes are unencoded
            for i in range(0x40, len(data)):
                # ASSUMPTION: Rest of file is XOR encoded with a single byte
                # ASSUMPTION: Last byte in file is 0xFF
                data_ba[i] ^= data_ba[-1] ^ 0xFF
            f.seek(0)
            f.write(data_ba)
            f.truncate()

if __name__ == "__main__":
    main()
