Name:           pterm

Version:        6.0.4
Release:        1%{?dist}
Summary:        PLATO Terminal Emulator

License:        DtCyber
URL:            https://cyber1.org/
Source0:        https://cyber1.org/download/linux/pterm-6.0.4.tar.bz2
Source1:        pterm.desktop
Source2:        pterm.png
Patch1:         pterm-python-version.patch
Patch2:         pterm-fix-permissions.patch

BuildRequires:  SDL-devel
BuildRequires:  wxWidgets-devel
BuildRequires:  libsndfile-devel
BuildRequires:  gcc-c++
BuildRequires:  desktop-file-utils
BuildRequires:  svn
BuildRequires:  python3
BuildRequires:  make


%description
The pterm program emulates a PLATO terminal (at the moment the
"PLATO V" a.k.a. PPT, without the loadable program capability),
for use with the cyber1 CYBIS (PLATO) system.


%prep
%autosetup -p1


%build
# (ugly) fixup for bug in el packaging
%if (0%{?rhel} == 7)
mkdir fixup
ln -s /usr/bin/wx-config-3.0 fixup/wx-config
export PATH=fixup:$PATH
%endif
%make_build
make mofiles
# fixup end-of-line encoding on doc file
sed -i 's/\r$//' CHANGES-pterm.txt


%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/locale/nl/LC_MESSAGES/
mkdir -p %{buildroot}%{_datadir}/pixmaps
mkdir -p %{buildroot}%{_datadir}/applications
install -m 0755 pterm          %{buildroot}%{_bindir}/
install -m 0644 nl/pterm.mo    %{buildroot}%{_datadir}/locale/nl/LC_MESSAGES/
install -m 0644 %{SOURCE1}     %{buildroot}%{_datadir}/applications/pterm.desktop
desktop-file-validate          %{buildroot}%{_datadir}/applications/pterm.desktop
install -m 0644 %{SOURCE2}     %{buildroot}%{_datadir}/pixmaps/pterm.png


%files
%doc CHANGES-pterm.txt
%license license.txt pterm-license.txt
%{_bindir}/*
%lang(nl) %{_datadir}/locale/nl/LC_MESSAGES/*
%{_datadir}/pixmaps/*
%{_datadir}/applications/*


%changelog

* Mon May 06 2019 Gary Buhrmaster <gary.buhrmaster@gmail.com> 6.0.4-1
- Update to 6.0.4 release

* Wed Aug 01 2018 Gary Buhrmaster <gary.buhrmaster@gmail.com> 6.0.2-1
- Initial upload


