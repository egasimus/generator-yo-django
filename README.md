Yo, Django!
===

[insert relevant gif of Jamie Foxx turning around]

Introduction
---

[Django](https://www.djangoproject.com/) is freaking *great*. So is [Vagrant](http://www.vagrantup.com/). However, one of the main difficulties that I encounter in my day-to-day work as a Django developer involve setting up a new project, as well as deploying what I build to an actual production server. Both involve a fair share of, well, *bureaucracy*, and I am embarrased to say that, for me, starting a new Django project usually involves copying over a previous one and deleting all irrelevant bits, then hoping nobody sees those few instances of the old project's name that I only ever notice after a few commits have gone upstream.

Compared to old-fashioned PHP, the time we save by writing high-level abstractions in a sane programming language, we easily lose in preparing a project that can be deployed to our own platform of choice. This is where [Yeoman](http://yeoman.io/) comes in. Answer a bunch of questions at an user-friendly console interface and get the scaffolding for a full-blown, production-ready, [twelve-factor](http://12factor.net/)-conformant modern Web application, so you can immediately get started writing business logic -- what could be better than that?

Project status
---

This project is in a pre-alpha stage right now; that said, as long as you stick to the default options, you should end up with something working. That's not much, I know. However, I currently have little time to develop things beyond my own preferred setup. This is why I am hoping the brilliant Django community will pick this up and implement the various bits that differ from my own preference. Databases, services, cloud platforms, even other Python frameworks -- you name it. All tickets and pull requests welcome.

See what the defaults are &mdash; and whether they're any good for you &mdash; as well as what's in store for the future at the [features page](https://github.com/egasimus/generator-yo-django/blob/master/docs/features.md).

Current goals
---

* Get MySQL running.
* Re-implement at least the default setup in [Puppet](http://puppetlabs.com/).
