%global	projname gramps-web-api
%global	srcname gramps-webapi
%bcond tests 0

Name:		python-%{srcname}
Version:	2.7.0
Release:	4%{?dist}
Summary:	RESTful API for the gramps application

License:	AGPL-3.0
URL:		https://github.com/gramps-project/gramps-web-api
Source0:	https://github.com/gramps-project/gramps-web-api/archive/refs/tags/%{projname}-%{version}.tar.gz
Source1:	setup-api.sh
Source2:	gramps-webapi.service
Source3:	gramps-webapi.env
BuildArch:	noarch
Requires:	python3-torch, dialog
Requires(pre):	gramps
BuildRequires:	systemd
%{?systemd requires}

%global _description %{expand:
RESTful API for the gramps application
 
While this can be used solely as a local RESTful API, the intent of this
package is to provide the needed backend services for the gramps-web
interface.}

%description %_description

%package -n python3-%{srcname}
Summary:	%{summary}
Patch0:		gramps-desktop.patch

%if %{with tests}
BuildRequires:	pytest, python3-torch, python3-openai
%endif

%description -n python3-%{srcname} %_description

%prep
%autosetup -n %{projname}-%{version}
cp -p %{SOURCE1} .
cp -p %{SOURCE2} .
cp -p %{SOURCE3} .

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files 'gramps_webapi*'
mkdir -p %{buildroot}/%{_datadir}/gramps-web
mkdir -p %{buildroot}/%{_libexecdir}/gramps-web
mkdir -p %{buildroot}/%{_sysconfdir}/sysconfig
cp -p setup-api.sh %{buildroot}/%{_libexecdir}/gramps-web
cp -p gramps-webapi.service %{buildroot}/%{_libexecdir}/gramps-web
cp -p gramps-webapi.env %{buildroot}/%{_sysconfdir}/sysconfig/gramps-webapi

%check
%if %{with tests}
%pyproject_check_import
%pytest
%endif

%post
if [ $1 -gt 1 ]
then
fi
%systemd_post %{Source3}
%{_libexecdir}/gramps-web/setup-api.sh

%preun
%systemd_preun %{Source3}

%postun
%systemd_postun_with_restart %{Source3}

%files -n python3-%{srcname} -f %{pyproject_files}
%license LICENSE
%doc README.md
%{_datadir}/gramps-web
%{_libexecdir}/gramps-web
%{_sysconfdir}/sysconfig/gramps-webapi

%changelog
* Thu Feb 13 2025 Al Stone <ahs3@fedoraproject.org> - 2.0.7-4
- Changed how and where config and setup gets done; there will be a
  /usr/share/gramps-web directory for data now, not /root/.gramps
  as in the docker config
- Added a systemd service to start the API
- A post install scriptlet will do initial setup of the API configuration

* Sat Jan 25 2025 Al Stone <ahs3@fedoraproject.org> - 2.0.7-3
- The python3-torch module is required at run-time, so added it

* Thu Jan 23 2025 Al Stone <ahs3@fedoraproject.org> - 2.0.7-2
- Initial attempt at testing deferred due to test dependency on python3-openai
- Use proper output package name

* Mon Jan 13 2025 Al Stone <ahs3@fedoraproject.org> - 2.0.7-1
- Initial attempt at packaging
- Starting with release v2.0.7
