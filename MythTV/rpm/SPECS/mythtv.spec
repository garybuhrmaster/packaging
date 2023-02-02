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
%if (0%{?rhel} == 7)
%global py_prefix python
%endif
%endif

#
# Adjust __python for for el7 bytecompile
#
%if (0%{?rhel} == 7)
%global __python %{py_prefix}
%endif

#
# Mitigation for a FTBFS in F36
#
%if (0%{?fedora} == 36)
%undefine _package_note_file
%endif

################################################################################


# Basic descriptive tags for this package:
Name:           mythtv
Summary:        A digital video recorder (DVR) application
URL:            http://www.mythtv.org/

#
# Specify the commit hash for the source for this rpm
#
%global commit  %{?MYTHTV_COMMIT}%{!?MYTHTV_COMMIT:0}

# Version/Release info
Version:        %{?MYTHTV_VERSION}%{!?MYTHTV_VERSION:0.0}
Release:        100%{?dist}

# The primary license is GPLv2+, but bits are borrowed from a number of
# projects... For a breakdown of the licensing, see PACKAGE-LICENSING.
License:        GPLv2+ and LGPLv2+ and LGPLv2 and (GPLv2 or QPL) and (GPLv2+ or LGPLv2+)

# Source based on commit hash
Source0:        https://github.com/MythTV/%{name}/archive/%{commit}/%{name}-%{commit}.tar.gz

Source200:      mythtv-mythbackend.service
Source201:      mythtv-99-mythbackend.rules
Source202:      mythtv-logrotate.conf
Source203:      mythtv-mythjobqueue.service
Source204:      mythtv-mythmediaserver.service
Source210:      mythtv-mythbackend-tmpfiles.conf
Source220:      mythtv-LICENSING
Source300:      mythtv-mythfrontend.png
Source301:      mythtv-mythfrontend.desktop
Source302:      mythtv-mythtv-setup.png
Source303:      mythtv-mythtv-setup.desktop

# Global MythTV and Shared Build Requirements

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
%if ("%{toolchain}" == "clang")
%if ((0%{?fedora}) || (0%{?rhel} > 7))
BuildRequires:  llvm
BuildRequires:  clang
BuildRequires:  lld
%else
BuildRequires:  llvm-toolset-7.0
%endif
%else
%if ((0%{?fedora}) || (0%{?rhel} > 7))
BuildRequires:  gcc-c++
BuildRequires:  gcc
%else
BuildRequires:  devtoolset-10
%endif
%endif
BuildRequires:  desktop-file-utils
%if %{with qt6}
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qt5compat-devel
%else
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtscript-devel
BuildRequires:  qt5-qtwebkit-devel
%endif
BuildRequires:  freetype-devel
%if ((0%{?fedora}) || (0%{?rhel} > 7))
BuildRequires:  mariadb-connector-c-devel
%else
BuildRequires:  mariadb-devel
%endif
BuildRequires:  libcec-devel
BuildRequires:  libvpx-devel
BuildRequires:  lm_sensors-devel
BuildRequires:  nasm
BuildRequires:  systemd-rpm-macros

# X, and Xv video support
BuildRequires:  libXv-devel
BuildRequires:  libXxf86vm-devel
BuildRequires:  libXinerama-devel
BuildRequires:  libXrandr-devel
BuildRequires:  mesa-libGLU-devel
%ifarch %arm
BuildRequires:  mesa-libGLES-devel
%endif
BuildRequires:  xorg-x11-proto-devel
BuildRequires:  libdrm-devel

# OpenGL video output and vsync support
BuildRequires:  libGL-devel
BuildRequires:  libGLU-devel

# Misc A/V format support
BuildRequires:  fftw-devel
BuildRequires:  flac-devel
BuildRequires:  lame-devel
BuildRequires:  libcdio-devel
BuildRequires:  libcdio-paranoia-devel
BuildRequires:  libogg-devel
BuildRequires:  libtheora-devel
BuildRequires:  libvorbis-devel
BuildRequires:  taglib-devel
%if %{with rpmfusion}
BuildRequires:  x264-devel
BuildRequires:  x265-devel
BuildRequires:  xvidcore-devel
%endif
BuildRequires:  exiv2-devel
BuildRequires:  expat-devel
BuildRequires:  nv-codec-headers
BuildRequires:  libaom-devel
BuildRequires:  libdav1d-devel
# (non-free) BuildRequires:  fdk-aac-devel

# External library support
BuildRequires:  hdhomerun-devel
%if ((0%{?fedora}) || ((0%{?rhel}) > 8))
BuildRequires:  libbluray-devel
%endif
BuildRequires:  libsamplerate-devel
BuildRequires:  soundtouch-devel
BuildRequires:  libXNVCtrl-devel
BuildRequires:  lzo-devel
%if ((0%{?fedora}) || ((0%{?rhel}) && ((0%{?rhel}) < 9)))
BuildRequires:  minizip-devel
%endif
BuildRequires:  libzip-devel
BuildRequires:  gnutls-devel

# Audio framework support
BuildRequires:  alsa-lib-devel
BuildRequires:  jack-audio-connection-kit-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  avahi-compat-libdns_sd-devel

# Bluray support
BuildRequires:  libxml2-devel
#BuildRequires:  libudf-devel

