#
# spec file for package hdhomerun_record
#

%define		debug_package %{nil}

%define		__os_install_post /usr/lib/rpm/brp-compress %{nil}

# Determine if we are attempting a cross build
%define		cross_build 1
%if "%{_host_cpu}" == "%{_target_cpu}"
	%define	cross_build 0
%else
	%if "%{_host_cpu}" == "x86_64"
		%ifarch %{ix86} x86_64
			%define cross_build 0
		%endif
	%else
		%if "%{_host_cpu}" == "aarch64"
			%ifarch %{arm} aarch64
				%define cross_build 0
			%endif
		%else
			%if "%{_host_cpu}" == "ppc64"
				%ifarch ppc64 ppc
					%define cross_build 0
				%endif
			%endif
		%endif
	%endif
%endif

Name:		hdhomerun-record
Version:	0.0.%{?HDHRDVR_VERSION}%{!?HDHRDVR_VERSION:0}
Release:	1%{?dist}
Group:		Applications/Internet
Summary:	SiliconDust HDHomeRun DVR server
Vendor:		SiliconDust USA Inc.
License:	Proprietary
URL:		https://www.silicondust.com/

Source0:	https://download.silicondust.com/hdhomerun/hdhomerun_record_linux%{?HDHRDVR_VERSION:_%{HDHRDVR_VERSION}}
Source51:	hdhomerun_record-tmpfiles.conf
Source52:	hdhomerun_record.service
Source53:	hdhomerun_record.init
Source54:	hdhomerun.conf
Source55:	hdhomerun_record.xml
Source56:	hdhomerun_record.sysconfig
Source60:	hdhomerun_record.8
Source61:	hdhomerun.conf.5
Source70:	hdhomerun_record-doc.README
Source71:	hdhomerun_record-doc.LICENSE
Source72:	hdhomerun_record-doc.README.init

%if 0%{?rhel} == 6
BuildRequires:	coreutils
BuildRequires:	tar
Requires(pre):	initscripts
Requires(pre):	chkconfig
Requires(pre):	shadow-utils
Requires(pre):	glibc-common
Requires(post):	initscripts
Requires(post):	chkconfig
Requires(preun):	initscripts
Requires(preun):	chkconfig
Requires(postun):	initscripts
%if 0%{?cross_build}
%ifarch %{arm} aarch64
BuildRequires: binutils-aarch64-linux-gnu
%endif
%ifarch %{ix86} x86_64
BuildRequires: binutils-x86_64-linux-gnu
%endif
%ifarch ppc64 ppc
BuildRequires: binutils-powerpc64-linux-gnu
%endif
%endif
%else
%if 0%{?suse_version}
BuildRequires:	coreutils
BuildRequires:	tar
BuildRequires:	systemd-rpm-macros
Requires(pre):	shadow
Requires(pre):	glibc
%{?systemd_requires}
%if 0%{?cross_build}
%ifarch %{arm} aarch64
BuildRequires: cross-aarch64-binutils
%endif
%ifarch %{ix86} x86_64
BuildRequires: cross-x86_64-binutils
%endif
%ifarch ppc64 ppc
BuildRequires: cross-powerpc64-binutils
%endif
%endif
%else
%if 0%{?mageia_version}
BuildRequires:	coreutils
BuildRequires:	tar
BuildRequires:	firewalld-filesystem
Requires:	systemd
Requires:	firewalld-filesystem
Requires(pre):	rpm-helper
Requires(pre):	shadow-utils
Requires(pre):	glibc
Requires(pre):	systemd
Requires(post):	rpm-helper
Requires(post):	systemd
Requires(preun):	rpm-helper
Requires(preun):	systemd
Requires(postun):	rpm-helper
Requires(postun):	systemd
%if 0%{?cross_build}
%ifarch %{arm} aarch64
BuildRequires:	binutils-aarch64-linux-gnu
%endif
%ifarch %{ix86} x86_64
BuildRequires:	binutils-x86_64-linux-gnu
%endif
%ifarch ppc64 ppc
BuildRequires:	binutils-powerpc64-linux-gnu
%endif
%endif
%else
BuildRequires:	coreutils
BuildRequires:	tar
BuildRequires:	systemd
BuildRequires:	firewalld-filesystem
Requires:	systemd
Requires:	firewalld-filesystem
Requires(pre):	shadow-utils
Requires(pre):	glibc-common
Requires(pre):	systemd
Requires(pre):	firewalld-filesystem
Requires(post):	systemd
Requires(preun):	systemd
Requires(postun):	systemd
Requires(postun):	firewalld-filesystem
%if 0%{?cross_build}
%ifarch %{arm} aarch64
BuildRequires: binutils-aarch64-linux-gnu
%endif
%ifarch %{ix86} x86_64
BuildRequires: binutils-x86_64-linux-gnu
%endif
%ifarch ppc64 ppc
BuildRequires: binutils-powerpc64-linux-gnu
%endif
%endif
%endif
%endif
%endif
Requires(post):	util-linux
Requires(post):	coreutils


