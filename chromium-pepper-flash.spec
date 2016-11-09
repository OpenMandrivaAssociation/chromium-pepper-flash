# Thanks to malcolmlewis for help with this script
# Thanks to Tom "spot" Callaway for much of the patchwork
# Thanks to jhaygood for most of the icu patch
%define	debug_package %nil

Name:           chromium-pepper-flash
Url:            http://www.google.com/chrome
Summary:        Chromium Flash player plugin
Version:        23.0.0.207
Release:        1
License:        Free
Group:          Networking/WWW
Source0:        https://fpdownload.adobe.com/pub/flashplayer/pdc/%{version}/flash_player_ppapi_linux.i386.tar.gz
Source1:        https://fpdownload.adobe.com/pub/flashplayer/pdc/%{version}/flash_player_ppapi_linux.x86_64.tar.gz
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
tar xvf %{SOURCE0} 
%endif
%ifarch x86_64
tar xvf %{SOURCE1}
%endif

# check version matches
RPM_VER=`cat manifest.json | python -c 'import sys,json; print(json.load(sys.stdin)["version"])'`

if [ "$RPM_VER" != "%{version}" ]; then
  echo "VERSION MISMATCH, Rpm version $RPM_VER this package %{version}"
  exit 1
fi


%install
mkdir -p %{buildroot}%{_libdir}/chromium/PepperFlash/
install -m644 *.{so,json} %{buildroot}%{_libdir}/chromium/PepperFlash/ 
mkdir -p %{buildroot}%{_sysconfdir}/chromium/
install -m644 default %{buildroot}%{_sysconfdir}/chromium/default

%files
%dir %{_libdir}/chromium/
%{_sysconfdir}/chromium/default
%{_libdir}/chromium/PepperFlash/
