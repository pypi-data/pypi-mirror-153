# Architecture and Toolchain Matrix

The following combinations of architecture and toolchain are supported.

|               | arc | arm | arm64 | hexagon | i386 | mips | parisc | powerpc | riscv | s390 | sh  | sparc | x86_64 |
| ------------- | --- | --- | ----- | ------- | ---- | ---- | ------ | ------- | ----- | ---- | --- | ----- | ------ |
| clang-10      | no  | yes | yes   | yes     | yes  | yes  | no     | yes     | yes   | yes  | no  | yes   | yes    |
| clang-11      | no  | yes | yes   | yes     | yes  | yes  | no     | yes     | yes   | yes  | no  | yes   | yes    |
| clang-nightly | no  | yes | yes   | yes     | yes  | yes  | no     | yes     | yes   | yes  | no  | yes   | yes    |
| clang-android | no  | yes | yes   | yes     | yes  | no   | no     | no      | no    | no   | no  | no    | yes    |
| gcc-11        | no  | yes | yes   | no      | yes  | yes  | yes    | yes     | yes   | yes  | yes | yes   | yes    |
| gcc-10        | no  | yes | yes   | no      | yes  | yes  | yes    | yes     | yes   | yes  | yes | yes   | yes    |
| gcc-8         | yes | yes | yes   | no      | yes  | yes  | yes    | yes     | yes   | yes  | yes | yes   | yes    |
| gcc-9         | yes | yes | yes   | no      | yes  | yes  | yes    | yes     | yes   | yes  | yes | yes   | yes    |
| rust          | no  | yes | yes   | no      | no   | no   | no     | yes     |yes    | no   | no  | no    | yes    |
| rustclang     | no  | yes | yes   | no      | no   | no   | no     | yes     |yes    | no   | no  | no    | yes    |
| rustgcc       | no  | yes | yes   | no      | no   | no   | no     | yes     |yes    | no   | no  | no    | yes    |
| rustllvm      | no  | yes | yes   | no      | no   | no   | no     | yes     |yes    | no   | no  | no    | yes    |

This can be retrieved programatically with the following command:

```
curl -s "https://api.tuxbuild.com/v1/supportmatrix"
```
