#
# This spec file was split from the original
# larger mythtv spec file.  This work builds
# on previous works from (at least):
#
#    Chris Petersen <cpetersen@mythtv.org>
#    Jarod Wilson <jarod@wilsonet.com>
#    Richard Shaw <hobbes1069@gmail.com>
#    Axel Thimm <Axel.Thimm@ATrpms.net>
#    David Bussenschutt <buzz@oska.com>
#    Nicolas Chauvet <kwizart@gmail.com>
#    Sérgio Basto <sergio@serjux.com>
#    Adrian Reber <adrian@lisas.de>
#    Xavier Bachelot <xavier@bachelot.org>
#    Paul Howarth <paul@city-fan.org>
#


################################################################################

# The following options are disabled by default.  Use --with to enable them
%bcond_with     llvm
%bcond_with     toolchain_clang
%bcond_with     toolchain_gcc
%bcond_with     python2
%bcond_with     lto
%bcond_with     qt6

# The following options are enabled by default.  Use --without to disable them
%bcond_without  rpmfusion

################################################################################

#
# _hardended_build is the default for recent releases.
#
%global _hardened_build 1

%global _pkgverify_level digest

#
# At least for now, we need to opt-out of LTO flags if
# we are not explicitly handing it via our overrides
#
%if %{without lto}
%global _lto_cflags %{nil}
%endif

#
# Adjust toolchain for gcc/clang (default to gcc if toolchain not set)
#
%if 0%{!?toolchain:1}
%global toolchain gcc
%endif
%if %{with llvm} || %{with toolchain_clang}
%global toolchain clang
%endif
%if %{with toolchain_gcc}
%global toolchain gcc
%endif

#
# Default to python3, but allow override (needed for fixes/30)
#
%global py_prefix python3
%if %{with python2}
%global py_prefix python2
%endif

################################################################################


#
# Basic descriptive tags for this package:
#
Name:           mythtv-plugins
Summary:        Plugins for MythTV
URL:            http://www.mythtv.org/

#
# Specify the commit hash for the source for this rpm
#
%global commit  %{?MYTHTV_COMMIT}%{!?MYTHTV_COMMIT:0}

# Version/Release info
Version:        %{?MYTHTV_VERSION}%{!?MYTHTV_VERSION:0.0}
Release:        100%{?dist}

# The primary license is GPLv2+, but bits are borrowed from a number of
# projects... For a breakdown of the licensing, see the base LICENSING.
License:        GPLv2+ and LGPLv2+ and LGPLv2 and (GPLv2 or QPL) and (GPLv2+ or LGPLv2+)

# Plugins are now in the mythtv source repo
Source0:        https://github.com/MythTV/mythtv/archive/%{commit}/mythtv-%{commit}.tar.gz


BuildRequires:  mythtv-devel%{?_isa}            = %{version}-%{release}
BuildRequires:  %{py_prefix}-MythTV             = %{version}-%{release}
BuildRequires:  git-core
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  binutils
BuildRequires:  make
BuildRequires:  cmake
%if ("%{toolchain}" == "clang")
BuildRequires:  llvm
BuildRequires:  clang
BuildRequires:  lld
%else
BuildRequires:  gcc-c++
BuildRequires:  gcc
%endif
%if %{with qt6}
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qt5compat-devel
BuildRequires:  qt6-qtwebengine-devel
%else
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtscript-devel
BuildRequires:  qt5-qtwebkit-devel
BuildRequires:  qt5-qtwebengine-devel
%endif
BuildRequires:  freetype-devel
BuildRequires:  mariadb-connector-c-devel
BuildRequires:  perl(XML::Simple)
BuildRequires:  perl(DateTime::Format::ISO8601)
BuildRequires:  perl(XML::XPath)
BuildRequires:  perl(Date::Manip)
BuildRequires:  perl(Image::Size)
BuildRequires:  perl(SOAP::Lite)
BuildRequires:  perl(JSON)
BuildRequires:  %{py_prefix}
BuildRequires:  %{py_prefix}-pycurl
BuildRequires:  %{py_prefix}-lxml
%if (0%{?fedora})
BuildRequires:  %{py_prefix}-oauth
%endif
BuildRequires:  %{py_prefix}-oauthlib
BuildRequires:  %{py_prefix}-rpm-macros
BuildRequires:  %{py_prefix}-devel
BuildRequires:  libvorbis-devel
BuildRequires:  flac-devel
BuildRequires:  lame-devel
BuildRequires:  libexif-devel
BuildRequires:  zlib-devel
BuildRequires:  libcdio-paranoia-devel
BuildRequires:  fftw-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  avahi-compat-libdns_sd-devel
%if (0%{?rhel} >= 10)
BuildRequires:  pipewire-jack-audio-connection-kit-devel
%else
BuildRequires:  jack-audio-connection-kit-devel
%endif
BuildRequires:  libass-devel
%if ((0%{?fedora}) || ((0%{?rhel}) && ((0%{?rhel}) < 9)))
BuildRequires:  libcrystalhd-devel
%endif
%if ((0%{?fedora}) && ((0%{?fedora}) < 41))
BuildRequires:  libomxil-bellagio-devel
%endif
BuildRequires:  vulkan-headers
BuildRequires:  libavc1394-devel
BuildRequires:  libiec61883-devel
BuildRequires:  libraw1394-devel
BuildRequires:  libogg-devel
BuildRequires:  libtheora-devel
BuildRequires:  libva-devel
BuildRequires:  libvdpau-devel
BuildRequires:  libvpx-devel
BuildRequires:  libXinerama-devel
BuildRequires:  libxml2-devel
BuildRequires:  libXrandr-devel
BuildRequires:  libXv-devel
BuildRequires:  libXxf86vm-devel
BuildRequires:  libdrm-devel
BuildRequires:  libaom-devel
BuildRequires:  libdav1d-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  systemd-devel
%if %{with rpmfusion}
BuildRequires:  x264-devel
BuildRequires:  x265-devel
BuildRequires:  xvidcore-devel
%endif
BuildRequires:  nv-codec-headers
BuildRequires:  xz-devel
BuildRequires:  SDL2-devel
BuildRequires:  taglib-devel
BuildRequires:  dcraw
BuildRequires:  hdhomerun-devel
%if ((0%{?fedora}) || ((0%{?rhel}) > 8))
BuildRequires:  libbluray-devel
%endif
BuildRequires:  libsamplerate-devel
BuildRequires:  soundtouch-devel
%if ((0%{?fedora}) || ((0%{?rhel}) && ((0%{?rhel}) < 10)))
# Current MythTV does not use libXNVCtrl as XrandX works
BuildRequires:  libXNVCtrl-devel
%endif
BuildRequires:  lzo-devel
%if ((0%{?fedora}) || ((0%{?rhel}) && ((0%{?rhel}) < 9)))
BuildRequires:  minizip-devel
%endif
BuildRequires:  libzip-devel
BuildRequires:  gnutls-devel

