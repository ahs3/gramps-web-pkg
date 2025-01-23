%global srcname limits
%global srcnamenu webargs
%bcond tests 0

Name:           python-%{srcname}
Version:        4.0.1
Release:        2%{?dist}
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

%if %{with tests}
BuildRequires:	pytest, python3-etcd3
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
%pyproject_save_files 'limits*'

%check
# Testing in this case relies on an etcd3 module that in turn
# relies on a deprecated protobuf module.  We'll have to defer
# testing here until this can be sorted out upstream.
%if %{with tests}
%pyproject_check_import
%pytest
%endif

# Note that there is no %%files section for the unversioned python module
%files -n python3-%{srcname} -f %{pyproject_files}
%license LICENSE.txt
%doc HISTORY.rst
%doc README.rst

%changelog
* Wed Jan 22 2025 Al Stone <ahs3@fedorproject.org> - 4.0.1-2
- Tried to implement %check for testing; however, the tests currently
  require the etcd3 module, which in turn requires a deprecated protobuf.
  For now, do not do %check testing until we can get all the upstream
  infrastructure in place.

* Mon Jan 20 2025 Al Stone <ahs3@fedorproject.org> - 4.0.1-1
- Initial packaging for 4.0.1
