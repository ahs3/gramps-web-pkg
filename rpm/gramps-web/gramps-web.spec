Name:		gramps-web
Version:	20250113
Release:	1%{?dist}
Summary:	Helper package for installing gramps-web on a server

BuildArch:	noarch
License:	GPLv2
URL:		https://github.com/ahs3/gramps-web-pkg
Source0:	https://github.com/ahs3/gramps-web-pkg/%{name}-%{version}.tar.gz

BuildRequires:	python3-devel

# services required to run gramps-web
Requires:	nginx, mstmp

# front- and back-end components for gramps-web
Requires:	gramps-web-api, gramps-web-frontend

%description
Helper package for installing gramps-web on a server

This package will install the gramps-web-api and the gramps-web-frontend
packages and all of their dependencies.  Additionally, a script is provided
to assist in the initial configuration of the gramps-web server.

%prep
%setup -q

%build

%install

%files

%changelog
* Mon Jan 13 2025 Al Stone <ahs3@fedoraproject.org> - 20250113-1
- Initial attempt at packaging

