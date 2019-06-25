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

################################################################################

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

# For el7, include software collections to get gcc 8
%if (0%{?rhel} == 7)
BuildRequires:  devtoolset-8
%endif

# Global MythTV and Shared Build Requirements

BuildRequires:  git
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  gcc-c++
BuildRequires:  gcc
BuildRequires:  desktop-file-utils
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtscript-devel
BuildRequires:  qt5-qtwebkit-devel
BuildRequires:  freetype-devel
BuildRequires:  mariadb-devel
BuildRequires:  libcec-devel
BuildRequires:  libvpx-devel
BuildRequires:  lm_sensors-devel
BuildRequires:  lirc-devel
BuildRequires:  nasm, yasm-devel

# X, and Xv video support
BuildRequires:  libXmu-devel
BuildRequires:  libXv-devel
BuildRequires:  libXvMC-devel
BuildRequires:  libXxf86vm-devel
BuildRequires:  libXinerama-devel
BuildRequires:  libXrandr-devel
BuildRequires:  mesa-libGLU-devel
%ifarch %arm
BuildRequires:  mesa-libGLES-devel
%endif
BuildRequires:  xorg-x11-proto-devel

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
BuildRequires:  x264-devel
BuildRequires:  x265-devel
BuildRequires:  xvidcore-devel
BuildRequires:  exiv2-devel
BuildRequires:  nv-codec-headers
# (non-free) BuildRequires:  fdk-aac-devel

# External library support
BuildRequires:  hdhomerun-devel
BuildRequires:  libbluray-devel
BuildRequires:  libsamplerate-devel
BuildRequires:  libXNVCtrl-devel
BuildRequires:  lzo-devel
BuildRequires:  minizip-devel

# Audio framework support
BuildRequires:  sox-devel
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
BuildRequires:  libcrystalhd-devel
%if 0%{?fedora}
BuildRequires:  libomxil-bellagio-devel
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

%if 0%{?fedora}
BuildRequires:  python2-devel
BuildRequires:  python2-mysql
BuildRequires:  python2-urlgrabber
BuildRequires:  python2-lxml
%else
BuildRequires:  python-devel
BuildRequires:  MySQL-python
BuildRequires:  python-urlgrabber
BuildRequires:  python-lxml
%endif

# python fixups
BuildRequires:  /usr/bin/pathfix.py



################################################################################
# Requirements for the mythtv meta package

Requires:       mythtv-base             = %{version}-%{release}
Requires:       mythtv-backend          = %{version}-%{release}
Requires:       mythtv-base-themes      = %{version}-%{release}
Requires:       mythtv-docs             = %{version}-%{release}
Requires:       mythtv-frontend         = %{version}-%{release}
Requires:       mythtv-setup            = %{version}-%{release}
Requires:       mythtv-mythwelcome      = %{version}-%{release}
Requires:       mythtv-mythshutdown     = %{version}-%{release}
Requires:       perl-MythTV             = %{version}-%{release}
Requires:       php-MythTV              = %{version}-%{release}
Requires:       python-MythTV           = %{version}-%{release}
Requires:       mythtv-mythffmpeg       = %{version}-%{release}
Requires:       mariadb
%if 0%{?fedora} || 0%{?rhel} > 7
Recommends:     xmltv
%endif

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

Requires(pre):  mythtv-filesystem       = %{version}-%{release}

%description docs
MythTV documentation

################################################################################

%package devel
Summary:        Development files for mythtv
BuildArch:      noarch

Requires(pre):  mythtv-filesystem       = %{version}-%{release}
Requires:       mythtv-libs             = %{version}-%{release}
Requires:       qt5-qtbase-devel        >= 5.2
Requires:       qt5-qtscript-devel      >= 5.2
Requires:       qt5-qtwebkit-devel      >= 5.2

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

Requires:       mythtv-mythffmpeg-libs  = %{version}-%{release}
Requires:       qt5-qtbase-mysql

%description libs
MythTV run-time libraries

################################################################################

%package base-themes
Summary:        Core user interface themes for mythtv

Requires(pre):  mythtv-filesystem       = %{version}-%{release}

%description base-themes
MythTV base themes for graphical applications

################################################################################

%package frontend
Summary:        Client component of mythtv (a DVR)

Requires(pre):  mythtv-filesystem       = %{version}-%{release}
Requires:       mythtv-base             = %{version}-%{release}
Requires:       mythtv-base-themes      = %{version}-%{release}
Requires:       mythtv-libs             = %{version}-%{release}
Requires:       python-MythTV           = %{version}-%{release}
Requires:       perl-MythTV             = %{version}-%{release}

%description frontend
MythTV frontend, a graphical interface for recording and
viewing television, video, and music content.

################################################################################

%package backend
Summary:        Server component of mythtv (a DVR)

Requires:       mythtv-base             = %{version}-%{release}
Requires:       mythtv-base-themes      = %{version}-%{release}
Requires:       mythtv-libs             = %{version}-%{release}
Requires:       mythtv-mythffmpeg       = %{version}-%{release}
Requires:       python-MythTV           = %{version}-%{release}
Requires:       perl-MythTV             = %{version}-%{release}
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
%{?fedora:Recommends:  xmltv-grabbers}

