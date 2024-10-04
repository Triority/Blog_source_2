---
title: Surface Pro使用rEFind引导Windows和Ubuntu双系统
tags:
  - linux
  - 教程
cover: /img/b3ebe4434dfdbe95d46db4c08a30255.jpg
categories:
  - 折腾记录
date: 2024-04-14 22:10:50
description: 优雅的双系统引导
---
# Start
最近换了新的平板，从surface pro 7 i5 8+128G换成了surface pro 7 plus i7 16+512G，可以说是解决了以前一切的使用痛点(也许有个LTE会更加完美?但是不太必要)，由于windows系统无与伦比的巨大功耗，准备再分出64G安装一个ubuntu用于应急情况

写这篇文章还有一个原因就是在我大一刚买电脑时候参考的C\*\*N上一篇很好的双系统安装教程文章现在改成收费了，让我十分不爽，也重新写一份给入门的同学们看，最后有关surface的特定内容忽略就好。关于双系统中Ubuntu系统的卸载可以参考[这篇之前的文章](https://triority.cc/2022/windows-ubuntu-uninstall/){% spoiler （这篇文章的结尾还有C\*\*N那篇文章的链接） %}

# 安装Ubuntu
提前准备了一个64G空白位置用于安装ubuntu22.04 LTS系统，启动盘制作好后，在按下音量+的时候按电源键开机，直到进入BIOS松开音量键，设置U盘启动，关闭安全启动(如果你有)，进入ubuntu安装程序。

{% note warning disabled %}
安全启动(Secureboot)仅允许受信任的系统在Surface上启动，安装非windows系统会无法直接启动
一旦关闭安全启动，如果你开启了bitlocker进入windows系统需要输入密钥，而且windows hello无法使用。
后面会写如何打开安全启动情况下使用linux
{% endnote %}

安装程序中一路continue在`install type`界面中选择`Something else`，然后`continue`，设置系统分区。

找到刚才留出的64G空间，也就是显示的`free space`，选择后点击加号新建分区。需要新建的分区如下：
+ `/swap`交换分区作为虚拟内存，逻辑分区，一般内存8G甚至更小的需要给8-16G左右，16G及以上看自己情况，我觉得我不需要所以没有设置
+ `/boot`分区放置Ubuntu的启动引导文件，逻辑分区，默认ext4，大小512M即可
+ `/` 根目录，逻辑分区，默认ext4，如果你不打算单独分出`/home`分区那么剩下的空间都给这里，否则给个几十G就足够了(如果你的总空间比较小给十几G也可以总之大概1/4吧)
+ `/home`用户目录，默认ext4，如果你单独设置了这个路径，那么剩下的空间都给这里就可以了

然后下面`Device for boot loader installation`选择刚才设置的`/boot`的设备，我这里是`/dev/nvme0n1p5`然后继续continue，直到系统安装完成

如果你只是想安装一个双系统而不想用rEFind，可以用ubuntu来引导Windows启动，但是这样每次进入都会默认选择第一项进入ubuntu。我们可以把它改成保存上次设置
```
sudo nano /etc/default/grub
```
```
# If you change this file, run 'update-grub' afterwards to update
# /boot/grub/grub.cfg.
# For full documentation of the options in this file, see:
#   info -f grub -n 'Simple configuration'
# 下面这个默认是0改成saved即可
GRUB_DEFAULT=saved
GRUB_TIMEOUT_STYLE=hidden
# 这个是等待时间，默认10s没啥必要改成3了
GRUB_TIMEOUT=3 
GRUB_DISTRIBUTOR=`lsb_release -i -s 2> /dev/null || echo Debian`
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash"
GRUB_CMDLINE_LINUX=""

# Uncomment to enable BadRAM filtering, modify to suit your needs
# This works with Linux (no patch required) and with any kernel that obtains
# the memory map information from GRUB (GNU Mach, kernel of FreeBSD ...)
#GRUB_BADRAM="0x01234567,0xfefefefe,0x89abcdef,0xefefefef"

# Uncomment to disable graphical terminal (grub-pc only)
#GRUB_TERMINAL=console

# The resolution used on graphical terminal
# note that you can use only modes which your graphic card supports via VBE
# you can see them in real GRUB with the command `vbeinfo'
#GRUB_GFXMODE=640x480

# Uncomment if you don't want GRUB to pass "root=UUID=xxx" parameter to Linux
#GRUB_DISABLE_LINUX_UUID=true

# Uncomment to disable generation of recovery mode menu entries
#GRUB_DISABLE_RECOVERY="true"

# Uncomment to get a beep at grub start
#GRUB_INIT_TUNE="480 440 1"
```
# 安装rEFind
rEFInd是一个非常好看好用的UEFI启动管理器，如果不用第三方引导，启动windows要么先启动ubuntu然后选择启动windows，要么BIOS设置windows优先然后每次启动ubuntu都要修改bios(然后再改回去十分离谱不建议)

rEFind在ubuntu或windows都可以安装，但是在windows下极其麻烦，强烈建议在ubuntu安装，下面也是这样做的。

进入ubuntu系统：
```
sudo apt-add-repository ppa:rodsmith/refind  	
sudo apt-get update  	
sudo apt-get install refind
```
安装过程中会有一些询问，不用看直接yes就好

完成到这一步，电脑默认会首选`rEFInd`引导，如果没有，去BIOS中设置一下引导顺序为`rEFind`优先

现在其实已经可以使用了，但是比较丑陋，所以接下来我们安装一个主题来美化

# (可选)美化：rEFind主题设置
## 配置文件信息
`rEFind`的配置信息位于`/boot/efi/EFI/refind/refind.conf`

```conf
# refind.conf
# Configuration file for the rEFInd boot menu
#
 
# Timeout in seconds for the main menu screen. Setting the timeout to 0
# disables automatic booting (i.e., no timeout). Setting it to -1 causes
# an immediate boot to the default OS *UNLESS* a keypress is in the buffer
# when rEFInd launches, in which case that keypress is interpreted as a
# shortcut key. If no matching shortcut is found, rEFInd displays its
# menu with no timeout.
#
#设置默认等待时间为5s
#timeout 0代表无限等待 timeout -1代表立即进入对应的系统
timeout 5


# Set the screen's video resolution. Pass this option either:
#  * two values, corresponding to the X and Y resolutions
#  * one value, corresponding to a GOP (UEFI) video mode
# Note that not all resolutions are supported. On UEFI systems, passing
# an incorrect value results in a message being shown on the screen to
# that effect, along with a list of supported modes. On EFI 1.x systems
# (e.g., Macintoshes), setting an incorrect mode silently fails. On both
# types of systems, setting an incorrect resolution results in the default
# resolution being used. A resolution of 1024x768 usually works, but higher
# values often don't.
# Default is "0 0" (use the system default resolution, usually 800x600).
#
#分辨率设置，我建议这里别动，上面注释中也说了。1024*768以上的分辨率并不支持，我是默认的，没动它，所以没事别自己搞个1920 1080（更新：可用）
#resolution 1024 768
#resolution 1440 900
#resolution 3


# Directories that should NOT be scanned for boot loaders. By default,
# rEFInd doesn't scan its own directory, the EFI/tools directory, the
# EFI/memtest directory, the EFI/memtest86 directory, or the
# com.apple.recovery.boot directory. Using the dont_scan_dirs option
# enables you to "blacklist" other directories; but be sure to use "+"
# as the first element if you want to continue blacklisting existing
# directories. You might use this token to keep EFI/boot/bootx64.efi out
# of the menu if that's a duplicate of another boot loader or to exclude
# a directory that holds drivers or non-bootloader utilities provided by
# a hardware manufacturer. If a directory is listed both here and in
# also_scan_dirs, dont_scan_dirs takes precedence. Note that this
# blacklist applies to ALL the filesystems that rEFInd scans, not just
# the ESP, unless you precede the directory name by a filesystem name or
# partition unique GUID, as in "myvol:EFI/somedir" to exclude EFI/somedir
# from the scan on the myvol volume but not on other volumes.
#
#这部分看注释的意思，应该是不扫描ESP分区的某些文件夹，我自己为了去除某些多余
#的启动项，于是设置了dont_scan_dirs ESP:/EFI/ubuntu，但不知道为什么，没有用，启动项里仍会出现Ubuntu的引导项，所以我不建议在这部分选择屏蔽引导项.
#dont_scan_dirs ESP:/EFI/boot,EFI/Dell,EFI/memtest86


# Files that should NOT be included as EFI boot loaders (on the
# first line of the display). If you're using a boot loader that
# relies on support programs or drivers that are installed alongside
# the main binary or if you want to "blacklist" certain loaders by
# name rather than location, use this option. Note that this will
# NOT prevent certain binaries from showing up in the second-row
# set of tools. Most notably, various Secure Boot and recovery
# tools are present in this list, but may appear as second-row
# items.
# The file may be specified as a bare name (e.g., "notme.efi"), as
# a complete pathname (e.g., "/EFI/somedir/notme.efi"), or as a
# complete pathname with volume (e.g., "SOMEDISK:/EFI/somedir/notme.efi"
# or 2C17D5ED-850D-4F76-BA31-47A561740082:/EFI/somedir/notme.efi").
# OS tags hidden via the Delete or '-' key in the rEFInd menu are
# added to this list, but stored in NVRAM.
# The default is shim.efi,shim-fedora.efi,shimx64.efi,PreLoader.efi,
# TextMode.efi,ebounce.efi,GraphicsConsole.efi,MokManager.efi,HashTool.efi,
# HashTool-signed.efi,bootmgr.efi,fb{arch}.efi
# (where "{arch}" is the architecture code, like "x64").
#
#这部分和上面那部分类似，都是屏蔽之用，区别在于上面部分是针对文件夹，这部分是针
#对具体文件，这部分在去除某些启动项有着极为关键的作用，我将详细展开叙述。
#dont_scan_files shim.efi,MokManager.efi
```

## 删除多余启动项
`refind`他针对某些`.efi`的文件会选择无脑的引导，因此我们为了简洁或者美观，需要屏蔽某些文件的引导，屏蔽不会修改原EFI分区中的系统引导文件。针对我的`ubuntu`，引导文件位于`ubuntu/grubx64.efi`（EFI分区的相对路径），以及我的`windows`引导文件，位于`Microsoft/Boot/bootmgfw.efi`，而我们需要保留的就这两个，其他的一律屏蔽。下面命令代表屏蔽了`ubuntu`文件夹下的`shim.efi`引导文件和其他文件XXX

```
dont_scan_files /EFI/ubuntu/shim.efi,XXX,XXX
```

## 主题配置
在`refind.conf`文件最后需要加一行指令来加载主题文件(（相对路径是指你的主题配置文件`theme.config`在以`refind`目录为根目录的文件路径）)
```
include <相对路径>/theme.config 
```
比如我的theme文件位于`refind`目录下的`themes/rEFInd-minimal`处
```
include themes/rEFInd-minimal/theme.conf
```
`refind`文件夹位于EFI分区目录，`theme`文件夹位于`refind`文件夹，主题文件位于`theme`文件夹

关于`theme.conf`文件，这是[官方介绍文档](https://github.com/topics/refind-theme)

```conf
# Minimal refind theme

# Hide user interface elements for personal preference or to increase
# security:
#  banner      - the rEFInd title banner (built-in or loaded via "banner")
#  label       - boot option text label in the menu
#  singleuser  - remove the submenu options to boot Mac OS X in single-user
#                or verbose modes; affects ONLY MacOS X
#  safemode    - remove the submenu option to boot Mac OS X in "safe mode"
#  hwtest      - the submenu option to run Apple's hardware test
#  arrows      - scroll arrows on the OS selection tag line
#  hints       - brief command summary in the menu
#  editor      - the options editor (+, F2, or Insert on boot options menu)
#  all         - all of the above
# Default is none of these (all elements active)
#
hideui singleuser,hints,arrows,label,badges


# Set the name of a subdirectory in which icons are stored. Icons must
# have the same names they have in the standard directory. The directory
# name is specified relative to the main rEFInd binary's directory. If
# an icon can't be found in the specified directory, an attempt is made
# to load it from the default directory; thus, you can replace just some
# icons in your own directory and rely on the default for others.
# Default is "icons".
#各种系统的启动图标
icons_dir themes/rEFInd-minimal/icons


# Use a custom title banner instead of the rEFInd icon and name. The file
# path is relative to the directory where refind.efi is located. The color
# in the top left corner of the image is used as the background color
# for the menu screens. Currently uncompressed BMP images with color
# depths of 24, 8, 4 or 1 bits are supported, as well as PNG images.
#这是启动界面背景图片路径，也是相对路径，且暂时似乎只支持png格式的图片
banner themes/rEFInd-minimal/background.png


# Tells rEFInd whether to display banner images pixel-for-pixel (noscale)
# or to scale banner images to fill the screen (fillscreen). The former is
# the default.
#默认全屏填充
banner_scale fillscreen


# Custom images for the selection background. There is a big one (144 x 144)
# for the OS icons, and a small one (64 x 64) for the function icons in the
# second row. If only a small image is given, that one is also used for
# the big icons by stretching it in the middle. If only a big one is given,
# the built-in default will be used for the small icons.
#
# Like the banner option above, these options take a filename of an
# uncompressed BMP image file with a color depth of 24, 8, 4, or 1 bits,
# or a PNG image. The PNG format is required if you need transparency
# support (to let you "see through" to a full-screen banner).
#
selection_big   themes/rEFInd-minimal/selection_big.png
selection_small themes/rEFInd-minimal/selection_small.png

# Which non-bootloader tools to show on the tools line, and in what
# order to display them:
#  shell           - the EFI shell (requires external program; see rEFInd
#                    documentation for details)
#  gptsync         - the (dangerous) gptsync.efi utility (requires external
#                    program; see rEFInd documentation for details)
#  apple_recovery  - boots the Apple Recovery HD partition, if present
#  mok_tool        - makes available the Machine Owner Key (MOK) maintenance
#                    tool, MokManager.efi, used on Secure Boot systems
#  about           - an "about this program" option
#  exit            - a tag to exit from rEFInd
#  shutdown        - shuts down the computer (a bug causes this to reboot
#                    EFI systems)
#  reboot          - a tag to reboot the computer
#  firmware        - a tag to reboot the computer into the firmware's
#                    user interface (ignored on older computers)
# Default is shell,apple_recovery,mok_tool,about,shutdown,reboot,firmware
#
showtools shutdown
```
# (可选)安装Ubuntu下的surface硬件驱动

{% note info modern %}
感谢[linux-surface项目的贡献](https://github.com/linux-surface/linux-surface)
{% endnote %}

导入用于签名软件包的密钥
```
wget -qO - https://raw.githubusercontent.com/linux-surface/linux-surface/master/pkg/keys/surface.asc \
    | gpg --dearmor | sudo dd of=/etc/apt/trusted.gpg.d/linux-surface.gpg
```
如果你的网络不是特别好可能会报错，你可以把这个命令的下载和导入分开执行，下载链接可以直接使用文件替换
```
wget https://raw.githubusercontent.com/linux-surface/linux-surface/master/pkg/keys/surface.asc
cat surface.asc | gpg --dearmor | sudo dd of=/etc/apt/trusted.gpg.d/linux-surface.gpg
```
然后添加存储库配置并更新APT
```
echo "deb [arch=amd64] https://pkg.surfacelinux.com/debian release main" \
	| sudo tee /etc/apt/sources.list.d/linux-surface.list

sudo apt update
```
安装linux-surface内核及其依赖项，还可以启用iptsd服务以使用触摸屏
```
sudo apt install linux-image-surface linux-headers-surface iptsd libwacom-surface
sudo systemctl enable iptsd
```
如果在启用服务时候报错没有找到服务配置文件可能需要自己创建然后写入
```
sudo nano /lib/systemd/system/iptsd.service
```
```
[Unit]
Description=Intel Precise Touch & Stylus Daemon
Documentation=https://github.com/linux-surface/iptsd

[Service]
Type=simple
ExecStart=/usr/local/bin/iptsd

[Install]
WantedBy=default.target
```
重启电脑，surface硬件基本都可以使用了

# (对于下面的可选项十分重要重要重要)风险提示和过程解释
{% note danger modern %}
接下来的操作涉及系统引导等底层的重要内容，如果你没有基本的计算机知识建议到这里点到为止。要进行下面的操作务必了解你在做什么以及如何修复或回滚你的操作，最严重的后果可能会让你的电脑变成砖头。请先看下图，这是写这篇文章时候我遇到的错误
![](/img/b3ebe4434dfdbe95d46db4c08a30255.jpg)
{% endnote %}


下面简要介绍一下我们在做什么以及为什么要这样做


# (可选)surface开启安全启动：签名ubuntu的内核
由于我们在安装surface驱动的时候更改了系统内核，会导致`secure boot`在开启状态下无法直接引导系统，所以我们需要将内核进行签名，将Linux-Surface内核的密钥导入到引导加载程序中，以便内核可以引导而不禁用`secure boot`

安装签名工具
```
sudo apt install linux-surface-secureboot-mok
```
有的版本的mok会直接给你一个密码来给你，后面导入的流程里就不会再需要输入密码了。安装时候终端输出都会告诉你，类似这样
```bash
triority@triority-Surface-Pro-7-PLUS:~$ sudo apt install linux-surface-secureboot-mok
[sudo] password for triority: 
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
The following NEW packages will be installed:
  linux-surface-secureboot-mok
0 upgraded, 1 newly installed, 0 to remove and 94 not upgraded.
Need to get 5,616 B of archives.
After this operation, 18.4 kB of additional disk space will be used.
Get:1 https://pkg.surfacelinux.com/debian release/main amd64 linux-surface-secureboot-mok amd64 20231003-1 [5,616 B]
Fetched 5,616 B in 8s (678 B/s)                          
Selecting previously unselected package linux-surface-secureboot-mok.
(Reading database ... 195210 files and directories currently installed.)
Preparing to unpack .../linux-surface-secureboot-mok_20231003-1_amd64.deb ...
Unpacking linux-surface-secureboot-mok (20231003-1) ...
Setting up linux-surface-secureboot-mok (20231003-1) ...

The secure-boot certificate has been installed to

    /usr/share/linux-surface-secureboot/surface.cer

It will now be automatically enrolled for you and guarded with the password

    surface

To finish the enrollment process you need to reboot, where you will then be
asked to enroll the certificate. During the import, you will be prompted for
the password mentioned above. Please make sure that you are indeed adding
the right key and confirm by entering 'surface'.

Note that you can always manage your secure-boot keys, including the one
just enrolled, from inside Linux via the 'mokutil' tool.
```

然后下载[linux-surface签名公钥](https://raw.githubusercontent.com/linux-surface/linux-surface/master/pkg/keys/surface.cer)

导入公钥
```
sudo mokutil --import surface.cer
```
此过程会要求你输入一个一次性密码，一定要记住一会要用，但是只会用这一次

重启后会进入一个比较原始的蓝色界面，回车后选择`import mok`，然后continue直到要求你输入刚才设置的密码，然后完成即可

完成后即可进入UEFI，在`secure boot`中将`boot configuration`改为`Microsoft & 3rd party CA`就可以使用安全启动了

# (可选)surface开启安全启动：签名rEFind
其实最开始跟上面差不多，看看目录内容(我闲的,没必要)然后导入密钥
```bash
triority@triority-Surface-Pro-7-PLUS:~$ sudo ls /boot/efi/EFI
Boot  Microsoft  refind  tools ubuntu
triority@triority-Surface-Pro-7-PLUS:~$ sudo ls /boot/efi/EFI/ubuntu
BOOTX64.CSV  grub.cfg  grubx64.efi  mmx64.efi  shimx64.efi
triority@triority-Surface-Pro-7-PLUS:~$ sudo ls /boot/efi/EFI/refind/keys
altlinux.cer          openSUSE-UEFI-CA-Certificate.cer
canonical-uefi-ca.cer         redhatsecureboot003.cer
centossecureboot201.cer         redhatsecureboot401.cer
centossecurebootca2.cer         redhatsecurebootca2.cer
debian.cer          redhatsecurebootca4.cer
fedora-ca.cer          refind.cer
microsoft-kekca-public.cer        refind_local.cer
microsoft-pca-public.cer        refind_local.crt
microsoft-uefica-public.cer        SLES-UEFI-CA-Certificate.cer
openSUSE-UEFI-CA-Certificate-4096.cer
triority@triority-Surface-Pro-7-PLUS:~$ sudo ls /boot/efi/EFI/refind
BOOT.CSV  drivers_x64  icons  keys  refind.conf  refind_x64.efi  vars
triority@triority-Surface-Pro-7-PLUS:~$ sudo cp -i /boot/efi/EFI/ubuntu/shimx64.efi /boot/efi/EFI/refind
triority@triority-Surface-Pro-7-PLUS:~$ sudo cp -i /boot/efi/EFI/ubuntu/mmx64.efi /boot/efi/EFI/refind
triority@triority-Surface-Pro-7-PLUS:~$ sudo mokutil -i /boot/efi/EFI/refind/keys/refind.cer
input password: 
input password again: 
triority@triority-Surface-Pro-7-PLUS:~$
```
