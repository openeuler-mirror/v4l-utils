Name:           v4l-utils
Version:        1.14.2
Release:        7
Summary:        Linux utilities and libraries to handle media devices
License:        GPLv2+ and GPLv2
URL:            http://www.linuxtv.org/downloads/v4l-utils/
Source0:        http://linuxtv.org/downloads/v4l-utils/v4l-utils-%{version}.tar.bz2
Patch0000:      v4l-utils-sysmacros.patch
Patch0001:      0001-fix-compilation-failed.patch
Patch0002:      0002-fix-clang.patch

BuildRequires:  alsa-lib-devel desktop-file-utils doxygen gettext
BuildRequires:  kernel-headers libjpeg-devel qt5-qtbase-devel systemd-devel
Requires:       udev
Provides:       qv4l2 = %{version}-%{release} libdvbv5 = %{version}-%{release}
Obsoletes:      qv4l2 < %{version}-%{release} libdvbv5 < %{version}-%{release}

%description
v4l-utils are a series of packages for handling media devices(TV devices,capture devices,
radio devices, remote controllers).It provides a series of libraries and utilities to be
used to control several aspect of the media boards.

%package        devel-tools
Summary:        Tools for v4l2 / DVB driver development
License:        GPLv2+ and GPLv2
Requires:       v4l-utils = %{version}-%{release}

%description    devel-tools
Tools for v4l2 / DVB driver development.


%package -n     libv4l
Summary:        Collection of video4linux support libraries 
# Some of the decompression helpers are GPLv2, the rest is LGPLv2+
License:        LGPLv2+ and GPLv2
URL:            http://hansdegoede.livejournal.com/3636.html

%description -n libv4l
libv4l is a collection of libraries which adds a thin abstraction layer on
top of video4linux2 devices. The purpose of this (thin) layer is to make it
easy for application writers to support a wide variety of devices without
having to write separate code for different devices in the same class. libv4l
consists of 3 different libraries: libv4lconvert, libv4l1 and libv4l2.

libv4lconvert offers functions to convert from any (known) pixel-format
to V4l2_PIX_FMT_BGR24 or V4l2_PIX_FMT_YUV420.

libv4l1 offers the (deprecated) v4l1 API on top of v4l2 devices, independent
of the drivers for those devices supporting v4l1 compatibility (which many
v4l2 drivers do not).

libv4l2 offers the v4l2 API on top of v4l2 devices, while adding for the
application transparent libv4lconvert conversion where necessary.




%package        devel
Summary:        Development files for v4l-utils
License:        LGPLv2+ and GPLv2
URL:            http://hansdegoede.livejournal.com/3636.html
Requires:       %{name} = %{version}-%{release}
Provides:       libv4l-devel = %{version}-%{release} libdvbv5-devel = %{version}-%{release}
Obsoletes:      libv4l-devel < %{version}-%{release} libdvbv5-devel < %{version}-%{release}

%description    devel
The devel package contains libraries and header files for developing applications that
use v4l-utils.

%package        help
Summary:   Help document for the v4l-utils package
Buildarch: noarch

%description    help
Help document for the v4l-utils package.

%prep
%autosetup -p1

%build
%configure --disable-static --enable-libdvbv5 --enable-doxygen-man
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
%make_build
make doxygen-run

%install
%{!?_udevrulesdir: %global _udevrulesdir /lib/udev/rules.d}
%make_install
%delete_la
install -d %{buildroot}%{_mandir}/man3/
cp -arv %{_builddir}/%{name}-%{version}/doxygen-doc/man/man3 $RPM_BUILD_ROOT%{_mandir}/
rm $RPM_BUILD_ROOT%{_mandir}/man3/_*3
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/qv4l2.desktop
%find_lang %{name}
%find_lang libdvbv5
mv lib/libdvbv5/README lib/libdvbv5/README.libdvbv5

%post
/sbin/ldconfig

%postun
/sbin/ldconfig


%post -n libv4l -p /sbin/ldconfig

%postun -n libv4l -p /sbin/ldconfig


%files -f %{name}.lang -f libdvbv5.lang
%doc README lib/libdvbv5/README.libdvbv5
%dir %{_sysconfdir}/rc_keymaps
%config(noreplace) %{_sysconfdir}/rc_maps.cfg
%{_udevrulesdir}/70-infrared.rules
%{_udevrulesdir}/../rc_keymaps/*
%{_bindir}/cx18-ctl
%{_bindir}/cec*
%{_bindir}/dvb*
%{_bindir}/ir-ctl
%{_bindir}/ir-keytable
%{_bindir}/ivtv-ctl
%{_bindir}/media-ctl
%{_bindir}/rds-ctl
%{_bindir}/v4l2-ctl
%{_bindir}/v4l2-sysfs-path
%{_bindir}/qv4l2
%{_datadir}/applications/qv4l2.desktop
%{_datadir}/icons/hicolor/*/apps/qv4l2.*
%{_libdir}/libdvbv5*.so.*

%files -n libv4l
%doc ChangeLog README.libv4l TODO
%license COPYING.libv4l COPYING
%{_libdir}/libv4l
%{_libdir}/libv4l*.so.*



%files devel-tools
%doc README
%{_bindir}/decode_tm6000
%{_bindir}/v4l2-compliance
%{_sbindir}/v4l2-dbg

%files devel
%doc README.lib-multi-threading
%{_includedir}/libv4l*.h
%{_libdir}/libv4l*.so
%{_libdir}/pkgconfig/libv4l*.pc
%{_includedir}/libdvbv5/*.h
%{_libdir}/libdvbv5*.so
%{_libdir}/pkgconfig/libdvbv5*.pc
%exclude %{_libdir}/{v4l1compat.so,v4l2convert.so}

%files help
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3*

%changelog
* Wed Jun 28 2023 yoo <sunyuechi@iscas.ac.cn> - 1.14.2-7
- fix clang build error

* Mon Aug 2 2021 Haiwei Li <lihaiwei8@huawei.com> - 1.14.2-6
- Fix complication failed due to gcc upgrade

* Wed Nov 13 2019 caomeng <caomeng5@huawei.com> - 1.14.2-5
- let libv4l1.so.0 in libv4l

* Mon Oct 28 2019 Lijin Yang <yanglijin@huawei.com> - 1.14.2-4
- Package init
