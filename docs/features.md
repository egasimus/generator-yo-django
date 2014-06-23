Features
===

This is a list of all the currently supported or planned features of yo-django, roughly corresponding to some of the choices you might be offered when running the generator itself.

Web frameworks
---

* **Django** &mdash; http://www.djangoproject.com

#### Django project templates
* **modern** &mdash; My current go-to project setup, refined from [nigma's *django-modern-template*](https://github.com/nigma/django-modern-template).
* `todo` **basic** &mdash; The default Django setup, as created by `manage.py startproject`.
* `todo` **mini** &mdash; A lightweight project not necessarily needing a database, inspired by [Syte](https://github.com/rigoneri/syte) and [Meghan Blanchette's *Simplifying Django*](http://radar.oreilly.com/2014/04/simplifying-django.html?utm_source=Python+Weekly+Newsletter&utm_campaign=ef1c091c06-Python_Weekly_Issue_135_April_17_2014&utm_medium=email&utm_term=0_9e26887fc5-ef1c091c06-312699433).

#### Django features and niceties
* `todo` **Social authentication**
* `todo` Custom **user model**
* `todo` Custom **admin site**
* `todo` Custom **permissions** with [Authority](https://github.com/jezdez/django-authority)
* `toto` **APIs** with [Django REST framework](http://www.django-rest-framework.org/) and [Tastypie](http://tastypieapi.org/)

Databases and services
---

* [**PostgreSQL**](http://www.postgresql.org)
* [**memcached**](http://memcached.org/)
* `wip` [**MySQL**](http://www.mysql.com/)
* `todo` [**SQLite**](http://www.sqlite.org/)
* `todo` [**MongoDB**](http://django-nonrel.org/)
* `todo` [**redis**](http://redis.io/)

Infrastructure
---

* [**Fabric**](http://www.fabfile.org/) is my management tool of choice which allows complex operations to be automated with single commands.
* [**Vagrant**](http://www.vagrantup.com) &mdash; a convenient solution for automated management of virtual machines.

#### Vagrant providers
* [**VirtualBox**](https://www.virtualbox.org/) &mdash; a free virtualization engine from Oracle.
* `todo` [**AWS**](https://github.com/mitchellh/vagrant-aws) &mdash; a major goal of yo-django is to generate projects which can be deployed to cloud services with minimum fuss.
* `todo` [**Docker**](http://www.docker.com) &mdash; a containerization engine for Linux which offers most of the benefits of a virtual server for your app without incurring the significant resource overhead of a full-blown VM.

#### Vagrant provisioners
* **shell** &mdash; Most of what's currently going on is currently glued together by this sketchy shell script that took me a while to get right. This isn't particularly convenient for medium to large projects, therefore I'd like to eventually migrate to...
* `wip` [**Puppet**](https://docs.vagrantup.com/v2/provisioning/puppet_apply.html)
* `todo` [**Chef**](https://docs.vagrantup.com/v2/provisioning/ansible.html)
* `todo` [**Ansible**](https://docs.vagrantup.com/v2/provisioning/ansible.html)
