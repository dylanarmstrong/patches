#!/usr/bin/env python3

###              ###
#   CK3 Patcher    #
#  Version 1.9.2   #
###              ###

filename = "./ck3"


def patch(offset, replace):
    with open(filename, "r+b") as f:
        f.seek(offset)
        f.write(replace)


# Patch checksum, so custom UI mods do not disable Ironman
def patch_checksum(s):
    # Looking for OnChecksumCalculated
    find = b"\x53\x48\x83\xec\x28\x48\x8d\x05\xa4\x16\x8e\x05"
    # We want to start on byte 48, and not 53
    offset = s.find(find) + 1
    if offset > 1:
        # Replace with a JMP to return immediately, as this method only sets if value doesn't match
        print("Patching checksum offset: {}".format(hex(offset)))
        patch(offset, b"\xe9\x75\x00\x00\x00")
    else:
        # Already patched
        find = b"\x53\xe9\x75\x00\x00\x00\x8d"
        offset = s.find(find)
        if offset > 0:
            print("Cannot patch checksum, already patched")
        else:
            print("Cannot patch checksum, unsupported version")


def main():
    s = None
    with open(filename, "rb") as f:
        s = f.read()
    if s is None:
        print("Cannot read {}".format(filename))
        exit(1)
    else:
        patch_checksum(s)


if __name__ == "__main__":
    main()