%description backend
MythTV backend, the server for video capture and content services.

################################################################################

%package setup
Summary:        Program to setup the MythTV backend

Requires:       mythtv-base             = %{version}-%{release}
Requires:       mythtv-base-themes      = %{version}-%{release}
Requires:       mythtv-libs             = %{version}-%{release}

%description setup
MythTV provides a unified graphical interface for recording and viewing
television programs.  Refer to the mythtv package for more information.

This package contains only the setup software for configuring the
mythtv backend.

################################################################################

%package mythwelcome
Summary:        Program to shutdown and wakeup the MythTV backend

Requires:       mythtv-base             = %{version}-%{release}
Requires:       mythtv-base-themes      = %{version}-%{release}
Requires:       mythtv-libs             = %{version}-%{release}

%description mythwelcome
MythTV provides a unified graphical interface for recording and viewing
television programs.  Refer to the mythtv package for more information.

This package contains only the mythwelcome software for
system shutdown and wakeup

################################################################################

%package mythshutdown
Summary:        Program to shutdown and wakeup the MythTV system

Requires:       mythtv-base             = %{version}-%{release}
Requires:       mythtv-base-themes      = %{version}-%{release}
Requires:       mythtv-libs             = %{version}-%{release}

%description mythshutdown
MythTV provides a unified graphical interface for recording and viewing
television programs.  Refer to the mythtv package for more information.

This package contains only the mythshutdown software for
system shutdown and wakeup

################################################################################

%package base
Summary:        Common components needed by multiple other MythTV components

Requires(pre):  shadow-utils
Requires(pre):  mythtv-filesystem       = %{version}-%{release}
Requires:       google-droid-sans-mono-fonts
Requires:       google-droid-sans-fonts
Requires:       perl(Date::Manip)
Requires:       perl(DateTime::Format::ISO8601)
Requires:       perl(Image::Size)
Requires:       perl(JSON)
Requires:       perl(LWP::Simple)
Requires:       perl(SOAP::Lite)
Requires:       perl(XML::Simple)
Requires:       perl(XML::XPath)
%if 0%{?fedora}
Requires:       python2-future
Requires:       python2-requests
Requires:       python2-requests-cache
%else
Requires:       python-future
Requires:       python-requests
Requires:       python-requests-cache
%endif


%description base
MythTV provides a unified graphical interface for recording and viewing
television programs.  Refer to the mythtv package for more information.

This package contains components needed by multiple other MythTV components.

################################################################################

%package mythffmpeg
Summary:        MythTV build of FFMpeg

Requires:       mythtv-mythffmpeg-libs  = %{version}-%{release}

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

Requires(pre):  mythtv-filesystem       = %{version}-%{release}
Requires:       php-common

%description -n php-MythTV
MythTV PHP bindings

################################################################################

%package -n python2-MythTV
Summary:        Python bindings for MythTV
BuildArch:      noarch

%if 0%{?fedora}
Requires(pre):  python2-libs
Requires:       python2-mysql
Requires:       python2-lxml
Requires:       python2-future
Requires:       python2-urlgrabber
%else
Requires(pre):  python-libs
Requires:       MySQL-python
Requires:       python-lxml
Requires:       python-future
Requires:       python-urlgrabber
%endif

%{?python_provide:%python_provide python2-MythTV}

%description -n python2-MythTV
MythTV python bindings

################################################################################

%prep

%autosetup -p1 -n %{name}-%{commit}

pathfix.py -pni "%{__python2} %{py2_shbang_opts}" .

################################################################################

%build

%if (0%{?rhel} == 7)
source scl_source enable devtoolset-8 >/dev/null 2>/dev/null && true || true
%endif

pushd mythtv

    # Similar to 'percent' configure, but without {_target_platform} and
    # {_exec_prefix} etc... MythTV no longer accepts the parameters that the
    # configure macro passes, so we do this manually.

    CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS ; \
    CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS ; \

    ./configure                                     \
        --extra-cflags="${CFLAGS}"                  \
        --extra-cxxflags="${CXXFLAGS}"              \
        --prefix=%{_prefix}                         \
        --bindir=%{_bindir}                         \
        --libdir-name=%{_lib}                       \
        --compile-type=profile                      \
        --python=/usr/bin/python2                   \
        --perl-config-opts="INSTALLDIRS=vendor OPTIMIZE=\"$RPM_OPT_FLAGS\"" \
        --enable-libmp3lame                         \
        --enable-libx264                            \
        --enable-libx265                            \
        --enable-libxvid                            \
        --enable-libvpx

    make %{?_smp_mflags}

popd

################################################################################

%install

%if (0%{?rhel} == 7)
source scl_source enable devtoolset-8 >/dev/null 2>/dev/null && true || true
%endif

