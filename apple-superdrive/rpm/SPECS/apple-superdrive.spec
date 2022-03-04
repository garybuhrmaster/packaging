Name:           apple-superdrive
Version:        1.0.0
Release:        1%{?dist}
Summary:        Apple SuperDrive activation udev rule
License:        BSD

Source0:        90-apple-superdrive.rules

BuildArch:      noarch
BuildRequires:  systemd-rpm-macros
Requires:       sg3_utils

%description
Enable the use of an Apple SuperDrive on Linux

%prep


%install
mkdir -p %buildroot%{_udevrulesdir}
install -m0644 %SOURCE0 %buildroot%{_udevrulesdir}/


%files
%{_udevrulesdir}/*


%changelog
* Wed Jul 28 2021 Gary Buhrmaster <gary.buhrmaster@gmail.com> - 1.0.0-1
- initial packaging