# Subtitle support
BuildRequires:  libass-devel

# Need dvb headers to build in dvb support
BuildRequires:  kernel-headers

# FireWire cable box support
BuildRequires:  libavc1394-devel
BuildRequires:  libiec61883-devel
BuildRequires:  libraw1394-devel

# HW video support
BuildRequires:  libvdpau-devel
BuildRequires:  libva-devel
%if ((0%{?fedora}) || ((0%{?rhel}) && ((0%{?rhel}) < 9)))
BuildRequires:  libcrystalhd-devel
%endif
%if (0%{?fedora})
BuildRequires:  libomxil-bellagio-devel
%endif

# Wayland (extras) support
BuildRequires:  wayland-devel
%if %{with qt6}
BuildRequires:  qt6-qtbase-private-devel
BuildRequires:  libxkbcommon-devel
%else
BuildRequires:  qt5-qtbase-private-devel
%endif

# Vulkan support
%if ((0%{?fedora}) || (0%{?rhel} > 7))
BuildRequires:  vulkan-headers
%endif

# systemd ready and journald logging support
BuildRequires:  systemd-devel
BuildRequires:  systemd

# API Build Requirements
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Config)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(Sys::Hostname)
BuildRequires:  perl(DBI)
BuildRequires:  perl(HTTP::Request)
BuildRequires:  perl(Net::UPnP::QueryResponse)
BuildRequires:  perl(Net::UPnP::ControlPoint)
BuildRequires:  perl(DBD::mysql)
BuildRequires:  perl(IO::Socket::INET6)
BuildRequires:  perl(LWP::UserAgent)
BuildRequires:  perl(XML::Simple)

BuildRequires:  %{py_prefix}
BuildRequires:  %{py_prefix}-pycurl
BuildRequires:  %{py_prefix}-lxml
BuildRequires:  %{py_prefix}-rpm-macros
%if ("%{py_prefix}" != "python3")
BuildRequires:  %{py_prefix}-urlgrabber
%endif
%if ((0%{?fedora}) || (0%{?rhel} > 7) || ((0%{?rhel} == 7) && ("%{py_prefix}" == "python")))
BuildRequires:  %{py_prefix}-requests
%endif
%if ((0%{?rhel} == 7) && ("%{py_prefix}" == "python3"))
BuildRequires:  python36-requests
%endif
%if ((0%{?fedora}) || (0%{?rhel} > 7) || ((0%{?rhel} == 7) && ("%{py_prefix}" == "python")))
BuildRequires:  %{py_prefix}-simplejson
%endif
%if ((0%{?rhel} == 7) && ("%{py_prefix}" == "python3"))
BuildRequires:  python36-simplejson
%endif
BuildRequires:  %{py_prefix}-future
%if ((0%{?fedora}) || (0%{?rhel} > 7))
BuildRequires:  %{py_prefix}-mysqlclient
%endif
%if ((0%{?rhel} == 7) && ("%{py_prefix}" == "python"))
BuildRequires:  MySQL-python
%endif
%if ((0%{?rhel} == 7) && ("%{py_prefix}" == "python3"))
BuildRequires:  python36-mysql
%endif
BuildRequires:  %{py_prefix}-devel
BuildRequires:  %{py_prefix}-setuptools


################################################################################
# Requirements for the mythtv meta package

Requires:       mythtv-filesystem               = %{version}-%{release}
Requires:       mythtv-base%{?_isa}             = %{version}-%{release}
Requires:       mythtv-backend%{?_isa}          = %{version}-%{release}
Requires:       mythtv-base-themes%{?_isa}      = %{version}-%{release}
Requires:       mythtv-docs                     = %{version}-%{release}
Requires:       mythtv-frontend%{?_isa}         = %{version}-%{release}
Requires:       mythtv-setup%{?_isa}            = %{version}-%{release}
Requires:       mythtv-mythwelcome%{?_isa}      = %{version}-%{release}
Requires:       mythtv-mythshutdown%{?_isa}     = %{version}-%{release}
Requires:       perl-MythTV                     = %{version}-%{release}
Requires:       php-MythTV                      = %{version}-%{release}
Requires:       %{py_prefix}-MythTV             = %{version}-%{release}
Requires:       mythtv-mythffmpeg%{?_isa}       = %{version}-%{release}
Requires:       mariadb
Requires:       mariadb-server

################################################################################

%description
MythTV provides a unified graphical interface for recording and viewing
television programs. Refer to the mythtv package for more information.

There are also several add-ons and themes available. In order to facilitate
installations with smart/apt-get/yum and other related package
resolvers this meta-package can be used to install all in one sweep.

MythTV implements the following DVR features, and more, with a
unified graphical interface:

- Basic 'live-tv' functionality. Pause/Fast Forward/Rewind "live" TV.
- Video compression using RTjpeg or MPEG-4, and support for DVB and
  hardware encoder cards/devices.
- Program listing retrieval using XMLTV
- Themable, semi-transparent on-screen display
- Electronic program guide
- Scheduled recording of TV programs
- Resolution of conflicts between scheduled recordings
- Basic video editing

################################################################################

%package docs
Summary:        MythTV documentation
BuildArch:      noarch

