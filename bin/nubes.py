#!/usr/bin/python3
#
# Virtual Machine Management System
#
# Copyright (c) 2022 Alexei A. Smekalkine <ikle@ikle.ru>
#
# SPDX-License-Identifier: BSD-2-Clause
#

import json, os, random

from subprocess import run, DEVNULL

def runs (*args):
	run (args, stdout = DEVNULL, stderr = DEVNULL)

def runc (*args):
	run (args, stdout = DEVNULL, check = True)

class Config:
	def __init__ (o, root, name):
		o.home = os.environ['HOME']
		o.root = root
		o.name = name

		conf = os.path.join (o.root, o.name + '.json')

		o.vars = json.load (open (conf, 'r'))

class Template (Config):
	def __init__ (o, root, name):
		super().__init__ (root, name)

		if not 'type' in o.vars:
			raise KeyError ('No type specified')

		o.template = os.path.join (o.root, o.vars['type'] + '.xml')

		if not 'g' in o.vars:
			o.vars['g'] = random.randint (16, 255)

		if not 'n' in o.vars:
			o.vars['n'] = random.randint (0, 255)

		o.vars['name']	= o.name
		o.vars['gg']	= '{0:02x}'.format (o.vars['g'])
		o.vars['nn']	= '{0:02x}'.format (o.vars['n'])

	def gen_xml (o):
		os.makedirs (o.xmls, exist_ok = True)

		with open (o.xml, 'w') as xml:
			for line in open (o.template, 'r'):
				xml.write (line.format (**o.vars))

class Net (Template):
	def __init__ (o, name):
		super().__init__ ('nubes/net', name)

		if not 'iface' in o.vars:
			o.vars['iface'] = o.name

		o.xmls = o.home + '/.local/lib/nubes/net'
		o.xml  = os.path.join (o.xmls, o.name + '.xml')

class VM (Template):
	def __init__ (o, name):
		super().__init__ ('nubes/vm', name)

		o.vars['images'] = o.home + '/.local/lib/nubes/images'
		o.vars['ttys']   = o.home + '/.local/lib/nubes/ttys'

		o.xmls = o.home + '/.local/lib/nubes/vm'
		o.xml  = os.path.join (o.xmls, o.name + '.xml')

