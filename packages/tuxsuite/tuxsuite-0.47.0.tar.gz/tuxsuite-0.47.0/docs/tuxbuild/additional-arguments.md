# Additional Arguments

## No Wait

`--no-wait` is an optional argument which submits the build and
returns immediately printing the build artifacts to `stdout`.

## Show Logs

`--show-logs` is an optional argument to print build logs to stderr, after the
build(s), in the event of warnings or errors.

## Quiet Mode

Passing `-q`/`--quiet` to `build` or `build-set` will cause tuxsuite to
produce minimal output. In particular:

- Only the final build artifacts URLs will be printed to `stdout`.
- No progress information will be printed while waiting for the builds to finish.
- Warnings and errors, including build failures, will be printed to `stderr`.

```
$ tuxsuite build --quiet --git-repo 'https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git' --git-ref master --target-arch arm64 --kconfig defconfig --toolchain gcc-9
https://builds.tuxbuild.com/_YNU6WjSnKv_Akdajrnhyw/
```

This is handy for use in automation/CI scripts.

## json-out

The `--json-out \<filename.json\>` command-line option accepts a filesystem path,
where it will write a status file in json format at the end of a build or a
build-set. The file will contain, for example:

```json
{
    "build_key": "1oiYvkUr1ctXdkV7KCLZ6320JVw",
    "build_name": "arm64 clang-nightly tinyconfig mainline",
    "build_status": "pass",
    "client_token": "6f288ec4-38aa-4968-8082-04790901fc44",
    "download_url": "https://builds.tuxbuild.com/1oiYvkUr1ctXdkV7KCLZ6320JVw/",
    "environment": {},
    "errors_count": 0,
    "git_describe": "v5.11",
    "git_ref": "master",
    "git_repo": "https://github.com/torvalds/linux.git",
    "git_sha": "f40ddce88593482919761f74910f42f4b84c004b",
    "git_short_log": "f40ddce88593 (\"Linux 5.11\")",
    "kconfig": [
        "tinyconfig"
    ],
    "kernel_image": "",
    "kernel_version": "5.11.0",
    "make_variables": {},
    "status_message": "build completed",
    "target_arch": "arm64",
    "targets": [],
    "toolchain": "clang-nightly",
    "tuxbuild_status": "complete",
    "warnings_count": 0
}
```

The --json-out result of a build set will contain a list of entries.

## image-sha

`--image-sha` is an optional argument which submits the build and
instructs tuxbuild to use / pin the container image specified by the
complete sha256 of the image. The container image complete sha256 is
64 hexadecimal digits.

## no-cache

`--no-cache` is an optional argument which performs the build without
using any compilation cache.
