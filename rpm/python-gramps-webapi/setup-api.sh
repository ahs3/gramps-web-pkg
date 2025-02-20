#!/bin/bash
#
#   set up the environment for the gramps web api
#

if [ -f /etc/sysconfig/gramps-webapi ]
then
	source /etc/sysconfig/gramps-webapi
else
	LANGUAGE=en
	GRAMPSHOME="/usr/share/gramps-web"
fi
export GRAMPSHOME
DATADIR=$GRAMPSHOME
CFG="config/config.cfg"

trap cleanup SIGINT SIGTERM
cleanup () {
	# placeholder for any clean up needed
	echo "cleaning up..."
}

# start building up the environment
[ ! -d $DATADIR ] && mkdir -p $DATADIR
pushd $DATADIR 2>&1 >/dev/null
for ii in config gramps grampsdb indexdir secret static
do
	[ ! -d $DATADIR/$ii ] && mkdir -p $DATADIR/$ii
done

if [ ! -f $CFG ]
then
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

