%global srcname gramps-ql

Name:           python-%{srcname}
Version:        0.3.0
Release:        1%{?dist}
Summary:        GQL: the Gramps Query Language

License:        MIT
URL:            https://pypi.org/project/gramps-ql/
Source:         %{pypi_source}
BuildArch:      noarch

%global _description %{expand:
This Python library provides GQL, a query language to a Gramps database.
The syntax is inspired by JQL, the Jira Query Language.}

%description %_description

%py_provides python3-%{srcname}
%package -n python3-%{srcname}
Summary:        %{summary}
BuildRequires:	git

%description -n python3-%{srcname} %_description

%prep
%autosetup -n %{srcname}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files 'gramps_ql*'

# Note that there is no %%files section for the unversioned python module
%files -n python3-%{srcname} -f %{pyproject_files}
%license LICENSE
%doc README.md

%changelog
* Tue Jan 21 2025 Al Stone <ahs3@fedorproject.org> - 0.3.0-1
- Initial build of 0.3.0
