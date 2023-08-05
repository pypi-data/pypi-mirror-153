# Toolchains

`toolchain` is a required argument, and may be one of the following values:

- `gcc-8`
- `gcc-9`
- `gcc-10`
- `gcc-11`
- `clang-10`
- `clang-11`
- `clang-12`
- `clang-13`
- `clang-14`
- `clang-nightly`
- `clang-android`
- `rust`
- `rustgcc`
- `rustclang`
- `rustllvm`

Most toolschains are obtained from Debian and are updated on the first day of
each month, with the following exceptions:

- `clang-nightly` comes from [apt.llvm.org](https://apt.llvm.org/) directly,
  and is updated daily.
- `clang-android` comes from the [Android Clang/LLVM
  Prebuilts](https://android.googlesource.com/platform/prebuilts/clang/host/linux-x86/)
  repository and is updated monthly.
- For `rust`, `rustgcc`, `rustclang` and `rustllvm`, `rustc` comes as prebuilt
  binary release from [rust-lang.org](https://rust-lang.org/), `gcc` and
  `clang` come from Debian, and they are updated monthly.

## Examples

### `tuxsuite build`

Perform an arm64 tinyconfig build against mainline using the most recent
nightly version of Clang.

```sh
tuxsuite build \
--git-repo 'https://github.com/torvalds/linux.git' \
--git-ref master \
--target-arch arm64 \
--toolchain clang-nightly \
--kconfig tinyconfig
```

### `tuxsuite build-set`

Perform an arm64 tinyconfig build-set with 4 supported versions of clang.

Given `./example.yaml` containing the following:

```yaml
sets:
  - name: example
    builds:
      - toolchain: clang-nightly
        target_arch: arm64
        kconfig: tinyconfig
      - toolchain: clang-12
        target_arch: arm64
        kconfig: tinyconfig
      - toolchain: clang-11
        target_arch: arm64
        kconfig: tinyconfig
      - toolchain: clang-10
        target_arch: arm64
        kconfig: tinyconfig
```

Perform the build-set:

```sh
tuxsuite build-set \
--git-repo 'https://github.com/torvalds/linux.git' \
--git-ref master \
--tux-config example.yaml \
--set-name example
```