%description
This package provides the SiliconDust HDHomeRun DVR recorder service.


%prep
%setup -q -c -T

dd if=%{SOURCE0} bs=4096 skip=1 2>/dev/null | tar -xvz


%build

# Nothing to build
echo "Nothing to build"


%install

%if 0%{?rhel} == 6
# No automated tmpfiles - in init script
%else
install -D -m 0644 %{SOURCE51} %{buildroot}%{_tmpfilesdir}/hdhomerun_record.conf
%endif

%if 0%{?rhel} == 6
install -D -m 0644 %{SOURCE53} %{buildroot}%{_initddir}/hdhomerun_record
install -D -m 0644 %{SOURCE56} %{buildroot}%{_sysconfdir}/sysconfig/hdhomerun_record
%else
install -D -m 0644 %{SOURCE52} %{buildroot}%{_unitdir}/hdhomerun_record.service
%endif

install -D -m 0644 %{SOURCE54} %{buildroot}%{_sysconfdir}/hdhomerun.conf

%if 0%{?rhel} == 6
# No firewalld in rhel6
%else
install -D -m 0644 %{SOURCE55} %{buildroot}%{_prefix}/lib/firewalld/services/hdhomerun_record.xml
%endif

mkdir -p %{buildroot}%{_localstatedir}/run/hdhomerun

install -D -m 0644 %{SOURCE60} %{buildroot}%{_mandir}/man8/hdhomerun_record.8

install -D -m 0644 %{SOURCE61} %{buildroot}%{_mandir}/man5/hdhomerun.conf.5

%if 0%{?rhel} == 6
install -D -m 0644 %{SOURCE72} %{buildroot}%{_datadir}/doc/hdhomerun_record/README
%else
install -D -m 0644 %{SOURCE70} %{buildroot}%{_datadir}/doc/hdhomerun_record/README
%endif
install -D -m 0644 %{SOURCE71} %{buildroot}%{_datadir}/doc/hdhomerun_record/LICENSE

%ifarch %{ix86}
install -D -m 0755 hdhomerun_record_x86 %{buildroot}%{_bindir}/hdhomerun_record
%if !0%{?cross_build}
strip --strip-unneeded %{buildroot}%{_bindir}/hdhomerun_record
%else
%if 0%{?suse_version}
x86_64-suse-linux-strip --strip-unneeded %{buildroot}%{_bindir}/hdhomerun_record
%else
x86_64-linux-gnu-strip --strip-unneeded %{buildroot}%{_bindir}/hdhomerun_record
%endif
%endif
%endif

%ifarch x86_64
if [ -e "hdhomerun_record_x64" ]; then
install -D -m 0755 hdhomerun_record_x64 %{buildroot}%{_bindir}/hdhomerun_record
else
install -D -m 0755 hdhomerun_record_x86 %{buildroot}%{_bindir}/hdhomerun_record
fi
%if !0%{?cross_build}
strip --strip-unneeded %{buildroot}%{_bindir}/hdhomerun_record
%else
%if 0%{?suse_version}
x86_64-suse-linux-strip --strip-unneeded %{buildroot}%{_bindir}/hdhomerun_record
%else
x86_64-linux-gnu-strip --strip-unneeded %{buildroot}%{_bindir}/hdhomerun_record
%endif
%endif
%endif

%ifarch %{arm} aarch64
install -D -m 0755 hdhomerun_record_arm %{buildroot}%{_bindir}/hdhomerun_record
%if !0%{?cross_build}
strip --strip-unneeded %{buildroot}%{_bindir}/hdhomerun_record
%else
%if 0%{?suse_version}
aarch64-suse-linux-strip --strip-unneeded %{buildroot}%{_bindir}/hdhomerun_record
%else
aarch64-linux-gnu-strip --strip-unneeded %{buildroot}%{_bindir}/hdhomerun_record
%endif
%endif
%endif

%ifarch ppc64 ppc
install -D -m 0755 hdhomerun_record_ppc %{buildroot}%{_bindir}/hdhomerun_record
%if !0%{?cross_build}
strip --strip-unneeded %{buildroot}%{_bindir}/hdhomerun_record
%else
%if 0%{?suse_version}
powerpc64-suse-linux-strip --strip-unneeded %{buildroot}%{_bindir}/hdhomerun_record
%else
powerpc64-linux-gnu-strip --strip-unneeded %{buildroot}%{_bindir}/hdhomerun_record
%endif
%endif
%endif

%__spec_install_post


%files
%defattr(755,root,root,-)
%{_bindir}/hdhomerun_record

