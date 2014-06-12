'use strict';
var util = require('util');
var path = require('path');
var yeoman = require('yeoman-generator');
var yosay = require('yosay');
var chalk = require('chalk');



var DjangoEgasimusGenerator = yeoman.generators.Base.extend({


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
              message: 'Project name? ' +
                       '[a valid, non-clashing name for your new Python module]', },

            { type:    'input',
              name:    'djangoVersion',
              message: 'Django version to use?',
              default: '1.6.6', },

            { type:    'input',
              name:    'baseBoxURL',
              message: 'URL for base Vagrant box?',
              default: 'https://s3-eu-west-1.amazonaws.com/egasimus-vm-images/' +
                       'ubuntu-12.04.4-server-amd64.box' },

            { type:    'input',
              name:    'hostIP',
              message: 'Host IP? [only visible to your own computer]',
              default: '33.33.33.1', },

            { type:    'confirm',
              name:    'hasDatabase',
              message: 'Will you be needing a database?',
              default: true, },

            { type:    'list',
              name:    'dbType',
              message: 'What database do you need set up?',
              choices: ['PostgreSQL', 'MySQL'],
              default: 'PostgreSQL', },

            { type:    'input',
              name:    'dbName',
              message: 'Database name?', },

            { type:    'input',
              name:    'dbPassword',
              message: 'Database root password?', },

            { type:    'confirm',
              name:    'fix12879',
              message: 'Are you using VirtualBox 4.3.10? (fixes VB#12879)',
              default: false }, ];

        this.prompt(prompts, function (props) {
            this.answers = props;
            this.answers.wwwDir = '/www/' + props.projectName;
            this.answers.logDir = '/var/log/' + props.projectName;
            
            this.answers.projectUser = this.answers.projectGroup =
            this.answers.baseBoxName =
            this.answers.dbName = this.answers.dbUser = props.projectName;
            
            this.answers.secretKey = self._secretKey(96);
            done();
        }.bind(this));
    },


    app: function () {
        //this.sourceRoot('./templates');
   
        var t = ['fabfile.py',
                 'Vagrantfile',
                 'provision.sh'
                ]

        for (var i = 0; i < t.length; i++) {
            this.log('Generating ' + t[i]);
            this.template('_' + t[i],  t[i], this.answers);
        }

        this.copy('manage.py', 'manage.py');
        /*
        this.copy('README', 'README');
        this.copy('requirements.txt', 'requirements.txt');
        this.copy('Vagrantfile', 'Vagrantfile');
        this.copy('wsgi.py', 'wsgi.py');

        this.mkdir('deploy');
        this.mkdir('docs');
        this.mkdir('fixtures');
        this.mkdir('libs');
        this.mkdir('locale');
        this.mkdir('packer');
        this.mkdir(this.answers.projectName);*/
    },


    projectfiles: function () {}

});


module.exports = DjangoEgasimusGenerator;
