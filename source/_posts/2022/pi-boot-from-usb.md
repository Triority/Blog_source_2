---
title: 树莓派从usb设备启动
date: 2022-08-02 10:49:26
tags:
- 笔记
- 树莓派
- linux
description: 树莓派目前最大的性能瓶颈莫过于sd卡读取速度，pi4支持usb3.0后就可以用外置usb启动来提高性能[于是瓶颈就成了cpu......]
cover: /img/raspberry_overclocking.png
categories: 
- 旅游&摄影
---
## 修改 Ubuntu 以进行 USB 引导
### 查找和装载存储设备
首先，使用`lsblk`命令找到您的存储设备，这将显示连接到系统的所有存储设备：
```
pi@triority:~ $ lsblk
NAME        MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
sda           8:0    0 149.1G  0 disk
├─sda1        8:1    0   256M  0 part
└─sda2        8:2    0     3G  0 part
mmcblk0     179:0    0  28.8G  0 disk
├─mmcblk0p1 179:1    0   256M  0 part /boot
└─mmcblk0p2 179:2    0  28.6G  0 part /
```
SD卡将始终以mmcblk开头，因此可以排除该卡。这使得usb设备成为系统上唯一的其他磁盘设备。
在`MOUNTPOINT`列下的输出中，可以看到它是空白的。这意味着驱动器未安装在系统上。
现在，创建两个挂载点并挂载 Ubuntu 驱动器。使用这些命令替换自己的驱动器，它不一定是 `/dev/sda`：
```
sudo mkdir /mnt/boot
sudo mkdir /mnt/writable
sudo mount /dev/sda1 /mnt/boot
sudo mount /dev/sda2 /mnt/writable
```
正确挂载所有内容后，`lsblk`命令的输出应如下所示，现在填充了挂载点字段：
```
pi@triority:~ $ lsblk
NAME        MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
sda           8:0    0 149.1G  0 disk
├─sda1        8:1    0   256M  0 part /mnt/boot
└─sda2        8:2    0     3G  0 part /mnt/writable
mmcblk0     179:0    0  28.8G  0 disk
├─mmcblk0p1 179:1    0   256M  0 part /boot
└─mmcblk0p2 179:2    0  28.6G  0 part /
```
### 使用脚本修改已挂载的分区
如果你只是想让你的Ubuntu分区可启动，一个自动化脚本可以做到这一点。只要您已将分区挂载为 `/mnt/boot` 和` /mnt/writeable`，脚本就会对 Ubuntu 20.04 / 20.10 进行必要的更改！该脚本的[源代码](https://github.com/TheRemote/Ubuntu-Server-raspi4-unofficial/blob/master/BootFix.sh "源代码")
由于脚本在github访问困难，可以直接复制下面
```
#!/bin/bash
# Script that fixes an Ubuntu 20.04 / 20.10 partition created by the official Raspberry Pi Imager to boot with a Raspberry Pi 4
# by James A. Chambers - https://jamesachambers.com/raspberry-pi-4-ubuntu-20-04-usb-mass-storage-boot-guide

# First image your drive with Ubuntu 20.04 or 20.10 using the official Pi Imager tool
# Next connect your drive to the Raspberry Pi
# Find drive using lsblk (normally it's /dev/sda but check first) -- unmount if it was automatically mounted with sudo umount mountpoint (ex: sudo umount /media/pi/system-boot)
# Mount boot partition with sudo mount /dev/sda1 /mnt/boot
# Mount writable partition with sudo mount /dev/sda2 /mnt/writable
# Now you are ready to run this script to update the partition for Raspberry Pi booting

# Safety check, check for /boot directory and /usr/bin/raspinfo - NO LONGER USED - See Issue #140
# if ! command -v git >/dev/null ; then
#    echo "Safety check:  git was not found.  Please install using sudo apt install git.  Exiting..."
#    exit 1
# fi

# Safety check, run as sudo
if [ $(id -u) != 0 ]; then
   echo "Safety check:  This script is meant to be ran as root or sudo.  Please run using sudo ./BootFix.sh.  Exiting..."
   exit 1
fi

# Safety check -- check for system-boot automount
if [ -d /media/*/system-boot ]; then
   echo "Safety check:  automount detected at /media/*/system-boot.  Please unmount the automount in File Explorer or with sudo umount /media/$LOGNAME/system-boot."
   exit 1
fi

# Safety check -- check for writable automount
if [ -d /media/*/writable ]; then
   echo "Safety check:  automount detected at /media/*/writable.  Please unmount the automount in File Explorer or with sudo umount /media/$LOGNAME/system-boot."
   exit 1
fi

# Find the "writable" root filesystem mount
if [ -d /mnt/writable ] && [ -d /mnt/writable/usr/lib/u-boot ] ; then
    mntWritable='/mnt/writable'
else
    echo "The partition 'writable' was not found in /mnt/writable.  Make sure you have mounted your USB mass storage device (ex: sudo mount /dev/sda2 /mnt/writable)."
    exit 1
fi
echo "Found writable partition at $mntWritable"

# Find the "system-boot" boot filesystem mount
if [ -d /mnt/boot ] && [ -e /mnt/boot/vmlinuz ]; then
    mntBoot='/mnt/boot'
else
    echo "The 'boot' partition was not found in /mnt/boot.  Make sure you have mounted your USB mass storage device (ex: sudo mount /dev/sda1 /mnt/boot)."
    exit 1
fi
echo "Found boot partition at $mntBoot"

# Commented out -- not necessary after 20.04.2 and causes issues
# Clone firmware repository
#if [ ! -d rpi-firmware ]; then
#   git clone https://github.com/Hexxeh/rpi-firmware.git --depth 1
#else
#   cd rpi-firmware
#   git pull
#   cd ..
#fi

# Update firmware
#echo "Updating firmware..."
#if [ -d rpi-firmware ]; then
#   sudo cp rpi-firmware/*.dat "$mntBoot"
#   sudo cp rpi-firmware/*.elf "$mntBoot"
#   sudo cp rpi-firmware/*.bin "$mntBoot"
#   # Update DTBs if not Ubuntu Server 20.04
#   if cat "$mntWritable/etc/os-release" | grep -q "Ubuntu 20.04.1"; then
#      if [ ! -d "$mntWritable/lib/X11" ]; then
#         if cat "$mntBoot/config.txt" | grep -q "arm_64bit=1"; then
#            # Ubuntu server 20.04.1 64 bit- skip copying DTBs
#            echo "Skipping copying DTBs for Ubuntu Server 20.04.1 64 bit"
#         else
#            sudo cp rpi-firmware/*.dtb "$mntBoot"
#         fi
#      else
#         sudo cp rpi-firmware/*.dtb "$mntBoot"
#      fi
#   else
#      sudo cp rpi-firmware/*.dtb "$mntBoot"
#   fi
#   rm -rf rpi-firmware
#else
#    echo "Failed to clone rpi-firmware repository with git.  Are you connected to the internet?  Exiting..."
#    rm -rf rpi-firmware
#    exit 1
#fi

# Decompress the kernel
echo "Decompressing kernel from vmlinuz to vmlinux..."
zcat -qf "$mntBoot/vmlinuz" > "$mntBoot/vmlinux"
echo "Kernel decompressed"

# Check if 32 bit or 64 bit and modify config.txt
if cat "$mntBoot/config.txt" | grep -q "arm_64bit=1"; then

# Update config.txt with correct parameters
echo "Updating config.txt with correct parameters..."

cat <<EOF | sudo tee "$mntBoot/config.txt">/dev/null
# Please DO NOT modify this file; if you need to modify the boot config, the
# usercfg.txt file is the place to include user changes. Please refer to
# the README file for a description of the various configuration files on
# the boot partition.

# The unusual ordering below is deliberate; older firmwares (in particular the
# version initially shipped with bionic) don't understand the conditional
# [sections] below and simply ignore them. The Pi4 doesn't boot at all with
# firmwares this old so it's safe to place at the top. Of the Pi2 and Pi3, the
# Pi3 uboot happens to work happily on the Pi2, so it needs to go at the bottom
# to support old firmwares.

[pi4]
max_framebuffers=2
dtoverlay=vc4-fkms-v3d
boot_delay
kernel=vmlinux
initramfs initrd.img followkernel

[pi2]
boot_delay
kernel=vmlinux
initramfs initrd.img followkernel

[pi3]
boot_delay
kernel=vmlinux
initramfs initrd.img followkernel

[all]
arm_64bit=1
device_tree_address=0x03000000

# The following settings are defaults expected to be overridden by the
# included configuration. The only reason they are included is, again, to
# support old firmwares which don't understand the include command.

enable_uart=1
cmdline=cmdline.txt

include syscfg.txt
include usercfg.txt

EOF

# End 64 bit
else

# Update config.txt with correct parameters
echo "Updating config.txt with correct parameters..."

cat <<EOF | sudo tee "$mntBoot/config.txt">/dev/null
# Please DO NOT modify this file; if you need to modify the boot config, the
# usercfg.txt file is the place to include user changes. Please refer to
# the README file for a description of the various configuration files on
# the boot partition.

# The unusual ordering below is deliberate; older firmwares (in particular the
# version initially shipped with bionic) don't understand the conditional
# [sections] below and simply ignore them. The Pi4 doesn't boot at all with
# firmwares this old so it's safe to place at the top. Of the Pi2 and Pi3, the
# Pi3 uboot happens to work happily on the Pi2, so it needs to go at the bottom
# to support old firmwares.

[pi4]
max_framebuffers=2
dtoverlay=vc4-fkms-v3d
boot_delay
kernel=vmlinux
initramfs initrd.img followkernel

[pi2]
boot_delay
kernel=vmlinux
initramfs initrd.img followkernel

[pi3]
boot_delay
kernel=vmlinux
initramfs initrd.img followkernel

[all]
device_tree_address=0x03000000

# The following settings are defaults expected to be overridden by the
# included configuration. The only reason they are included is, again, to
# support old firmwares which don't understand the include command.

enable_uart=1
cmdline=cmdline.txt

include syscfg.txt
include usercfg.txt

EOF

# End 32 bit
fi


# Create script to automatically decompress kernel (source: https://www.raspberrypi.org/forums/viewtopic.php?t=278791)
echo "Creating script to automatically decompress kernel..."
cat << \EOF | sudo tee "$mntBoot/auto_decompress_kernel">/dev/null
#!/bin/bash -e
# auto_decompress_kernel script
BTPATH=/boot/firmware
CKPATH=$BTPATH/vmlinuz
DKPATH=$BTPATH/vmlinux
# Check if compression needs to be done.
if [ -e $BTPATH/check.md5 ]; then
   if md5sum --status --ignore-missing -c $BTPATH/check.md5; then
      echo -e "\e[32mFiles have not changed, Decompression not needed\e[0m"
      exit 0
   else
      echo -e "\e[31mHash failed, kernel will be compressed\e[0m"
   fi
fi
# Backup the old decompressed kernel
mv $DKPATH $DKPATH.bak
if [ ! $? == 0 ]; then
   echo -e "\e[31mDECOMPRESSED KERNEL BACKUP FAILED!\e[0m"
   exit 1
else
   echo -e "\e[32mDecompressed kernel backup was successful\e[0m"
fi
# Decompress the new kernel
echo "Decompressing kernel: "$CKPATH".............."
zcat -qf $CKPATH > $DKPATH
if [ ! $? == 0 ]; then
   echo -e "\e[31mKERNEL FAILED TO DECOMPRESS!\e[0m"
   exit 1
else
   echo -e "\e[32mKernel Decompressed Succesfully\e[0m"
fi
# Hash the new kernel for checking
md5sum $CKPATH $DKPATH > $BTPATH/check.md5
if [ ! $? == 0 ]; then
   echo -e "\e[31mMD5 GENERATION FAILED!\e[0m"
else
   echo -e "\e[32mMD5 generated Succesfully\e[0m"
fi
exit 0
EOF
sudo chmod +x "$mntBoot/auto_decompress_kernel"

# Create apt script to automatically decompress the kernel
echo "Creating apt script to automatically decompress kernel..."
echo 'DPkg::Post-Invoke {"/bin/bash /boot/firmware/auto_decompress_kernel"; };' | sudo tee "$mntWritable/etc/apt/apt.conf.d/999_decompress_rpi_kernel" >/dev/null
sudo chmod +x "$mntWritable/etc/apt/apt.conf.d/999_decompress_rpi_kernel"

# Successful
echo "Updating Ubuntu partition was successful!  Shut down your Pi, remove the SD card then reconnect the power."
```
然后新建一个脚本文件：
```
nano BootFix.sh
```
粘贴后`ctrl+o`保存，`ctrl+x`退出
然后执行：
```
chmod +x BootFix.sh
sudo ./BootFix.sh
```
只要您正确挂载了分区，它就会修改分区并告诉您它已成功：
```
pi@triority:~ $ sudo ./BootFix.sh
Found writable partition at /mnt/writable
Found boot partition at /mnt/boot
Decompressing kernel from vmlinuz to vmlinux...
Kernel decompressed
Updating config.txt with correct parameters...
Creating script to automatically decompress kernel...
Creating apt script to automatically decompress kernel...
Updating Ubuntu partition was successful!  Shut down your Pi, remove the SD card then reconnect the power.
```
使用以下命令卸载分区：
```
sudo umount /mnt/boot
sudo umount /mnt/writable
```
现在可以关闭并从中取出SD卡，只插入USB设备。重新连接电源启动！