# Git Ref and Git SHA

Either `git-ref` or `git-sha` must be specified.

If `git-ref` (or `git_ref` in a build-set) is specified, the branch name or tag
name will be checked out and built.

If `git-sha` (or `git_sha` in a build-set) is specified, the specific commit
will be checked out and built. Partial SHAs are not allowed - it must be a full
40-character git SHA.

## Examples

### `tuxsuite build`

#### Build using `git-sha`

Perform an x86_64 defconfig build using clang-12 against a specific git SHA.

```sh
tuxsuite build \
--git-repo 'https://github.com/torvalds/linux.git' \
--git-sha f40ddce88593482919761f74910f42f4b84c004b \
--target-arch x86_64 \
--toolchain clang-12 \
--kconfig defconfig
```

#### Build using `git-ref`

Perform an x86_64 defconfig build using clang-12 against a specific git tag.

```sh
tuxsuite build \
--git-repo 'https://github.com/torvalds/linux.git' \
--git-ref v5.11 \
--target-arch x86_64 \
--toolchain clang-12 \
--kconfig defconfig
```

### `tuxsuite build-set`

In a build-set, `git_sha` or `git_ref` may be listed in the build-set file if
it varies for each build, but usually it is given at the command line so that a
build-set file can be reused against multiple git versions.

#### Specifying git-ref at the command line

Perform an x86_64 defconfig build-set with 4 versions of clang.

Given `./example.yaml` containing the following:

```yaml
sets:
  - name: example
    builds:
      - toolchain: clang-nightly
        target_arch: arm64
        kconfig: defconfig
      - toolchain: clang-12
        target_arch: arm64
        kconfig: defconfig
      - toolchain: clang-11
        target_arch: arm64
        kconfig: defconfig
      - toolchain: clang-10
        target_arch: arm64
        kconfig: defconfig
```

Perform the build-set:

```sh
tuxsuite build-set \
--git-repo 'https://github.com/torvalds/linux.git' \
--git-ref master \
--tux-config example.yaml \
--set-name example
```

#### Specifying git_ref in a build-set

Perform an arm64 tinyconfig build-set against three different git versions.

**Note that it is `git_ref` and `git_sha` in a build-set file, and `git-ref`
and `git-sha` at the command-line.**

Given `./example.yaml` containing the following:

```yaml
sets:
  - name: example
    builds:
      - toolchain: clang-nightly
        target_arch: arm64
        kconfig: tinyconfig
        git_repo: https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git
        git_ref: v5.9
      - toolchain: clang-nightly
        target_arch: arm64
        kconfig: tinyconfig
        git_repo: https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git
        git_ref: v5.10
      - toolchain: clang-nightly
        target_arch: arm64
        kconfig: tinyconfig
        git_repo: https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git
        git_ref: master
```

Perform the build-set:

```sh
tuxsuite build-set \
--git-repo "https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git" \
--tux-config example.yaml \
--set-name example
```
