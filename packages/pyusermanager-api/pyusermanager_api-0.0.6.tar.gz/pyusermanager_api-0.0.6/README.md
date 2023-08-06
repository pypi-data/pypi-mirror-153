This Project implements api routes for the pyusermanager

# Changelog

## v0.0.6

* min lenght for groups is now 1 char

## v0.0.3

* implements changes from pyusermanager v2.0.7
* now defines app.ctx.AuthProvider so other modules can use it
* instead of using api_misc.is_logged_in or api_misc.is_in_group now uses app.ctx.AuthProvider

## v0.0.2

* implements changes from pyusermanager v2.0.6