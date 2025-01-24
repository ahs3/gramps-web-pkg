%global srcname object-ql
%bcond tests 1

Name:           python-%{srcname}
Version:        0.1.2
Release:        2%{?dist}
Summary:        An object query language for the Gramps Project and others

License:        MIT
URL:            https://pypi.org/project/object-ql/
Source:         %{pypi_source}
BuildArch:      noarch

%global _description %{expand:
An Object Query Language, for the Gramps Project and other objects.  This
project is designed to be a drop-in replacement gramps-ql.}

%description %_description

%py_provides python3-%{srcname}
%package -n python3-%{srcname}
Summary:        %{summary}

%if %{with tests}
BuildRequires:  pytest, python3-pyparsing
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
%pyproject_save_files 'object_ql*'

%check
%if %{with tests}
%pyproject_check_import
%pytest
%endif

# Note that there is no %%files section for the unversioned python module
%files -n python3-%{srcname} -f %{pyproject_files}
%license LICENSE
%doc README.md

%changelog
* Thu Jan 23 2025 Al Stone <ahs3@fedorproject.org> - 0.1.2-2
- Turn on %check

* Tue Jan 21 2025 Al Stone <ahs3@fedorproject.org> - 0.1.2-1
- Initial build of 0.1.2
