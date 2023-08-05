# Build Sets

TuxBuild can perform individual builds, but the real power is in performing a
large number of builds in parallel.

Build sets allow multiple builds to be defined in a structured YAML file, and
built in parallel with the `tuxbuild build-set` command.

The build set file is designed to be shareable, and may be referenced by URL or
file path so that many people and systems can reuse the same shared build set.

All of the command-line options that define a build can also be defined in a
build set file. If an argument is set in both a build set and also at the
command-line, the build set will have precedence.

Typically, things like `git-repo` and `git-ref` are excluded from build set
files, so that any build set can be run against any kernel. However, there are
use-cases for defining git parameters in build set files, and it is supported.

## Examples

### Curated Build Sets

TuxSuite includes a curated example set of builds as a starting point at
[examples/](https://gitlab.com/Linaro/tuxsuite/-/tree/master/examples).

To build the `tinyconfigs` set from
[examples/](https://gitlab.com/Linaro/tuxsuite/-/tree/master/examples), run the following.

```
tuxsuite build-set --git-repo 'https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git' --git-ref master --tux-config https://gitlab.com/Linaro/tuxsuite/-/raw/master/examples/buildsets.yaml --set-name tinyconfigs
```

> **_NOTE:_** From version 0.43.0 of TuxSuite cli all build sets are
> converted to [plans](../plan/index.md) internally, which provides an
> efficient way of submitting multiple builds from the command line to
> the TuxBuild backend.
