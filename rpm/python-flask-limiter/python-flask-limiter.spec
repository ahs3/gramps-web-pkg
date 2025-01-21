%global srcname flask-limiter

Name:           python-%{srcname}
Version:        3.10.1
Release:        1%{?dist}
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

# Note that there is no %%files section for the unversioned python module
%files -n python3-%{srcname} -f %{pyproject_files}
%license LICENSE.txt
%doc HISTORY.rst
%doc README.rst

%changelog
* Mon Jan 20 2025 Al Stone <ahs3@fedorproject.org> - 3.10.1-1
- First version of Fedora packaging