pushd mythtv

    make install                          INSTALL_ROOT=%{buildroot} -j 1

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
    install -m 0644 UPGRADING             %{buildroot}%{_datadir}/doc/%{name}/
    install -m 0644 AUTHORS               %{buildroot}%{_datadir}/doc/%{name}/
    install -m 0644 COPYING               %{buildroot}%{_datadir}/doc/%{name}/
    install -m 0644 FAQ                   %{buildroot}%{_datadir}/doc/%{name}/
    install -m 0644 keys.txt              %{buildroot}%{_datadir}/doc/%{name}/
    install -m 0644 %{SOURCE220}          %{buildroot}%{_datadir}/doc/%{name}/LICENSING
    cp -r           data                  %{buildroot}%{_datadir}/doc/%{name}/
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
    install -m 0644 %{SOURCE302}          %{buildroot}%{_datadir}/pixmaps/mythtv-setup.png
    install -m 0644 %{SOURCE303}          %{buildroot}%{_datadir}/applications/mythtv-setup.desktop

popd

################################################################################

%pre base
# Add the "mythtv" user, with membership in the audio and video group
getent group mythtv >/dev/null || groupadd -r mythtv
getent passwd mythtv >/dev/null || \
    useradd -r -g mythtv \
    -d "/var/lib/mythtv" -s /bin/sh \
    -c "mythbackend user" mythtv
for group in 'video' 'audio' 'cdrom' 'dialout'
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

%post libs -p /sbin/ldconfig

%post mythffmpeg-libs -p /sbin/ldconfig

%post backend
    %systemd_post mythbackend.service
    %systemd_post mythjobqueue.service
    %systemd_post mythmediaserver.service

%preun backend
    %systemd_preun mythbackend.service
    %systemd_preun mythjobqueue.service
    %systemd_preun mythmediaserver.service

%postun libs -p /sbin/ldconfig

%postun mythffmpeg-libs -p /sbin/ldconfig

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
%{_bindir}/mythwikiscripts
%{_bindir}/mythmetadatalookup
%{_bindir}/mythutil
%{_datadir}/mythtv/mythconverg*.pl
%attr(0755, mythtv, mythtv) %dir %{_localstatedir}/lib/mythtv
%attr(0755, mythtv, mythtv) %dir %{_localstatedir}/lib/mythtv/.mythtv
%attr(0644, mythtv, mythtv) %config(noreplace) %{_localstatedir}/lib/mythtv/.mythtv/config.xml


%files filesystem
%defattr(0644, root, root, 0755)
%dir %{_datadir}/mythtv


%files libs
%defattr(0755, root, root, 0755)
%{_libdir}/libmyth*
%exclude %{_libdir}/libmythavdevice.*
%exclude %{_libdir}/libmythavfilter.*
%exclude %{_libdir}/libmythavformat.*
%exclude %{_libdir}/libmythavcodec.*
%exclude %{_libdir}/libmythpostproc.*
%exclude %{_libdir}/libmythswresample.*
%exclude %{_libdir}/libmythswscale.*
%exclude %{_libdir}/libmythavutil.*
%{_libdir}/mythtv/filters


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
%{_datadir}/mythtv/MXML_scpd.xml
%{_datadir}/mythtv/backend-config/
%{_unitdir}/mythbackend.service
%{_unitdir}/mythjobqueue.service
%{_unitdir}/mythmediaserver.service
%{_udevrulesdir}/99-mythbackend.rules
%{_datadir}/mythtv/internetcontent
%{_datadir}/mythtv/html
%{_datadir}/mythtv/externrecorder
%{_tmpfilesdir}/*


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
%{_datadir}/mythtv/CDS_scpd.xml
%{_datadir}/mythtv/CMGR_scpd.xml
%{_datadir}/mythtv/MFEXML_scpd.xml
%{_datadir}/mythtv/MSRR_scpd.xml
%{_datadir}/mythtv/devicemaster.xml
%{_datadir}/mythtv/deviceslave.xml
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
%{_libdir}/libmythavdevice.*
%{_libdir}/libmythavfilter.*
%{_libdir}/libmythavformat.*
%{_libdir}/libmythavcodec.*
%{_libdir}/libmythpostproc.*
%{_libdir}/libmythswresample.*
%{_libdir}/libmythswscale.*
%{_libdir}/libmythavutil.*


%files -n perl-MythTV
%defattr(0644, root, root, 0755)
%{perl_vendorlib}/MythTV.pm
%dir %{perl_vendorlib}/MythTV
%{perl_vendorlib}/MythTV/*.pm
%{perl_vendorlib}/IO/Socket/INET/MythTV.pm
%exclude %{perl_vendorarch}/auto/MythTV/.packlist


%files -n php-MythTV
%defattr(0644, root, root, 0755)
%{_datadir}/mythtv/bindings


%files -n python2-MythTV
%defattr(0644, root, root, 0755)
%attr(0755, root, root) %{_bindir}/mythpython
%{python2_sitelib}/*


################################################################################


%changelog

* Wed May 09 2018 Gary Buhrmaster <gary.buhrmaster@gmail.com> - 29.0
- Rework for managed rebuilds

