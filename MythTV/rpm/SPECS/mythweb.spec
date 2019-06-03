Name:           mythweb
Summary:        The web interface to MythTV
URL:            http://www.mythtv.org/

#
# Specify the commit hash for the source for this rpm
#
%global commit  %{?MYTHWEB_COMMIT}%{!?MYTHWEB_COMMIT:0}

Version:        %{?MYTHWEB_VERSION}%{!?MYTHWEB_VERSION:0.0}
Release:        100%{?dist}

License:        GPLv2 and LGPLv2 and MIT

# Source based on commit hash
Source0:        https://github.com/MythTV/%{name}/archive/%{commit}/%{name}-%{commit}.tar.gz

# This is needed for perl dependency auto-detection
BuildRequires:  perl-generators

Requires:       httpd
Requires:       php
Requires:       php-mysqli
Requires:       php-process
Requires:       php-MythTV
Requires:       perl
Requires:       perl(DBD::mysql)
Requires:       perl-MythTV
Requires:       mythtv-mythffmpeg

BuildArch:      noarch

################################################################################

%description
The web interface to MythTV.

################################################################################

%prep

%autosetup -p1 -n %{name}-%{commit}

# Build package mythweb.conf
cp mythweb.conf.apache mythweb.conf

################################################################################

%build
# Nothing to build

################################################################################

%install

# docs
mkdir -p %{buildroot}%{_datadir}/doc/%{name}
install -D -m 0644 INSTALL               %{buildroot}%{_datadir}/doc/%{name}/
install -D -m 0644 README                %{buildroot}%{_datadir}/doc/%{name}/
install -D -m 0644 LICENSE               %{buildroot}%{_datadir}/doc/%{name}/
install -D -m 0644 mythweb.conf.apache   %{buildroot}%{_datadir}/doc/%{name}/
install -D -m 0644 mythweb.conf.nginx    %{buildroot}%{_datadir}/doc/%{name}/
install -D -m 0644 mythweb.conf.lighttpd %{buildroot}%{_datadir}/doc/%{name}/
install -D -m 0644 Dockerfile            %{buildroot}%{_datadir}/doc/%{name}/

# docroot files (html, perl, php, etc.)
mkdir -p %{buildroot}%{_var}/www/html/%{name}
install -D -m 0644 mythweb.php           %{buildroot}%{_var}/www/html/%{name}/
install -D -m 0755 mythweb.pl            %{buildroot}%{_var}/www/html/%{name}/
cp -r              classes               %{buildroot}%{_var}/www/html/%{name}/
cp -r              configuration         %{buildroot}%{_var}/www/html/%{name}/
cp -r              data                  %{buildroot}%{_var}/www/html/%{name}/
cp -r              includes              %{buildroot}%{_var}/www/html/%{name}/
cp -r              js                    %{buildroot}%{_var}/www/html/%{name}/
cp -r              modules               %{buildroot}%{_var}/www/html/%{name}/
cp -r              skins                 %{buildroot}%{_var}/www/html/%{name}/
cp -r              tests                 %{buildroot}%{_var}/www/html/%{name}/

# httpd config
mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf.d
install -p -m 0644 mythweb.conf %{buildroot}%{_sysconfdir}/httpd/conf.d/mythweb.conf

################################################################################

%files
%defattr(-, root, root, 0755)
%config(noreplace) %{_sysconfdir}/httpd/conf.d/mythweb.conf
%{_datadir}/doc/%{name}
%dir %{_var}/www/html/%{name}
%attr(-, apache, apache) %{_var}/www/html/%{name}/data
%{_var}/www/html/%{name}/mythweb.php
%{_var}/www/html/%{name}/mythweb.pl
%{_var}/www/html/%{name}/classes
%{_var}/www/html/%{name}/configuration
%{_var}/www/html/%{name}/includes
%{_var}/www/html/%{name}/js
%{_var}/www/html/%{name}/modules
%{_var}/www/html/%{name}/skins
%{_var}/www/html/%{name}/tests

################################################################################

%preun
#
# Remove any locally cached content to allow a clean uninstall
#
if [ "$1" = "0" ]; then
    rm -rf %{_var}/www/html/%{name}/data/cache
    mkdir -p 0755 %{_var}/www/html/%{name}/data/cache
    rm -rf %{_var}/www/html/%{name}/data/tv_icons
    mkdir -p 0755 %{_var}/www/html/%{name}/data/tv_icons
fi

################################################################################

%changelog

* Wed May 09 2018 Gary Buhrmaster <gary.buhrmaster@gmail.com> - 29.0
- Rework for managed rebuilds

* Mon Apr 17 2017 Richard Shaw <hobbes1069@gmail.com> - 0.28.1-1
- Update to latest upstream release, 0.28.1.

* Mon Mar 20 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.28-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec  1 2016 Richard Shaw <hobbes1069@gmail.com> - 0.28-6
- Remove obsolete scripts. Since data was moved to /var/lib data migration is
  no longer necessary.
- Fixes RFBZ#4357.

* Wed Oct 26 2016 Paul Howarth <paul@city-fan.org> - 0.28-5
- BR: perl-generators for proper dependency generation
  (https://fedoraproject.org/wiki/Changes/Build_Root_Without_Perl)

* Wed Oct 19 2016 Richard Shaw <hobbes1069@gmail.com> - 0.28-4
- Update to latest fixes.

* Thu Sep 08 2016 Sérgio Basto <sergio@serjux.com> - 0.28-2
- v0.28-rc1 already support mysqli, https://code.mythtv.org/trac/ticket/12588
- Requires php-mysqli, because in php7, "php-mysql" package and "mysql.so"
- extension have been removed.

* Tue Apr 19 2016 Richard Shaw <hobbes1069@gmail.com> - 0.28-1
- Update to latest fixes.

* Fri Feb 19 2016 Richard Shaw <hobbes1069@gmail.com> - 0.27.6-2
- Update to latest fixes.

* Wed Jul 29 2015 Richard Shaw <hobbes1069@gmail.com> - 0.27.5-1
- Update to latest upstream release.

* Wed May 27 2015 Richard Shaw <hobbes1069@gmail.com> - 0.27.4-2
- Update to latest fixes release.

* Thu Oct 23 2014 Richard Shaw <hobbes1069@gmail.com> - 0.27.4-1
- Update to latest upstream release.

* Sun Jul 27 2014 Richard Shaw <hobbes1069@gmail.com> - 0.27.3-1
- Update to latest upstream release.

* Mon May 26 2014 Richard Shaw <hobbes1069@gmail.com> - 0.27.1-1
- Update to latest upstream release.

* Fri May 16 2014 Richard Shaw <hobbes1069@gmail.com> - 0.27-2
- Update to latest fixes release.
