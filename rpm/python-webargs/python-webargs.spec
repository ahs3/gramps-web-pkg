%global srcname webargs
%bcond tests 0

Name:           python-%{srcname}
Version:        8.6.0
Release:        2%{?dist}
Summary:        A Python library for parsing and validating HTTP request objects

License:        MIT
URL:            https://webargs.readthedocs.io/en/latest/
Source:         %{pypi_source}
BuildArch:      noarch

%global _description %{expand:
webargs is a Python library for parsing and validating HTTP request 
objects, with built-in support for popular web frameworks, including 
Flask, Django, Bottle, Tornado, Pyramid, Falcon, and aiohttp..}

%description %_description

%py_provides python3-%{srcname}
%package -n python3-%{srcname}
Summary:        %{summary}

%if %{with tests}
BuildRequires:  pytest, python3-pytest-aiohttp, python3-bottle, python3-django
BuildRequires:  python3-falcon, python3-flask, python3-pyramid, python3-webtest
BuildRequires:  python3-tornado, python3-webtest-aiohttp
%endif

%description -n python3-%{srcname} %_description

%prep
%autosetup -n %{srcname}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files 'webargs*'

%check
%if %{with tests}
%pyproject_check_import
%pytest
%endif

# Note that there is no %%files section for the unversioned python module
%files -n python3-%{srcname} -f %{pyproject_files}
%license LICENSE
%license NOTICE
%doc AUTHORS.rst
%doc CHANGELOG.rst
%doc README.rst

%changelog
* Thu Jan 23 2025 Al Stone <ahs3@fedorproject.org> - 8.6.0-2
- Enable %check; deferred due to possible stale upstream for the
  python3-webtest-aiohttp module as a dependency

* Sun Jan 19 2025 Al Stone <ahs3@fedorproject.org> - 8.6.0-1
- Update to 8.6.0 source
- Use generate_buildrequires instead of explicit package list
- changelog cleanup
- build/install modernization

* Thu Sep 29 2022 Andrii Verbytskyi <andrii.verbytskyi@mpp.mpg.de> - 8.3.0-1
- Cleanup 
