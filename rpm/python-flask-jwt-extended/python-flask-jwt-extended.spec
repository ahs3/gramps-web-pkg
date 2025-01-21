%global srcname flask_jwt_extended

Name:           python-%{srcname}
Version:        4.7.1
Release:        1%{?dist}
Summary:        Adds support to Flask for using JSON Web Tokens (JWT)

License:        MIT
URL:            https://pypi.org/project/Flask-JWT-Extended/
Source:         %{pypi_source}
BuildArch:      noarch

%global _description %{expand:
Flask-JWT-Extended not only adds support for using JSON Web Tokens (JWT)
to Flask for protecting routes, but also many helpful (and optional)
features built in to make working with JSON Web Tokens easier. These
include:
    - Adding custom claims to JSON Web Tokens
    - Automatic user loading (current_user).
    - Custom claims validation on received tokens
    - Refresh tokens
    - First class support for fresh tokens for making sensitive changes.
    - Token revoking/blocklisting
    - Storing tokens in cookies and CSRF protection
}

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
%pyproject_save_files 'flask_jwt_extended*' +auto

# Note that there is no %%files section for the unversioned python module
%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.md

%changelog
* Mon Jan 20 2025 Al Stone <ahs3@fedorproject.org> - 4.7.1-1
- First version of Fedora packaging
