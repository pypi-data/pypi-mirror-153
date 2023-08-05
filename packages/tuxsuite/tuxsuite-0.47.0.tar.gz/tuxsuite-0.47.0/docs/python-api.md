# Python client API

The tuxsuite client can also be used from Python programs. The authentication
token needs to be in place in `~/.config/tuxsuite/config.ini`, or via the
`$TUXSUITE_TOKEN` environment variable.

## Single builds

```python
import tuxsuite

params = {
    "git_repo": "https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git",
    "git_ref": "master",
    "target_arch": "arm64",
    "toolchain": "gcc-9",
    "kconfig": [
      "defconfig"
    ],
}

# fire and forget
build = tuxsuite.Build(**params)
build.build()

# submit a build and wait for it to finish, quietly
build = tuxsuite.Build(**params)
build.build()
state = build.wait()
print(f"{state.icon} #{build}: #{state.message}")

# submit build and watch its progress
build = tuxsuite.Build(**params)
build.build()
for state in build.watch():
  print(f"{state.icon} #{build}: #{state.message}")
```

## Build sets

Build sets have a very similar api as individual builds, except that 1) the
majority of the parameters comes from the build set configured in
`~/.config/tuxsuite/builds.yaml` and 2) `wait()` will return a list of build
states. `watch()` works similarly but you get updates for all the builds as
soon as they change state.

```python
params = {
    "git_repo": "https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git",
    "git_ref": "master",
}
set_name = "my-build-set"

# fire and forget
build_set = tuxsuite.BuildSet(set_name, **params)
build_set.build()

# submit a build set, quietly wait for all of them to finish, then print their
# results
build_set = tuxsuite.BuildSet(set_name, **params)
build_set.build()
results = build_set.wait():
for state in results:
  print(f"{state.icon} #{state.build}: #{state.message}")

# submit build set and watch progress by printing each status update as it
# arrives
build_set = tuxsuite.BuildSet(set_name, **params)
build_set.build()
for state in build_set.watch():
  print(f"{state.icon} #{state.build}: #{state.message}")
```

## Single tests

```python
import tuxsuite

params = {
    "device": "qemu-x86_64",
    "kernel": "https://storage.tuxboot.com/x86_64/bzImage",
    "tests": ["ltp-smoke"],
}

# fire and forget
test = tuxsuite.Test(**params)
test.test()

# submit a test and wait for it to finish, quietly
test = tuxsuite.Test(**params)
test.test()
state = test.wait()
print(f"{state.icon} #{build}: #{state.message}")

# submit test and watch its progress
test = tuxsuite.Test(**params)
test.test()
for state in test.watch():
  print(f"{state.icon} #{test}: #{state.message}")
```
