# Define environment variables and make them persist
export DJANGO_SETTINGS_MODULE=<%= projectName %>.conf.dev
export DB_PASSWORD=password
export SECRET_KEY=sdgjwe-94rth9*g--G98G08g08045ccc.....sdfwYH54hfhaty5yeao0-
echo "
DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
DB_PASSWORD=$DB_PASSWORD
SECRET_KEY=$SECRET_KEY" | tee -a /etc/environment


# Create system user and group
groupadd <%= projectGroup %>
useradd <%= projectUser %> -g <%= projectGroup %> || usermod s4c -g <%= projectGroup %>
useradd vagrant -G <%= projectGroup %> || usermod vagrant -G <%= projectGroup %>
useradd ubuntu -G <%= projectGroup %> || usermod ubuntu -G <%= projectGroup %>


# Alias /vagrant as /www/s4c-cms
mkdir /www && ln -s /vagrant <%= wwwDir %>


# Install various app requirements
apt-get update -q -y && apt-get install -q -y uwsgi uwsgi-plugin-python
pip install --requirement <%= wwwDir %>/app-requirements.txt


# Prepare app's static, media, and log directories.
mkdir -p /www/media /www/static /var/log/s4c
chmod 774 /www/media /www/static /var/log/s4c
chown <%= projectUser %>:<%= projectGroup %> /www/media


# Prepare log files.
touch /var/log/s4c/app.log /var/log/s4c/db.log \
      /var/log/s4c/request.log /var/log/s4c/test.log
chown --recursive s4c:s4c /var/log/s4c
chmod 664 /var/log/s4c/*


# Collect static files and set permissions
python /www/s4c-cms/manage.py collectstatic -c --noinput
chown --recursive s4c:s4c /www/static
find /www/static -type f -exec chmod 664 {} +


# Create a MySQL database and user
mysql -u root --password=thisisthedefaultmysqlrootpassword -e \
    "CREATE DATABASE s4c DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;"

mysql -u root --password=thisisthedefaultmysqlrootpassword -e \
    "GRANT ALL PRIVILEGES ON s4c.* To 's4c'@'localhost' IDENTIFIED BY '$DB_PASSWORD';"


# Install PhantomJS
# curl -s https://phantomjs.googlecode.com/files/phantomjs-1.9.2-linux-x86_64.tar.bz2 | tar --no-anchored -xj bin/phantomjs -O > /usr/bin/phantomjs
# chmod 777 /usr/bin/phantomjs


# Install and configure nginx and uwsgi
usermod www-data -G s4c || useradd www-data -G s4c
usermod nginx -G s4c || useradd nginx -G s4c
useradd uwsgi -G s4c || usermod uwsgi -G s4c
mkdir -p /var/log/uwsgi
chmod 774 /var/log/s4c /var/log/nginx /var/log/uwsgi
chown --recursive nginx:s4c /var/log/nginx
chown --recursive uwsgi:s4c /var/log/uwsgi


# Create database and Postgres user
# sudo -u postgres createdb s4c -E=utf8
# sudo -u postgres createuser s4c -d


# Sync DB and load initial data
python /www/s4c-cms/manage.py syncdb --noinput
python /www/s4c-cms/manage.py migrate


# Upload crontab
cp /www/s4c-cms/deploy/crontab.conf /etc/cron.d/s4c


# Configure and launch uWSGI
cp /vagrant/deploy/uwsgi_upstart.conf /etc/init/uwsgi.conf
chmod 0644 /etc/init/uwsgi.conf
mkdir -p /etc/uwsgi/vassals
chmod 770 /etc/uwsgi/vassals
chown --recursive uwsgi:s4c /etc/uwsgi/vassals
ln -s /vagrant/deploy/uwsgi_dev.ini /etc/uwsgi/vassals/s4c-cms.ini
service uwsgi restart


# Configure and launch nginx
ln -s /vagrant/deploy/nginx_dev.conf /etc/nginx/sites-available/s4c-cms
ln -s /etc/nginx/sites-available/s4c-cms /etc/nginx/sites-enabled/
unlink /etc/nginx/sites-enabled/default
service nginx restart
