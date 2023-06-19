## Binary Patches

### Note

Only tested on MacOS

### Run

```bash
cd ~/Library/Application Support/Steam/steamapps/common/Crusader Kings III/binaries/ck3.app/Contents/MacOS
python3 /path/to/ck3.py
```

### Compilation
`gcc patch.c -o patch && ./patch file`

### ck3.py
Disable checksum validation (Working on 1.9.2)

### eu4.c
Disable checksum validation (Not working as of 2018-09-25)

### eu4.py
Disable checksum validation and enable enable_all_commands (Working on 1.28.3)
