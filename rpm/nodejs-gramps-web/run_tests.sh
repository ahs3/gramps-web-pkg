#!/bin/bash
#
#   run some basic tests for the gramps-frontend
#
# NB: these tests are run from the source directory for now
#

CFG="config.cfg"
DEPS="\
	gramps \
	python3-gramps-webapi \
	python3-gunicorn \
	python3-torch \
"
API_PORT="5555"

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
for ii in $DEPS
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

# build the source directory -- just like in the spec build and install
mkdir -p pkg-testing
pushd pkg-testing
NPM_NAME="gramps-js"
VERSION="24.12.2"
SOURCE0="../${NPM_NAME}-${VERSION}.tgz"
SOURCE1="../${NPM_NAME}-${VERSION}-nm-prod.tgz"
SOURCE2="../${NPM_NAME}-${VERSION}-nm-dev.tgz"
#tar --strip-components=1 -xzf ${SOURCE0}
tar xzf ${SOURCE1}
tar xzf ${SOURCE2}
mkdir -p node_modules
pushd node_modules
ln -s ../node_modules_prod/* .
ln -s ../node_modules_prod/.bin .
popd

# so far, we've just built a possible runtime environment.  now, let's
# try to use it by starting the webapi and then the frontend
#
# build a config file
if [ -f $CFG ]
then
	echo "? existing $CFG file found, will not overwrite, continuing ..."
fi

# create an empty testing family tree
TREENAME="XYZZY Gramps Testing Only Family Tree XYZZY"
echo yes | gramps -r "$TREENAME"
cp ../run_api.sh .
cp ../data.gramps .
gramps -C "$TREENAME" -i data.gramps

# here doc might be better .... just lazy this time ...
echo "TREE=\"${TREENAME}\"" > $CFG
echo "BASE_URL=\"https://localhost\"" >> $CFG
echo "SECRET_KEY=\"my secret key\"" >> $CFG
echo "USER_DB_URI=\"sqlite:////tmp/gramps_frontend_test.sqlite\"" >> $CFG
echo "EMAIL_HOST=\"localhost\"" >> $CFG
echo "EMAIL_PORT=\"25\"" >> $CFG
echo "EMAIL_USE_TLS=False" >> $CFG
echo "EMAIL_USER=\"root@localhost\"" >> $CFG
echo "EMAIL_HOST_PASSWORD=\"\"" >> $CFG
echo "DEFAULT_FROM_EMAIL=\"gramps@localhost\"" >> $CFG

# try to run web api ....
gunicorn -w 2 -b 0.0.0.0:$API_PORT gramps_webapi:app --timeout 120 --limit-request-line 8190 &
api_pid=$!

# ... and if you've gotten this far, we can at least bring up the webapi
# now, try the frontend ....

# cleanup
kill $api_pid