%defattr(644,root,root,755)
%config(noreplace) %{_sysconfdir}/hdhomerun.conf
%if 0%{?rhel} == 6
# No automated tmpfiles
%else
%{_tmpfilesdir}/*
%endif
%{_mandir}/man8/*
%{_mandir}/man5/*
%{_datadir}/doc/*

%if 0%{?rhel} == 6
%defattr(755,root,root,-)
%config(noreplace) %{_initddir}/*
%config(noreplace) %{_sysconfdir}/sysconfig/*
%else
%defattr(644,root,root,-)
%{_unitdir}/*
%endif

%if 0%{?rhel} == 6
# No firewalld in rhel 6
%else
%defattr(644,root,root,-)
%{_prefix}/lib/firewalld/services/hdhomerun_record.xml
%endif

%defattr(755,hdhomerun,hdhomerun,755)
%dir %{_localstatedir}/run/hdhomerun/


%pre
getent group hdhomerun >/dev/null || groupadd -r hdhomerun
getent passwd hdhomerun >/dev/null || \
    useradd -r -g hdhomerun -d "/var/run/hdhomerun" -s /sbin/nologin \
    -c "HDHomeRun DVR server" hdhomerun
%if 0%{?suse_version}
%service_add_pre hdhomerun_record.service
%endif
exit 0


%post
%if 0%{?rhel} == 6
/sbin/chkconfig --add hdhomerun_record
%else
%if 0%{?suse_version}
%service_add_post hdhomerun_record.service
test -f /usr/bin/firewall-cmd && /usr/bin/firewall-cmd --reload --quiet || true
%else
%if 0%{?mageia}
systemctl --system daemon-reload
%firewalld_reload
%else
%systemd_post hdhomerun_record.service
%firewalld_reload
%endif
%endif
%endif
if [ $1 == 1 ] ; then
  if [ -f /etc/hdhomerun.conf -a -r /etc/hdhomerun.conf -a -w /etc/hdhomerun.conf -a ! -f /etc/hdhomerun.conf.rpmnew ] ; then
    grep -q "^[[:space:]]*StorageID[[:space:]]*=[[:space:]]*" /etc/hdhomerun.conf >/dev/null || \
      echo -e "\n\n# StorageID automatically added by package installation\nStorageID="`uuidgen`"\n" >>/etc/hdhomerun.conf
  fi
fi
exit 0


%preun
%if 0%{?rhel} == 6
if [ $1 == 0 ] ; then
  /sbin/service hdhomerun_record stop >/dev/null 2>&1
  /sbin/chkconfig --del hdhomerun_record
fi
%else
%if 0%{?suse_version}
%service_del_preun hdhomerun_record.service
%else
%systemd_preun hdhomerun_record.service
%endif
%endif
exit 0


%postun
%if 0%{?rhel} == 6
# Nothing to do for service based distro
%else
%if 0%{?suse_version}
%service_del_postun -n hdhomerun_record.service
test -f /usr/bin/firewall-cmd && /usr/bin/firewall-cmd --reload --quiet || true
%if 0%{?mageia}
systemctl --system daemon-reload
%firewalld_reload
%else
%else
%systemd_postun hdhomerun_record.service
%firewalld_reload
%endif
%endif
%endif
exit 0


%changelog

* Sat Nov 18 2017 Gary Buhrmaster <gary.buhrmaster@gmail.com>
- reset dist for new version

* Tue Sep 19 2017 Gary Buhrmaster <gary.buhrmaster@gmail.com>
- Remove provides/obsoletes, bump release

* Fri Jun 30 2017 Gary Buhrmaster <gary.buhrmaster@gmail.com>
- bump dist

* Thu Jun 29 2017 Gary Buhrmaster <gary.buhrmaster@gmail.com>
- support cross architecture building

* Wed Jun 28 2017 Gary Buhrmaster <gary.buhrmaster@gmail.com>
- install sysconfig file for rhel6

* Wed Jun 28 2017 Gary Buhrmaster <gary.buhrmaster@gmail.com>
- use install to create target directories

* Wed Jun 28 2017 Gary Buhrmaster <gary.buhrmaster@gmail.com>
- use macro definitions for _initddir and _tmpfilesdir

* Wed Jun 28 2017 Gary Buhrmaster <gary.buhrmaster@gmail.com>
- do not require firewalld install for suse

* Mon Jun 26 2017 Gary Buhrmaster <gary.buhrmaster@gmail.com>
- auto create storageid for new installs

* Mon Jun 26 2017 Gary Buhrmaster <gary.buhrmaster@gmail.com>
- Correct requires

* Mon Jun 26 2017 Gary Buhrmaster <gary.buhrmaster@gmail.com>
- add firewalld service definition

* Sun Jun 25 2017 Gary Buhrmaster <gary.buhrmaster@gmail.com>
- service configuration file is not config type

* Sat Jun 24 2017 Gary Buhrmaster <gary.buhrmaster@gmail.com>
- Insure scriptlets exit with 0

* Sat Jun 24 2017 Gary Buhrmaster <gary.buhrmaster@gmail.com>
- Update requires

* Thu Jun 22 2017 Gary Buhrmaster <gary.buhrmaster@gmail.com>
- Change _usr to _prefix macro usage

* Wed Jul 08 2015 Gary Buhrmaster <gary.buhrmaster@gmail.com>
- Initial package.
