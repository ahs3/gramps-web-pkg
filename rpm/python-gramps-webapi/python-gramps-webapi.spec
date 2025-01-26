%global	projname gramps-web-api
%global	srcname gramps-webapi
%bcond tests 0

Name:		python-%{srcname}
Version:	2.7.0
Release:	3%{?dist}
Summary:	RESTful API for the gramps application

License:	AGPL-3.0
URL:		https://github.com/gramps-project/gramps-web-api
Source0:	https://github.com/gramps-project/gramps-web-api/archive/refs/tags/%{projname}-%{version}.tar.gz
BuildArch:	noarch
Requires:	python3-torch

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
BuildRequires:  pytest, python3-torch, python3-openai
%endif

%description -n python3-%{srcname} %_description

%prep
%autosetup -n %{projname}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files 'gramps_webapi*'

%check
%if %{with tests}
%pyproject_check_import
%pytest
%endif

%files -n python3-%{srcname} -f %{pyproject_files}
%license LICENSE
%doc README.md

%changelog
* Sat Jan 25 2025 Al Stone <ahs3@fedoraproject.org> - 2.0.7-3
- The python3-torch module is required at run-time, so added it

* Thu Jan 23 2025 Al Stone <ahs3@fedoraproject.org> - 2.0.7-2
- Initial attempt at %check; deferred due to test dependency on python3-openai
- Use proper output package name

* Mon Jan 13 2025 Al Stone <ahs3@fedoraproject.org> - 2.0.7-1
- Initial attempt at packaging
- Starting with release v2.0.7
