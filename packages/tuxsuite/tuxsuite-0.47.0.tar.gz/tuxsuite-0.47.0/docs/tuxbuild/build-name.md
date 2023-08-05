# Build Name

`build-name` (or `build_name` in a build-set) is an optional argument that may
be passed in with each build. If supplied, the string will be passed through to
the resulting build status.

This is most typically used along with build-sets, to provide human friendly
names for various build combinations for reporting purposes.

## Examples

### `tuxsuite build`

Perform a mainline build with a descriptive build-name.

```sh
tuxsuite build \
--git-repo 'https://github.com/torvalds/linux.git' \
--git-ref master \
--target-arch arm64 \
--toolchain clang-nightly \
--kconfig tinyconfig \
--build-name "arm64 clang-nightly tinyconfig mainline"
```

The resulting `status.json` will have a `build_name` field with the desired
value passed through, excerpted below:

```json
{
    "build_key": "1oiYvkUr1ctXdkV7KCLZ6320JVw",
    "build_name": "arm64 clang-nightly tinyconfig mainline",
    "build_status": "pass",
...
```

### `tuxsuite build-set`

In a build-set, each build can have a `build_name`.

Given `./example.yaml` containing the following:

```yaml
sets:
  - name: example
    builds:
      - build_name: arm64 gcc-9 defconfig
        target_arch: arm64
        toolchain: gcc-9
        kconfig: defconfig
      - build_name: arm64 gcc-9 tinyconfig
        target_arch: arm64
        toolchain: gcc-9
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

The resulting `status.json` of each build will have a `build_name` field in
each build result.