Requires:       mythtv-filesystem               = %{version}-%{release}

%description docs
MythTV documentation

################################################################################

%package devel
Summary:        Development files for mythtv

Requires:       mythtv-filesystem               = %{version}-%{release}
Requires:       mythtv-libs%{?_isa}             = %{version}-%{release}
Requires:       mythtv-mythffmpeg-libs%{?_isa}  = %{version}-%{release}

%description devel
MythTV development headers and libraries

################################################################################

%package filesystem
Summary:        Filesystem definitions for mythtv
BuildArch:      noarch

%description filesystem
MythTV filesystem directory definitions

################################################################################

%package libs
Summary:        Libraries providing mythtv support

Requires:       mythtv-filesystem               = %{version}-%{release}
Requires:       mythtv-mythffmpeg-libs%{?_isa}  = %{version}-%{release}
%if %{with qt6}
Requires:       qt6-qtbase-mysql
%else
Requires:       qt5-qtbase-mysql
%endif

%description libs
MythTV run-time libraries

################################################################################

%package base-themes
Summary:        Core user interface themes for mythtv

Requires:       mythtv-filesystem               = %{version}-%{release}

%description base-themes
MythTV base themes for graphical applications

################################################################################

%package frontend
Summary:        Client component of mythtv (a DVR)

Requires:       mythtv-filesystem               = %{version}-%{release}
Requires:       mythtv-base%{?_isa}             = %{version}-%{release}
Requires:       mythtv-base-themes%{?_isa}      = %{version}-%{release}
Requires:       mythtv-libs%{?_isa}             = %{version}-%{release}
Requires:       %{py_prefix}-MythTV             = %{version}-%{release}
Requires:       perl-MythTV                     = %{version}-%{release}
%if ((0%{?fedora}) || (0%{?rhel} > 7))
Recommends:     libaacs
Recommends:     mesa-vdpau-drivers
%else
Requires:       libaacs
Requires:       mesa-vdpau-drivers
%endif
%if %{with qt6}
Requires:       qt6-qtwayland
%else
Requires:       qt5-qtwayland
%endif
%if ((0%{?fedora}) || (0%{?rhel} > 7))
Requires:       vulkan-loader
%endif

%description frontend
MythTV frontend, a graphical interface for recording and
viewing television, video, and music content.

################################################################################

%package backend
Summary:        Server component of mythtv (a DVR)

Requires:       mythtv-filesystem               = %{version}-%{release}
Requires:       mythtv-base%{?_isa}             = %{version}-%{release}
Requires:       mythtv-base-themes%{?_isa}      = %{version}-%{release}
Requires:       mythtv-libs%{?_isa}             = %{version}-%{release}
Requires:       mythtv-mythffmpeg%{?_isa}       = %{version}-%{release}
Requires:       %{py_prefix}-MythTV             = %{version}-%{release}
Requires:       perl-MythTV                     = %{version}-%{release}
Requires:       systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
%if ((0%{?fedora}) || (0%{?rhel} > 7))
Recommends:     xmltv-grabbers
%else
Requires:       xmltv-grabbers
%endif

%description backend
MythTV backend, the server for video capture and content services.

################################################################################

%package setup
Summary:        Program to setup the MythTV backend

Requires:       mythtv-filesystem               = %{version}-%{release}
Requires:       mythtv-base%{?_isa}             = %{version}-%{release}
Requires:       mythtv-base-themes%{?_isa}      = %{version}-%{release}
Requires:       mythtv-libs%{?_isa}             = %{version}-%{release}
%if ((0%{?fedora}) || (0%{?rhel} > 7))
Recommends:     xmltv
Recommends:     xmltv-grabbers
%else
Requires:       xmltv
Requires:       xmltv-grabbers
%endif
%if %{with qt6}
Requires:       qt6-qtwayland
%else
Requires:       qt5-qtwayland
%endif
%if ((0%{?fedora}) || (0%{?rhel} > 7))
Requires:       vulkan-loader
%endif

%description setup
MythTV provides a unified graphical interface for recording and viewing
television programs.  Refer to the mythtv package for more information.

This package contains only the setup software for configuring the
mythtv backend.

################################################################################

%package mythwelcome
Summary:        Program to shutdown and wakeup the MythTV backend

Requires:       mythtv-filesystem               = %{version}-%{release}
Requires:       mythtv-base%{?_isa}             = %{version}-%{release}
Requires:       mythtv-base-themes%{?_isa}      = %{version}-%{release}
Requires:       mythtv-libs%{?_isa}             = %{version}-%{release}
%if %{with qt6}
Requires:       qt6-qtwayland
%else
Requires:       qt5-qtwayland
%endif
%if ((0%{?fedora}) || (0%{?rhel} > 7))
Requires:       vulkan-loader
%endif

%description mythwelcome
MythTV provides a unified graphical interface for recording and viewing
television programs.  Refer to the mythtv package for more information.

This package contains only the mythwelcome software for
system shutdown and wakeup

################################################################################

%package mythshutdown
Summary:        Program to shutdown and wakeup the MythTV system

Requires:       mythtv-filesystem               = %{version}-%{release}
Requires:       mythtv-base%{?_isa}             = %{version}-%{release}
Requires:       mythtv-base-themes%{?_isa}      = %{version}-%{release}
Requires:       mythtv-libs%{?_isa}             = %{version}-%{release}

