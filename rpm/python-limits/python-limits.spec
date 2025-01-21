%global srcname limits
%global srcnamenu webargs

Name:           python-%{srcname}
Version:        4.0.1
Release:        1%{?dist}
Summary:        A Python library for parsing and validating HTTP request objects

License:        MIT
URL:            https://pypi.org/projects/limits
Source:         %{pypi_source}
BuildArch:      noarch

%global _description %{expand:
limits is a python library to perform rate limiting with commonly used storage backends (Redis, Memcached, MongoDB & Etcd).}

%description %_description

%py_provides python3-%{srcname}
%package -n python3-%{srcname}
Summary:        %{summary}

%description -n python3-%{srcname} %_description

%prep
%autosetup -n %{srcname}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files 'limits*'

# Note that there is no %%files section for the unversioned python module
%files -n python3-%{srcname} -f %{pyproject_files}
%license LICENSE.txt
%doc HISTORY.rst
%doc README.rst

%changelog
* Mon Jan 20 2025 Al Stone <ahs3@fedorproject.org> - 4.0.1-1
- Initial packaging for 4.0.1
