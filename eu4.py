#!/usr/bin/env python3

import re

###              ###
#   EU4 Patcher    #
#  Version 1.28.3  #
###              ###

filename = './eu4'

# Get address of bits
def search(find, s, offset = 0):
    return [(m.start() + offset) for m in re.finditer(find, s)]

def patch(offset, replace):
    with open(filename, 'r+b') as f:
        f.seek(offset)
        f.write(replace)

# Patch checksum, so custom mods do not disable Ironman
def patch_checksum(s):
    # Looking for SETE for checksum validation
    find = b'\x85\xc0\x0f\x94\x45\xef'
    # Replace 4th bit from offset
    offsets = search(find, s, 3)
    if len(offsets) > 0:
        # Replace 94 with 91 (SETE to SETNO)
        for offset in offsets:
            print('Patching checksum offset: {}'.format(hex(offset)))
            patch(offset, b'\x91')
    else:
        # Already patched
        find = b'\x85\xc0\x0f\x91\x45\xef'
        offsets = search(find, s)
        if len(offsets) > 0:
            print('Cannot patch checksum, already patched')
        else:
            print('Cannot patch checksum, unsupported version')

# Patch enable_all_commands
# Still requires any argument to enable_all_commands
def patch_enable_all_commands(s):
    find = b'\x39\xfa\x0f\x85\xd5\x00\x00\x00'
    offsets = search(find, s, 2)
    if len(offsets) > 0:
        # Replace JNZ to JMP
        for offset in offsets:
            print('Patching enable_all_commands offset: {}'.format(hex(offset)))
            patch(offset, b'\xe9\x78\x00\x00\x00\x90')
    else:
        # Already patched
        find = b'\x39\xfa\xe9\x78\x00\x00\x00\x90'
        offsets = search(find, s)
        if len(offsets) > 0:
            print('Cannot patch enable_all_commands, already patched')
        else:
            print('Cannot patch enable_all_commands, unsupported version')

# Decrypt Ironman save file (without 'deiron' command)
def decrypt():
    pass

def main():
    s = None
    with open(filename, 'rb') as f:
        s = f.read()
    if s is None:
        print('Cannot read {}'.format(filename))
        exit(1)
    else:
        patch_checksum(s)
        patch_enable_all_commands(s)

if __name__ == '__main__':
    main()