%description mythshutdown
MythTV provides a unified graphical interface for recording and viewing
television programs.  Refer to the mythtv package for more information.

This package contains only the mythshutdown software for
system shutdown and wakeup

################################################################################

%package base
Summary:        Common components needed by multiple other MythTV components

Requires(pre):  shadow-utils
Requires(pre):  grep
Requires:       mythtv-filesystem               = %{version}-%{release}
Requires:       logrotate
Requires:       google-droid-sans-mono-fonts
Requires:       google-droid-sans-fonts
Requires:       google-droid-serif-fonts
Requires:       perl(Date::Manip)
Requires:       perl(DateTime::Format::ISO8601)
Requires:       perl(Image::Size)
Requires:       perl(JSON)
Requires:       perl(LWP::Simple)
Requires:       perl(SOAP::Lite)
Requires:       perl(XML::Simple)
Requires:       perl(XML::XPath)

%description base
MythTV provides a unified graphical interface for recording and viewing
television programs.  Refer to the mythtv package for more information.

This package contains components needed by multiple other MythTV components.

################################################################################

%package mythffmpeg
Summary:        MythTV build of FFMpeg

Requires:       mythtv-mythffmpeg-libs%{?_isa}  = %{version}-%{release}

%description mythffmpeg
MythTV FFMpeg utilities.

################################################################################

%package mythffmpeg-libs
Summary:        Libraries for MythTV build of FFMpeg

%description mythffmpeg-libs
MythTV FFMpeg libraries

################################################################################

%package -n perl-MythTV
Summary:        Perl bindings for MythTV
BuildArch:      noarch

Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl(IO::Socket::INET6)
Requires:       perl(Config)
Requires:       perl(DBD::mysql)
Requires:       perl(Net::UPnP)
Requires:       perl(Net::UPnP::ControlPoint)
Requires:       perl(File::Copy)
Requires:       perl(Sys::Hostname)
Requires:       perl(DBI)
Requires:       perl(HTTP::Request)
Requires:       perl(POSIX)
Requires:       perl(LWP::UserAgent)
Requires:       perl(Fcntl)
Requires:       perl(Exporter)

%description -n perl-MythTV
MythTV perl bindings

################################################################################

%package -n php-MythTV
Summary:        PHP bindings for MythTV
BuildArch:      noarch

Requires:       mythtv-filesystem               = %{version}-%{release}
Requires:       php-common

%description -n php-MythTV
MythTV PHP bindings

################################################################################

%if ("%{py_prefix}" == "python3")
%package -n python3-MythTV
%else
%package -n python2-MythTV
%endif
Summary:        Python bindings for MythTV
BuildArch:      noarch

Requires:       %{py_prefix}-libs
Requires:       %{py_prefix}-lxml
Requires:       %{py_prefix}-future
%if ("%{py_prefix}" != "python3")
BuildRequires:  %{py_prefix}-urlgrabber
%endif
%if ((0%{?fedora}) || (0%{?rhel} > 7) || ((0%{?rhel} == 7) && ("%{py_prefix}" == "python")))
Requires:       %{py_prefix}-requests
%endif
%if ((0%{?rhel} == 7) && ("%{py_prefix}" == "python3"))
Requires:       python36-requests
%endif
%if ((0%{?fedora}) || (0%{?rhel} > 7) || ((0%{?rhel} == 7) && ("%{py_prefix}" == "python")))
Requires:       %{py_prefix}-simplejson
%endif
%if ((0%{?rhel} == 7) && ("%{py_prefix}" == "python3"))
Requires:       python36-simplejson
%endif
%if ((0%{?fedora}) || (0%{?rhel} > 7))
Requires:       %{py_prefix}-mysqlclient
%endif
%if ((0%{?rhel} == 7) && ("%{py_prefix}" == "python"))
Requires:       MySQL-python
%endif
%if ((0%{?rhel} == 7) && ("%{py_prefix}" == "python3"))
Requires:       python36-mysql
%endif
%if ((0%{?fedora}) || (0%{?rhel} > 7))
Requires:       %{py_prefix}-requests-cache
%endif

%if ("%{py_prefix}" == "python3")
Obsoletes:      python2-MythTV                  <= %{version}-%{release}
%endif

%if ("%{py_prefix}" == "python3")
%{?python_provide:%python_provide python3-MythTV}
%else
%{?python_provide:%python_provide python2-MythTV}
%endif

%if ("%{py_prefix}" == "python3")
%description -n python3-MythTV
%else
%description -n python2-MythTV
%endif
MythTV python bindings

################################################################################

%prep

%autosetup -p1 -n %{name}-%{commit}

%if ("%{py_prefix}" == "python3")
%if (0%{?rhel} == 7)
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" .
%else
%py3_shebang_fix .
%endif
%else
pathfix.py -pni "%{__python2} %{py2_shbang_opts}" .
%endif

################################################################################

%build

%if (0%{?rhel} == 7)
%if ("%{toolchain}" == "clang")
source scl_source enable llvm-toolset-7.0 >/dev/null 2>/dev/null && true || true
%else
source scl_source enable devtoolset-10 >/dev/null 2>/dev/null && true || true
%endif
%endif

