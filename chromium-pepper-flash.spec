# Thanks to malcolmlewis for help with this script
# Thanks to Tom "spot" Callaway for much of the patchwork
# Thanks to jhaygood for most of the icu patch
%define	debug_package %nil

Name:           chromium-pepper-flash
Url:            http://www.google.com/chrome
Summary:        Chromium Flash player plugin
Version:        18.0.0.194
Release:        1
License:        Free
Group:          Networking/WWW
Source0:        https://dl.google.com/linux/direct/google-chrome-stable_current_i386.rpm
Source1:        https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
Source3:	default.config
# Use x86/x86_64 pre-built libs
ExclusiveArch:  %{ix86} x86_64
Requires:       chromium-browser
BuildRequires:	python

%description
Pepper API based Adobe Flash plugin for Google's Open Source browser Chromium.

%prep
%setup -c -T
cp %{SOURCE3} default
sed -i 's/FLASH_VERSION=/FLASH_VERSION=%{version}/g' default

%build
%ifarch i586
rpm2cpio %{SOURCE0} | cpio -idmv
%endif
%ifarch x86_64
rpm2cpio %{SOURCE1} | cpio -idmv
%endif

# check version matches
RPM_VER=`cat opt/google/chrome/PepperFlash/manifest.json | python -c 'import sys,json; print json.load(sys.stdin)["version"]'`

if [ "$RPM_VER" != "%{version}" ]; then
  echo "VERSION MISMATCH, Rpm version $RPM_VER this package %{version}"
  exit 1
fi


%install
mkdir -p %{buildroot}%{_libdir}/chromium/PepperFlash/
install -m644 opt/google/chrome/PepperFlash/* %{buildroot}%{_libdir}/chromium/PepperFlash/ 
mkdir -p %{buildroot}%{_sysconfdir}/chromium/
install -m644 default %{buildroot}%{_sysconfdir}/chromium/default

%files
%dir %{_libdir}/chromium/
%{_sysconfdir}/chromium/default
%{_libdir}/chromium/PepperFlash/
