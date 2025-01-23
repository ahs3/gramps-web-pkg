%global srcname etcd3
%bcond tests 0

Name:           python-%{srcname}
Version:        0.12.0
Release:        1%{?dist}
Summary:        Python client for the etcd API v3

License:        Apache-2.0
URL:            https://python-etcd3.readthedocs.io/en/latest/
Source:         %{pypi_source}
BuildArch:      noarch

%global _description %{expand:
Python client for the etcd API v3, supported under python 2.7, 3.4 and 3.5.}

%description %_description

%py_provides python3-%{srcname}
%package -n python3-%{srcname}
Summary:        %{summary}
BuildRequires:  python3-pytest, python3-hypothesis, python3-mock

%description -n python3-%{srcname} %_description

%prep
%autosetup -n %{srcname}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files 'etcd3*'

%check
# Deferring testing on this for now; this package appears to
# be a bit crufty, to the point where some of the testing tools
# needed are deprecated (e.g., python-mock).
%if %{with tests}
%pyproject_check_import
%pytest
%endif

# Note that there is no %%files section for the unversioned python module
%files -n python3-%{srcname} -f %{pyproject_files}
%license LICENSE
%doc AUTHORS.rst
%doc HISTORY.rst
%doc README.rst

%changelog
* Thu Jan 23 2025 Al Stone <ahs3@fedorproject.org> - 0.12.0-1
- Initial Fedora packaging
