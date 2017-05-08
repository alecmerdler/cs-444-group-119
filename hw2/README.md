# Assignment #2

## Concurrency #2

Dining Philosophers problem implemented in Python 2.7.

### Implementation Details

- Avoids deadlock by blocking until left fork is acquired
- After left fork acquired, attempt non-blocking to acquire right fork. If not available, immediately drop left fork and go back to thinking

### Instructions

1. Run the simulation: `python2 philosophers.py`
3. Exit using `Ctrl+C`
2. Run the tests: `python2 test_dining_philosophers.py`
4. Exit using `Ctrl+C`

## SSTF Scheduler

### Instructions

1. Clone two clean kernel sources: `git clone git://git.yoctoproject.org/linux-yocto-3.14 linux-yocto-3.14-clean && git clone git://git.yoctoproject.org/linux-yocto-3.14 linux-yocto-3.14-working`

2. Add modified files: `cp Kconfig.iosched Makefile sstf-iosched.c linux-yocto-3.14-working/block`

3. Create patch: `diff -rupN linux-yocto-3.14-clean/block linux-yocto-3.14-working > assn2.patch`

4. Apply patch: `cp assn2.patch linux-yocto-3.14-clean/block && cd linux-yocto-3.14-clean/block && patch < assn2.patch`

5. Build kernel as normal: `make -j4 all`

6. (Terminal 1) Start VM: `qemu-system-i386 -gdb tcp::5619 -S -nographic -kernel linux-yocto-3.14-clean/arch/x86/boot/bzImage -drive file=core-image-lsb-sdk-qemux86.ext3 -enable-kvm -net none -usb -localtime --no-reboot --append "root=/dev/hda rw console=ttyS0 debug"`

7. (Terminal 2) Run `gdb`

8. (Terminal 2) Run `target remote:5619`, then `continue`

9. (Terminal 1) Prompt should ask you to login. Type `root` and hit enter

10. (Terminal 1) Switch to SSTF scheduler: `echo 'sstf' > /sys/block/hdc/queue/scheduler`

11. (Terminal 1) Confirm scheduler: `cat /sys/block/hdc/queue/scheduler`

12. (Terminal 1) TODO run test script and check log files for output confirming scheduler change
