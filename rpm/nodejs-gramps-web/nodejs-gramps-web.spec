%global srcname gramps-web
%global npm_name gramps-js
%bcond tests 1

Name:		nodejs-gramps-web
Version:	24.12.2
Release:	1%{?dist}
Summary:	The frontend for the Gramps Web genealogical research system

License:	AGPL-3.0-only and 0BSD and AGPL and Apache-2.0 and BSD-2-Clause and BSD-3-Clause and CC0-1.0 and ISC and MIT and Unlicense and W3C-20150513
URL:		https://github.com/gramps-project/gramps-web
Source0:	https://github.com/gramps-project/gramps-web/archive/refs/tags/%{srcname}-%{version}.tar.gz
Source1:	%{npm_name}-%{version}-nm-prod.tgz
Source2:	%{npm_name}-%{version}-nm-dev.tgz
Source3:	%{npm_name}-%{version}-bundled-licenses.txt

BuildArch:	noarch
ExclusiveArch:	%{nodejs_arches} noarch
Requires:	nodejs, python3-gunicorn
BuildRequires:	npm, nodejs-devel

%global _description %{expand:
This package contains only the javascript frontend for the Gramps Web
genealogical research system.  It is only useful when used in conjunction
with the gramps-webapi.}

%description %_description

%prep
%autosetup -n %{srcname}-%{version}
cp %{SOURCE3} .

%build
tar xfz %{SOURCE1}
mkdir -p node_modules
pushd node_modules
ln -s ../node_modules_prod/* .
ln -s ../node_modules_prod/.bin .
popd

%install
mkdir -p %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pr index.html %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pr package.json package-lock.json %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pr *.js *.css %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pr fonts images lang src %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pr node_modules node_modules_prod %{buildroot}%{nodejs_sitelib}/%{npm_name}

%check
%nodejs_symlink_deps --check
tar xfz %{SOURCE2}
echo $(pwd)
ls
# this is what the packaging reqts suggests...
# %{__nodejs} -e 'require("./")'
#
# but this is the only thing i can get working for now ...
# npm run start
#
# but even that has to be done from an interactive shell ...

%files
%license LICENSE %{npm_name}-%{version}-bundled-licenses.txt
%doc README.md
%doc default.conf.template
%{nodejs_sitelib}/%{npm_name}

%changelog
* Sat Feb 1 2025 Al Stone <ahs3@fedoraproject.org> - 24.12.2-1
- Initial attempt at packaging
- Still need to get the %check step working properly, but this at
  least does prep, build, and install

