Django 1.6 Yak Shave
==============

Tool for starting (setting) up Django 1.6 projects with best practices (wrote for my personal use in linux). 

Usage:
Once this package is installed, go to any directory and simply follow the below command (just like $ django-admin.py startproject mysite), 

<!-- language:console -->

	$ django-yak-shave.py startproject mysite

For creating a project at a particular directory use optional destination option '-d' option.

<!-- language:console -->

	$ django-yak-shave.py startproject mysite -d=/user/dusk/Code/myproject


For creating a project from existing template from local or Github using the option '--template' just like when using 'django-admin.py'.

<!-- language:console -->

	$ django-yak-shave.py startproject --template=/user/dusk/Code/myproject/my_project_template myproject
	$ django-yak-shave.py startproject --template=https://github.com/githubuser/django-project-template/archive/master.zip myproject

The above will result in creating a Django project with the below structure (some people don't need media directory, they can say "no" when the script asks them "do you want to create settings for media directory! (yes or no):").

<!-- language:console -->

	mysite/
	    manage.py
	    media
	    static
	    templates
	    mysite/
	        __init__.py
	        urls.py
	        wsgi.py
	        settings/
	            __init__.py
	            base.py
	            local.py
	            production.py
	            staging.py
	            test.py
