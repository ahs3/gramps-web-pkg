#!/bin/bash
#
#   run some basic tests for the gramps-webapi
#

CURDIR=$(pwd)
CFG="config.cfg"
DEPS="\
	gramps \
	python3-flask-limiter \
	python3-gramps-ql \
	python3-object-ql \
	python3-sifts \
"
PKGNAME="python3-gramps-webapi"
TESTDIR="${CURDIR}/pkg-testing"

trap cleanup SIGINT SIGTERM
cleanup () {
	# placeholder for any clean up needed
	echo "cleaning up..."
}

is_installed() {
	pkgname="$1"
	if [ -h /etc/fedora-release ]
	then
		res=$(rpm -qa | grep $pkgname)
		[ -z "$res" ] && return 1

	elif [ -f /etc/debian_release || -f /etc/os-release ]
	then
		echo "? not implemented yet"
		return 1
	fi

	return 0
}

# make sure the right packages are installed
not_found=""
for ii in $PKGNAME $DEPS
do
	if is_installed $ii
	then
		echo package $ii installed
	else
		echo "? package $ii is not installed"
		not_found="${not_found}${ii}"
	fi
done

if [ ! -z "$not_found" ]
then
	echo "? please install needed packages and try again"
	exit 1
fi

# starting building up the testing environment
if [ -d $TESTDIR ]
then
	echo "The $TESTDIR directory already exists."
	while true
	do
		read -p "Is it okay to remove it [y/n]? " answer
		case $answer in
			[Yy]*)	echo "removing ..."
				rm -rf $TESTDIR
				break
				;;
			[Nn]*)	echo "halting test."
				exit 0
				;;
		esac
	done
fi
mkdir -p $TESTDIR
pushd $TESTDIR

# create a random flask secret key
mkdir -p secret
python3 -c "import secrets;print(secrets.token_urlsafe(32))" | \
	tr -d "\n" > secret/secret
if [ -z "$TMP_SECRET_KEY" ]
then
	export TMP_SECRET_KEY=$(cat secret/secret)
fi

# create an empty testing family tree
TREENAME="XYZZY Gramps Testing Only Family Tree XYZZY"
echo yes | gramps -r "$TREENAME"
gramps -C "$TREENAME" -i $CURDIR/data.gramps

# build a config file
if [ -f $CFG ]
then
	echo "? existing $CFG file found, will not overwrite, continuing ..."
else
	cat > $CFG <<EndOfConfig
TREE="${TREENAME}"
BASE_URL="https://localhost"
SECRET_KEY="${TMP_SECRET_KEY}"
USER_DB_URI="sqlite:////${TESTDIR}/gramps_webapi_test.sqlite"
SEARCH_INDEX_DB_URI="sqlite:///${TESTDIR}/indexdir/search_index.db"
EMAIL_HOST="localhost"
EMAIL_PORT="25"
EMAIL_USE_TLS=False
EMAIL_USER="root@localhost"
EMAIL_HOST_PASSWORD=""
DEFAULT_FROM_EMAIL="gramps@localhost"
EndOfConfig

fi

# create the search index if it doesn't already exist
if [ -z "$(ls -A indexdir 2>/dev/null)" ]
then
	python3 -m gramps_webapi --config $CFG search index-full
fi

# create some dummy user accounts
python3 -m gramps_webapi --config $CFG user add owner owner \
	--fullname Owner --role 4
python3 -m gramps_webapi --config $CFG user add editor editor \
	--fullname Editor --role 3
python3 -m gramps_webapi --config $CFG user add contributor contributor \
	--fullname Contributor --role 2
python3 -m gramps_webapi --config $CFG user add member member \
	--fullname member --role 1
python3 -m gramps_webapi --config $CFG user add guest guest \
	--fullname member --role 0
python3 -m gramps_webapi --config $CFG user add --role -1 disabled disabled

# try to run web api ....
# will need to ctrl-c to quit
LANGUAGE=en python3 -O -m gramps_webapi --config $CFG run --port 5555

# ... and if you've gotten this far, we can at least bring up the webapi
# so now we need to see if it can be queried/used in any way ....

