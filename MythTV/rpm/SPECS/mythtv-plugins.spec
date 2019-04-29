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
BuildRequires:  python-MythTV             = %{version}-%{release}
BuildRequires:  git
BuildRequires:  perl-generators
BuildRequires:  gcc-c++
BuildRequires:  gcc
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtscript-devel
BuildRequires:  qt5-qtwebkit-devel
BuildRequires:  freetype-devel
BuildRequires:  mariadb-devel
BuildRequires:  perl(XML::Simple)
BuildRequires:  perl(DateTime::Format::ISO8601)
BuildRequires:  perl(XML::XPath)
BuildRequires:  perl(Date::Manip)
BuildRequires:  perl(Image::Size)
BuildRequires:  perl(SOAP::Lite)
BuildRequires:  perl(JSON)
BuildRequires:  python
BuildRequires:  python-pycurl
BuildRequires:  python-lxml
BuildRequires:  python-oauth
BuildRequires:  libvorbis-devel
BuildRequires:  flac-devel
BuildRequires:  lame-devel
BuildRequires:  libexif-devel
BuildRequires:  zlib-devel
BuildRequires:  ncurses-devel
BuildRequires:  libcdio-paranoia-devel
BuildRequires:  fftw-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  avahi-compat-libdns_sd-devel
BuildRequires:  jack-audio-connection-kit-devel
BuildRequires:  libass-devel
BuildRequires:  libavc1394-devel
BuildRequires:  libcrystalhd-devel
%if 0%{?fedora}
BuildRequires:  libomxil-bellagio-devel
%endif
BuildRequires:  libiec61883-devel
BuildRequires:  libogg-devel
BuildRequires:  libraw1394-devel
BuildRequires:  libtheora-devel
BuildRequires:  libva-devel
BuildRequires:  libvdpau-devel
BuildRequires:  libvpx-devel
BuildRequires:  libXinerama-devel
BuildRequires:  libxml2-devel
BuildRequires:  libXrandr-devel
BuildRequires:  libXv-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  systemd-devel
BuildRequires:  x264-devel
BuildRequires:  x265-devel
BuildRequires:  xvidcore-devel
BuildRequires:  nv-codec-headers
BuildRequires:  xz-devel
BuildRequires:  SDL2-devel
BuildRequires:  taglib-devel
BuildRequires:  dcraw
BuildRequires:  hdhomerun-devel
BuildRequires:  libbluray-devel
BuildRequires:  libsamplerate-devel
BuildRequires:  libXNVCtrl-devel
BuildRequires:  lzo-devel
BuildRequires:  minizip-devel

%if 0%{?fedora}
BuildRequires:  python2-devel
%else
BuildRequires:  python-devel
%endif

# python fixups
BuildRequires:  /usr/bin/pathfix.py

################################################################################

# Package for all (buildable) MythTV plugins

Requires(pre):  mythtv-filesystem       = %{version}-%{release}
Requires(pre):  mythtv-base             = %{version}-%{release}
Requires(pre):  mythtv-libs             = %{version}-%{release}
Requires(pre):  mythtv-base-themes      = %{version}-%{release}
Requires:       mythtv-frontend         = %{version}-%{release}
Requires:       python-MythTV           = %{version}-%{release}
Requires:       cdrecord
Requires:       dvd+rw-tools
Requires:       dvdauthor
Requires:       mjpegtools
Requires:       mkisofs
Requires:       pmount
Requires:       perl(XML::Simple)
Requires:       perl(DateTime::Format::ISO8601)
Requires:       perl(XML::XPath)
Requires:       perl(Date::Manip)
Requires:       perl(Image::Size)
Requires:       perl(SOAP::Lite)
Requires:       perl(JSON)
Requires:       perl(XML::SAX::Base)
Requires:       python-pycurl
Requires:       python-lxml
Requires:       python-oauth
Requires:       python-imaging
Requires:       dcraw

################################################################################

%description
This is a consolidation of all the official MythTV plugins that used to be
distributed as separate downloads from mythtv.org.

################################################################################

%prep

%setup -q -n mythtv-%{commit}

pathfix.py -pni "%{__python2} %{py2_shbang_opts}" .

################################################################################

%build

pushd mythplugins

    # Similar to 'percent' configure, but without {_target_platform} and
    # {_exec_prefix} etc... MythTV no longer accepts the parameters that the
    # configure macro passes, so we do this manually.

    CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS ; \
    CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS ; \

    ./configure \
        --extra-cflags="${CFLAGS}"                  \
        --extra-cxxflags="${CXXFLAGS}"              \
        --prefix=%{_prefix}                         \
        --bindir=%{_bindir}                         \
        --python=/usr/bin/python2                   \
        --compile-type=profile

    make %{?_smp_mflags}

popd

################################################################################

%install

pushd mythplugins

    make install INSTALL_ROOT=%{buildroot}

popd

################################################################################

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

################################################################################

%files
%defattr(0644, root, root, 0755)

%attr(0755, root, root)%{_bindir}/*
%dir %{_libdir}/mythtv/plugins
%attr(0755, root, root)%{_libdir}/mythtv/plugins/*
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

* Wed May 09 2018 Gary Buhrmaster <gary.buhrmaster@gmail.com> - 29.0
- Rework for managed rebuilds


