%global srcname sifts

Name:           python-%{srcname}
Version:        1.0.0
Release:        1%{?dist}
Summary:        Simple full text and semantic search

License:        MIT
URL:            https://pypi.org/project/sifts/
Source:         %{pypi_source}
BuildArch:      noarch

%global _description %{expand:
Sifts is a simple but powerful Python package for managing and
querying document collections with support for both SQLite and
PostgreSQL databases.}

%description %_description

%py_provides python3-%{srcname}
%package -n python3-%{srcname}
Summary:        %{summary}
BuildRequires:  git

%description -n python3-%{srcname} %_description

%prep
%autosetup -n %{srcname}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files 'sifts*'

# Note that there is no %%files section for the unversioned python module
%files -n python3-%{srcname} -f %{pyproject_files}
%license LICENSE
%doc README.md

%changelog
* Mon Jan 20 2025 Al Stone <ahs3@fedorproject.org> - 1.0.0-1
- Initial pass at packaging v1.0.0
