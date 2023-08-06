# Running under QEMU

TuxRun allows to run a linux kernel under QEMU.

!!! note "Supported devices"
    See the [architecture matrix](devices.md#qemu-devices) for the supported devices.

## Boot testing

In order to run a simple boot test on arm64:

```shell
tuxrun --device qemu-arm64 --kernel http://storage.tuxboot.com/arm64/Image
```

!!! tip "Artefact URLs"
    Artefacts (kernel, dtb, rootfs, ...) can be either local or remote
    (http/https url). TuxRun will automatically download a remote artefacts.

## Modules overlay

TuxRun allows to provide a custom **modules.tar.xz** archive that will be
extracted on top of the rootfs.

```shell
tuxrun --device qemu-arm64 \
       --kernel http://storage.tuxboot.com/arm64/Image \
       --modules modules.tar.xz
```

!!! warning "Modules format"
    The modules archive should be a **tar archive**, compressed with **xz**.

!!! tip "Overlays"
    Any overlay can be applied to the rootfs with the **--overlay** option.
    This option can be specified multiple times. Each overlay should be a
    **tar archive** compressed with **xz**.

## Boot arguments

You can specify custom boot arguments with:

```shell
tuxrun --device qemu-arm64 \
       --kernel http://storage.tuxboot.com/arm64/Image \
       --boot-args "initcall_debug"
```

## Running tests

You can run a specific test with:

```shell
tuxrun --device qemu-arm64 \
       --kernel http://storage.tuxboot.com/arm64/Image \
       --tests ltp-smoke
```

!!! tip "Multiple tests"
    Multiple tests can be specified after **--tests**.
    The tests will be executed one by one, in the order specified on the command-line.

## Custom command

You can run any command **inside** the VM with:

```shell
tuxrun --device qemu-arm64 \
       --kernel http://storage.tuxboot.com/arm64/Image \
       -- cat /proc/cpuinfo
```

!!! tip "Command and tests"
    When combining a custom command and tests, the custom command will be ran
    after all the tests.

## Timeouts

You can override the default timeouts with:

```shell
tuxrun --device qemu-armv5 \
       --tests ltp-smoke
       --timeouts deploy=10 boot=12 ltp-smoke=32
```

This will set the timeouts to:

* `deploy`: 10 minutes
* `boot`: 12 minutes
* `ltp-smoke`: 32 minutes

## TuxMake and TuxBuild

You can run tests against TuxMake or TuxBuild artefacts with `--tuxmake` or `--tuxbuild`:

```shell
tuxrun --tuxmake ~/.cache/tuxmake/builds/1
tuxrun --tuxbuild https://builds.tuxbuild.com/<ksuid>/
```

!!! tip "default device"
    For some architectures (like ARM), the tuxrun device should be specified with `--device`.
