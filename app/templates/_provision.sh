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
useradd <%= projectUser %> -g <%= projectGroup %> || usermod <%= projectUser %> -g <%= projectGroup %>
useradd vagrant -G <%= projectGroup %> || usermod vagrant -G <%= projectGroup %>
useradd ubuntu -G <%= projectGroup %> || usermod ubuntu -G <%= projectGroup %>


# Alias /vagrant as <%= wwwDir %>
mkdir /www && ln -s /vagrant <%= wwwDir %>


# Update package cache
apt-get update -q -y


# Install various app requirements
apt-get install -q -y python python-pip
pip install --upgrade pip
ln -s /usr/local/bin/pip /usr/bin/pip
pip install --requirement <%= wwwDir %>/requirements.txt


# Prepare app's static, media, and log directories.
mkdir -p /www/media /www/static <%= logDir %>
chmod 774 /www/media /www/static <%= logDir %>
chown <%= projectUser %>:<%= projectGroup %> /www/media


# Prepare log files.
touch <%= logDir %>/app.log <%= logDir %>/db.log \
      <%= logDir %>/request.log <%= logDir %>/test.log
chown --recursive <%= projectUser %>:<%= projectGroup %> <%= logDir %>
chmod 664 <%= logDir %>/*


# Collect static files and set permissions
python <%= wwwDir %>/manage.py collectstatic -c --noinput
chown --recursive <%= projectUser %>:<%= projectGroup %> /www/static
find /www/static -type f -exec chmod 664 {} +


<% if (dbType == 'mysql') { %>
# Create a MySQL database and user
mysql -u root --password=thisisthedefaultmysqlrootpassword -e \
    "CREATE DATABASE <%= dbName %> DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;"

mysql -u root --password=thisisthedefaultmysqlrootpassword -e \
    "GRANT ALL PRIVILEGES ON <%= dbName %>.* To '<%= dbUser %>'@'localhost' IDENTIFIED BY '$DB_PASSWORD';"
<% } %>


<% if (dbType == 'postgres') { %>
# Create database and Postgres user
sudo -u postgres createdb <%= dbName %> -E=utf8
sudo -u postgres createuser <%= dbUser %> -d
<% } %>


# Install PhantomJS
# curl -s https://phantomjs.googlecode.com/files/phantomjs-1.9.2-linux-x86_64.tar.bz2 | tar --no-anchored -xj bin/phantomjs -O > /usr/bin/phantomjs
# chmod 777 /usr/bin/phantomjs



# Install and configure nginx and uwsgi
usermod www-data -G <%= projectGroup %> || useradd www-data -G <%= projectGroup %>
usermod nginx -G <%= projectGroup %> || useradd nginx -G <%= projectGroup %>
useradd uwsgi -G <%= projectGroup %> || usermod uwsgi -G <%= projectGroup %>
mkdir -p /var/log/uwsgi
chmod 774 <%= logDir %> /var/log/nginx /var/log/uwsgi
chown --recursive nginx:<%= projectGroup %> /var/log/nginx
chown --recursive uwsgi:<%= projectGroup %> /var/log/uwsgi



# Sync DB and load initial data
python <%= wwwDir %>/manage.py syncdb --noinput
python <%= wwwDir %>/manage.py migrate


# Upload crontab
cp <%= wwwDir %>/deploy/crontab.conf /etc/cron.d/<%= projectName %>


# Configure and launch uWSGI
cp /vagrant/deploy/uwsgi_upstart.conf /etc/init/uwsgi.conf
chmod 0644 /etc/init/uwsgi.conf
mkdir -p /etc/uwsgi/vassals
chmod 770 /etc/uwsgi/vassals
chown --recursive uwsgi:<%= projectGroup %> /etc/uwsgi/vassals
ln -s /vagrant/deploy/uwsgi_dev.ini /etc/uwsgi/vassals/<%= projectName %>.ini
service uwsgi restart


# Configure and launch nginx
ln -s /vagrant/deploy/nginx_dev.conf /etc/nginx/sites-available/<%= projectName %>
ln -s /etc/nginx/sites-available/<%= projectName %> /etc/nginx/sites-enabled/
unlink /etc/nginx/sites-enabled/default
service nginx restart
