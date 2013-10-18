#!/usr/bin/env python

import os

INDEX_HTML="""<!DOCTYPE html>
<html ng-app="%(app)s">

<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="shortcut icon" type="image/png" href="/images/favicon.png">

    <title>%(app)s</title>
    <!-- Bootstrap -->
    <link href="//netdna.bootstrapcdn.com/twitter-bootstrap/%(bootstrap_version)s/css/bootstrap.min.css" rel="stylesheet">
    <!-- Custom styles -->
    <link href="/stylesheets/style.css" rel="stylesheet">
</head>

<body>
    <div class="navbar navbar-inverse navbar-fixed-top">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="#">%(app)s</a>
        </div>
        <div class="collapse navbar-collapse">
          <ul class="nav navbar-nav">
            <li class="active"><a href="#">Home</a></li>
            <li><a href="#about">About</a></li>
            <li><a href="#contact">Contact</a></li>
          </ul>
        </div><!--/.nav-collapse -->
      </div>
    </div>

    <div class="container">
      <div ng-view></div>
    </div>

    <div>Angular ToDo App: v<span app-version></span>

    <!-- Placed at the end of the document so the pages load faster -->
    <script src="//ajax.googleapis.com/ajax/libs/jquery/%(jquery_version)s/jquery.min.js"></script>
    <script src="//netdna.bootstrapcdn.com/twitter-bootstrap/%(bootstrap_version)s/js/bootstrap.min.js"></script>
    <script src="//ajax.googleapis.com/ajax/libs/angularjs/%(angularjs_version)s/angular.js"></script>
    <script src="//ajax.googleapis.com/ajax/libs/angularjs/%(angularjs_version)s/angular-route.js"></script>
    <script src="//ajax.googleapis.com/ajax/libs/angularjs/%(angularjs_version)s/angular-resource.js"></script>
    <script src="javascripts/app.js"></script>
    <script src="javascripts/services.js"></script>
    <script src="javascripts/controllers.js"></script>
    <script src="javascripts/filters.js"></script>
    <script src="javascripts/directives.js"></script>
</body>

</html>
"""

APP_JS="""'use_strict';

/* Declare app level module which depends on filters, and services */
var app = '%(app)s';
angular.module(app, ['ngRoute',
    app + '.filters',
    app + '.services',
    app + '.directives',
    app + '.controllers'
])
    .config(['$routeProvider',
        function ($routeProvider) {
            $routeProvider.when('/', {
                templateUrl: 'partials/main.html',
                controller: 'MainCtrl'
            });
            $routeProvider.otherwise({
                redirectTo: '/'
            });
        }
    ]);
"""

CONTROLLERS_JS="""'use strict';

/* Controllers */
angular.module(app + '.controllers', [])
    .controller('MainCtrl', ['$scope',
        function ($scope) {}
    ]);
"""

FILTERS_JS="""'use strict';

/* Filters */
angular.module(app + '.filters', [])
    .filter('interpolate', ['version',
        function (version) {
            return function (text) {
                return String(text).replace(/\\%%VERSION\\%%/mg, version);
            }
        }
    ]);
"""

SERVICES_JS="""'use strict';

/* Services */
angular.module(app + '.services', ['ngResource'])
    .value('version', '0.1')
    .factory('Conf', function ($location) {
        return {
            'apiBase': '/api',
        }
    })
    .factory('Tasks', function ($resource, Conf) {
        return $resource(Conf.apiBase + '/tasks/:id', {}, {
            add: {
                method: 'POST',
                isArray: true
            }
        });
    });
"""

DIRECTIVES_JS="""'use strict';

/* Directives */
angular.module(app + '.directives', [])
    .directive('appVersion', ['version',
        function (version) {
            return function (scope, elm, attrs) {
                elm.text(version);
            };
        }
    ]);
"""

MAIN_HTML="""<div class="jumbotron">
  <h1>Hello, world!</h1>
  <p>This is a simple hero unit, a simple jumbotron-style component for
  calling extra attention to featured content or information.</p>
  <p><a class="btn btn-primary btn-lg">Learn more</a></p>
</div>
"""

STYLE_CSS="""body {
  padding-top: 100px;
}
"""

def write(filename, content):
  f = open(filename, 'w')
  f.write(content)
  f.close()

def makedirs(path):
  if not os.access(path, os.F_OK) or not os.path.isdir(path):
    os.makedirs(path)

def code_generate(app, angularjs_version,
    bootstrap_version, jquery_version):
  makedirs('javascripts')
  makedirs('partials')
  makedirs('stylesheets')

  write('index.html', INDEX_HTML % locals())
  write('javascripts/app.js', APP_JS % locals())
  write('javascripts/filters.js', FILTERS_JS % locals())
  write('javascripts/services.js', SERVICES_JS % locals())
  write('javascripts/directives.js', DIRECTIVES_JS % locals())
  write('javascripts/controllers.js', CONTROLLERS_JS % locals())
  write('partials/main.html', MAIN_HTML % locals())
  write('stylesheets/style.css', STYLE_CSS % locals())

DEFAULT_ANGULARJS_VERSION = '1.2.0-rc.3'
DEFAULT_BOOTSTRAP_VERSION = '3.0.0'
DEFAULT_JQUERY_VERSION = '2.0.3'

if __name__ == '__main__':
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument('app', help='the name of the AngularJS App')
  parser.add_argument('--angularjs_version', help='the version of AngularJS',
      default=DEFAULT_ANGULARJS_VERSION)
  parser.add_argument('--bootstrap_version', help='the version of Twitter Bootstrap',
      default=DEFAULT_BOOTSTRAP_VERSION)
  parser.add_argument('--jquery_version', help='the version of JQuery',
      default=DEFAULT_JQUERY_VERSION)

  args = parser.parse_args()
  code_generate(args.app,
      args.angularjs_version,
      args.bootstrap_version,
      args.jquery_version)
