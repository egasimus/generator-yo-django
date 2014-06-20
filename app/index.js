'use strict';
var util = require('util');
var path = require('path');
var yeoman = require('yeoman-generator');
var yosay = require('yosay');
var chalk = require('chalk');



var YoDjangoGenerator = yeoman.generators.Base.extend({


    init: function () {},


    _secretKey: function(length) {
        var mask = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ' +
                   '0123456789~`!@#$%^&*()_+-={}[]:;<>?,./|',
            result = '';
    
        for (var i = length; i > 0; --i)
            result += mask[Math.round(Math.random() * (mask.length - 1))];
        return result;
    },


    askFor: function () {
        var self = this;
        var done = this.async();

        this.log(yosay('Uh, hi? I\'m the "django-egasimus" generator you asked for...'));
        this.log(yosay('...and I\'m going to set up your Django+Vagrant project...'));
        this.log(yosay('...because fuck you, that\'s why.'));

        var prompts = [
          { type:    'input',
            name:    'projectName',
            message: 'Project name?', },

          { type:    'list',
            name:    'projectType',
            message: 'Project type?',
            choices: ['mini', 'modern', 'default'],
            default: 'modern' },

          { type:    'input',
            name:    'djangoVersion',
            message: 'Django version to use?',
            default: '1.6.5', },

          { type:    'input',
            name:    'baseBoxURL',
            message: 'URL for base Vagrant box?',
            default: 'https://oss-binaries.phusionpassenger.com/vagrant/' +
                     'boxes/latest/ubuntu-14.04-amd64-vbox.box' },

          { type:    'input',
            name:    'hostIP',
            message: 'IP for virtual machine? [only visible to your own computer]',
            default: '6.6.6.2', },

          { type:    'list',
            name:    'provisioner',
            message: 'Provision VM using:',
            choices: ['shell', 'puppet'],
            default: 'shell', },

          { type:    'list',
            name:    'server',
            message: 'Your server of choice:',
            choices: ['nginx', 'apache'],
            default: 'nginx', },

          { type:    'confirm',
            name:    'hasDatabase',
            message: 'Will you be needing a database?',
            default: true, },

          { type:    'confirm',
            name:    'fix12879',
            message: 'Are you using VirtualBox 4.3.10? (fixes VB#12879)',
            default: false }, ];

        this.prompt(prompts, function (props) {
            this.answers = props;

            this.answers.wwwDir = '/www/' + props.projectName;
            this.answers.logDir = '/var/log/' + props.projectName;
            
            this.answers.projectUser = this.answers.projectGroup =
            this.answers.baseBoxName = props.projectName;
            
            this.answers.secretKey = self._secretKey(96);

            if (props.hasDatabase) {
                 var dbPrompts = [
                   { type:    'list',
                     name:    'dbType',
                     message: 'DB: What database do you need?',
                     choices: ['postgres', 'mysql'],
                     default: 'postgres', },
 
                   { type:    'input',
                     name:    'dbName',
                     message: 'DB: Database name?',
                     default: this.answers.projectName},
 
                   { type:    'input',
                     name:    'dbUser',
                     message: 'DB: Database username?',
                     default: this.answers.projectName},

                   { type:    'input',
                     name:    'dbPassword',
                     message: 'DB: Database root password? [insecure]',
                     default: this.answers.projectName}, ];

                this.prompt(dbPrompts, function (dbProps) {
                    this.answers.dbType     = dbProps.dbType;
                    this.answers.dbUser     = dbProps.dbUser;
                    this.answers.dbName     = dbProps.dbName;
                    this.answers.dbPassword = dbProps.dbPassword;
                    done();
                }.bind(this)); }
            else done();

        }.bind(this));
    },


    app: function () {
   
        var t = ['fabfile.py',
                 'Vagrantfile',
                 'provision.sh',
                 'requirements.txt',
                 'wsgi.py',
                 'README',
                 'deploy/nginx.conf',
                 'manifests/default.pp',
                 ];

        if (this.answers.provisioner == 'puppet')
            t.push('manifests/default.pp');

        var c = ['manage.py',
                 'deploy/uwsgi_upstart.conf'],

            d = ['deploy',
                 'docs',
                 'fixtures',
                 'libs',
                 'locale',
                 'manifests',
                 this.answers.projectName];

        for (var i = 0; i < d.length; i++) {
            this.mkdir(d[i]);
        }

        for (var i = 0; i < t.length; i++) {
            this.log('Generating ' + t[i]);
            var n = t[i].split('/');
            n[n.length-1] = '_' + n[n.length-1];
            this.template(n.join('/'), t[i], this.answers);
        }

        for (var i = 0; i < c.length; i++) {
            this.copy(c[i], c[i]);
        }

    },


    projectfiles: function () {}

});


module.exports = YoDjangoGenerator;
