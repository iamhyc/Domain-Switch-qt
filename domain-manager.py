#!/usr/bin/python
import runpy
from sys import argv
from functools import partial
from helper.PathHelper import *
from helper.ConfigHelper import load_json

def m_init():
	global global_var, work_dir, config
	global_var = {}

	work_dir = fileDirPath(__file__)
	config = load_json(pathShift(work_dir, 'config.json'))

	global_var.update({'VDM_ENV':		config})
	global_var.update({'__user_dir__':	currentPath()})
	global_var.update({'__work_dir__':	fileDirPath(__file__)})
	global_var.update({'userShift':		partial(pathShift, currentPath())})
	global_var.update({'workShift':		partial(pathShift, work_dir)})
	pass

def main():
	func_map = {
		'plugin': 'plugin-manager.pyc'
	}

	with workSpace(pathShift(work_dir, 'manager')) as wrk:
		if len(argv)>1 and func_map.has_key(argv[1]):
			global_var.update({'argv':	argv[2:]})
			runpy.run_path(func_map[argv[1]],
							global_var, '__main__')
			pass
		else:
			global_var.update({'argv':	argv})
			global_var.update({'CFG':	partial(pathShift, 
				fileFullPath(config['config-dir']))})
			runpy.run_path('manager.pyc',
							global_var, '__main__')
			pass
		pass
	pass

if __name__ == '__main__':
	m_init()
	try: #cope with Interrupt Signal
		main()
	except Exception as e:
		print(e) #for debug
	finally:
		exit()