#!/bin/bash
#
#   run some basic tests for the gramps-webapi
#

CFG="config.cfg"
DEPS="\
	gramps \
	python3-flask-limiter \
	python3-gramps-ql \
	python3-object-ql \
	python3-sifts \
"
PKGNAME="python-gramps-webapi"

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

# build a config file
if [ -f $CFG ]
then
	echo "? existing $CFG file found, will not overwrite, continuing ..."
fi

# create an empty testing family tree
TREENAME="XYZZY Gramps Testing Only Family Tree XYZZY"
echo yes | gramps -r "$TREENAME"
gramps -C "$TREENAME" -i data.gramps

# here doc might be better .... just lazy this time ...
echo "TREE=\"${TREENAME}\"" > $CFG
echo "BASE_URL=\"https://localhost\"" >> $CFG
echo "SECRET_KEY=\"my secret key\"" >> $CFG
echo "USER_DB_URI=\"sqlite:////tmp/gramps_webapi_test.sqlite\"" >> $CFG
echo "EMAIL_HOST=\"localhost\"" >> $CFG
echo "EMAIL_PORT=\"25\"" >> $CFG
echo "EMAIL_USE_TLS=False" >> $CFG
echo "EMAIL_USER=\"root@localhost\"" >> $CFG
echo "EMAIL_HOST_PASSWORD=\"\"" >> $CFG
echo "DEFAULT_FROM_EMAIL=\"gramps@localhost\"" >> $CFG

# try to run web api ....
# will need to ctrl-c to quit
LANGUAGE=en python3 -O -m gramps_webapi --config $CFG run --port 5555

# ... and if you've gotten this far, we can at least bring up the webapi

# cleanup (don't use -f unless you're sure)
rm -r ./thumbnail_cache
