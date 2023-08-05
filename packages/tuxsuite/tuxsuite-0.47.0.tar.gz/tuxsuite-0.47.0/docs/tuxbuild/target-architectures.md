# Target Architectures

`target-arch` (or `target_arch` in a build-set) is a required argument, and
defines the architecture of the resulting kernel. It may be one of the following:

- `arc`
- `arm`
- `arm64`
- `hexagon`
- `i386`
- `mips`
- `parisc`
- `powerpc`
- `riscv`
- `s390`
- `sh`
- `sparc`
- `x86_64`

Each architecture will be built from an x86_64 host.

## Examples

### `tuxsuite build`

Perform a powerpc tinyconfig build against mainline using the most recent
nightly version of Clang.

```sh
tuxsuite build \
--git-repo 'https://github.com/torvalds/linux.git' \
--git-ref master \
--target-arch powerpc \
--toolchain clang-nightly \
--kconfig tinyconfig
```

### `tuxsuite build-set`

Perform a defconfig build-set against 12 architectures using gcc-9 on latest
mainline.

Given `./example.yaml` containing the following:

```yaml
sets:
  - name: example
    builds:
      - {target_arch: arc,     toolchain: gcc-9, kconfig: defconfig}
      - {target_arch: arm,     toolchain: gcc-9, kconfig: defconfig}
      - {target_arch: arm64,   toolchain: gcc-9, kconfig: defconfig}
      - {target_arch: i386,    toolchain: gcc-9, kconfig: defconfig}
      - {target_arch: mips,    toolchain: gcc-9, kconfig: defconfig}
      - {target_arch: parisc,  toolchain: gcc-9, kconfig: defconfig}
      - {target_arch: powerpc, toolchain: gcc-9, kconfig: defconfig}
      - {target_arch: riscv,   toolchain: gcc-9, kconfig: defconfig}
      - {target_arch: s390,    toolchain: gcc-9, kconfig: defconfig}
      - {target_arch: sh,      toolchain: gcc-9, kconfig: defconfig}
      - {target_arch: sparc,   toolchain: gcc-9, kconfig: defconfig}
      - {target_arch: x86_64,  toolchain: gcc-9, kconfig: defconfig}
```

Perform the build-set:

```sh
tuxsuite build-set \
--git-repo 'https://github.com/torvalds/linux.git' \
--git-ref master \
--tux-config example.yaml \
--set-name example
```
