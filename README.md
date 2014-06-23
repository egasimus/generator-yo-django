Yo, Django!
===

[insert relevant gif of Jamie Foxx turning around]

Introduction
---

[Django](https://www.djangoproject.com/) is freaking *great*. So is [Vagrant](http://www.vagrantup.com/). However, one of the main difficulties that I encounter in my day-to-day work as a Django developer involve setting up a project, as well as deploying what I build to an actual production server. Both involve a fair share of, well, *bureaucracy*, and I am embarrased to say that, for me, starting a new Django project usually involves copying over a previous one and deleting all irrelevant bits, then hoping nobody sees those few instances of the old project's name that I only notice after a few commits.

The time we save by writing high-level abstractions in a sane programming language, compared to old-fashioned PHP, we lose in deploying to our own platform of choice. This is where [Yeoman](http://yeoman.io/) comes in. Answer a bunch of questions at an user-friendly console interface and get the scaffolding for a full-blown, production-ready, [twelve-factor](http://12factor.net/)-conformant modern Web application, so you can immediately get started writing business logic -- what could be better than that?

Project status
---

This project is in a pre-alpha stage right now; that said, as long as you stick to the default options, you should end up with something working. However, I currently have little time to develop things beyond my own preferred setup. This is why I am hoping the community will pick this up and implement any features they would like to see.

Current goals
---

* Get MySQL running.
* Re-implement at least the default setup in [Puppet](http://puppetlabs.com/).
