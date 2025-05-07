#
# spec file for package hdhomerun_record
#

%global		debug_package %{nil}

%global		_build_id_links none

%global		__os_install_post /usr/lib/rpm/brp-compress %{nil}

%global		_pkgverify_level digest


Name:		hdhomerun-record
Version:	0.0.%{?HDHRDVR_VERSION}%{!?HDHRDVR_VERSION:0}
Release:	1%{?dist}
Group:		Applications/Internet
Summary:	SiliconDust HDHomeRun DVR server
Vendor:		SiliconDust USA Inc.
License:	Proprietary
URL:		https://www.silicondust.com/

Source0:	https://download.silicondust.com/hdhomerun/hdhomerun_record_linux%{?HDHRDVR_VERSION:_%{HDHRDVR_VERSION}}
Source50:	hdhomerun_record-sysusers.conf
Source51:	hdhomerun_record-tmpfiles.conf
Source52:	hdhomerun_record.service
Source54:	hdhomerun.conf
Source55:	hdhomerun_record.xml
Source60:	hdhomerun_record.8
Source61:	hdhomerun.conf.5
Source70:	hdhomerun_record-doc.README
Source71:	hdhomerun_record-doc.LICENSE

%if 0%{?suse_version}
BuildRequires:	coreutils
BuildRequires:	tar
BuildRequires:	systemd-rpm-macros
Requires(pre):	coreutils
Requires(pre):	systemd
Requires(pre):	glibc
%{?systemd_requires}
%else
%if 0%{?mageia}
BuildRequires:	coreutils
BuildRequires:	tar
BuildRequires:	firewalld-filesystem
BuildRequires:	systemd
Requires:	systemd
Requires:	firewalld-filesystem
Requires(pre):	rpm-helper
Requires(pre):	coreutils
Requires(pre):	glibc
Requires(pre):	systemd
Requires(post):	rpm-helper
Requires(post):	systemd
Requires(preun):	rpm-helper
Requires(preun):	systemd
Requires(postun):	rpm-helper
Requires(postun):	systemd
%else
BuildRequires:	coreutils
BuildRequires:	tar
BuildRequires:	systemd
BuildRequires:	firewalld-filesystem
Requires:	systemd
Requires:	firewalld-filesystem
Requires(pre):	coreutils
Requires(pre):	glibc-common
Requires(pre):	systemd
Requires(pre):	firewalld-filesystem
Requires(post):	systemd
Requires(preun):	systemd
Requires(postun):	systemd
Requires(postun):	firewalld-filesystem
%endif
%endif
Requires(post):	util-linux
Requires(post):	coreutils
Requires(post):	grep
#
# User/Group provides
#
Provides:	user(hdhomerun)
Provides:	group(hdhomerun)


%description
This package provides the SiliconDust HDHomeRun DVR recorder service.


%prep
%setup -q -c -T

dd if=%{SOURCE0} bs=4096 skip=1 2>/dev/null | tar -xvz


%build

# Nothing to build
echo "Nothing to build"


%install

install -D -m 0644 %{SOURCE50} %{buildroot}%{_sysusersdir}/hdhomerun_record.conf

install -D -m 0644 %{SOURCE51} %{buildroot}%{_tmpfilesdir}/hdhomerun_record.conf

install -D -m 0644 %{SOURCE52} %{buildroot}%{_unitdir}/hdhomerun_record.service

install -D -m 0644 %{SOURCE54} %{buildroot}%{_sysconfdir}/hdhomerun.conf

install -D -m 0644 %{SOURCE55} %{buildroot}%{_prefix}/lib/firewalld/services/hdhomerun_record.xml

mkdir -p %{buildroot}%{_localstatedir}/run/hdhomerun

install -D -m 0644 %{SOURCE60} %{buildroot}%{_mandir}/man8/hdhomerun_record.8

install -D -m 0644 %{SOURCE61} %{buildroot}%{_mandir}/man5/hdhomerun.conf.5

install -D -m 0644 %{SOURCE70} %{buildroot}%{_datadir}/doc/hdhomerun_record/README
install -D -m 0644 %{SOURCE71} %{buildroot}%{_datadir}/doc/hdhomerun_record/LICENSE

%ifarch %{ix86}
install -D -m 0755 hdhomerun_record_x86 %{buildroot}%{_bindir}/hdhomerun_record
%endif

%ifarch x86_64
if [ -f "hdhomerun_record_x64" ]; then
install -D -m 0755 hdhomerun_record_x64 %{buildroot}%{_bindir}/hdhomerun_record
else
install -D -m 0755 hdhomerun_record_x86 %{buildroot}%{_bindir}/hdhomerun_record
fi
%endif

%ifarch %{arm}
install -D -m 0755 hdhomerun_record_arm %{buildroot}%{_bindir}/hdhomerun_record
%endif

%ifarch aarch64
if [ -f "hdhomerun_record_arm64" ]; then
install -D -m 0755 hdhomerun_record_arm64 %{buildroot}%{_bindir}/hdhomerun_record
else
install -D -m 0755 hdhomerun_record_arm %{buildroot}%{_bindir}/hdhomerun_record
fi
%endif

%ifarch ppc64 ppc
install -D -m 0755 hdhomerun_record_ppc %{buildroot}%{_bindir}/hdhomerun_record
%endif


%files
%defattr(755,root,root,-)
%{_bindir}/hdhomerun_record

%defattr(644,root,root,755)
%config(noreplace) %{_sysconfdir}/hdhomerun.conf
%{_sysusersdir}/*
%{_tmpfilesdir}/*
%{_mandir}/man8/*
%{_mandir}/man5/*
%{_datadir}/doc/*

%defattr(644,root,root,-)
%{_unitdir}/*

%defattr(644,root,root,-)
%{_prefix}/lib/firewalld/services/hdhomerun_record.xml

%defattr(755,hdhomerun,hdhomerun,755)
%dir %{_localstatedir}/run/hdhomerun/


%pre
# Add the "hdhomerun" user
%sysusers_create_package hdhomerun %{SOURCE50}
%if 0%{?suse_version}
%service_add_pre hdhomerun_record.service
%endif
exit 0


%post
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
if [ $1 == 1 ] ; then
  if [ -f /etc/hdhomerun.conf -a -r /etc/hdhomerun.conf -a -w /etc/hdhomerun.conf -a ! -f /etc/hdhomerun.conf.rpmnew ] ; then
    grep -q "^[[:space:]]*StorageID[[:space:]]*=[[:space:]]*" /etc/hdhomerun.conf >/dev/null || \
      echo -e "\n\n# StorageID automatically added by package installation\nStorageID="`uuidgen`"\n" >>/etc/hdhomerun.conf
  fi
fi
exit 0


%preun
%if 0%{?suse_version}
%service_del_preun hdhomerun_record.service
%else
%systemd_preun hdhomerun_record.service
%endif
exit 0


%postun
%if 0%{?suse_version}
%service_del_postun_without_restart hdhomerun_record.service
test -f /usr/bin/firewall-cmd && /usr/bin/firewall-cmd --reload --quiet || true
%else
%if 0%{?mageia}
systemctl --system daemon-reload
%firewalld_reload
%else
%systemd_postun hdhomerun_record.service
%firewalld_reload
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
