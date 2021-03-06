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
apt-get update -qy


# Install installers
apt-get install -qy python python-dev python-pip software-properties-common
pip install --upgrade pip
ln -s /usr/local/bin/pip /usr/bin/pip


# Add extra PPAs and update again
<% if (server === 'nginx') { %>
apt-add-repository -y ppa:nginx/development
<% } %>
<% if (wsgi === 'uwsgi') { %>
apt-add-repository -y ppa:chris-lea/uwsgi
<% } %>
apt-get update -qy


# Install selected server
<% if (server === 'nginx') { %>
apt-get install -qy nginx
<% } %>


# Install selected WSGI server
<% if (wsgi === 'uwsgi') { %>
apt-get install -qy uwsgi 
cp /vagrant/config/uwsgi_upstart.conf /etc/init/uwsgi.conf
chmod 0644 /etc/init/uwsgi.conf
mkdir -p /etc/uwsgi/vassals && chmod 770 /etc/uwsgi/vassals
chown --recursive uwsgi:<%= projectGroup %> /etc/uwsgi/vassals
ln -s /vagrant/config/uwsgi_dev.ini /etc/uwsgi/vassals/<%= projectName %>.ini
service uwsgi restart
<% } %>


# Install selected database
<% if (dbType === 'mysql') { %>
echo 'mysql-server mysql-server/root_password password thisisthedefaultmysqlrootpassword' | debconf-set-selections
echo 'mysql-server mysql-server/root_password_again password thisisthedefaultmysqlrootpassword' | debconf-set-selections
apt-get -qy install mysql-server python-mysqldb
mysql -u root --password=thisisthedefaultmysqlrootpassword -e \
    "CREATE DATABASE <%= dbName %> DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;"
mysql -u root --password=thisisthedefaultmysqlrootpassword -e \
    "GRANT ALL PRIVILEGES ON <%= dbName %>.* To '<%= dbUser %>'@'localhost' IDENTIFIED BY '$DB_PASSWORD';"
<% } %>


<% if (dbType === 'postgres') { %>
apt-get -qy install postgresql-9.3 postgresql-client-9.3 libpq-dev
mv /etc/postgresql/9.3/main/postgresql.conf /etc/postgresql/9.3/main/postgresql.conf.old
mv /etc/postgresql/9.3/main/pg_hba.conf /etc/postgresql/9.3/main/pg_hba.conf.old
cp /vagrant/config/postgresql.conf /etc/postgresql/9.3/main/postgresql.conf
cp /vagrant/config/pg_hba.conf /etc/postgresql/9.3/main/pg_hba.conf
service postgresql restart
sudo -u postgres createdb <%= dbName %> -E=utf8
sudo -u postgres createuser <%= dbUser %> -d
<% } %>


<% if (cache === 'memcached') { %>
apt-get -qy install memcached
<% } %>


# Install required Python libraries
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
# cp <%= wwwDir %>/config/crontab.conf /etc/cron.d/<%= projectName %>


# Configure and launch uWSGI

# Configure and launch nginx
ln -s /vagrant/config/nginx.conf /etc/nginx/sites-available/<%= projectName %>
ln -s /etc/nginx/sites-available/<%= projectName %> /etc/nginx/sites-enabled/
unlink /etc/nginx/sites-enabled/default
service nginx restart
