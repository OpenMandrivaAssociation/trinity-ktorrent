%bcond clang 1
%bcond avahi 1

# TDE variables
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif

%define tde_pkg ktorrent
%define tde_prefix /opt/trinity


%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity


Name:		trinity-%{tde_pkg}
Version:	2.2.8
Release:	%{?tde_version:%{tde_version}_}3
Summary:	BitTorrent client for Trinity
Group:		Applications/Utilities
URL:		http://ktorrent.org

License:	GPLv2+


Source0:		https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/applications/internet/%{tarball_name}-%{tde_version}.tar.xz

BuildSystem:	  cmake

BuildOption:    -DCMAKE_BUILD_TYPE="RelWithDebInfo"
BuildOption:    -DCMAKE_INSTALL_PREFIX=%{tde_prefix}
BuildOption:    -DSHARE_INSTALL_PREFIX=%{tde_prefix}/share
BuildOption:    -DBUILD_ALL=ON -DWITH_ALL_OPTIONS=ON
BuildOption:    -DWITH_GCC_VISIBILITY=%{!?with_clang:ON}%{?with_clang:OFF}

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:  trinity-tde-cmake

BuildRequires:	desktop-file-utils
BuildRequires:	gettext

%{!?with_clang:BuildRequires:	gcc-c++}

# GMP support
BuildRequires:	pkgconfig(gmp)

# AVAHI support
#  Disabled on RHEL4 and RHEL5
%if %{with avahi}
BuildRequires:	pkgconfig(avahi-tqt)
BuildRequires:  pkgconfig(avahi-client)
Requires:		trinity-avahi-tqt
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
 
# /shrug
#build -a
# # Fix build issue since 14.1.4 (settings.h not generated as expected)
# pushd src/libktorrent
# /opt/trinity/bin/tdeconfig_compiler ../../../src/libktorrent/ktorrent.kcfg ../../../src/libktorrent/settings.kcfgc
# popd

%install -a
%find_lang %{tde_pkg}

# Unwanted files
%__rm -f "%{?buildroot}%{tde_prefix}/%{_lib}/libktorrent.so"


%files -f %{tde_pkg}.lang
%defattr(-,root,root,-)
%{tde_prefix}/bin/ktcachecheck
%{tde_prefix}/bin/ktorrent
%{tde_prefix}/bin/ktshell
%{tde_prefix}/bin/kttorinfo
%{tde_prefix}/bin/ktupnptest
%{tde_prefix}/%{_lib}/libktorrent.so.*
%{tde_prefix}/%{_lib}/libktorrent.la
%{tde_prefix}/%{_lib}/trinity/ktinfowidgetplugin.la
%{tde_prefix}/%{_lib}/trinity/ktinfowidgetplugin.so
%{tde_prefix}/%{_lib}/trinity/ktipfilterplugin.la
%{tde_prefix}/%{_lib}/trinity/ktipfilterplugin.so
%{tde_prefix}/%{_lib}/trinity/ktlogviewerplugin.la
%{tde_prefix}/%{_lib}/trinity/ktlogviewerplugin.so
%{tde_prefix}/%{_lib}/trinity/ktpartfileimportplugin.la
%{tde_prefix}/%{_lib}/trinity/ktpartfileimportplugin.so
%{tde_prefix}/%{_lib}/trinity/ktrssfeedplugin.la
%{tde_prefix}/%{_lib}/trinity/ktrssfeedplugin.so
%{tde_prefix}/%{_lib}/trinity/ktscanfolderplugin.la
%{tde_prefix}/%{_lib}/trinity/ktscanfolderplugin.so
%{tde_prefix}/%{_lib}/trinity/ktschedulerplugin.la
%{tde_prefix}/%{_lib}/trinity/ktschedulerplugin.so
%{tde_prefix}/%{_lib}/trinity/ktsearchplugin.la
%{tde_prefix}/%{_lib}/trinity/ktsearchplugin.so
%{tde_prefix}/%{_lib}/trinity/ktstatsplugin.la
%{tde_prefix}/%{_lib}/trinity/ktstatsplugin.so
%{tde_prefix}/%{_lib}/trinity/ktupnpplugin.la
%{tde_prefix}/%{_lib}/trinity/ktupnpplugin.so
%{tde_prefix}/%{_lib}/trinity/ktwebinterfaceplugin.la
%{tde_prefix}/%{_lib}/trinity/ktwebinterfaceplugin.so
%{tde_prefix}/share/applications/tde/ktorrent.desktop
%{tde_prefix}/share/apps/ktorrent/
%{tde_prefix}/share/config.kcfg/*.kcfg
%{tde_prefix}/share/icons/hicolor/*/*/*.png
%{tde_prefix}/share/icons/hicolor/*/*/*.svgz
%{tde_prefix}/share/services/*.desktop
%{tde_prefix}/share/servicetypes/ktorrentplugin.desktop
%{tde_prefix}/share/doc/tde/HTML/en/ktorrent/

%if 0%{?with_avahi}
%{tde_prefix}/%{_lib}/trinity/ktzeroconfplugin.la
%{tde_prefix}/%{_lib}/trinity/ktzeroconfplugin.so
%endif
%{tde_prefix}/share/man/man1/ktorrent.1*

