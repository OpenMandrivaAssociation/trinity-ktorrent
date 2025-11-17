#
# Please submit bugfixes or comments via http://www.trinitydesktop.org/
#

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif
%define tde_pkg ktorrent
%define tde_prefix /opt/trinity
%define tde_bindir %{tde_prefix}/bin
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}
%define tde_mandir %{tde_datadir}/man
%define tde_tdeappdir %{tde_datadir}/applications/tde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity

%if 0%{?mdkversion}
%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1
%endif

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity
%global toolchain %(readlink /usr/bin/cc)


Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	2.2.8
Release:	%{?tde_version}_%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}
Summary:	BitTorrent client for Trinity
Group:		Applications/Utilities
URL:		http://ktorrent.org

%if 0%{?suse_version}
License:	GPL-2.0+
%else
License:	GPLv2+
%endif

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:		%{tde_prefix}

Source0:		https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/applications/internet/%{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}.tar.xz

BuildRequires:	cmake make
BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils
BuildRequires:	gettext
%if "%{?toolchain}" != "clang"
BuildRequires:	gcc-c++
%endif
BuildRequires:	pkgconfig
BuildRequires:	fdupes

# SUSE desktop files utility
%if 0%{?suse_version}
BuildRequires:	update-desktop-files
%endif

%if 0%{?opensuse_bs} && 0%{?suse_version}
# for xdg-menu script
BuildRequires:	brp-check-trinity
%endif

# GMP support
BuildRequires:	pkgconfig(gmp)

# AVAHI support
#  Disabled on RHEL4 and RHEL5
%if 0%{?fedora} >= 15 || 0%{?mgaversion} || 0%{?mdkversion} || 0%{?rhel} >= 6 || 0%{?suse_version}
%define with_avahi 1
BuildRequires:	trinity-avahi-tqt-devel
BuildRequires:  pkgconfig(avahi-client)
Requires:		trinity-avahi-tqt
%if 0%{?mgaversion} || 0%{?mdkversion}
Requires:		%{_lib}avahi-client3
%else
Requires:		avahi
%endif
%endif

# GEOIP
BuildRequires:  pkgconfig(geoip)

BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(ice)
BuildRequires:  pkgconfig(sm)

%description
KTorrent is a BitTorrent program for Trinity. Its features include speed capping
(both down and up), integrated searching, UDP tracker support, preview of
certain file types (video and audio) and integration into the TDE Panel
enabling background downloading.
 

##########

%if 0%{?suse_version} && 0%{?opensuse_bs} == 0
%debug_package
%endif

##########


%prep
%autosetup -n %{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}


%build
if ! rpm -E %%cmake|grep -e 'cd build\|cd ${CMAKE_BUILD_DIR:-build}'; then
  %__mkdir_p build
  cd build
fi

%cmake \
  -DCMAKE_BUILD_TYPE="RelWithDebInfo" \
  -DCMAKE_C_FLAGS="${RPM_OPT_FLAGS}" \
  -DCMAKE_CXX_FLAGS="${RPM_OPT_FLAGS}" \
  -DCMAKE_SKIP_RPATH=OFF \
  -DCMAKE_SKIP_INSTALL_RPATH=OFF \
  -DCMAKE_INSTALL_RPATH="%{tde_libdir}" \
  -DCMAKE_VERBOSE_MAKEFILE=ON \
  -DWITH_GCC_VISIBILITY=OFF \
  \
  -DBIN_INSTALL_DIR=%{tde_bindir} \
  -DLIB_INSTALL_DIR=%{tde_libdir} \
  -DCMAKE_INSTALL_PREFIX=%{tde_prefix} \
  -DSHARE_INSTALL_PREFIX=%{tde_datadir} \
  -DLIB_INSTALL_DIR=%{tde_libdir} \
  \
  -DBUILD_ALL=ON \
  -DWITH_ALL_OPTIONS=ON \
%if 0%{?suse_version} == 1699
  -DWITH_BUILTIN_GEOIP=ON \
  -DWITH_SYSTEM_GEOIP=OFF \
%endif
  \
  ..

# Fix build issue since 14.1.4 (settings.h not generated as expected)
pushd src/libktorrent
/opt/trinity/bin/tdeconfig_compiler ../../../src/libktorrent/ktorrent.kcfg ../../../src/libktorrent/settings.kcfgc
popd

%__make %{?_smp_mflags}


%install
export PATH="%{tde_bindir}:${PATH}"
%__make install DESTDIR="%{buildroot}" -C build

%find_lang %{tde_pkg}

# Unwanted files
%__rm -f "%{?buildroot}%{tde_libdir}/libktorrent.so"


%files -f %{tde_pkg}.lang
%defattr(-,root,root,-)
%{tde_bindir}/ktcachecheck
%{tde_bindir}/ktorrent
%{tde_bindir}/ktshell
%{tde_bindir}/kttorinfo
%{tde_bindir}/ktupnptest
%{tde_libdir}/libktorrent.so.*
%{tde_libdir}/libktorrent.la
%{tde_tdelibdir}/ktinfowidgetplugin.la
%{tde_tdelibdir}/ktinfowidgetplugin.so
%{tde_tdelibdir}/ktipfilterplugin.la
%{tde_tdelibdir}/ktipfilterplugin.so
%{tde_tdelibdir}/ktlogviewerplugin.la
%{tde_tdelibdir}/ktlogviewerplugin.so
%{tde_tdelibdir}/ktpartfileimportplugin.la
%{tde_tdelibdir}/ktpartfileimportplugin.so
%{tde_tdelibdir}/ktrssfeedplugin.la
%{tde_tdelibdir}/ktrssfeedplugin.so
%{tde_tdelibdir}/ktscanfolderplugin.la
%{tde_tdelibdir}/ktscanfolderplugin.so
%{tde_tdelibdir}/ktschedulerplugin.la
%{tde_tdelibdir}/ktschedulerplugin.so
%{tde_tdelibdir}/ktsearchplugin.la
%{tde_tdelibdir}/ktsearchplugin.so
%{tde_tdelibdir}/ktstatsplugin.la
%{tde_tdelibdir}/ktstatsplugin.so
%{tde_tdelibdir}/ktupnpplugin.la
%{tde_tdelibdir}/ktupnpplugin.so
%{tde_tdelibdir}/ktwebinterfaceplugin.la
%{tde_tdelibdir}/ktwebinterfaceplugin.so
%{tde_tdeappdir}/ktorrent.desktop
%{tde_datadir}/apps/ktorrent/
%{tde_datadir}/config.kcfg/*.kcfg
%{tde_datadir}/icons/hicolor/*/*/*.png
%{tde_datadir}/icons/hicolor/*/*/*.svgz
%{tde_datadir}/services/*.desktop
%{tde_datadir}/servicetypes/ktorrentplugin.desktop
%{tde_tdedocdir}/HTML/en/ktorrent/

%if 0%{?with_avahi}
%{tde_tdelibdir}/ktzeroconfplugin.la
%{tde_tdelibdir}/ktzeroconfplugin.so
%endif
%{tde_mandir}/man1/ktorrent.1*

