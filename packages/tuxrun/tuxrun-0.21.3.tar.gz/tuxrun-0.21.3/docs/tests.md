# Tests

TuxRun support some tests, each tests is supported on some but not all architectures.

!!! tip "Listing tests"
    You can list the supported tests with:
    ```shell
    tuxrun --list-tests
    ```

## FVP AEMvA device

The following tests are supported by the default root filesystem.

Device    | Tests                                                             | Parameters |
----------|-------------------------------------------------------------------|------------|
fvp-aemva | command                                                           |            |
fvp-aemva | kselftest-(gpio, ipc, ir, kcmp, kexec, kvm, rseq, rtc)            |  KSELFTEST |
fvp-aemva | kunit\*                                                           |            |
fvp-aemva | ltp-(fcntl-locktests, fs_bind, fs_perms_simple, fsx, nptl, smoke) |            |
fvp-aemva | perf                                                              |            |
fvp-aemva | rcutorture                                                        |            |
fvp-aemva | v4l2                                                              |            |

The following tests are not supported by the default root filesystem. You should
provide a custom root filesystem.

Device    | Tests                                                                                                                                         |
----------|-----------------------------------------------------------------------------------------------------------------------------------------------|
fvp-aemva | libgpiod                                                                                                                                      |
fvp-aemva | libhugtlbfs                                                                                                                                   |
fvp-aemva | ltp-(cap_bounds, commands, containers, crypto, cve, filecaps, fs, hugetlb, io, ipc, math, mm, pty, sched, securebits, syscalls, tracing)      |

!!! tip "Passing parameters"
    In order to pass parameters, use `tuxrun --parameters KSELFTEST=http://.../kselftest.tar.xz`

!!! info "kselftest parameters"
    The `CPUPOWER` and `KSELFTEST` parameters are not mandatory. If kselftest
    is present on the filesystem (in `/opt/kselftests/default-in-kernel/`) then the
    parameter is not required.

!!! warning "KUnit config"
    In order to run KUnit tests, the kernel should be compiled with
    ```
    CONFIG_KUNIT=m
    CONFIG_KUNIT_ALL_TESTS=m
    ```
    The **modules.tar.xz** should be given with `--modules https://.../modules.tar.xz`.


## FVP Modello devices

Device              | Tests        | Parameters                       |
--------------------|--------------|----------------------------------|
fvp-morello-android | binder       |                                  |
fvp-morello-android | bionic       | GTEST_FILTER\* BIONIC_TEST_TYPE\*|
fvp-morello-android | boottest     |                                  |
fvp-morello-android | boringssl    | SYSTEM_URL                       |
fvp-morello-android | compartment  | USERDATA                         |
fvp-morello-android | device-tree  |                                  |
fvp-morello-android | dvfs         |                                  |
fvp-morello-android | libjpeg-turbo| LIBJPEG_TURBO_URL, SYSTEM_URL    |
fvp-morello-android | libpdfium    | PDFIUM_URL, SYSTEM_URL           |
fvp-morello-android | libpng       | PNG_URL, SYSTEM_URL              |
fvp-morello-android | lldb         | LLDB_URL, TC_URL                 |
fvp-morello-android | logd         | USERDATA                         |
fvp-morello-android | multicore    |                                  |
fvp-morello-android | zlib         | SYSTEM_URL                       |
fvp-morello-busybox | purecap      |                                  |
fvp-morello-oe      | fwts         |                                  |

!!! tip "Passing parameters"
    In order to pass parameters, use `tuxrun --parameters USERDATA=http://.../userdata.tar.xz`

!!! tip "Default parameters"
    **GTEST_FILTER** is optional and defaults to
    ```
    string_nofortify.*-string_nofortify.strlcat_overread:string_nofortify.bcopy:string_nofortify.memmove
    ```
    **BIONIC_TEST_TYPE** is optional and defaults to `static`. Valid values are `dynamic` and `static`.

## QEMU devices

The following tests are supported by the default root filesystem.

Device  | Tests                                                             | Parameters         |
--------|-------------------------------------------------------------------|--------------------|
qemu-\* | command                                                           |                    |
qemu-\* | kselftest-(gpio, ipc, ir, kcmp, kexec, kvm, rseq, rtc)            | CPUPOWER KSELFTEST |
qemu-\* | kunit\*                                                           |                    |
qemu-\* | ltp-(fcntl-locktests, fs_bind, fs_perms_simple, fsx, nptl, smoke) |                    |
qemu-\* | perf                                                              |                    |
qemu-\* | rcutorture                                                        |                    |
qemu-\* | v4l2                                                              |                    |

The following tests are not supported by the default root filesystem. You should
provide a custom root filesystem.

Device  | Tests                                                                                                                                    |
--------|------------------------------------------------------------------------------------------------------------------------------------------|
qemu-\* | libgpiod                                                                                                                                 |
qemu-\* | libhugtlbfs                                                                                                                              |
qemu-\* | ltp-(cap_bounds, commands, containers, crypto, cve, filecaps, fs, hugetlb, io, ipc, math, mm, pty, sched, securebits, syscalls, tracing) |

!!! tip "Passing parameters"
    In order to pass parameters, use `tuxrun --parameters KSELFTEST=http://.../kselftest.tar.xz`

!!! info "kselftest parameters"
    The `CPUPOWER` and `KSELFTEST` parameters are not mandatory. If kselftest
    is present on the filesystem (in `/opt/kselftests/default-in-kernel/`) then the
    parameter is not required.

!!! warning "KUnit config"
    In order to run KUnit tests, the kernel should be compiled with
    ```
    CONFIG_KUNIT=m
    CONFIG_KUNIT_ALL_TESTS=m
    ```
    The **modules.tar.xz** should be given with `--modules https://.../modules.tar.xz`.