pushd mythtv

    # Similar to 'percent' configure, but without {_target_platform} and
    # {_exec_prefix} etc... MythTV no longer accepts the parameters that the
    # configure macro passes, so we do this manually.

%if (0%{?rhel} == 7)
    CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS ;
    CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS ;
    FFLAGS="${FFLAGS:-%optflags -I%_fmoddir}" ; export FFLAGS ;
    FCFLAGS="${FCFLAGS:-%optflags -I%_fmoddir}" ; export FCFLAGS ;
    LDFLAGS="${LDFLAGS:-%__global_ldflags}"; export LDFLAGS ;
%else
    %{set_build_flags}
%endif

%if (%{with lto} && (((0%{?fedora}) && ((0%{?fedora}) < 33)) || ((0%{?rhel}) && ((0%{?rhel}) < 9))))
    #
    # Support LTO builds on el and older Fedora
    #
%if ("%{toolchain}" == "clang")
    CFLAGS="${CFLAGS} -flto" ; export CFLAGS ;
    CXXFLAGS="${CXXFLAGS} -flto" ; export CXXFLAGS;
    FFLAGS="${FFLAGS} -flto" ; export FFLAGS ;
    FCFLAGS="${FCFLAGS} -flto" ; export FCFLAGS ;
%else
    CFLAGS="${CFLAGS} -flto=auto -ffat-lto-objects" ; export CFLAGS ;
    CXXFLAGS="${CXXFLAGS} -flto=auto -ffat-lto-objects" ; export CXXFLAGS;
    FFLAGS="${FFLAGS} -flto=auto -ffat-lto-objects" ; export FFLAGS ;
    FCFLAGS="${FCFLAGS} -flto=auto -ffat-lto-objects" ; export FCFLAGS ;
%endif
%endif

%if ("%{toolchain}" == "gcc")
    #
    # gcc flag additions (equivalent to the llvm defaults)
    #
    CFLAGS="${CFLAGS} -fno-semantic-interposition" ; export CFLAGS ;
    CXXFLAGS="${CXXFLAGS} -fno-semantic-interposition" ; export CXXFLAGS;
    FFLAGS="${FFLAGS} -fno-semantic-interposition" ; export FFLAGS ;
    FCFLAGS="${FCFLAGS} -fno-semantic-interposition" ; export FCFLAGS ;
%endif

%if ("%{toolchain}" == "clang")
    #
    # llvm flag additions
    #
    LDFLAGS="${LDFLAGS} -fuse-ld=lld -Wl,--build-id=sha1" ; export LDFLAGS ;
%endif

%if %{with lto}
    #
    # Insure LDFLAGS have the correct CFLAGS
    # (the linker defaults to using flags from
    # the first object, which may, or may not,
    # include all the flags you want to be
    # invoked, so we make it explicit.)
    #
    LDFLAGS="${LDFLAGS} ${CFLAGS}"; export LDFLAGS;
%endif

%if (("%{toolchain}" == "clang") && (0%{?rhel} == 7))
    #
    # adjust flags for older llvm version in el7
    #
    CFLAGS="${CFLAGS//-fstack-clash-protection}" ; export CFLAGS ;
    CXXFLAGS="${CXXFLAGS//-fstack-clash-protection}" ; export CXXFLAGS ;
    FFLAGS="${FFLAGS//-fstack-clash-protection}" ; export FFLAGS ;
    FCFLAGS="${FCFLAGS//-fstack-clash-protection}" ; export FCFLAGS ;
    LDFLAGS="${LDFLAGS//-fstack-clash-protection}" ; export LDFLAGS ;
%endif

    ./configure                                     \
%if %{with qt6}
        --qmake="qmake6"                            \
%else
        --qmake="qmake-qt5"                         \
%endif
%if ("%{toolchain}" == "clang")
        --cc="clang"                                \
        --cxx="clang++"                             \
%if %{with lto}
        --enable-lto                                \
        --ar="llvm-ar"                              \
        --ranlib="llvm-ranlib"                      \
        --nm="llvm-nm -g"                           \
%endif
%else
        --cc="gcc"                                  \
        --cxx="g++"                                 \
%if %{with lto}
        --enable-lto                                \
        --ar="gcc-ar"                               \
        --ranlib="gcc-ranlib"                       \
        --nm="gcc-nm -g"                            \
%endif
%endif
        --extra-cflags="${CFLAGS}"                  \
        --extra-cxxflags="${CXXFLAGS}"              \
        --extra-ldflags="${LDFLAGS}"                \
        --prefix=%{_prefix}                         \
        --bindir=%{_bindir}                         \
        --libdir-name=%{_lib}                       \
        --compile-type=profile                      \
%if ("%{py_prefix}" == "python3")
        --python=%{__python3}                       \
%else
        --python=%{__python2}                       \
%endif
        --perl-config-opts="INSTALLDIRS=vendor"     \
        --enable-libmp3lame                         \
%if %{with rpmfusion}
        --enable-libx264                            \
        --enable-libx265                            \
        --enable-libxvid                            \
%endif
        --enable-libvpx

    %{make_build}

popd

################################################################################

%install

