""" 
Copyright 2014 Prabakaran Santhanam

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

	http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import subprocess
import sys

import os
import shutil
import argparse

def main(argv):
	# Creating argparser to parse command line variables
	parser = argparse.ArgumentParser()
	parser.add_argument("startproject", help="start a django project")
	parser.add_argument("project_name", help="name of the django project")
	parser.add_argument("-d", "--d", help="directory")
	parser.add_argument("--template", "-template", help="existing template")
	args = parser.parse_args()

	# Creating Django project
	script = 'django-admin.py'
	#command = 'startproject'
	#project_name = " ".join(sys.argv[2:])
	if args.d and args.template:
		p = subprocess.Popen([script, 
	                       args.startproject, args.project_name, args.d,  
			       "--template="+args.template], 
			       stdout=subprocess.PIPE, 
			       stderr=subprocess.PIPE)
	elif args.d:
		p = subprocess.Popen([script, 
	                       args.startproject, args.project_name, 
			       args.d], 
			       stdout=subprocess.PIPE, 
			       stderr=subprocess.PIPE)
	elif args.template:
		p = subprocess.Popen([script, 
	                       args.startproject, args.project_name, 
			       "--template="+str(args.template)], 
			       stdout=subprocess.PIPE, 
			       stderr=subprocess.PIPE)
	else:
		p = subprocess.Popen([script, 
	                       args.startproject, args.project_name], 
			       stdout=subprocess.PIPE, 
			       stderr=subprocess.PIPE)


	sys.stdout.write("Creating your Django project..... \n")

	out, err = p.communicate()

	if err:
		print "Cleaning everything..... "
		if "django-admin.py" not in err:
			print err
		if args.startproject is not "startproject":
			print "error: unrecognized argument: %s" %(args.startproject)

		print "example command: django-yak-shave.py startproject mysite"
		sys.exit()


	sys.stdout.write("Your Django project created successfully..... \n")

	# Getting cwd from terminal
	if args.d:
		to_walk = os.path.join(os.path.expanduser(args.d), args.project_name)
		walk_dj = list(os.walk(to_walk))
	else:
		p = subprocess.Popen(['pwd'], stdout=subprocess.PIPE)
		outer_dir = p.stdout.readline()[:-1]
		to_walk = os.path.join(outer_dir, args.project_name)
		walk_dj = list(os.walk(to_walk))

	# Setting up settings dir
	if args.d:
		current_dir, dirs, file_list = walk_dj[0]
	else:
		current_dir, dirs, file_list = walk_dj[1]
	file_list.sort()

	settings_dir = os.path.join(current_dir, 'settings')
	settings_file_list = ['__init__.py', 'local.py', 'test.py', 'staging.py', 'production.py']
	standard_file_list = ['__init__.py', 'settings.py', 'urls.py', 'wsgi.py']

	sys.stdout.write("Modifying settings structure..... \n")

	if file_list == standard_file_list:
		os.mkdir(settings_dir)
		shutil.move(os.path.join(current_dir, 'settings.py'), os.path.join(settings_dir, 'base.py'))
		for f in settings_file_list:
			with open(os.path.join(settings_dir, f), 'wb') as temp_file:
				if f == '__init__.py':
					init_to_write = 'from .base import *\n\ntry:\n\tfrom .local import *\nexcept ImportError:\n\tpass'
					temp_file.write(init_to_write) # Should write imports into the file

	sys.stdout.write("successfully created settings directory and respective settings files..... \n")


	# Setting up templates, static & media dirs
	def ask_yes_r_no(prompt, retries=10, complaint='Yes or no, please!'):
		""" Asking user permission to create templates, static & media directories """
		while True:
			ok = raw_input(prompt)
			if ok in ('y', 'ye', 'yes'):
				return True
			if ok in ('n', 'no', 'nop', 'nope'):
				return False
			retries = retries - 1
			if retries < 0:
				raise IOError('Cannot understand your option, so shave yourself the rest of the yak.')
			print complaint


	dir_list = ['static', 'templates', 'media']

	# Reading settings from local template
	local_lines = ["\nSTATICFILES_DIRS = (\n    os.path.join(BASE_DIR, 'static'),\n    )\n", 
						"\n\n# Templates directory\nTEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]\n", 
						"\n\n# Media files\nMEDIA_URL = '/media/'\nMEDIA_ROOT = os.path.join(BASE_DIR, 'media')\n"]

	# This thing breaks when directory is specified 
	# Creating necessary directories and adding settings to local.py
	for directory in dir_list:
		option = ask_yes_r_no("do you want to create settings for "+directory+" directory! (yes or no): ")

		# Writing imports
		if directory == 'static':
			with open(os.path.join(settings_dir, 'local.py'), 'a') as local_settings:
				local_settings.write("import os")
		# Creatings directories
		if option == True:
			os.mkdir(os.path.join(walk_dj[0][0], directory))

			# Writing respective settings to local.py
			with open(os.path.join(settings_dir, 'local.py'), 'a') as local_settings:
				local_settings.write(local_lines[dir_list.index(directory)])

			sys.stdout.write("successfully setup "+directory+" directory(& respective settings). \n")

		elif option == False:
			print "Skipping "+directory+" directory creation & setting up..... "
            

if __name__ == '__main__':
    main(sys.argv)
