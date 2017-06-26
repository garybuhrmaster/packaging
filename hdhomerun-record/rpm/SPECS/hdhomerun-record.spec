#
# spec file for package hdhomerun_record
#

%define		debug_package %{nil}

Name:		hdhomerun-record
Version:	0.0.%{HDHRDVR_VERSION}
Release:	1%{?dist}
Provides:	hdhomerun_record = 0.0.20150901atest1-2
Obsoletes:	hdhomerun_record <= 0.0.20150901atest1-2
Group:		Applications/Internet
Summary:	SiliconDust HDHomeRun DVR server
Vendor:		SiliconDust USA Inc.
License:	Proprietary
URL:		http://www.silicondust.com/

Source0:	http://download.silicondust.com/hdhomerun/hdhomerun_record_linux_%{HDHRDVR_VERSION}
Source51:	hdhomerun_record-tmpfiles.conf
Source52:	hdhomerun_record.service
Source53:	hdhomerun_record.init
Source54:	hdhomerun.conf
Source55:	hdhomerun_record.xml
Source60:	hdhomerun_record.8
Source61:	hdhomerun.conf.5
Source70:	hdhomerun_record-doc.README
Source71:	hdhomerun_record-doc.LICENSE
Source72:	hdhomerun_record-doc.README.init

%if 0%{?rhel} == 6
Requires(pre):	initscripts
Requires(pre):	shadow-utils
Requires(pre):	glibc-common
%else
%if 0%{?suse_version}
Requires(pre):	shadow
Requires(pre):	glibc
BuildRequires:	systemd-rpm-macros
Requires(post):	firewalld
%{?systemd_requires}
%else
BuildRequires:	systemd
Requires(pre):	shadow-utils
Requires(pre):	glibc-common
Requires(pre):	systemd
Requires(post):	systemd
Requires(preun):	systemd
Requires(postun):	systemd
Requires(post):	firewalld-filesystem
%endif
%endif


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
mkdir -p %{buildroot}%{_prefix}/lib/tmpfiles.d
install -m 0644 %{SOURCE51} %{buildroot}%{_prefix}/lib/tmpfiles.d/hdhomerun_record.conf
%endif

%if 0%{?rhel} == 6
mkdir -p %{buildroot}%{_sysconfdir}/rc.d/init.d
install -m 0644 %{SOURCE53} %{buildroot}%{_sysconfdir}/rc.d/init.d/hdhomerun_record
%else
mkdir -p %{buildroot}%{_unitdir}
install -m 0644 %{SOURCE52} %{buildroot}%{_unitdir}/
%endif

mkdir -p %{buildroot}%{_sysconfdir}/
install -m 0644 %{SOURCE54} %{buildroot}%{_sysconfdir}/

%if 0%{?rhel} == 6
# No firewalld in rhel6
%else
mkdir -p %{buildroot}%{_prefix}/lib/firewalld/services
install -m 0644 %{SOURCE55} %{buildroot}%{_prefix}/lib/firewalld/services/hdhomerun_record.xml
%endif

mkdir -p %{buildroot}%{_localstatedir}/run/hdhomerun

mkdir -p %{buildroot}%{_mandir}/man8
install -m 0644 %{SOURCE60} %{buildroot}%{_mandir}/man8/

mkdir -p %{buildroot}%{_mandir}/man5
install -m 0644 %{SOURCE61} %{buildroot}%{_mandir}/man5/

mkdir -p %{buildroot}%{_datadir}/doc/hdhomerun_record
%if 0%{?rhel} == 6
install -m 0644 %{SOURCE72} %{buildroot}%{_datadir}/doc/hdhomerun_record/README
%else
install -m 0644 %{SOURCE70} %{buildroot}%{_datadir}/doc/hdhomerun_record/README
%endif
install -m 0644 %{SOURCE71} %{buildroot}%{_datadir}/doc/hdhomerun_record/LICENSE

mkdir -p %{buildroot}%{_bindir}

%ifarch %{ix86}
install -m 0755 hdhomerun_record_x86 %{buildroot}%{_bindir}/hdhomerun_record
%endif

%ifarch x86_64
if [ -e "hdhomerun_record_x64" ]; then
install -m 0755 hdhomerun_record_x64 %{buildroot}%{_bindir}/hdhomerun_record
else
install -m 0755 hdhomerun_record_x86 %{buildroot}%{_bindir}/hdhomerun_record
fi
%endif

%ifarch armv7hl aarch64
install -m 0755 hdhomerun_record_arm %{buildroot}%{_bindir}/hdhomerun_record
%endif

%ifarch ppc %{power64}
install -m 0755 hdhomerun_record_ppc %{buildroot}%{_bindir}/hdhomerun_record
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
%{_prefix}/lib/tmpfiles.d/*
%endif
%{_mandir}/man8/*
%{_mandir}/man5/*
%{_datadir}/doc/*

%if 0%{?rhel} == 6
%defattr(755,root,root,-)
%config(noreplace) %{_sysconfdir}/rc.d/init.d/hdhomerun_record
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
%else
%systemd_post hdhomerun_record.service
%firewalld_reload
%endif
%endif
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
if [ $1 == 1 ] ; then
  /sbin/service hdhomerun_record condrestart >/dev/null 2>&1
fi
%else
%if 0%{?suse_version}
%service_del_postun hdhomerun_record.service
%else
%systemd_postun_with_restart hdhomerun_record.service
%firewalld_reload
%endif
%endif
exit 0


%changelog

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
