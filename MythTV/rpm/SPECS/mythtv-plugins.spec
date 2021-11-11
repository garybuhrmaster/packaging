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

#
# At least for now, we need to opt-out of LTO flags if
# we are not explicitly handing it via our overrides
#
%if %{without lto}
%global _lto_cflags %{nil}
%endif

#
# Default to python3, but allow override (needed for fixes/30)
#
%global py_prefix python3
%if %{with python2}
%global py_prefix python2
%if (0%{?rhel} == 7)
%global py_prefix python
%endif
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


BuildRequires:  mythtv-devel              = %{version}-%{release}
BuildRequires:  %{py_prefix}-MythTV       = %{version}-%{release}
BuildRequires:  git-core
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  binutils
BuildRequires:  make
%if ((0%{?fedora}) || (0%{?rhel} > 7))
BuildRequires:  cmake
%else
BuildRequires:  cmake3
%endif
%if %{with llvm}
%if ((0%{?fedora}) || (0%{?rhel} > 7))
BuildRequires:  llvm
BuildRequires:  clang
BuildRequires:  lld
%else
BuildRequires:  llvm-toolset-7.0
%endif
%else
%if ((0%{?fedora}) || (0%{?rhel} > 8))
BuildRequires:  gcc-c++
BuildRequires:  gcc
%else
%if (0%{?rhel} == 7)
BuildRequires:  devtoolset-10
%else
BuildRequires:  gcc-toolset-10
%endif
%endif
%endif
%if %{with qt6}
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qt5compat-devel
%else
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtscript-devel
%if ((0%{?fedora}) || ((0%{?rhel}) && ((0%{?rhel}) < 9)))
BuildRequires:  qt5-qtwebkit-devel
%endif
%endif
BuildRequires:  freetype-devel
%if ((0%{?fedora}) || (0%{?rhel} > 7))
BuildRequires:  mariadb-connector-c-devel
%else
BuildRequires:  mariadb-devel
%endif
BuildRequires:  perl(XML::Simple)
BuildRequires:  perl(DateTime::Format::ISO8601)
BuildRequires:  perl(XML::XPath)
BuildRequires:  perl(Date::Manip)
%if ((0%{?fedora}) || ((0%{?rhel}) && ((0%{?rhel}) < 9)))
BuildRequires:  perl(Image::Size)
BuildRequires:  perl(SOAP::Lite)
%endif
BuildRequires:  perl(JSON)
BuildRequires:  %{py_prefix}
BuildRequires:  %{py_prefix}-pycurl
BuildRequires:  %{py_prefix}-lxml
%if ((0%{?fedora}) || ((0%{?rhel} == 7) && ("%{py_prefix}" == "python")))
BuildRequires:  %{py_prefix}-oauth
%endif
BuildRequires:  %{py_prefix}-rpm-macros
BuildRequires:  %{py_prefix}-devel
BuildRequires:  /usr/bin/pathfix.py
BuildRequires:  libvorbis-devel
BuildRequires:  flac-devel
BuildRequires:  lame-devel
BuildRequires:  libexif-devel
BuildRequires:  zlib-devel
BuildRequires:  libcdio-paranoia-devel
BuildRequires:  fftw-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  avahi-compat-libdns_sd-devel
%if ((0%{?fedora}) || ((0%{?rhel}) && ((0%{?rhel}) < 9)))
BuildRequires:  jack-audio-connection-kit-devel
%endif
BuildRequires:  libass-devel
BuildRequires:  libcrystalhd-devel
%if (0%{?fedora})
BuildRequires:  libomxil-bellagio-devel
%endif
%if ((0%{?fedora}) || (0%{?rhel} > 7))
BuildRequires:  vulkan-headers
%endif
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
BuildRequires:  libXNVCtrl-devel
BuildRequires:  lzo-devel
BuildRequires:  minizip-devel
BuildRequires:  libzip-devel
BuildRequires:  gnutls-devel
BuildRequires:  libmpeg2-devel

################################################################################

# Package for all (buildable) MythTV plugins

Requires:       mythtv-frontend         = %{version}-%{release}
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
%if ((0%{?fedora}) || ((0%{?rhel}) && ((0%{?rhel}) < 9)))
Requires:       perl(Image::Size)
Requires:       perl(SOAP::Lite)
%endif
Requires:       perl(JSON)
Requires:       perl(XML::SAX::Base)
Requires:       %{py_prefix}-pycurl
Requires:       %{py_prefix}-lxml
%if ((0%{?fedora}) || ((0%{?rhel} == 7) && ("%{py_prefix}" == "python")))
Requires:       %{py_prefix}-oauth
%endif
%if ((0%{?fedora}) || ((0%{?rhel} == 7) && ("%{py_prefix}" == "python")))
Requires:       %{py_prefix}-imaging
%endif
%if ((0%{?rhel} == 7) && ("%{py_prefix}" == "python3"))
Requires:       python36-imaging
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
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" .
%else
pathfix.py -pni "%{__python2} %{py2_shbang_opts}" .
%endif

################################################################################

%build

%if (0%{?rhel} == 7)
%if %{with llvm}
source scl_source enable llvm-toolset-7.0 >/dev/null 2>/dev/null && true || true
%else
source scl_source enable devtoolset-10 >/dev/null 2>/dev/null && true || true
%endif
%endif
%if ((%{without llvm}) && (0%{?rhel} == 8))
source scl_source enable gcc-toolset-10 >/dev/null 2>/dev/null && true || true
%endif

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

%if (0%{?rhel} == 7)
%if %{with llvm}
source scl_source enable llvm-toolset-7.0 >/dev/null 2>/dev/null && true || true
%else
source scl_source enable devtoolset-10 >/dev/null 2>/dev/null && true || true
%endif
%endif
%if ((%{without llvm}) && (0%{?rhel} == 8))
source scl_source enable gcc-toolset-10 >/dev/null 2>/dev/null && true || true
%endif

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

%if (0%{?rhel} == 7)
%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%endif

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


