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

1. Clone clean kernel source: `git clone git://git.yoctoproject.org/linux-yocto-3.14 linux-yocto-3.14-clean`

2. Apply patch: `cp assn2.patch linux-yocto-3.14-clean/block && cd linux-yocto-3.14-clean/block && patch < assn2.patch`
3. Build kernel as normal
4. Connect to kernel using `gdb`
5. Switch to SSTF scheduler: `echo 'sstf' > /sys/block/hdc/queue/scheduler`
6. Confirm scheduler: `cat /sys/block/hdc/queue/scheduler`