################################################################################

# Package for all (buildable) MythTV plugins

Requires:       mythtv-frontend%{?_isa}         = %{version}-%{release}
Requires:       wodim
Requires:       dvd+rw-tools
Requires:       dvdauthor
Requires:       mjpegtools
Requires:       genisoimage
Requires:       pmount
Requires:       perl(XML::Simple)
Requires:       perl(DateTime::Format::ISO8601)
Requires:       perl(XML::XPath)
Requires:       perl(Date::Manip)
Requires:       perl(Image::Size)
Requires:       perl(SOAP::Lite)
Requires:       perl(JSON)
Requires:       perl(XML::SAX::Base)
Requires:       %{py_prefix}-pycurl
Requires:       %{py_prefix}-lxml
%if (0%{?fedora})
Requires:       %{py_prefix}-oauth
%endif
Requires:       %{py_prefix}-oauthlib
%if (0%{?fedora})
Requires:       %{py_prefix}-imaging
%endif
Requires:       dcraw

################################################################################

%description
This is a consolidation of all the official MythTV plugins that used to be
distributed as separate downloads from mythtv.org.

################################################################################

%prep

%autosetup -p1 -n mythtv-%{commit}

%if ("%{py_prefix}" == "python3")
%py3_shebang_fix .
%else
pathfix.py -pni "%{__python2} %{py2_shbang_opts}" .
%endif

################################################################################

%build

pushd mythplugins

    # mythplugins configure obtains most options from the
    # mythtv configuration stored in mythconfig.mak in order
    # to insure the plugins are compatible with the base
    # libraries.  --prefix is used to find mythconfig.mak

    ./configure \
        --prefix=%{_prefix}                         \
%if ("%{py_prefix}" == "python3")
        --python=%{__python3}
%else
        --python=%{__python2}
%endif

    %{make_build}

popd

################################################################################

%install

pushd mythplugins

    make install INSTALL_ROOT=%{buildroot}

    # In the case that some plugins are not built due to
    # upstream library differences (and to avoid failing
    # the build entirely), create a few directories if
    # they do not exist.

    mkdir -p %{buildroot}%{_datadir}/mythtv/metadata/Game
    mkdir -p %{buildroot}%{_datadir}/mythtv/mytharchive
    mkdir -p %{buildroot}%{_datadir}/mythtv/mythnetvision
    mkdir -p %{buildroot}%{_datadir}/mythtv/mythnews
    mkdir -p %{buildroot}%{_datadir}/mythtv/mythweather

    # Fixup a few files from mythgame that rpmlint reports
    if [ -e "%{buildroot}%{_datadir}/mythtv/metadata/Game/giantbomb/giantbomb_api.py" ] ; then
       chmod a+x %{buildroot}%{_datadir}/mythtv/metadata/Game/giantbomb/giantbomb_api.py
    fi
    if [ -e "%{buildroot}%{_datadir}/mythtv/metadata/Game/giantbomb/giantbomb_exceptions.py" ] ; then
       chmod a+x %{buildroot}%{_datadir}/mythtv/metadata/Game/giantbomb/giantbomb_exceptions.py
    fi

    # remove unnecessary packaging/SCM files
    find %{buildroot} -name .gitignore -delete >/dev/null
    find %{buildroot} -name .packlist -delete >/dev/null

    %{_fixperms} %{buildroot}

popd

################################################################################

%files

%{_bindir}/*
%dir %{_libdir}/mythtv/plugins
%{_libdir}/mythtv/plugins/*
%{_datadir}/mythtv/themes/default/*
%{_datadir}/mythtv/themes/default-wide/*
%{_datadir}/mythtv/i18n/*
%{_datadir}/mythtv/*.xml
%{_datadir}/mythtv/metadata/Game
%{_datadir}/mythtv/mytharchive
%{_datadir}/mythtv/mythnetvision
%{_datadir}/mythtv/mythnews
%{_datadir}/mythtv/mythweather

################################################################################

%changelog

* Wed May 09 2018 Gary Buhrmaster <gary.buhrmaster@gmail.com>
- Rework for managed rebuilds


