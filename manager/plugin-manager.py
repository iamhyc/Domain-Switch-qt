#!/usr/bin/python
"""
Plugin Manager
@author: Mark Hong
#call: temporarily register
#install: cp plugin files to install dir
"""
import plugins
from optparse import OptionParser
from helper.ImportHelper import *
from helper.PathHelper import *
from helper.PrintHelper import *
from helper.ConfigHelper import *
from functools import partial

def main():
	global IMPORT_ENV
	printh('Plugin Manager', 'main')
	print([__user_dir__, __work_dir__, currentPath()])

	IMPORT_ENV.append(workShift('helper'))
	require('PrintHelper', 'printh')("test", "require test")
	
	PluginProxy = require("PluginProxy")
	imp = require('ImportHelper').require_cur
	imp_cur = partial(imp, this=PluginProxy)
	PluginProxy.__dict__.update({'require':require, 'required':imp_cur})
	PluginProxy.PluginProxy()
	pass

if __name__ == '__main__':
	global options
	parser = OptionParser()
	parser.add_option("-l", "--list",
		action="store_true",
		dest="list_flag", 
		default=False, 
		help="list all plugins.")
	parser.add_option("-q", "--quiet",
		action="store_true",
		dest="verbose", 
		default=False, 
		help="silient without debug information")
	parser.add_option("-a", "--add",
		dest="plugin_name", 
		default="", 
		help="install a new plugin from PWD")
	parser.add_option("-r", "--remove",
		dest="plugin_name", 
		default="", 
		help="remove an existing plugin")
	parser.add_option("-d", "--debug",
		dest="plugin_name", 
		default="", 
		help="test environment for developing plugin")

	(options, args) = parser.parse_args()
	main()