# Make Variables

The make variables argument is an optional positional set of arguments that
accepts key value pairs that are passed through as make variables to the build.

The set of available make variables is limited to the following.

- `C`
- `W`
- `LLVM`
- `LLVM_IAS`
- `LD`
- `AR`
- `NM`
- `STRIP`
- `OBJCOPY`
- `OBJDUMP`
- `READELF`
- `HOSTAR`
- `HOSTLD`

## Examples

### `tuxsuite build`

Example:

```
tuxsuite build \
--git-repo https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git \
--git-ref master \
--target-arch arm \
--toolchain clang-10 \
--kconfig tinyconfig \
W=1 LLVM=1
```

### `tuxsuite build-set`

In order to pass make variables in build-set use the following
syntax in a build-set file (`./example.yaml`):

```
sets:
  - name: example
    builds:
      - target_arch: arm64
        toolchain: clang-nighly
        kconfig: allnoconfig
        make_variables:
          C: "1"
          W: "1"
          LLVM: "1"
```

Perform the build-set:

```sh
tuxsuite build-set \
--git-repo 'https://github.com/torvalds/linux.git' \
--git-ref master \
--tux-config example.yaml \
--set-name example
```
