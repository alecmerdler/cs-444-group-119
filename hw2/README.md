# Assignment #2

## Concurrency #2


## SSTF Scheduler

### Instructions

1. Clone clean kernel source: `git clone git://git.yoctoproject.org/linux-yocto-3.14 linux-yocto-3.14-clean`

2. Apply patch: `cp assn2.patch linux-yocto-3.14-clean/block && cd linux-yocto-3.14-clean/block && patch < assn2.patch`
3. Build kernel as normal
4. Connect to kernel using `gdb`
5. Switch to SSTF scheduler: `echo 'sstf' > /sys/block/hdc/queue/scheduler`
6. Confirm scheduler: `cat /sys/block/hdc/queue/scheduler`