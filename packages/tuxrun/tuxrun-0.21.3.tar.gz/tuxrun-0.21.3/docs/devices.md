# Devices

TuxRun supports many architectures for both FVP and QEMU.

!!! tip "Listing devices"
    You can list the supported devices with:
    ```shell
    tuxrun --list-devices
    ```

## FVP devices

Device                | FVP version         |OS         |
----------------------|---------------------|-----------|
fvp-aemva             | RevC AEMvA 11.17.21 |           |
fvp-morello-android   | Morello 0.11.33     | Android   |
fvp-morello-baremetal | Morello 0.11.33     | Baremetal |
fvp-morello-busybox   | Morello 0.11.33     | Busybox   |
fvp-morello-oe        | Morello 0.11.33     | OE        |
fvp-morello-ubuntu    | Morello 0.11.33     | Ubuntu    |

## QEMU devices

Device        | Description         | Machine     | CPU              | Kernel
--------------|---------------------|-------------|------------------|--------
qemu-arm64    | 64-bit ARMv8        | virt        | Cortex-A57       | Image
qemu-arm64be  | 64-bit ARMv8 (BE)   | virt        | Cortex-A57       | Image
qemu-armv5    | 32-bit ARM          | versatilepb | arm926           | zImage
qemu-armv7    | 32-bit ARM          | virt        | Cortex-A15       | zImage
qemu-armv7be  | 32-bit ARM (BE)     | virt        | Cortex-A15       | zImage
qemu-i386     | 32-bit X86          | q35         | coreduo          | bzImage
qemu-mips32   | 32-bit MIPS         | malta       | mips32r6-generic | vmlinux
qemu-mips32el | 32-bit MIPS (EL)    | malta       | mips32r6-generic | vmlinux
qemu-mips64   | 64-bit MIPS         | malta       | 20Kc             | vmlinux
qemu-mips64el | 64-bit MIPS (EL)    | malta       | 20Kc             | vmlinux
qemu-ppc32    | 32-bit PowerPC      | ppce500     | e500mc           | uImage
qemu-ppc64    | 64-bit PowerPC      | pSeries     | Power8           | vmlinux
qemu-ppc64le  | 64-bit PowerPC (EL) | pSeries     | Power8           | vmlinux
qemu-riscv64  | 64-bit RISC-V       | virt        | rv64             | Image
qemu-s390     | 64-bit s390         | max,zpci=on | s390-ccw-virtio  | bzImage
qemu-sh4      | 32-bit SH           | r2d         | sh7785           | zImage
qemu-sparc64  | 64-bit Sparc        | sun4u       | UltraSPARC II    | vmlinux
qemu-x86_64   | 64-bit X86          | q35         | Nehalem          | bzImage