%if (0%{?rhel} == 7)
%if ("%{toolchain}" == "clang")
source scl_source enable llvm-toolset-7.0 >/dev/null 2>/dev/null && true || true
%else
source scl_source enable devtoolset-10 >/dev/null 2>/dev/null && true || true
%endif
%endif

pushd mythtv

    make install                          INSTALL_ROOT=%{buildroot}

    # log and rotate configuration
    mkdir -p                              %{buildroot}%{_localstatedir}/log/mythtv
    mkdir -p                              %{buildroot}%{_sysconfdir}/logrotate.d
    install -m 0644 %{SOURCE202}          %{buildroot}%{_sysconfdir}/logrotate.d/mythtv

    # Remove mythffserver (removed with v30 commit d24aa851 for FFmpeg 4.0 merge,
    # and deprecated in earlier FFmpeg variants, so do not package it in any case)
    rm -f                                 %{buildroot}%{_bindir}/mythffserver

    # Remove mythhdhomerun_config (removed with v30 commit 4b577277 and the upstream
    # hdhomerun_config binary is available as part of all current distros packages)
    rm -f                                 %{buildroot}%{_bindir}/mythhdhomerun_config

    # Add in a dummy mythexternrecorder if not built for an older mythtv
    # (mythexternrecorder added in v30 commit 826d57e3, and backported to
    # later fixes/29)
    if [ ! -e "%{buildroot}%{_bindir}/mythexternrecorder" ] ; then
    touch                                 %{buildroot}%{_bindir}/mythexternrecorder
    fi

    # Insure various files/directories exist for optional feature builds
    if [ ! -e "%{buildroot}%{_bindir}/mythwikiscripts" ] ; then
    touch                                 %{buildroot}%{_bindir}/mythwikiscripts
    fi
    if [ ! -e "%{buildroot}%{_bindir}/mythpython" ] ; then
    touch                                 %{buildroot}%{_bindir}/mythpython
    fi
    %if ("%{py_prefix}" == "python3")
    mkdir -p                              %{buildroot}%{python3_sitelib}/MythTV
    %else
    mkdir -p                              %{buildroot}%{python2_sitelib}/MythTV
    %endif
    mkdir -p                              %{buildroot}%{perl_vendorlib}/MythTV
    if [ ! -e "%{buildroot}%{perl_vendorlib}/MythTV.pm" ] ; then
    touch                                 %{buildroot}%{perl_vendorlib}/MythTV.pm
    fi
    mkdir -p                              %{buildroot}%{perl_vendorlib}/IO/Socket/INET
    if [ ! -e "%{buildroot}%{perl_vendorlib}/IO/Socket/INET/MythTV.pm" ] ; then
    touch                                 %{buildroot}%{perl_vendorlib}/IO/Socket/INET/MythTV.pm
    fi
    mkdir -p                              %{buildroot}%{_datadir}/mythtv/bindings/php
    mkdir -p                              %{buildroot}%{_datadir}/mythtv/hardwareprofile
    mkdir -p                              %{buildroot}%{_datadir}/mythtv/metadata
    mkdir -p                              %{buildroot}%{_datadir}/mythtv/internetcontent

    # Add in dummy filters directory if not installed as future merge
    # (from render branch) will be deleting filters directory
    mkdir -p                              %{buildroot}%{_libdir}/mythtv/filters

    # Add in dummy externrecorder if not installed
    mkdir -p                              %{buildroot}%{_datadir}/%{name}/externrecorder

    # dir for backend, and starter config.xml
    mkdir -p %{buildroot}%{_localstatedir}/lib/mythtv/.mythtv
    install -m 0644 contrib/config_files/config.xml \
                                          %{buildroot}%{_localstatedir}/lib/mythtv/.mythtv/config.xml

    # docs
    mkdir -p                              %{buildroot}%{_datadir}/doc/%{name}
    install -m 0644 README*               %{buildroot}%{_datadir}/doc/%{name}/
    if [ -e "../README.md" ] ; then
    install -m 0644 ../README.md          %{buildroot}%{_datadir}/doc/%{name}/
    fi
    if [ -e "UPGRADING" ] ; then
    install -m 0644 UPGRADING             %{buildroot}%{_datadir}/doc/%{name}/
    fi
    install -m 0644 AUTHORS               %{buildroot}%{_datadir}/doc/%{name}/
    if [ -e "COPYING" ] ; then
    install -m 0644 COPYING               %{buildroot}%{_datadir}/doc/%{name}/
    fi
    if [ -e "FAQ" ] ; then
    install -m 0644 FAQ                   %{buildroot}%{_datadir}/doc/%{name}/
    fi
    if [ -e "keys.txt" ] ; then
    install -m 0644 keys.txt              %{buildroot}%{_datadir}/doc/%{name}/
    fi
    if [ -e "keybindings.txt" ] ; then
    install -m 0644 keybindings.txt       %{buildroot}%{_datadir}/doc/%{name}/
    fi
    if [ -e "../LICENSE" ] ; then
    install -m 0644 ../LICENSE            %{buildroot}%{_datadir}/doc/%{name}/
    fi
    install -m 0644 %{SOURCE220}          %{buildroot}%{_datadir}/doc/%{name}/LICENSING
    if [ -e "data" ] ; then
    cp -r           data                  %{buildroot}%{_datadir}/doc/%{name}/
    fi
    cp -r           database              %{buildroot}%{_datadir}/doc/%{name}/
    cp -r           contrib               %{buildroot}%{_datadir}/doc/%{name}/
    # turn off execute bits for any docs (to keep build happy)
    find                                  %{buildroot}%{_datadir}/doc/%{name}/ \
                                          -type f -executable -exec chmod -x {} \;
    # tmpfiledir
    mkdir -p                              %{buildroot}%{_tmpfilesdir}
    install -m 0644 %{SOURCE210}          %{buildroot}%{_tmpfilesdir}/mythbackend.conf

    # systemd config
    mkdir -p -m 0755                      %{buildroot}%{_unitdir}
    install -m 0644 %{SOURCE200}          %{buildroot}%{_unitdir}/mythbackend.service
    install -m 0644 %{SOURCE203}          %{buildroot}%{_unitdir}/mythjobqueue.service
    install -m 0644 %{SOURCE204}          %{buildroot}%{_unitdir}/mythmediaserver.service

    # Install udev rules for devices that may initialize late in the boot
    # process so they are available for mythbackend.
    mkdir -p                              %{buildroot}%{_udevrulesdir}
    install -m 0644 %{SOURCE201}          %{buildroot}%{_udevrulesdir}/99-mythbackend.rules

    # devel
    mkdir -p                              %{buildroot}%{_datadir}/%{name}/build/
    install -m 0644 settings.pro          %{buildroot}%{_datadir}/%{name}/build/

    # Desktop entries
    mkdir -p                              %{buildroot}%{_datadir}/pixmaps
    mkdir -p                              %{buildroot}%{_datadir}/applications
    install -m 0644 %{SOURCE300}          %{buildroot}%{_datadir}/pixmaps/mythfrontend.png
    install -m 0644 %{SOURCE301}          %{buildroot}%{_datadir}/applications/mythfrontend.desktop
    desktop-file-validate                 %{buildroot}%{_datadir}/applications/mythfrontend.desktop
    install -m 0644 %{SOURCE302}          %{buildroot}%{_datadir}/pixmaps/mythtv-setup.png
    install -m 0644 %{SOURCE303}          %{buildroot}%{_datadir}/applications/mythtv-setup.desktop
    desktop-file-validate                 %{buildroot}%{_datadir}/applications/mythtv-setup.desktop

    # remove unnecessary packaging/SCM files
    find %{buildroot} -name .gitignore -delete >/dev/null
    find %{buildroot} -name .packlist -delete >/dev/null

    %{_fixperms} %{buildroot}

