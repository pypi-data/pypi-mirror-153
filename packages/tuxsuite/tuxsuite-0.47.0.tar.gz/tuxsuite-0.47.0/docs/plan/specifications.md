# Plan Specifications

A plan is a yaml file with the folowing specification.

## Full plan example

Full plan example:

```yaml
version: 1
name: <plan name>
description: <plan description>
jobs:
- build: {toolchain: gcc-8, target_arch: i386, kconfig: tinyconfig}
  test: {device: qemu-i386, tests: [ltp-smoke]}

- builds:
  - {toolchain: gcc-8, target_arch: i386, kconfig: tinyconfig}
  - {toolchain: gcc-9, target_arch: i386, kconfig: tinyconfig}
  - {toolchain: gcc-10, target_arch: i386, kconfig: tinyconfig}
  test: {device: qemu-i386, tests: [ltp-smoke]}
- builds:
  - {toolchain: clang-10, target_arch: i386, kconfig: tinyconfig}
  - {toolchain: clang-11, target_arch: i386, kconfig: tinyconfig}
  - {toolchain: clang-nightly, target_arch: i386, kconfig: tinyconfig}
  test: {device: qemu-i386}

- build: {toolchain: clang-nightly, target_arch: i386, kconfig: tinyconfig}
  tests:
  - {device: qemu-i386}
  - {device: qemu-i386, tests: [ltp-smoke]}

- builds:
  - {toolchain: gcc-8, target_arch: i386, kconfig: tinyconfig}
  - {toolchain: gcc-9, target_arch: i386, kconfig: tinyconfig}
  - {toolchain: gcc-10, target_arch: i386, kconfig: tinyconfig}
  tests:
  - {device: qemu-i386}
  - {device: qemu-i386, tests: [ltp-smoke]}

- tests:
  - {kernel: https://storage.tuxboot.com/arm64/Image, device: qemu-arm64, tests: [ltp-smoke]}
  - {kernel: https://storage.tuxboot.com/i386/bzImage, device: qemu-i386, tests: [ltp-smoke]}
  - {kernel: https://storage.tuxboot.com/mips64/vmlinux, device: qemu-mips64, tests: [ltp-smoke]}
  - {kernel: https://storage.tuxboot.com/ppc64/vmlinux, device: qemu-ppc64, tests: [ltp-smoke]}
  - {kernel: https://storage.tuxboot.com/riscv64/Image, device: qemu-riscv64, tests: [ltp-smoke]}
  - {kernel: https://storage.tuxboot.com/x86_64/bzImage, device: qemu-x86_64, tests: [ltp-smoke]}
```

## Version

Currently, tuxsuite only supports version 1.

```yaml
version: 1
```

## Name and description

The name and description are only used if they are not defined on the command line.

```yaml
name: plan name
description: plan description
```

They can be overriden on the command line:

```
tuxsuite plan --name "another name" --description "antoher description"
```

## Jobs

Most of the configuration takes place in the `jobs` section.

This section is a list of dictionary with one or two keys each.

Allowed combinations are:

* builds
* builds and test
* builds and tests
* build and test
* build and tests
* tests

### Combinations

Each combinations has a different meaning:

* **builds**: list of builds
* **builds** and **test**: list of builds. For each build, the given test will be run
* **builds** and **tests**: list of builds. For each build, the given tests will be run
* **build** and **test**: a single build. The test will be run for this build
* **build** and **tests**: a single build. Every test will be run for this build
* **tests**: a list of kernels and modules to test

### Builds

A build is defined by a dictionary:

```yaml
toolchain: gcc-8
target_arch: i386
kconfig: defconfig
```

When specifying multiple builds, the job should be a list of dictionaries like:

```yaml
- builds:
  - {toolchain: gcc-8, target_arch: i386, kconfig: tinyconfig}
  - {toolchain: gcc-9, target_arch: i386, kconfig: tinyconfig}
  - {toolchain: gcc-10, target_arch: i386, kconfig: tinyconfig}
```

### Tests

A test is defined by a dictionary:

```yaml
device: qemu-i386
tests: [ltp-smoke]
```

In this case, the test is valid only when linked with a test.

To define a single test, a `kernel` is mandatory:

```yaml
device: qemu-i386
tests: [ltp-smoke]
kernel: https://storage.tuxboot.com/i386/bzImage
```
