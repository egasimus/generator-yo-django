'use strict';
var util = require('util');
var path = require('path');
var yeoman = require('yeoman-generator');
var yosay = require('yosay');
var chalk = require('chalk');
var prettyjson = require('prettyjson');


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
            name:    'baseBoxName',
            message: 'Name of base Vagrant box?', // todo include output
            default: 'yo-django'                  // of vagrant box list 

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
            message: 'HTTP server:',
            choices: ['nginx', 'apache'],
            default: 'nginx', },

          { type:    'list',
            name:    'wsgi',
            message: 'WSGI app server:',
            choices: ['uwsgi', 'gunicorn'],
            default: 'uwsgi' },

          { type:    'list',
            name:    'cache',
            message: 'Cache server:',
            choices: ['none', 'memcached'],
            default: 'memcached' },

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
            
            this.answers.projectUser = this.answers.projectGroup = props.projectName;
            
            this.answers.secretKey = self._secretKey(128);

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

        var answers = this.answers;

        this.log(prettyjson.render(answers));

        // Make directories

        var p = function(dir) {return answers.projectName + '/' + dir}
        
        var d = ['config',
                 'docs',
                 'fixtures',
                 'libs',
                 'locale',
                 p(''),
                 p('apps'),
                 p('conf'),
                 p('static'),
                 p('template'),
                ];

        if (answers.provisioner === 'puppet')
            d = d.concat(['manifests']);

        for (var i = 0; i < d.length; i++) this.mkdir(d[i]);

        // Process templates
    
        var t = ['fabfile.py',
                 'Vagrantfile',
                 'requirements.txt',
                 'wsgi.py',
                 'README',
                 'project/conf/base.py',
                 'project/conf/dev.py'];

        if (answers.provisioner === 'puppet')
            t = t.concat(['manifests/default.pp']);

        if (answers.provisioner === 'shell')
            t = t.concat(['provision.sh']);

        if (answers.provisioner === 'server');
            t = t.concat(['config/nginx.conf']);

        for (var i = 0; i < t.length; i++) {
            this.log('Generating ' + t[i]);
            var n  = t[i].split('/'),
                n2 = t[i].split('/');
            n[n.length-1] = '_' + n[n.length-1];
            if (n2[0] === 'project') n2[0] = answers.projectName;
            this.template(n.join('/'), n2.join('/'), answers);
        }

        // Copy rest of files

        var c = ['__init__.py',
                 'manage.py',
                 'project/apps.pth',
                 'project/__init__.py',
                 'project/urls.py',
                 'project/conf/__init__.py'];

        if (answers.wsgi === 'uwsgi')
            c = c.concat(['config/uwsgi_upstart.conf',]);

        if (answers.dbType === 'postgres')
            c = c.concat(['config/pg_hba.conf',
                          'config/postgresql.conf',]);

        for (var i = 0; i < c.length; i++) {
            var n = c[i].split('/');
            if (n[0] === 'project') n[0] = answers.projectName;
            this.copy(c[i], n.join('/'));
        }

    },


    projectfiles: function () {}

});


module.exports = YoDjangoGenerator;