popd

################################################################################

%pre base
# Add the "mythtv" user, with membership in the audio and video group
getent group mythtv >/dev/null || groupadd -r mythtv
getent passwd mythtv >/dev/null || \
    useradd -r -g mythtv \
    -d "/var/lib/mythtv" -s /bin/sh \
    -c "mythbackend user" mythtv
for group in 'video' 'audio' 'cdrom' 'dialout' 'render'
{
    ent=`getent group $group 2>/dev/null`
    # only proceed if the group exists
    if [ $? -eq 0 ]; then
        cnt=`echo "$ent" | cut -d: -f4 | tr ',' '\n' | grep -c '^mythtv$'`
        cnt=$(($cnt + 0))
        if [ $cnt -lt 1 ]; then
            usermod -a -G $group mythtv
        fi
    fi
}
exit 0

%if (0%{?rhel} == 7)
%post libs -p /sbin/ldconfig
%endif

%if (0%{?rhel} == 7)
%post mythffmpeg-libs -p /sbin/ldconfig
%endif

%post backend
    %systemd_post mythbackend.service
    %systemd_post mythjobqueue.service
    %systemd_post mythmediaserver.service

%preun backend
    %systemd_preun mythbackend.service
    %systemd_preun mythjobqueue.service
    %systemd_preun mythmediaserver.service

%if (0%{?rhel} == 7)
%postun libs -p /sbin/ldconfig
%endif

%if (0%{?rhel} == 7)
%postun mythffmpeg-libs -p /sbin/ldconfig
%endif

%postun backend
    %systemd_postun_with_restart mythbackend.service
    %systemd_postun_with_restart mythjobqueue.service
    %systemd_postun_with_restart mythmediaserver.service

################################################################################


%files
%defattr(0644, root, root, 0755)


%files docs
%defattr(0644, root, root, 0755)
%{_datadir}/doc/%{name}


%files devel
%defattr(0644, root, root, 0755)
%{_libdir}/libmyth*.so
%{_includedir}/%{name}
%{_datadir}/mythtv/build


