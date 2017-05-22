obj-m := sbd.o
KDIR := ../linux-yocto-3.14-working
PWD := $(shell pwd)
default:
	$(MAKE) -C $(KDIR) SUBDIRS=$(PWD) modules

