%global	projname gramps-web-api
%global	srcname gramps-webapi
%bcond tests 0

Name:		python-%{srcname}
Version:	2.7.0
Release:	7%{?dist}
Summary:	RESTful API for the gramps application

License:	AGPL-3.0-or-later
URL:		https://github.com/gramps-project/gramps-web-api
Source0:	https://github.com/gramps-project/gramps-web-api/archive/refs/tags/%{projname}-%{version}.tar.gz
Source1:	gramps-webapi.service
Source2:	gramps-webapi.env
BuildArch:	noarch
%{?systemd requires}

%global _description %{expand:
RESTful API for the gramps application
 
While this can be used solely as a local RESTful API, the intent of this
package is to provide the needed backend services for the gramps-web
interface.}

%description %_description

%package -n python3-%{srcname}
Summary:	%{summary}
Patch0:		gramps-requires.patch
%py_provides	python3-gramps-webapi
BuildRequires:	python3-devel, systemd
Requires(pre):	gramps

%if %{with tests}
BuildRequires:	pytest, python3-torch, python3-openai
%endif


%description -n python3-%{srcname} %_description

%prep
%autosetup -n %{projname}-%{version}
cp -p %{SOURCE1} .
cp -p %{SOURCE2} .

%generate_buildrequires
%pyproject_buildrequires -x python3-torch

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files 'gramps_webapi*'
mkdir -p %{buildroot}/%{_datadir}/gramps-web
mkdir -p %{buildroot}/%{_sysconfdir}/sysconfig
mkdir -p %{buildroot}/%{_unitdir}
cp -p gramps-webapi.service %{buildroot}/%{_unitdir}/
cp -p gramps-webapi.env %{buildroot}/%{_sysconfdir}/sysconfig/gramps-webapi

%check
%if %{with tests}
%pyproject_check_import
%pytest
%endif

%post
if [ $1 -gt 1 ]
then
fi
%systemd_post %{SOURCE2}

LANGUAGE=en
export LANGUAGE
GRAMPSHOME="/usr/share/gramps-web"
export GRAMPSHOME

DATADIR=$GRAMPSHOME
CFG="config/config.cfg"

# start building up the environment
[ ! -d $DATADIR ] && mkdir -p $DATADIR
pushd $DATADIR 2>&1 >/dev/null
for ii in config gramps grampsdb indexdir secret static
do
	[ ! -d $DATADIR/$ii ] && mkdir -p $DATADIR/$ii
done

if [ -f $CFG ]
then
	# do not overwrite this if it exists
	exit 0
else
cat > $CFG <<EOF
GRAMPSHOME="$DATADIR"
TREE="Example"
BASE_URL="https://localhost:5555/"
SECRET_KEY="XYZZY"
USER_DB_URI="sqlite:////usr/share/gramps-web/gramps/gramps_webapi.sqlite"
DATABASE_PATH="/usr/share/gramps-web/gramps/grampsdb"
MEDIA_BASE_DIR="/usr/share/doc/gramps/example/gramps/"
SEARCH_INDEX_DB_URI="sqlite:////usr/share/gramps-web/indexdir/search_index.db"
STATIC_PATH="/usr/share/gramps-web/static"
CORS_ORIGINS="*"
EOF
fi

# create a random flask secret key
python3 -c "import secrets;print(secrets.token_urlsafe(32))" | \
	tr -d "\n" > secret/secret
chmod 600 secret/secret
if [ -z "$TMP_SECRET_KEY" ]
then
	export TMP_SECRET_KEY=$(cat secret/secret)
fi
sed -i "s/XYZZY/${TMP_SECRET_KEY}/" $CFG

# create an example family tree
cp /usr/share/doc/gramps/example/gramps/example.gramps .
gramps -C Example -i example.gramps \
	--config=database.path:/usr/share/gramps-web/gramps/grampsdb

# create the text search index
if [ -z "$(ls -A indexdir 2>/dev/null)" ]
then
	python3 -m gramps_webapi --config $CFG search index-incremental
fi

# add user accounts
python3 -m gramps_webapi --config $CFG user add --role 4 owner owner
python3 -m gramps_webapi --config $CFG user add --role 3 editor editor
python3 -m gramps_webapi --config $CFG user add --role 2 contributor contributor
python3 -m gramps_webapi --config $CFG user add --role 1 disabled disabled
python3 -m gramps_webapi --config $CFG user add --role 0 guest guest


%preun
%systemd_preun %{SOURCE2}

%postun
%systemd_postun_with_restart %{SOURCE2}

%files -n python3-%{srcname} -f %{pyproject_files}
%license LICENSE
%doc README.md
%{_datadir}/gramps-web
%{_unitdir}/gramps-webapi.service
%{_sysconfdir}/sysconfig/gramps-webapi

%changelog
* Thu Mar 27 2025 Al Stone <ahs3@fedoraproject.org> - 2.0.7-7
- Requires were not working well with the auto dependency generations of
  them; changed the patch to pyproject.toml to get torch included properly

* Wed Mar 26 2025 Al Stone <ahs3@fedoraproject.org> - 2.0.7-6
- Re-did the post scriptlet
- Correct typos in systemd service
- Fixed dependency on python3-torch

* Tue Mar 25 2025 Al Stone <ahs3@fedoraproject.org> - 2.0.7-5
- Systemd files were not being included in the .rpm

* Thu Feb 13 2025 Al Stone <ahs3@fedoraproject.org> - 2.0.7-4
- Changed how and where config and setup gets done; there will be a
  /usr/share/gramps-web directory for data now, not /root/.gramps
  as in the docker config
- Added a systemd service to start the API
- A post install scriptlet will do initial setup of the API configuration

* Sat Jan 25 2025 Al Stone <ahs3@fedoraproject.org> - 2.0.7-3
- The python3-torch module is required at run-time, so added it

* Thu Jan 23 2025 Al Stone <ahs3@fedoraproject.org> - 2.0.7-2
- Initial attempt at testing deferred due to test dependency on python3-openai
- Use proper output package name

* Mon Jan 13 2025 Al Stone <ahs3@fedoraproject.org> - 2.0.7-1
- Initial attempt at packaging
- Starting with release v2.0.7
