# initial set up things (one time)
mkvirtualenv twittercoding --python=/usr/bin/python3.4
workon twittercoding
git clone https://github.com/DanBuchan/twittercoding.git
mkdir db_backup

#install application
cd twittercoding
pip install -r requirements

# set up empty db
rm db.sqlite3
python manage.py
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

#find wsgi.py in /home/einarthorsen/twittercoding/twittercoding
#virtualenv at /home/einarthorsen/.virtualenvs/twittercoding/

#In web tab, create new web app, manual config, python 3.4
# 1. Add path to virtualenv
# 2. Click to edit provided .wsgi, delete/comment out the basic wsgi config
#    uncommment django section, update path="", update os.environ,

# back on console edit application settings to set static paths
#  /home/einarthorsen/twittercoding/twittercoding.settings.py
# 1. set DEBUG=false
# 2. set ALLOWED_HOSTS =
# 3. Add STATIC_ROOT = os.path.join(BASE_DIR, "static")
# 4. blank STATIC_PATH

python manage.py collectstatic

#backup a couple of things for later use
cp twittercoding/settings.py ../db_backup/
cp db.sqlite3 ../db_backup/db.sqlite3.empty
# if you want to return the db to an empty state
# cp ~/db_backup/db.sqlite3.empty ~/twittercoding/twittercoding


# return to web tab
# Add static files URL /static/
# Add static files path /home/einarthorsen/twittercoding/static
# Clikc Restart app button
