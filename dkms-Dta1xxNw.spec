%define modname Dta1xxNw
%define version 1.2.0.7
%define release %mkrel 1
%define modversion %{version}-%{release}

Name:     dkms-%{modname}
Version:  %{version}
Release:  %{release}
Summary:  Kernel network driver for Dektec Dta1xx
# Actually it's a very permissive license, but it tells the kernel it is GPL
# so let's distribute it as GPLv2
License:  GPLv2
# Extracted from http://www.dektec.com/Products/SDK/LinuxSDK/Downloads/LinuxSDK.zip
# which contains several drivers and some non free libraries
Source0:  %{modname}.tar.gz
Patch0:   Dta1xx-netdev_ops.patch
Url:      http://www.dektec.com/downloads/Drivers.asp
Group:    Development/Kernel
Requires(post):  dkms
Requires(preun): dkms
Buildroot:  %{_tmppath}/%{modname}-%{version}-%{release}-buildroot
BuildArch:  noarch

%description
The Dta1xxNw driver is a network driver for DekTec's DTA-1XX series 
of PCI cards.
Currently the driver provides support for the following cards:
 - DTA-160   (GigE TS-over-IP + 3 ASI Ports for PCI Bus)
 - DTA-2160  (GigE TS-over-IP + 3 ASI Ports for PCI Express Bus)

%prep
%setup -q -n %{modname}
%patch0 -p0

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_usrsrc}/%{modname}-%{modversion}
cp -a * %{buildroot}%{_usrsrc}/%{modname}-%{modversion}/
cat > %{buildroot}%{_usrsrc}/%{modname}-%{modversion}/dkms.conf <<EOF

PACKAGE_VERSION="%{modversion}"

# Items below here should not have to change with each driver version
PACKAGE_NAME="%{modname}"
CLEAN="make clean"
BUILT_MODULE_NAME[0]="%{modname}"
DEST_MODULE_LOCATION[0]="/kernel/drivers/misc/dektec"
REMAKE_INITRD="no"
AUTOINSTALL="yes"
EOF

%post
dkms add -m %{modname} -v %{modversion} --rpm_safe_upgrade \
&& dkms build -m %{modname} -v %{modversion} --rpm_safe_upgrade \
&& dkms install -m %{modname} -v %{modversion} --rpm_safe_upgrade --force

cat > /etc/udev/rules.d/10-%{modname}.rules << DEK
BUS=="usb", SYSFS{manufacturer}=="DEKTEC", NAME="usb/DekTec/\%k", MODE="0666"
DEK

%preun
dkms remove -m %{modname} -v %{modversion} --rpm_safe_upgrade --all

%clean
rm -rf %buildroot

%files
%defattr(-,root,root)
%doc Readme
/usr/src/%{modname}-%{modversion}

