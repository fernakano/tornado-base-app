Base Tornado App seed for dead simple projects.
==========================================

Tornado base app is (as its name suggests) a tornado app which do all the boring stuff for you.

It provides a couple os simple features.

* Simple Template Rendering
* Serve static files
* Simple http request
* Simple websocket creation

To install requirements use:  

	pip install -r requirements.txt

To configure the app edit:
	
	app.yaml
	
Usage (default settings):

    ./app.py

If you use stuff like Twitter's OAuth, you may have different settings in production and in development.

    ./app.py --version=version

Will override default settings with extra settings.


