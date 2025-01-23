%global srcname flask-limiter
%bcond tests 0

Name:           python-%{srcname}
Version:        3.10.1
Release:        2%{?dist}
Summary:        Add rate limiting to Flask applications

License:        MIT
URL:            https://pypi.org/project/Flask-Limiter/
Source:         %{pypi_source}
BuildArch:      noarch

%global _description %{expand:
Add rate limiting to Flask applications

You can configure rate limits at different levels such as:
   - Application wide global limits per user
   - Default limits per route
   - By Blueprints
   - By Class-based views
   - By individual routes

Flask-Limiter can be configured to fit your application in many ways,
including:
   - Persistance to various commonly used storage backends (such as Redis,
     Memcached, MongoDB and Etcd) via limits
   - Any rate limiting strategy supported by limits}

%description %_description

%py_provides python3-%{srcname}
%package -n python3-%{srcname}
Summary:        %{summary}

%if %{with tests}
BuildRequires:	pytest, python3-coverage, python3-pytest-cov
BuildRequires:	python3-pytest-mock, python3-lovely-pytest-docker
BuildRequires:	python3-pymemcache, python3-pymongo, python3-redis
BuildRequires:	python3-flask, python3-restful, python3-flask-restx
BuildRequires:  python3-asgiref
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
%pyproject_save_files 'flask_limiter*' +auto

%check
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
* Thu Jan 23 2025 Al Stone <ahs3@fedorproject.org> - 3.10.1-2
- Try to get %check working; the tests only work when done through
  a docker image, which is not terribly useful when trying to ship
  as a package; builds do not typically allow network connections
  for security reasons.  Put some basics in place, but will need to
  work on upstream.

* Mon Jan 20 2025 Al Stone <ahs3@fedorproject.org> - 3.10.1-1
- First version of Fedora packaging
