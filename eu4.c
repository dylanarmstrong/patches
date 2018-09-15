#include <stdio.h>

// Patch eu4 file so checksum always validates
// Just changing SETE to SETNO
int main(int argc, char **argv) {
  FILE *fp = argc > 1 ? fopen(argv[1], "r+b") : stdin;
  unsigned char buf[16];
  int found1 = 0;
  int found2 = 0;
  int patched = 0;
  long int pos = 0;
  size_t bytes;
  size_t find1[6] = { 0xef, 0xff, 0x85, 0xf6, 0x0f, 0x94 };
  size_t find2[6] = { 0x59, 0x01, 0x85, 0xc0, 0x0f, 0x94 };
  size_t hex;
  size_t i;
  size_t patch[1] = { 0x91 };
  size_t read = sizeof buf;

  if (fp == NULL) {
    fprintf(stderr, "Can't open file at: %s\n", argv[1]);
    return 1;
  }

  while ((bytes = fread(buf, sizeof *buf, read, fp)) == read) {
    for (i = 0; i < read; i++) {
      pos++;

      hex = buf[i];

      if (hex == find1[found1]) {
        found1++;
      } else {
        found1 = 0;
      }

      if (hex == find2[found2]) {
        found2++;
      } else {
        found2 = 0;
      }

      if (found1 == 6 || found2 == 6) {
        patched++;
        printf("Patching 0x%lX\n", pos - i + 2);
        fseek(fp, pos - i + 2, SEEK_SET);
        fwrite(patch, 1, 1, fp);

        if (found1 == 6) {
          found1 = 0;
        } else if (found2 == 6) {
          found2 = 0;
        }
      }
    }
  }

  fclose(fp);

  if (patched != 2) {
    fprintf(stderr, "There should have been 2 offsets found!\n");
    return 1;
  }

  return 0;
}

