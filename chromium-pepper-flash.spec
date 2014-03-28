# Thanks to malcolmlewis for help with this script
# Thanks to Tom "spot" Callaway for much of the patchwork
# Thanks to jhaygood for most of the icu patch
%define	debug_package %nil

Name:           chromium-pepper-flash
Url:            http://www.google.com/chrome
Summary:        Chromium Flash player plugin
Version:        12.0.0.77
Release:        0.1
License:        Free
Group:          Networking/WWW
Source0:        https://dl.google.com/linux/direct/google-chrome-stable_current_i386.rpm
Source1:        https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
# Use x86/x86_64 pre-built libs
ExclusiveArch:  %{ix86} x86_64
Requires:       chromium-browser

%description
Pepper API based Adobe Flash plugin for Google's Open Source browser Chromium.

%package -n chromium-pdf-plugin
Summary:        Chromium PDF viewer plugin
License:        Non-OSS
Group:          Networking/WWW
Requires:       chromium-browser

%description -n chromium-pdf-plugin
Official PDF viewer plugin for Google's Open Source browser Chromium.

%prep
%setup -c -T

%build
%ifarch i586
rpm2cpio %{SOURCE0} | cpio -idmv
%endif
%ifarch x86_64
rpm2cpio %{SOURCE1} | cpio -idmv
%endif


%post
CHROMIUM_CONFIG='/etc/chromium/default'
# add ppapi flashplayer path to chromium config file
if [[ $(cat "$CHROMIUM_CONFIG") != *ppapi*path* ]]; then
    sed -i '/CHROMIUM_FLAGS/s|"$| --ppapi-flash-path=/usr/%{_libdir}/chromium/PepperFlash/libpepflashplayer.so"|' "$CHROMIUM_CONFIG"
  else
    : # do nothing
fi

%postun
CHROMIUM_CONFIG='/etc/chromium/default'
# remove ppapi flashplayer path from chromiun config file
if [ -f "$CHROMIUM_CONFIG" ]; then
    sed -i "s| --ppapi-flash-path=/usr/%{_libdir}/chromium/PepperFlash/libpepflashplayer.so||" "$CHROMIUM_CONFIG"
  else
    : # do nothing
fi

%install
mkdir -p %{buildroot}%{_libdir}/chromium/PepperFlash/
install -m644 opt/google/chrome/PepperFlash/* %{buildroot}%{_libdir}/chromium/PepperFlash/ 
install -m755 opt/google/chrome/libpdf.so %{buildroot}%{_libdir}/chromium/

%files
%dir %{_libdir}/chromium/
%{_libdir}/chromium/PepperFlash/

%files -n chromium-pdf-plugin
%{_libdir}/chromium/libpdf.so
