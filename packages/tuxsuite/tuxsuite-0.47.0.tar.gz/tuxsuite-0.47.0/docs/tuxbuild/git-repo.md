# Git Repo

`git-repo` (or `git_repo` in a build-set) is a required argument, and should be
an `https` url to a git repository.

## Examples

### `tuxsuite build`

Perform an i386 tinyconfig build against mainline using gcc-9.

```sh
tuxsuite build \
--git-repo 'https://github.com/torvalds/linux.git' \
--git-ref master \
--target-arch i386 \
--toolchain gcc-9 \
--kconfig tinyconfig
```

### `tuxsuite build-set`

In a build-set, `git_repo` may be listed in the build-set file if it varies for
each build, but usually it is given at the command line so that a build-set
file can be used againsted any repository.

#### Specifying git-repo at the command line

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

#### Specifying git_repo in a build-set

Perform an arm64 tinyconfig build-set against three different git repos and git
versions.

**Note that it is `git_repo` in a build-set file, and `git-repo` at the
command-line.**

Given `./example.yaml` containing the following:

```yaml
sets:
  - name: example
    builds:
      - toolchain: clang-nightly
        target_arch: arm64
        kconfig: tinyconfig
        git_repo: https://git.kernel.org/pub/scm/linux/kernel/git/next/linux-next.git
        git_ref: master
      - toolchain: clang-nightly
        target_arch: arm64
        kconfig: tinyconfig
        git_repo: https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git
        git_ref: linux-5.10.y
      - toolchain: clang-nightly
        target_arch: arm64
        kconfig: tinyconfig
        git_repo: https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git
        git_ref: master
```

Perform the build-set:

```sh
tuxsuite build-set \
--tux-config example.yaml \
--set-name example
```
