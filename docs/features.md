Features
===

This is a list of all the currently supported or planned features of yo-django, roughly corresponding to some of the choices you might be offered when running the generator itself.

### Web frameworks
* **Django** &mdash; http://www.djangoproject.com

#### Django project templates
* **modern** *(default)* &mdash; My current go-to project setup, refined from [nigma's *django-modern-template*](https://github.com/nigma/django-modern-template).

 Its main distinguishing feature is an `apps/` dir in the project root, which is then added to the PYTHONPATH so you can `import myapp` rather than `import apps.myapp`.

##### To do:
* **basic** *(todo)* &mdash; The default Django setup, as created by
  `manage.py startproject`.
* **mini** *(todo)* &mdash; A lightweight project not necessarily needing a database,
  inspired by [Syte](https://github.com/rigoneri/syte) and [Meghan Blanchette's *Simplifying Django*](http://radar.oreilly.com/2014/04/simplifying-django.html?utm_source=Python+Weekly+Newsletter&utm_campaign=ef1c091c06-Python_Weekly_Issue_135_April_17_2014&utm_medium=email&utm_term=0_9e26887fc5-ef1c091c06-312699433).

### Virtualization
* [**Vagrant**](http://www.vagrantup.com) &mdash; a convenient solution for automated management of virtual machines.

#### Vagrant providers
* [**VirtualBox**](https://www.virtualbox.org/) &mdash; a free virtualization engine from Oracle.

##### To do:
* [**Docker**](http://www.docker.com) *(todo)* &mdash; a containerization engine for Linux which gives you the benefits of an isolated work environment without the overhead of a full-blown WM