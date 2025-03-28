%global pkgname gramps-web

Name:		%{pkgname}
Version:	20250221
Release:	1%{?dist}
Summary:	Helper package for installing gramps-web on a server

BuildArch:	noarch
License:	GPLv2
URL:		https://github.com/ahs3/gramps-web-pkg
Source0:	%{pkgname}-%{VERSION}.tar.gz
Source1:	gramps-web.service
Source2:	README
Requires(pre):	systemd
%{?systemd requires}

# services required to run gramps-web
Requires:	MTA or /usr/sbin/sendmail
Requires:	nginx or webserver

# front- and back-end components for gramps-web
Requires(pre):	python3-gramps-webapi, nodejs-gramps-web

%description
Helper package for installing gramps-web on a server

This package will install the gramps-web-api and the gramps-web-frontend
from their packages, and all of their dependencies.  Additionally, a script
is provided to assist in the initial configuration of the gramps-web server.

%prep
%autosetup
cp -p %{SOURCE1} .
cp -p %{SOURCE2} .

%build
chmod 700 gweb

%install
mkdir -p %{buildroot}/%{_sysconfdir}/%{pkgname}
mkdir -p %{buildroot}/%{_sharedstatedir}/%{pkgname}
cp -p gweb %{buildroot}/%{_sysconfdir}/%{pkgname}

%files
%license COPYING
%doc README
%{_sysconfdir}/%{pkgname}
%{_sharedstatedir}/%{pkgname}

%post
if [ $1 -gt 1 ]
then
fi
%systemd_post %{SOURCE1}

%preun
%systemd_preun %{SOURCE1}

%postun
%systemd_postun_with_reload %{SOURCE1}

%changelog
* Fri Feb 21 2025 Al Stone <ahs3@fedoraproject.org> - 20250221-1
- Initial attempt at packaging