%files base
%defattr(0644, root, root, 0755)
%{_datadir}/mythtv/locales
%{_datadir}/mythtv/hardwareprofile
%{_datadir}/mythtv/i18n
%{_datadir}/mythtv/fonts
%defattr(-, root, root, 0755)
%{_datadir}/mythtv/metadata
%defattr(0644, root, root, 0755)
%config(noreplace) %{_sysconfdir}/logrotate.d/mythtv
%attr(0755, mythtv, mythtv) %dir %{_localstatedir}/log/mythtv
%defattr(0755, root, root, 0755)
%{_bindir}/mythccextractor
%{_bindir}/mythcommflag
%{_bindir}/mythpreviewgen
%{_bindir}/mythtranscode
%{_bindir}/mythmetadatalookup
%{_bindir}/mythutil
%{_datadir}/mythtv/mythconverg*.pl
%attr(0755, mythtv, mythtv) %dir %{_localstatedir}/lib/mythtv
%attr(0755, mythtv, mythtv) %dir %{_localstatedir}/lib/mythtv/.mythtv
%attr(0644, mythtv, mythtv) %config(noreplace) %{_localstatedir}/lib/mythtv/.mythtv/config.xml


%files filesystem
%defattr(0644, root, root, 0755)
%dir %{_datadir}/mythtv
%dir %{_datadir}/mythtv/bindings


%files libs
%defattr(0755, root, root, 0755)
%{_libdir}/libmyth*.so.*
%exclude %{_libdir}/libmythavdevice.*
%exclude %{_libdir}/libmythavfilter.*
%exclude %{_libdir}/libmythavformat.*
%exclude %{_libdir}/libmythavcodec.*
%exclude %{_libdir}/libmythpostproc.*
%exclude %{_libdir}/libmythswresample.*
%exclude %{_libdir}/libmythswscale.*
%exclude %{_libdir}/libmythavutil.*
%{_libdir}/mythtv/filters
%defattr(0644, root, root, 0755)
%{_datadir}/mythtv/MXML_scpd.xml
%{_datadir}/mythtv/CDS_scpd.xml
%{_datadir}/mythtv/CMGR_scpd.xml
%{_datadir}/mythtv/MSRR_scpd.xml


%files backend
%defattr(0755, root, root, 0755)
%{_bindir}/mythbackend
%{_bindir}/mythexternrecorder
%{_bindir}/mythfilldatabase
%{_bindir}/mythfilerecorder
%{_bindir}/mythjobqueue
%{_bindir}/mythmediaserver
%{_bindir}/mythreplex
%defattr(0644, root, root, 0755)
%{_datadir}/mythtv/backend-config/
%{_unitdir}/mythbackend.service
%{_unitdir}/mythjobqueue.service
%{_unitdir}/mythmediaserver.service
%{_udevrulesdir}/99-mythbackend.rules
%{_datadir}/mythtv/internetcontent
%{_datadir}/mythtv/html
%{_datadir}/mythtv/externrecorder
%{_tmpfilesdir}/*
%{_datadir}/mythtv/devicemaster.xml
%{_datadir}/mythtv/deviceslave.xml


%files setup
%defattr(0755, root, root, 0755)
%{_bindir}/mythtv-setup
%defattr(0644, root, root, 0755)
%{_datadir}/mythtv/setup.xml
%{_datadir}/pixmaps/mythtv-setup.png
%{_datadir}/applications/mythtv-setup.desktop


%files frontend
%defattr(0755, root, root, 0755)
%{_bindir}/mythavtest
%{_bindir}/mythfrontend
%{_bindir}/mythlcdserver
%{_bindir}/mythscreenwizard
%defattr(0644, root, root, 0755)
%{_datadir}/mythtv/MFEXML_scpd.xml
%{_datadir}/pixmaps/mythfrontend.png
%{_datadir}/applications/mythfrontend.desktop


%files mythshutdown
%defattr(0755, root, root, 0755)
%{_bindir}/mythshutdown


%files mythwelcome
%defattr(0755, root, root, 0755)
%{_bindir}/mythwelcome


%files base-themes
%defattr(0644, root, root, 0755)
%{_datadir}/mythtv/themes


%files mythffmpeg
%defattr(0755, root, root, 0755)
%attr(0755, root, root) %{_bindir}/mythffmpeg
%attr(0755, root, root) %{_bindir}/mythffprobe


%files mythffmpeg-libs
%defattr(0755, root, root, 0755)
%{_libdir}/libmythavdevice.so.*
%{_libdir}/libmythavfilter.so.*
%{_libdir}/libmythavformat.so.*
%{_libdir}/libmythavcodec.so.*
%{_libdir}/libmythpostproc.so.*
%{_libdir}/libmythswresample.so.*
%{_libdir}/libmythswscale.so.*
%{_libdir}/libmythavutil.so.*


%files -n perl-MythTV
%defattr(0644, root, root, 0755)
%{perl_vendorlib}/MythTV
%{perl_vendorlib}/MythTV.pm
%{perl_vendorlib}/IO/Socket/INET/MythTV.pm


%files -n php-MythTV
%defattr(0644, root, root, 0755)
%{_datadir}/mythtv/bindings/php


%if ("%{py_prefix}" == "python3")
%files -n python3-MythTV
%else
%files -n python2-MythTV
%endif
%defattr(0644, root, root, 0755)
%attr(0755, root, root) %{_bindir}/mythpython
%attr(0755, root, root) %{_bindir}/mythwikiscripts
%if ("%{py_prefix}" == "python3")
%{python3_sitelib}/*
%else
%{python2_sitelib}/*
%endif


################################################################################


%changelog

* Wed May 09 2018 Gary Buhrmaster <gary.buhrmaster@gmail.com>
- Rework for managed rebuilds

