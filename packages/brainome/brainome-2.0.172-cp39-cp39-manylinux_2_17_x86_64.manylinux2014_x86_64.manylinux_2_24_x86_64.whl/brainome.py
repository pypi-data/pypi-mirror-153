# Brainome Daimensions(tm)
#
# The Brainome Table Compiler(tm)
# As of v0.95 this compiler needs to be imported as a module.
#
# Copyright (c) 2019 - 2022 Brainome Incorporated. All Rights Reserved.
# BSD license, all text above must be included in any redistribution.
# See LICENSE.TXT for more information.
#
# This program may use Brainome's servers for cloud computing. Server use
# is subject to separate license agreement.
#
# Contact: help@brainome.ai
# for questions and suggestions.
#
import json
import logging
import os
import shutil
import subprocess
import sys
import traceback
import csv
from time import time
from typing import Union
from urllib.error import URLError
import urllib.request

import math
import numpy as np		# noqa
# recommended for pyinstaller/numpy per https://github.com/pyinstaller/pyinstaller/issues/4363
# import numpy.random.common		# noqa
# import numpy.random.bounded_integers		# noqa
# import numpy.random.entropy		# noqa

from log import command, critical, get_session_value, get_verbosity_level, set_exit_code, limits, note, \
	report, reporter_main, \
	session, get_report_output, \
	configure_log, set_json_out, warning
from brainome_common import BrainomeExit, BrainomeError
from daimensions.cloudconnect import AuthenticationError
from daimensions.autodetection import is_dataset_regression, UnableToDetectError
from encrypt_predictor import encrypt
from brainome_version import BtcVersion
from reporting.reporting import Reporting
import daimensions.meter as dmn
import daimensions.utils as dmnu
import daimensions.cleaning as cln		# use this for cleaning

CLASSIFICATION_MODEL_TYPES = ["SVM", "DT", "RF", "NN"]		# default search order
REGRESS_MODEL_TYPES = ["LR"]
ALL_MODEL_TYPES = CLASSIFICATION_MODEL_TYPES + REGRESS_MODEL_TYPES

logger = logging.getLogger(__name__)  # btc logger
reporting = Reporting()

# Bootstrapper for compiled single-file executables #####
try:
	cmd = "python3 -c \"import sys;print(sys.path)\""
	# logger.debug("Checking environment by running " + cmd)
	process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	result = process.communicate()[0]  # Block until finish
	pathes = eval(result)
	for path in pathes:
		sys.path.append(path)
	# logger.debug("PYTHONPATH=" + str(sys.path))

except:
	warning("Warning: We recommend to have Python3 installed and in your path.")
	logger.debug(traceback.format_exc())

me = sys.argv[0]
if ".staticx" in me:
	try:
		me = sys.argv[0]
		location = os.path.dirname(sys.argv[0])

		os.mkdir(location + "/daimensions")
		for fil in ["meter.so", "cloudconnect.so", "utils.so", "local.so", "virtualos.so", "rpcserver.so", "templates.so"]:
			src = location + "/" + fil
			dst = location + "/daimensions/" + fil
			if os.path.exists(src):
				shutil.copyfile(src, dst)
	except:
		critical(-42, "Internal error. Please make sure the current directory exists and is writeable. Exiting!")

# ## END Bootstrapper #####################

import tempfile  # noqa E402
import argparse  # noqa E402
import atexit  # noqa E402
import time  # noqa E402
import threading  # noqa E402
import itertools  # noqa E402
import signal  # noqa E402
import importlib  # noqa E402
import urllib  # noqa E402
import gzip  # noqa E402

from datetime import datetime, timedelta  # noqa E402

# note the global statements below have no effect
# global mappingstr
# global trainfile
# global numseeds
# global ignorecolumnstr
# global ignorelabelstr
# global targetstr
# global importantidxstr
mappingstr = ""  # blurb used in predictor
trainfile = ""  # blurb used in predictor - not a real filename
ignorecolumnstr = ""  # blurb used in predictor
ignorelabelstr = ""  # blurb used in predictor
targetstr = ""  # blurb used in predictor
importantidxstr = ""  # blurb used in predictor
BTCDEBUG = ""  # TODO why does BTCDEBUG exist? verify functionality
numseeds = 2

# global session singletons
CAN_EXE = None
CAN_LOCAL = None
CAN_XGBOOST = None
CAN_REMOTE = None
HAS_NUMPY = None
MAXEFFORT = 100
timestamp = datetime.now().strftime("%H:%M:%S:%f").replace(':', '')
cleanfile = "clean" + timestamp + ".csv"
stubfile = "stub" + timestamp + ".py"

# session metric tracking globals (system_meter dict, float, float)
smallest_mec = high_mec = low_mec = None
best_accuracy = low_accuracy = high_accuracy = None
least_bias_meter = least_bias_sm = None		# dict system meter
low_bias = high_bias = None		# float value {'model_bias': 16.42,...}
most_gen_ratio = high_gratio = low_gratio = None
overfitted = []


def can_local():
	global CAN_LOCAL
	if CAN_LOCAL is None:
		try:
			import daimensions.local as dmnl
			import daimensions.rpcserver  # noqa F401
			# logger.debug("canlocal() is true")
			CAN_LOCAL = True

			# can this instance run xgboost
			can_xgboost_test()

			# can this instance run numpy, torch, sklearn ?
			missinglibs = dmnl.checkLibraries()
			if not missinglibs == []:
				message = (
					"The following libraries are missing:", " ".join(missinglibs),
					"Please install them using your favorite Python3 package manager.",
					"We recommend pip: https://pip.pypa.io/en/stable/installing/")
				warning("\n".join(message))

		except ImportError:
			# logger.debug("canlocal() is false")
			CAN_LOCAL = False
	return CAN_LOCAL


def can_xgboost_test():
	global CAN_XGBOOST
	if CAN_XGBOOST is None:
		backupsysprefix = sys.prefix
		if sys.platform.endswith("win"):
			import brainome		# noqa
			sys.prefix = os.path.dirname(brainome.__file__)
		try:
			import xgboost as xgb  # noqa F401
			CAN_XGBOOST = True
		except ImportError as iex:
			warning("Warning: Cannot load xgboost. Random Forest not available.", exc=iex)
			CAN_XGBOOST = False
		sys.prefix = backupsysprefix
	return CAN_XGBOOST


class Spinner:
	""" wrapping task blocks that may take a long time,
	this class displays a fancy ascii spinner while timing the task.
	usage:
		with Spinner( "message prompt" ) as spinner:
			do a long task here
			user_response = spinner.ask("stop spinner for Y/N user input")
			if user_response:
				pass

	Spinner is sensitive to no tty terminal like  python3 </dev/null
	"""
	# default to silent, override by set_verbose_level(1)
	silent = True
	verbose_level = 0
	# always answer yes to prompts bypassing interrupting the process for user input.
	always_yes = False

	# taken from spinner.py
	# Copyright (c) 2012 Giorgos Verigakis <verigak@gmail.com>
	phases =\
		{'pie': ['◷', '◶', '◵', '◴'], 'moon': ['◑', '◒', '◐', '◓'], 'line': ['⎺', '⎻', '⎼', '⎽', '⎼', '⎻'],
			'pixel': ['⣾', '⣷', '⣯', '⣟', '⡿', '⢿', '⣻', '⣽'], 'spinner': ['-', '/', '|', '\\']}

	# -----
	def __init__(self, message, delay=0.1, spinner_visible=False, phase='pixel'):
		self.start_time = datetime.now()
		report(message, verbose_level=-1)
		self.msg = message
		if self.silent:
			return
		self.spinner = itertools.cycle(self.phases.get(phase, self.phases['spinner']))
		self.delay = delay
		self.busy = False
		self.spinner_visible = False		# TODO release Spinner annimation after process separation
		self.durationString = ""
		sys.stdout.write(message + "\r")			# write message
		sys.stdout.flush()

	@classmethod
	def set_always_yes(cls, yes: bool):
		# always overwrite files or whatever is asked
		cls.always_yes = yes

	@classmethod
	def set_verbose_level(cls, level: int):
		# any level greater than zero is non-silent
		cls.verbose_level = level
		cls.silent = level < 1

	def write_next(self):
		if self.silent:
			return
		with self._screen_lock:
			if self.spinner_visible:
				sys.stdout.write(next(self.spinner))
				self.spinner_visible = True
				sys.stdout.flush()

	def remove_spinner(self, cleanup=False):
		if self.silent:
			return
		with self._screen_lock:
			if self.spinner_visible:
				sys.stdout.flush()
				sys.stdout.write('\b')
				self.spinner_visible = False
			if cleanup:
				if self.verbose_level > 1:
					sys.stdout.write(f'{self.msg} done. {self.durationString}\n')  # overwrite spinner with blank
				else:
					sys.stdout.write(" \u001b[2K")  # clear line
					# sys.stdout.write(f'.\n')  # overwrite spinner with blank
				sys.stdout.flush()

	def spinner_task(self):
		try:
			if self.silent:
				return
			while self.busy:
				self.write_next()
				time.sleep(self.delay)
				self.remove_spinner()
		except KeyboardInterrupt:
			pass

	def __enter__(self):
		if self.silent:
			return self
		if sys.stdout.isatty():
			self._screen_lock = threading.Lock()
			self.busy = True
			self.thread = threading.Thread(target=self.spinner_task)
			self.thread.deamon = True  # dont wait for the spinner... ever
			self.thread.start()
		return self

	def __exit__(self, exception, value, tb):
		report("{0} done".format(self.msg), verbose_level=-1)
		# calculate duration
		stop_time = datetime.now()
		seconds = self.calulate_duration_sec(stop_time, self.start_time)
		# record duration into session for posterity
		self.record_session_duration(seconds)
		self.durationString = self.formatDurationExact(seconds)
		if self.silent:
			return
		if sys.stdout.isatty():
			self.busy = False
			self.remove_spinner(cleanup=True)
			time.sleep(self.delay)

	def record_session_duration(self, seconds):
		# using prompt msg as key to storing duration in session['duration'] dict
		prompt: str = self.msg.replace(" ", "_").replace(".", "").lower()
		durations = get_session_value('durations', {})
		durations[prompt] = seconds
		session('durations', durations, overwrite=True)

	@staticmethod
	def formatDurationExact(seconds) -> str:
		periods = [
			('y', (60 * 60 * 24 * 365)),
			('m', (60 * 60 * 24 * 30)),
			('d', (60 * 60 * 24)),
			('h', (60 * 60)),
			('m', 60),
			('s', 1)
		]

		try:
			strings = []
			if seconds < 1:
				return '< 1s'  # zero seconds
			for period_name, period_seconds in periods:
				if seconds >= period_seconds:
					period_value, seconds = divmod(int(seconds), period_seconds)
					strings.append("%s%s" % (period_value, period_name))
			logger.debug(strings)
			return " ".join(strings)
		except:  # noqa
			logger.warning(f"formatTime timestamp error '{seconds}'")
			return "-" * 8

	@staticmethod
	def calulate_duration_sec(now_time, then_time):
		seconds = (now_time - then_time).total_seconds()
		return seconds

	# interactive
	def ask(self, string) -> bool:
		""" interrupt the spinning to prompt the user for input """
		if self.always_yes:		# always YES returns True
			if not self.silent:
				print(string, "yes")
			return True
		elif self.silent:		# silent w/o YES does not prompt
			return False
		else:
			if sys.stdin.isatty():		# stdin available for user input
				# stop the spinner w/ silent
				self.silent = True
				try:
					return input(string).upper()[0] == 'Y'
				except: # noqa
					return False
				finally:
					# restart spinner
					self.silent = False
			else:						# no terminal available for user input -> False
				if not self.silent:
					print(string, "no (specify --yes or run in an interactive terminal)")
				return False


def ctrlchandler(signum, frame):
	# TODO remove cleanfile
	# TODO remove stubfile
	critical(-3, "CTRL-C: aborting.")
	# sys.exit(-3)


def ctrlchandler2(signum, frame):
	# TODO remove cleanfile
	# TODO remove stubfile
	# TODO Use this to stop training and clean up appropriately
	critical(-4, "CTRL-C: interrupt training.")
	# raise KeyboardInterrupt


def seconds_to_str(elapsed):
	td = timedelta(seconds=elapsed)
	return (':'.join(str(td).split(':')[:2])) + ':' + ((str(td).split(':'))[2])[:5]


def get_header(start_time: time, sysargs: []):
	now = datetime.now()
	endtime = time.time()
	elapsed = endtime - start_time
	args = " ".join(sysargs)
	header = "# Output of Brainome " + BtcVersion.get_version() + ".\n"
	header += "# Invocation: " + args + "\n"
	header += "# Total compiler execution time: " + seconds_to_str(elapsed) + ". Finished on: " + now.strftime(
		"%b-%d-%Y %H:%M:%S") + "."
	report(header, verbose_level=-1)
	return header


def get_license():
	return dmn.PermissionsManager.getLicenseString()


def estimateMETime(n_instances, verb="prime"):
	if n_instances < 10000:
		estimatestr = "a few seconds"
	elif n_instances < 1000000:
		estimatestr = "less than a minute"
	elif n_instances < 10000000:
		estimatestr = "a few minutes"
	else:
		estimatestr = "hours"
	estimate_decision_tree = {verb + '_time_estimate': estimatestr}
	session('estimate_decision_tree', estimate_decision_tree)
	report("Estimated time to " + verb + " a decision tree: " + estimatestr, verbose_level=1)
	return estimate_decision_tree


def can_exe() -> bool:
	# singleton pattern to prevent overuse
	global CAN_EXE
	if CAN_EXE is None:
		try:
			import PyInstaller.__main__  # noqa F401
			import pkg_resources

			logger.debug("PyInstaller.__main__ imported")
			CAN_EXE = True
		except ModuleNotFoundError:
			logger.debug("No module named 'PyInstaller'")
			CAN_EXE = False

		except pkg_resources.DistributionNotFound:
			logger.debug("PyInstaller.__main__ failed import")
			CAN_EXE = False

	return CAN_EXE


def can_remote():
	global CAN_REMOTE
	if CAN_REMOTE is None:
		try:
			import requests  # noqa F401
			logger.debug("requests imported")
			CAN_REMOTE = True
		except ImportError:
			logger.warning("requests failed import")
			CAN_REMOTE = False
	return CAN_REMOTE


# def has_numpy():
# 	global HAS_NUMPY
# 	if HAS_NUMPY is None:
# 		try:
# 			importlib.import_module("numpy")
# 			logger.debug("numpy imported")
# 			HAS_NUMPY = True
# 		except ImportError:
# 			logger.warning("numpy failed import")
# 			HAS_NUMPY = False
# 	return HAS_NUMPY

# output control characters
BOLD = "[01;1m"
BLA = "[01;30m"
# RED = "[01;31m"
# GRE = "[01;32m"
BLU = "[01;34m"
# YEL = "[01;33m"
# MAG = "[01;35m"
NOC = "[0m"
prolog_cloud = "Brainome Table Compiler\nlogin: Update your credentials.\nlogout: Force login.\nchpasswd: Change your password.\nterminate: Stop running cloud processes.\nwipe: Delete all files in the cloud."
prolog_local = "Brainome Table Compiler\nlogin: Update your credentials.\nlogout: Force login.\nchpasswd: Change your password."
prolog_offline = "Brainome Table Compiler"

advanced_help_text = "\n".join(
	["Advanced options:",
	 "  -e EFFORT             Increase compute time to improve accuracy. 1=<effort<100. Default: 1",
	 "  -balance              Treat classes as if they were balanced (only active for NN).",
	 "  -nopriming            Do not prime the model.",
	 "  -novalidation         Do not measure validation scores for created predictor.",
	 "  -O OPTIMIZE, --optimize OPTIMIZE",
	 "                        Maximize true positives towards a single class.",
	 "  -nofun                Stop compilation if there are warnings."])
epilog_text = " ".join(
	[
		BOLD, "Examples:\n", NOC,
		"Measure and build a random forest predictor for titanic\n",
		BLU, "\tbrainome https://download.brainome.ai/data/public/titanic_train.csv \n\n", NOC,
		"Build a better predictor by ignoring columns:\n",
		BLU, "\tbrainome titanic_train.csv -ignorecolumns \"PassengerId,Name\" -target Survived \n\n", NOC,
		"Automatically select the important columns by using ranking:\n",
		BLU, "\tbrainome titanic_train.csv -rank -target Survived \n\n", NOC,
		"Build a neural network model with effort of 5:\n",
		BLU, "\tbrainome titanic_train.csv -f NN -e 5 -target Survived\n\n", NOC,
		"Measure headerless dataset:\n",
		BLU, "\tbrainome https://download.brainome.ai/data/public/bank.csv -headerless -measureonly\n\n", NOC,
		'Full documentation can be found at https://www.brainome.ai/documentation'
	]
)


def run_argparse() -> argparse.Namespace:
	""" parse argv, produce beautiful documentation, live strong
		TODO federate this into run_argparse.py
	"""

	""" help descriptions all in one place """
	desc = {
		'prolog': BLA + 'Brainome Table Compiler (tm)  ' + BtcVersion.get_version() + NOC,
		'epilog': epilog_text,
		"required": BOLD + 'Required arguments' + NOC,
		'input': 'Table as CSV files and/or URLs or Command above',
		'optional': BOLD + 'Optional arguments' + NOC,
		'h': 'show this help message and exit',
		'hh': "show advanced help message",
		'version': "show program's version number and exit",
		'basic_io': BOLD + "CSV input file details" + NOC,
		'headerless': 'Headerless CSV input file.',
		'target': 'Specify target column by name or number. Default: last column of table.',
		'ignorecolumns': 'Comma-separated list of columns to ignore by name or number.',
		'basic': BOLD + 'Basic options' + NOC,
		'rank': 'Select the optimal subset of columns for accuracy on held out data\nIf optional parameter N is given, select the optimal N columns. Works best for DT.',
		'measureonly': 'Only output measurements, no predictor is built.',
		'f': 'Force model type: DT, NN, RF, LR  Default: RF',
		'effort': 'Increase compute time to improve accuracy. 1=<EFFORT<100. Default: 1',
		'nosplit': 'Use all of the data for training. Default: dataset is split between training and validation.',
		'forcesplit': 'Pass it an integer between 50 and 90 telling our system to use that percent of the data for training, and the rest for validation',
		'intermediate': BOLD + 'Intermediate options' + NOC,
		'nsamples': 'Train only on a subset of N random samples of the dataset. Default: entire dataset.',
		'biasmeter': 'Measure model bias',
		'ignoreclasses': 'Comma-separated list of classes to ignore.',
		'usecolumns': 'Comma-separated list of columns by name or number used to build the predictor.',
		'output': 'Predictor filename. Default: a.py',
		'v': "Verbose output",
		'quiet': "Quiet operation.",
		'y': 'Answers yes to all overwrite questions.',
		'nofun': 'Stop compilation if there are warnings.',
		'advanced': BOLD + 'Advanced options' + NOC,
		'balance': argparse.SUPPRESS,  # 'Treat classes as if they were balanced (only active for NN).',
		'optimize': argparse.SUPPRESS,  # 'Maximize true positives towards a single class.',
		'nopriming': 'Do not prime the model.',
		'novalidation': 'Do not measure validation scores for created predictor.',
		'experimental': None,  # 'Experimental Options',
		'language': argparse.SUPPRESS,  # 'Predictor language: py',
		'language-exe': argparse.SUPPRESS,  # 'Predictor language: py, exe',
		'brainome-only': None,  # 'Brainome Only', "For Brainome Use Only"
		'server': argparse.SUPPRESS,
		'port': argparse.SUPPRESS,
		'json': "Document the session using json formatting.",
		'nclasses': argparse.SUPPRESS,
		'stopat': argparse.SUPPRESS,
		'onnx': argparse.SUPPRESS,
		'cleanonly': argparse.SUPPRESS,
		'classmapping': argparse.SUPPRESS,
		'deprecated': None,
		'deprecated_opt': argparse.SUPPRESS,
		'modelonly': 'Perform only the measurements needed to build the model.',
		'degree': argparse.SUPPRESS,
		'regress': "Force regression model types",
		'classify': "Force classification model types",
		'regularization_strength': argparse.SUPPRESS,
	}

	parser = argparse.ArgumentParser(
		description=desc['prolog'],
		formatter_class=argparse.RawTextHelpFormatter,
		add_help=False,  # used to control optional arguments
		epilog=desc['epilog'],
		prog="brainome")

	required = parser.add_argument_group(desc['required'])
	required.add_argument('input', type=str, nargs='+', help=desc['input'])

	optional = parser.add_argument_group(desc['optional'])
	optional.add_argument("-h", action="help", help=desc['h'])
	# optional.add_argument("-hh", dest='advanced_help', action="store_true", default=False, help=desc['hh'])
	optional.add_argument(
		"-version", "--version", action="version", version='brainome ' + BtcVersion.get_version(), help=desc['version'])

	# Basic
	basic = parser.add_argument_group(desc['basic'])
	basic.add_argument('-headerless', action="store_true", help=desc['headerless'])
	basic.add_argument('-target', type=str, default="", help=desc['target'])  # ARGS.target
	basic.add_argument('-ignorecolumns', default="", type=str, help=desc['ignorecolumns'])
	basic.add_argument('-rank', dest='attributerank', nargs="?", const="0", default="-1", type=int, help=desc['rank'])
	basic.add_argument('-measureonly', action="store_true", help=desc['measureonly'])
	basic.add_argument('-f', dest='forcemodel', type=str, help=desc['f'])
	basic.add_argument('-nosplit', action="store_true", help=desc['nosplit'])
	basic.add_argument('-split', dest='forcesplit', type=int, default=-1, help=desc['forcesplit'])

	# Intermediate
	intermediate = parser.add_argument_group(desc['intermediate'])
	intermediate.add_argument('-nsamples', default=0, type=float, help=desc['nsamples'])
	intermediate.add_argument('-ignoreclasses', dest='ignorelabels', default="", type=str, help=desc['ignoreclasses'])
	intermediate.add_argument('-usecolumns', dest='importantcolumns', default="", type=str, help=desc['usecolumns'])
	intermediate.add_argument('-o', dest='output', type=str, default="a.py", help=desc['output'])
	intermediate.add_argument("-v", dest="verbosity", action="count", default=1, help=desc['v'])
	intermediate.add_argument("-q", dest='quiet', action="store_true", help=desc['quiet'])
	intermediate.add_argument('-y', dest='yes', action="store_true", help=desc['y'])
	intermediate.add_argument('-regress', dest='force_regress', action="store_true", help=desc['regress'])		# since v1.9
	intermediate.add_argument('-classify', dest='force_classify', action="store_true", help=desc['classify'])		# since v1.9
	#  intermediate.add_argument('-degree', dest='degree', type=int, help=desc['degree'])

	# Advanced
	advanced = parser.add_argument_group(desc['advanced'])
	advanced.add_argument('-e', dest='effort', default=1, type=int, help=desc['effort'])
	advanced.add_argument('-biasmeter', action="store_true", default=False, help=desc['biasmeter'])
	advanced.add_argument('-novalidation', action="store_true", help=desc['novalidation'])
	advanced.add_argument('-nofun', action="store_true", help=desc['nofun'])
	advanced.add_argument('-modelonly', action='store_true', help=desc['modelonly'])
	advanced.add_argument('-json', type=str, help=desc['json'])

	# Experimental
	experimental = parser.add_argument_group(desc['experimental'])
	experimental.add_argument(
		'-l', '--language', default="py",
		type=str,
		help=desc['language-exe'] if can_exe() else desc['language'])

	# Brainome Only
	brainome_only = parser.add_argument_group(desc['deprecated'])
	brainome_only.add_argument('-server', type=str, default='daimensions.brainome.ai', help=desc['server'])
	brainome_only.add_argument('-port', type=int, default=None, help=desc['port'])
	brainome_only.add_argument('-nc', '--nclasses', type=int, default=0, help=desc['nclasses'])
	brainome_only.add_argument('-stopat', default=100, type=float, help=desc['stopat'])
	brainome_only.add_argument('-onnx', action="store_true", help=desc['onnx'])
	brainome_only.add_argument('-cleanonly', action="store_true", help=desc['cleanonly'])
	brainome_only.add_argument('-cm', '--classmapping', type=str, default="{}", help=desc['classmapping'])
	brainome_only.add_argument('-nopriming', action="store_true", help=desc['deprecated_opt'])
	brainome_only.add_argument('-balance', action='store_true', help=desc['balance'])
	brainome_only.add_argument('-O', dest='optimize', type=str, default="all", help=desc['optimize'])
	brainome_only.add_argument('-C', dest='regularization_strength', default=0.001, type=float, help=desc['regularization_strength'])		# since v1.8
	brainome_only.add_argument('-alpha', dest='lr_regularization_strength', default=0.0, type=float)

	# Deprecated
	deprecated = parser.add_argument_group(desc['deprecated'])
	deprecated.add_argument('--help', action="help", help=desc['deprecated_opt'])
	# deprecated.add_argument('-Wall', action="store_true", help=desc['deprecated_opt'])
	# deprecated.add_argument('-pedantic', action="store_true", help=desc['deprecated_opt'])
	deprecated.add_argument('-magic', type=str, default="", help=desc['deprecated_opt'])
	deprecated.add_argument('-riskoverfit', action="store_true", help=desc['deprecated_opt'])
	# deprecated.add_argument("--verbosity", action="count", default=1, help=desc['deprecated_opt'])
	# deprecated.add_argument('--yes', action="store_true", help=desc['deprecated_opt'])
	# deprecated.add_argument('-importantcolumns', default="", type=str, help=desc['deprecated_opt'])
	# deprecated.add_argument("--quiet", dest='quiet', action="store_true", help=desc['deprecated_opt'])
	# deprecated.add_argument('--runlocalonly', action="store_true", default=can_local(), help=desc['deprecated_opt'])
	# deprecated.add_argument('-ignorelabels', default="", type=str, help=desc['deprecated_opt'])
	# deprecated.add_argument('--forcemodel', dest='forcemodel', type=str, help=desc['deprecated_opt'])
	# deprecated.add_argument('--output', dest='output', type=str, default="a.py", help=desc['deprecated_opt'])
	# deprecated.add_argument('--effort', default=1, type=int, help=desc['deprecated_opt'])
	# deprecated.add_argument('--optimize', type=str, default="all", help=desc['deprecated_opt'])

	return parser.parse_args()


def check_argparse_settings(btc_args: argparse.Namespace):
	""" check params and exit with code if found wrong """
	# code 0 (not 35)
	btc_args_input0 = btc_args.input[0].upper()
	if can_local() and btc_args_input0 == "TERMINATE" or btc_args_input0 == "WIPE":
		note("Cloud commands not available on local run. Exiting.")
		reporting.print_basic()
		raise BrainomeExit

	# code 20
	if btc_args.output is None:
		critical(20, "Error: -o cannot specify an empty filename.")

	# code 21
	if btc_args.attributerank >= 0 and btc_args.ignorecolumns != "" and btc_args.headerless:
		critical(21, "Error: Automatic ranking and manual exclusion of columns require a headered CSV file.")

	# code 22
	if not btc_args.effort > 0:
		critical(22, "Error: Effort must be > 0.")
	if btc_args.headerless and btc_args.ignorecolumns != "":
		for col in btc_args.ignorecolumns.split(','):
			try:
				int(col)
			except ValueError:
				critical(104, "Error: Headerless files require the ignorecolumns to be integers")
	if btc_args.headerless and btc_args.target != "":
		try:
			int(btc_args.target)
		except ValueError:
			critical(105, "Error: Headerless files require the user to specify the target column as an integer")
	# code 23
	if btc_args.stopat / 100.0 <= 0.0:
		critical(23, "Error: Stopping at too low.")

	# code 24
	if btc_args.stopat / 100.0 > 1.0:
		critical(24, "Error: Stopping can't be larger than 100.")

	# code 25
	if btc_args.forcemodel == "NN" and btc_args.effort > 20:
		critical(25, "Error: Max value for effort is 20 unless DT or RF is forced. Recommendation is 10.")

	if not btc_args.forcemodel == "NN" and btc_args.balance:
		critical(25, "-balance is only supported for Neural Networks")

	# code 25
	can_xgboost = can_xgboost_test()
	if btc_args.forcemodel == "RF" and not can_xgboost:
		critical(25, "Cannot specify RF model type without xgboost installed.")

	# code 26
	if btc_args.effort > MAXEFFORT:
		critical(26, "Error: Max value for effort is " + str(MAXEFFORT) + ". Recommendation is 10.")

	# code 27
	if btc_args.optimize != "all" and btc_args.balance:
		critical(27, "Error: Cannot use -O and -balance together.")

	if btc_args.optimize != "all" and not (btc_args.forcemodel == "NN" or (btc_args.forcemodel == "DT" and btc_args.attributerank >= 0) or (btc_args.forcemodel == "RF" and btc_args.attributerank >= 0)):
		critical(
			27,
			"Optimizing for TPR of a specific class is only supported with (-f NN) or (-f DT -rank) or (-f RF -rank)")

	# code 28
	if btc_args.language == "exe":
		if not can_exe():
			critical(28, "Error: Please install PyInstaller to generate executables.")
		if btc_args.onnx:
			critical(28, "Cannot use both onnx and language at the same time")
		if btc_args.output != "a.py":
			pre_output, ext_output = os.path.splitext(btc_args.output)
			if ext_output == 'py':
				# TODO assign proper error code
				critical(28, "Cannot specify language and python output at the same time")

	# code 29
	if btc_args.forcemodel and btc_args.forcemodel not in ALL_MODEL_TYPES:
		critical(
			29,
			"Error: For now, Brainome only supports neural nets, decision trees, random forests, SVMs and linear regression models.")

	# code 30
	if not btc_args.magic == "":
		critical(30, "Error: Magic not yet supported.")

	# code 31
	if btc_args.nosplit and btc_args.effort > 1:
		critical(31, "Error: -nosplit does not work for effort > 1.")

	# code 33
	if btc_args.importantcolumns != "" and btc_args.ignorecolumns != "" and btc_args.attributerank < 0:
		critical(33, "Error: -usecolumns does not work with -ignorecolumns except when attribute ranking.")

	# code 32
	if btc_args.effort > 1:
		if btc_args.nopriming or btc_args.measureonly:
			warning(
				"Warning: Effort parameter is mutually exclusive with -measureonly and -nopriming. Ignoring effort.")

	# code 102
	if btc_args.forcesplit != -1 and (btc_args.forcesplit < 10 or btc_args.forcesplit > 100):
		critical(102, "Error: Please provide a split for the training set that is at least 10% and at most 100%.")
	# code 34
	if not btc_args.classmapping == "{}":
		try:
			mapping = json.loads(btc_args.classmapping)  # noqa F841
		except json.JSONDecodeError as decode_err:
			critical(
				34, "Error: Class mapping needs to be in JSON syntax. For example: -cm {\\\"T\\\":1, \\\"F\\\":0}",
				exc=decode_err)
	else:
		mapping = {}

	# code 56. VERSION command discontinued
	if btc_args.input[0] == "VERSION":
		critical(56, "Error: VERSION command discontinued, use -version")

	# code 57
	if btc_args.nosplit and btc_args.forcesplit != -1:
		critical(57, "cannot use -nosplit together with -split")

	# code 54
	if btc_args.target != "" and btc_args.target in btc_args.importantcolumns.split(','):
		critical(
			54,
			f"The target {btc_args.target} cannot be in the set of columns to use as features {btc_args.importantcolumns.split(',')}.")
	if btc_args.target != "" and btc_args.target in btc_args.ignorecolumns.split(','):
		critical(
			54,
			f"The target {btc_args.target} cannot be in the set of columns to ignore {btc_args.ignorecolumns.split(',')}.")

	pre_output, ext_output = os.path.splitext(btc_args.output)
	if btc_args.onnx:
		# guard against onnx and non-NN models
		if btc_args.forcemodel and btc_args.forcemodel != "NN":
			critical(52, "Error: The -onnx flag can only be used with -f NN.")
		if ext_output != ".onnx":
			critical(46, "Error: The output filename for onnx must be .onnx")

	# TODO assign proper exit code
	if btc_args.regularization_strength != 0.001 and btc_args.forcemodel and btc_args.forcemodel != "SVM":
		critical(99, "Error: The -regularization_strength flag can only be used with -f SVM.")

	if btc_args.novalidation and not btc_args.forcemodel:
		critical(99, "Error: -novalidation requires a model to be specified with -f")
		# TODO remove this with new data_meter output

	# TODO assign proper exit codegit
	if btc_args.force_regress and btc_args.force_classify:
		critical(99, 'Error: cannot specify both -regress and -classify at the same time')

	# TODO assign proper exit code
	if btc_args.force_regress and btc_args.forcemodel and btc_args.forcemodel not in REGRESS_MODEL_TYPES:
		critical(99, 'Error: cannot specify both -regress and -f force model at the same time')

	# TODO assign proper exit code
	if btc_args.force_classify and btc_args.forcemodel and btc_args.forcemodel not in CLASSIFICATION_MODEL_TYPES:
		critical(99, 'Error: cannot specify both -classify and -f force model at the same time')

	return mapping		# loaded user json args_classmapping

def coerce_argparse_settings(ARGS):
	""" coherse args based on other args
	WARNING - THIS MODIFIES ARGS
	"""
	if ARGS.forcemodel == "QC":
		warning("Warning: --forcemodel QC is deprecated in favor of --forcemodel DT. Please update your scripting.")
		ARGS.forcemodel = "DT"  # Backwards compatibility to 0.96 and earlier

	if ARGS.novalidation and not ARGS.nosplit:
		# novalidation means we don't hold back validation content from training
		ARGS.nosplit = True

	# --quiet overrides --verbose
	if ARGS.quiet:
		logger.debug("quiet overrules any verbosity")
		ARGS.verbosity = -1

	# 100% forsesplit is same as nosplit aka riskoverfit
	if ARGS.forcesplit == 100:
		logger.debug("coerceing nosplit=True based on 100% forcesplit ")
		ARGS.nosplit = True
		ARGS.forcesplit = -1

	# SVM
	if ARGS.regularization_strength != 0.001:
		logger.debug("coherseing model to SVM")
		ARGS.forcemodel = "SVM"

	# onnx implies NN
	if ARGS.onnx:
		logger.debug("coherse model to NN")
		ARGS.forcemodel = 'NN'
		pre_output, ext_output = os.path.splitext(ARGS.output)
		# onnx implies output filename extension .onnx
		if ext_output != 'onnx':
			logger.debug("coherse output extension to onnx")
			ARGS.output = pre_output + '.onnx'

	if ARGS.language == "exe":
		if ARGS.output == "a.py":
			ARGS.output = "a.out"


def calculate_optimize(optimize, class_mapping, remapping):
	""" validate args -O against classmapping
	"""
	if optimize == 'all':
		return_optimize = -1
	else:
		mappy = "{}"
		if class_mapping != "{}":
			mappy = class_mapping
		if str(remapping) != "{}":
			mappy = str(remapping)
		try:
			return_optimize = int(float(optimize))
		except ValueError:
			return_optimize = str(optimize)

		if mappy != "{}":
			mappingdict = json.loads(mappy.replace("\'", "\""))
			if str(return_optimize) in list(mappingdict.keys()):
				return_optimize = int(mappingdict[str(return_optimize)])
			else:
				critical(52, "Error: -O received a label " + str(return_optimize) + " that is not found in the mappings keys " + str(mappingdict.keys()))
				# sys.exit(52)
	return return_optimize


def get_clean_report(inputfile, args_classmapping, classmap: str, remapping, ignorelabels, igncol, n_classes, n_attrs, target):
	""" output this information
	clean_report, mappingstr, targetstr, ignorelabelstr, ignorecolumnstr
	"""
	global mappingstr
	global trainfile
	global numseeds
	global ignorecolumnstr
	global ignorelabelstr
	global targetstr
	global importantidxstr
	clean_report = {}
	mappingstr = "mapping={}"
	if args_classmapping != "{}":
		mappingstr = "mapping=" + classmap
		clean_report['class_mapping'] = args_classmapping
	#
	if str(remapping) != "{}":
		mappingstr = "mapping=" + classmap
		clean_report['class_mapping'] = remapping

	targetstr = "target=" + "\"" + target + "\""
	clean_report['target'] = target

	ignorelabelstr = "ignorelabels=" + str(ignorelabels)
	clean_report['ignore_labels'] = ignorelabels

	ignorecolumnstr = "ignorecolumns=" + str(igncol)
	clean_report['ignore_columns'] = igncol

	pre_output, ext_output = os.path.splitext(inputfile)
	clean_state_file = pre_output + '.state'
	with open(clean_state_file, 'w', encoding='utf-8') as cs:
		print("# State from cleaning and preprocessing", file=cs)
		print("num_attr=" + str(n_attrs), file=cs)
		print("n_classes=" + str(n_classes), file=cs)
		print(mappingstr, file=cs)
		print(targetstr, file=cs)
		print(ignorelabelstr, file=cs)
		print(ignorecolumnstr, file=cs)
	clean_report['num_attributes'] = n_attrs
	clean_report['num_classes'] = n_classes
	clean_report['target'] = target
	clean_report['clean_file'] = inputfile
	clean_report['clean_state'] = clean_state_file
	note(f"Clean only output: {clean_state_file}, {inputfile}")

	return clean_report, mappingstr, targetstr, ignorelabelstr, ignorecolumnstr


def track_ALL_metrics(next_sm: dict, next_bias: dict) -> []:
	""" short cut call to simplify tracking """
	all_metrics = []
	all_metrics += track_smallest_MEC(next_results=next_sm)
	all_metrics += track_least_bias(next_system_meter=next_sm, next_bias_meter=next_bias)
	all_metrics += track_best_accuracy(next_results=next_sm)
	return all_metrics


def track_most_generalization_ratio(next_regress):
	""" pick the most generalized model
	"system_meter": {
		"regression_type": "LR",
		"generalization_ratio": 18.86
	}
	"""
	global most_gen_ratio, high_gratio, low_gratio
	most_gen_ratio = next_regress
	low_gratio = high_gratio = next_regress['generalization_ratio']
	return most_gen_ratio, high_gratio, low_gratio


def track_smallest_MEC(next_results: dict) -> (dict, float, float):
	""" picking the least MEC
	tracking low/high range
	"system_meter": {
		"model_capacity": 4,
	}
	"""
	global smallest_mec, high_mec, low_mec
	smallest_mec_value = smallest_mec.get('model_capacity', None) if smallest_mec else None
	next_mec_value = next_results.get('model_capacity', None) if next_results else None
	high_mec = max(high_mec, next_mec_value) if (high_mec and next_mec_value) else next_mec_value if next_mec_value else high_mec
	low_mec = min(low_mec, next_mec_value) if (low_mec and next_mec_value) else next_mec_value if next_mec_value else low_mec

	if next_mec_value is None or smallest_mec_value is None or (next_mec_value < smallest_mec_value):
		smallest_mec = next_results or smallest_mec	 # better smaller capacity

	return smallest_mec, low_mec, high_mec


def track_least_bias(next_system_meter: dict, next_bias_meter: dict) -> (dict, float, float):
	""" picking the least biased
	"bias_meter": {
		"model_bias": 21.6,
		"towards_class": 0,
		"away_from_class": 1,
		"algorithm": "DT"
	},
	tracking low/high range
	"""
	# track range
	global least_bias_sm, least_bias_meter, low_bias, high_bias
	least_bias_value = least_bias_meter.get('model_bias', None) if least_bias_meter else None
	next_bias_value = next_bias_meter.get('model_bias', None) if next_bias_meter else None
	high_bias = max(high_bias, next_bias_value) if (high_bias and next_bias_value) else next_bias_value if next_bias_value else high_bias
	low_bias = min(low_bias, next_bias_value) if (low_bias and next_bias_value) else next_bias_value if next_bias_value else low_bias

	if least_bias_value is None or next_bias_value is None or (next_bias_value < least_bias_value):
		least_bias_meter = next_bias_meter
		least_bias_sm = next_system_meter or least_bias_sm		# next winner

	return least_bias_sm, low_bias, high_bias


def get_stats(system_meter) -> (float, float, bool):
	""" extract accuracy (validation or training), capacity, and overfitting """
	if system_meter:
		accuracy = system_meter.get("validation_stats", {}).get('accuracy', None) or \
			system_meter.get("training_stats", {}).get('accuracy', None) or 0.0
		capacity = system_meter.get('model_capacity', None)
		overfitting = system_meter.get('overfitting', None)
		return accuracy, capacity, overfitting
	# default None cubed
	return None, None, None


def track_best_accuracy(next_results: dict) -> (dict, float, float):
	""" picking the highest accuracy without overfitting
	tie breaking with least MEC
	"""
	global best_accuracy, low_accuracy, high_accuracy, overfitted
	best_accuracy_value, best_capacity_value, best_overfit = get_stats(best_accuracy)
	next_accuracy_value, next_capacity_value, next_overfit = get_stats(next_results)

	high_accuracy = max(high_accuracy, next_accuracy_value) if (best_accuracy_value and next_accuracy_value) else next_accuracy_value if next_accuracy_value else high_accuracy
	low_accuracy = min(low_accuracy, next_accuracy_value) if (best_accuracy_value and next_accuracy_value) else next_accuracy_value if next_accuracy_value else low_accuracy

	if not next_overfit:
		if best_accuracy_value is None or next_accuracy_value is None or (best_accuracy_value < next_accuracy_value):
			best_accuracy = next_results or best_accuracy		# winner accuracy
		elif (best_accuracy_value == next_accuracy_value) and (next_capacity_value < best_capacity_value):
			best_accuracy = next_results  # tied accuracy, winner capacity
	else:
		if next_results:
			overfitted.append(next_results['classifier_type'])
	return best_accuracy, low_accuracy, high_accuracy


def canonize_best_model(algorithm_type: str, algorithms: list, output_file: str):
	""" decide the best algorithm for auto ml
	# if we are generating bias, then least bias is best
	# if non-overfit, then best_accuracy + smallest mec
	# else smallest mec as the consolation prise

	Four things this does:
		set system_meter
		set algorithm
		copy predictor file
		publish automl ranges
	"""
	global least_bias_sm, best_accuracy, smallest_mec
	best_model: Union[dict, None] = least_bias_sm or best_accuracy or smallest_mec

	algorithm_ = None
	# step 1 hook up system_meter with the only system_meter
	if best_model:
		try:
			algorithm_ = best_model.get('classifier_type', best_model.get('regression_type', best_model.get('algorithm', None)))
			if algorithm_ is None:
				raise ValueError('best_model is missing classifier_type and algorithm')
			elif len(algorithms) > 1:
				logger.info(f"Best results is for {algorithm_} ")
				note(f"{algorithm_} chosen as best model out of {len(algorithms)}")

			# set system_meter and algorithm
			session('system_meter', best_model, overwrite=True)
			session("algorithm", algorithm_, overwrite=True)
			if get_verbosity_level() <= 2:
				logger.debug("printing final system_meter")
				reporting.print_system_meter()

			# set bias_meter
			if least_bias_sm:
				bm = get_session_value(f"bias_meter_{algorithm_}", None)
				if bm:
					session("bias_meter", bm)
					reporting.print_bias_meter()  # Reporting bias_meter

			# copy the predictor to expected output
			pre_output, ext_output = os.path.splitext(output_file)
			alg_output_file = pre_output + f"_{algorithm_}" + ext_output
			if os.path.exists(alg_output_file):
				shutil.copyfile(alg_output_file, output_file)
				logger.debug(f"Writing {algorithm_} predictor file {alg_output_file}")

			# publish automl ranges
			publish_automl_scores(algorithm_type)
			if len(algorithms) > 1 and get_verbosity_level() >= 0:
				# print automl summary
				print(reporting.render_classify_summary(get_report_output()))
		except ValueError as verr:
			logger.debug("model system_meter ValueError", exc_info=verr)
			logger.error("system_meter is borked")

	elif len(algorithms) > 0:
		algorithm_ = algorithms[0]

	if algorithm_:
		# copy the predictor to expected output
		pre_output, ext_output = os.path.splitext(output_file)
		alg_output_file = pre_output + f"_{algorithm_}" + ext_output
		if os.path.exists(alg_output_file):
			shutil.copyfile(alg_output_file, output_file)
			note(f"Writing {algorithm_} predictor file {output_file}")
		else:
			note("Predictor file not written due to license violation.")

	return best_model


def publish_automl_scores(algorithm_type):
	if algorithm_type == "CLASSIFICATION":
		return publish_classify_scores()
	else:		# "REGRESSION":
		# TODO publish_regression_scores() or whatever
		pass


def publish_classify_scores():
	""" each tracked metric has a max/min value if any. """
	global smallest_mec, high_mec, low_mec
	global best_accuracy, low_accuracy, high_accuracy, overfitted
	global least_bias_sm, low_bias, high_bias
	automl_scores = {}
	if smallest_mec:
		automl_scores["mec"] = [smallest_mec["classifier_type"], low_mec, high_mec]
	if best_accuracy:
		automl_scores["accuracy"] = [best_accuracy["classifier_type"], low_accuracy, high_accuracy]
	if least_bias_meter:
		automl_scores["bias"] = [least_bias_meter["algorithm"], low_bias, high_bias]
	automl_scores['overfitted'] = overfitted
	session("auto_ml_scores", automl_scores)
	return automl_scores


@reporter_main()
def main(args):
	global mappingstr			# blurb used in predictor
	global trainfile			# blurb used in predictor - not a real filename
	global ignorecolumnstr		# blurb used in predictor
	global ignorelabelstr		# blurb used in predictor
	global targetstr			# blurb used in predictor
	global importantidxstr		# blurb used in predictor
	global BTCDEBUG			# TODO why does global BTCDEBUG exist? verify functionality
	global numseeds
	try:
		# earliest place to load xgboost here
		can_local()
		# starting time
		starttime = time.time()

		# record arguments
		command(args)

		# parse arguments
		ARGS = run_argparse()

		# validate arguments
		check_argparse_settings(ARGS)

		# coheres arguments based on combinations - modifies ARGS
		coerce_argparse_settings(ARGS)

		configure_log(ARGS.verbosity, ARGS.nofun)  # how verbose do we want the output
		Spinner.set_verbose_level(ARGS.verbosity)
		Spinner.set_always_yes(ARGS.yes)

		# record server and args
		session('server', ARGS.server)
		session('port', ARGS.port)

		if can_local():
			compiledas = " (local execution)"
		else:
			compiledas = " (cloud)"
		session('btc_version', BtcVersion.get_version())
		session('compiled_as', compiledas)
		# process JSON param
		set_json_out(ARGS.json, ARGS.yes)

		license_violation = False
		# BTC_LOCAL COMMANDS #####################
		if can_local():
			try:
				if ARGS.input[0].upper() == "LOGIN":
					args_email = args_pswd = None
					if len(ARGS.input) > 1 and isinstance(ARGS.input[1], str):  # user supplied username
						args_email = ARGS.input[1]
					if len(ARGS.input) > 2 and isinstance(ARGS.input[2], str):  # user supplied password
						args_pswd = ARGS.input[2]
					run_login_command(ARGS.server, ARGS.port, args_email, args_pswd)

				if ARGS.input[0].upper() == "LOGOUT":
					run_logout_command()

				license_violation = check_license_terms(ARGS.server, ARGS.port, ARGS.quiet)

			except AuthenticationError as auth_error:
				# code 106
				license_violation = True
				logger.warning('AuthenticationError', exc_info=auth_error)
				session('license_violation', license_violation)
				reporting.print_basic()
				critical(106, "Error corrupted license file.")
				# sys.exit(106)

			except ConnectionError as could_not_auth_exc:
				# code 38
				license_violation = True
				logger.warning("dontconnect exception", exc_info=could_not_auth_exc)
				session('license_violation', license_violation)
				reporting.print_basic()
				critical(38, "Error: Could not authorize.", could_not_auth_exc)
				# sys.exit(38)

		else:
			# BTC CLOUD  ####################
			if not can_remote():
				# code 39
				critical(
					39,
					"Error: Missing library. Please install the \'requests\' library. See: https://requests.readthedocs.io/en/master/user/install/")
				# sys.exit(39)

			try:
				if ARGS.input[0].upper() == "TERMINATE":
					run_terminate_command(ARGS.server, ARGS.port)

				if ARGS.input[0].upper() == "WIPE":
					run_wipe_command(ARGS.server, ARGS.port)

				if ARGS.input[0].upper() == "CHPASSWD":
					run_chpasswd_command(ARGS.server, ARGS.port)

				if ARGS.input[0].upper() == "LOGIN":
					args_email = args_pswd = None
					if len(ARGS.input) > 1 and isinstance(ARGS.input[1], str):  # user supplied username
						args_email = ARGS.input[1]
					if len(ARGS.input) > 2 and isinstance(ARGS.input[2], str):  # user supplied password
						args_pswd = ARGS.input[2]
					run_login_command(ARGS.server, ARGS.port, args_email, args_pswd)

				if ARGS.input[0].upper() == "LOGOUT":
					run_logout_command()

				# default cloud authentication
				dmn.Meter.connect(ARGS.server, ARGS.port, ARGS.quiet)
			except Exception as e:
				# code 42
				warning(str(e), exc=e)
				critical(
					42, "Error: Unable to connect to cloud service https://" + ARGS.server + ":" + str(ARGS.port),
					exc=e)
				# sys.exit(42)

		# BTCDEBUG = dmn.PermissionsManager.BTCDEBUG
		# limits('BTCDEBUG', BTCDEBUG)
		# LICENSE = dmn.PermissionsManager.getLicenseString()
		limits('license', dmn.PermissionsManager.getLicenseString())

		signal.signal(signal.SIGINT, ctrlchandler)

		if can_local():
			atexit.register(dmn.Meter.terminate)
		else:
			atexit.register(dmn.Meter.wipe)

		# VERSION = dmn.Meter.version()
		sysargs = sys.argv
		sysargs[0] = "brainome"  # Static compiler messes up invocation

		# this is the output file name, default a.py
		outputfile = calculate_outputfile(ARGS.output, ARGS.yes, ARGS.onnx, ARGS.language)

		# Reporting header & messages
		reporting.print_header()
		# handle multiple data sets from various sources: local file, http url, gz into one inputfile and trainfile
		inputfile, trainfile = process_inputfiles(ARGS.input, ARGS.headerless)

		# csv_header: [str] or [int]
		csv_header = get_csv_file_header(inputfile, ARGS.headerless)

		# target: UNION[str, int], target_column: int
		target, target_column, ignore_columns_list = \
			validate_dataset_cols(
				ARGS.headerless, ARGS.target, ARGS.ignorecolumns, ARGS.importantcolumns,
				ARGS.attributerank, csv_header)

		# SAVE target
		session('target', target)

		# algorithm_type in ["REGRESSION", "CLASSIFICATION"]
		algorithm_type = calculate_algorithm_type(ARGS, ARGS.headerless, inputfile, target_column)

		use_columns_list = ARGS.importantcolumns.split(',') if ARGS.importantcolumns and ARGS.attributerank < 0 else []
		column_index_map, ignorelabels, clean_file, n_attrs, \
			n_classes, n_instances, preprocessesed, \
			processed_header, remapping, subsampled = \
			process_dataset_to_clean(
				ARGS.target, ARGS.headerless, ARGS.nsamples, ARGS.ignorelabels, ARGS.classmapping,
				ignore_columns_list, use_columns_list, inputfile, (algorithm_type == 'REGRESSION'))

		classmap: str = process_classmap(ARGS.classmapping, remapping)

		if ARGS.cleanonly:
			finish_cleanonly_mode(
				ARGS.classmapping, clean_file,
				classmap, ignore_columns_list, ignorelabels, n_attrs, n_classes, remapping, target)

		# check dataset limits as defined in the license
		license_violation = check_license_limits(clean_file, n_attrs, n_instances) or license_violation
		session('license_violation', license_violation)

		check_args_nclasses(ARGS.nclasses, n_classes)

		if not can_local():
			dmn.Meter.wipe()  # This is necessary to delete the state. We should implement a deletestate() command instead

		ARGS.optimize = calculate_optimize(ARGS.optimize, ARGS.classmapping, remapping)

		col_idxs_to_keep = \
			calculate_cols_idxs_to_keep(
				ARGS.importantcolumns, ARGS.attributerank, ARGS.headerless, column_index_map, csv_header)

		# uploadfile = inputfile
		# important_columns_list should be the indices of the columns used by the predictor as they correspond
		# to the original CSV header
		if ARGS.attributerank >= 0:
			attribute_rank, ignore_columns_list, important_columns_list = \
				run_attribute_rank(
					ARGS.measureonly, ARGS.attributerank, ARGS.optimize, ARGS.headerless,
					col_idxs_to_keep, column_index_map, ignore_columns_list, clean_file, license_violation, processed_header)
			check_attribute_rank(attribute_rank)
			reporting.print_attribute_rank()
		elif use_columns_list:
			important_columns_list = use_columns_list
		else:
			important_columns_list = [str(x) for i, x in enumerate(csv_header) if str(x) != target and str(x) not in ignore_columns_list]
		important_columns_list = list(map(str, important_columns_list))

		# else:
		# 	ignore_columns_list = []
		logger.debug(f"numattrr={n_attrs}")
		logger.debug(f"ignore_columns_list={ignore_columns_list}")

		with Spinner("Splitting into training and validation..."):
			run_split_train_val(ARGS.nosplit, ARGS.attributerank, ARGS.forcesplit, (algorithm_type == 'REGRESSION'))

		if not ARGS.modelonly and not algorithm_type == 'REGRESSION':
			run_data_meter(ARGS.effort, cleanfile)

		logger.debug("calling server_ping()")
		dmn.Meter.server_ping(ARGS.server, ARGS.port, algorithm_type)

		if ARGS.measureonly or (ARGS.verbosity > 0 and ARGS.forcemodel == "DT"):
			report("Time estimate for Decision Tree:", verbose_level=1)
			estimateMETime(n_instances)

		reporting.print_data_meter()

		if ARGS.measureonly:
			finish_measure_only()

		# BUILDING models serially this way
		algorithms = calculate_algorithms(ARGS.forcemodel, algorithm_type)
		for algorithm in algorithms:
			# specialize output file
			pre_output, ext_output = os.path.splitext(outputfile)
			alg_output_file = pre_output + f"_{algorithm}" + ext_output
			# specialize model file
			# Build a model
			build_model(ARGS, algorithm, n_instances, numseeds, alg_output_file)

			# generate a predictor and system_meter
			encrypted_model_file, system_meter, print_system_meter = \
				generate_predictor(
					ARGS.headerless, ARGS.input, ARGS.classmapping, ARGS.attributerank, ARGS.ignorecolumns, ARGS.ignorelabels, ARGS.novalidation, ARGS.optimize,
					algorithm, classmap, csv_header, ignore_columns_list, important_columns_list,
					ignorelabels, license_violation, n_attrs, n_classes, preprocessesed,
					(algorithm_type == 'REGRESSION'), remapping, target, target_column,
					alg_output_file, starttime, sysargs)
			defer_temp_file(alg_output_file)		# clean up later

			if get_verbosity_level() > 2:
				logger.debug("printing interim system_meter")
				print(print_system_meter)

			# RUN BIAS_METER
			if ARGS.biasmeter:
				bias_meter = create_bias_meter(dmn, alg_output_file, algorithm)
				# track progress bias_meter
				session(f'bias_meter_{algorithm}', bias_meter)
				if get_verbosity_level() > 1:
					logger.debug("printing interim bias_meter")
					session('bias_meter', bias_meter, overwrite=True)
					reporting.print_bias_meter()
			else:
				# greasing the wheels
				bias_meter = None

			# keep track of best etc
			track_ALL_metrics(system_meter, bias_meter)

		canonize_best_model(algorithm_type, algorithms, outputfile)

		# RUN PYINSTALLER ON PREDICTOR
		if ARGS.language == "exe":
			create_binary_predictor(ARGS.output, outputfile)

	except BrainomeError as brainome_err:
		logger.info(f"BrainomeError captured {brainome_err.exit_code} {brainome_err.message}")
		return brainome_err.exit_code

	except BrainomeExit:
		logger.debug("Finishing")

	except Exception as e:
		logger.critical("Naked Exception Captured", exc_info=e)
		return 999
	finally:
		clean_temp_files()

	# clean exit
	return 0		# end main()


def finish_measure_only():
	report('measureonly done.', verbose_level=-1)
	# reporting.print_messages()
	raise BrainomeExit


def run_split_train_val(risk_overfit, attribute_rank, force_split, regression):
	dmn.Meter.splitTrainVal(
		filename=cleanfile, riskoverfit=risk_overfit, cleanfile=False,
		upload=(not attribute_rank >= 0), forcesplit=force_split, regression=regression)


def check_attribute_rank(attribute_rank):
	if float(attribute_rank['overfit_risk']) >= 0.9:
		warning_str = "WARNING: We detected a higher than usual risk of spurious features\n"
		warning_str += "    and attribute ranking may be compromised. We recommend assessing\n"
		warning_str += "    the predictor's validation accuracy, and if brainome did not split\n"
		warning_str += "    the data, using -split. Otherwise try building a model without\n"
		warning_str += "    -rank and/or adding more rows to the data."
		warning(warning_str)


def run_attribute_rank(args_measureonly, args_attributerank, args_optimize, args_headerless, col_idxs_to_keep, column_index_map, igncol, inputfile, license_violation, processed_header):
	""" running attribute ranking
	requires measureonly, attributerank, optimize, headerless

	igncol : use specified ignore columns
	ign_cols : columns to be ignored due to the result of attribute ranking
	"""
	logger.info(f'to_keep : {col_idxs_to_keep}')
	with Spinner("Ranking attributes..."):
		attrib_out, ign_cols, imp_cols = \
			dmn.Meter.attributerank(
				processed_header, filename=inputfile, just_rank=args_measureonly, topn=args_attributerank,
				returnjson=True, optimize_class=args_optimize, col_idxs_to_keep=col_idxs_to_keep)

		if ign_cols:
			if args_headerless:
				ign_cols = [str(column_index_map[int(idx)]) for idx in ign_cols]
			else:
				ign_cols = ign_cols
			igncol = [str(i) for i in igncol] + ign_cols

		if imp_cols:
			if args_headerless:
				impcol = [str(column_index_map[int(idx)]) for idx in imp_cols]
			else:
				impcol = imp_cols

		# uploadfile = None
		if attrib_out.startswith("{"):		# TODO convert to try except JSONDecodeError
			# need to deference attribute_rank['columns_selected_idx'] and ['columns_ignored_idx']
			attribute_rank = json.loads(attrib_out)
			if license_violation:
				# mask out select, ignore, and non-contributing features from output by using negative indexes
				n_to_select = len(attribute_rank['columns_selected_idx'])
				n_to_ignore = len(attribute_rank['columns_ignored_idx'])
				n_noncontrib = len(attribute_rank['columns_noncontributing_idx'])
				attribute_rank['columns_selected_idx'] = \
					[-(i + 1) for i in range(0, n_to_select)]
				attribute_rank['columns_ignored_idx'] = \
					[-(i + 1) for i in range(n_to_select + n_noncontrib, n_to_select + n_noncontrib + n_to_ignore)]
				attribute_rank['columns_noncontributing_idx'] = \
					[-(i + 1) for i in range(n_to_select, n_to_select + n_noncontrib)]
				attribute_rank['test_accuracy_progression'] = \
					[[-(i + 1), progress[1]] for i, progress in enumerate(attribute_rank['test_accuracy_progression'])]
			else:
				attribute_rank['columns_selected_idx'] = \
					[column_index_map[idx] for idx in attribute_rank['columns_selected_idx']]
				attribute_rank['columns_ignored_idx'] = \
					[column_index_map[idx] for idx in attribute_rank['columns_ignored_idx']]
				attribute_rank['columns_noncontributing_idx'] = \
					[column_index_map[idx] for idx in attribute_rank['columns_noncontributing_idx']]
				attribute_rank['test_accuracy_progression'] = \
					[[column_index_map[progress[0]], progress[1]] for progress in attribute_rank['test_accuracy_progression']]
			session('attribute_rank', attribute_rank)  # nee attributerank: json
			session('ignore_columns', igncol)  # nee ignorecolums: csv
		else:
			logger.error(
				"attribute_select failed to return json. Neither attribute_rank nor ignore_columns will be defined.")
	logger.info(f'attribute_rank: {attribute_rank}')
	logger.info(f'imp col: {impcol}')
	return attribute_rank, igncol, impcol


def calculate_cols_idxs_to_keep(important_columns, attribute_rank, headerless, column_index_map, csv_header):
	if important_columns != "" and attribute_rank >= 0:
		cols_to_keep = important_columns.split(',')
		if headerless:
			col_idxs_to_keep = [int(idx) for idx in cols_to_keep]
		else:
			col_idxs_to_keep = [csv_header.index(name) for name in cols_to_keep]
		col_idxs_to_keep = [column_index_map.index(idx) for idx in col_idxs_to_keep]
	else:
		col_idxs_to_keep = []
	return col_idxs_to_keep


def calculate_algorithms(force_model: str, algorithm_type: str) -> []:
	""" calculate the algorithm desired by user
	defined by ARGS.forcemodel, regression
	possible values
	autoc, DT, RF, NN, SVM,
	autor, LR, PR
	Default supplemental build parameters are supplied in build_model()
	"""
	if force_model:
		algorithms = [force_model]
	elif algorithm_type == 'REGRESSION':
		algorithms = REGRESS_MODEL_TYPES
	else:						# algorithm_type == 'CLASSIFICATION'
		recommended_algorithm = get_session_value("data_meter", {}).get("recommended", {}).get("model")
		algorithms = CLASSIFICATION_MODEL_TYPES
		if recommended_algorithm is not None:
			# start with the preferred algorithm - eliminate duplicates
			algorithms = list(dict.fromkeys([recommended_algorithm] + algorithms))
		if not can_xgboost_test():
			logger.info("xgboost not installed - dropping RF from candidates")
			algorithms.remove("RF")
	session('algorithms', algorithms)		# record
	return algorithms


def check_args_nclasses(args_nclasses, n_classes):
	""" if the user specifies -nc 3, they expect 3 classes in the data """
	# code 51
	if (args_nclasses > 0) and (not n_classes == args_nclasses):
		reporting.print_data_meter()
		critical(51, f"Error: Found {n_classes} classes in input. Parameter --nclasses enforces {args_nclasses}.")


def run_data_meter(effort, clean_file):
	with Spinner("Pre-training measurements...") as spinner:
		# TODO figure out why spinner is corrupting capacity stdout
		meterout = dmn.Meter.datameter(filename=clean_file, json=True)
		try:
			# trim leading noise from json response
			if meterout[0] != '{':
				meterout = meterout[meterout.find("{"):]
			data_meter = json.loads(meterout)
			if data_meter.get('recommended'):
				notes = data_meter['recommendations']['notes']
				# We currently always recommend RF, so there is no point to this.
				# recommend_model = data_meter['recommended']['model']
				# if recommend_model == 'DT' and measure_only:
				# 	notes.append('We recommend using Decision Tree -f DT.')
				# elif recommend_model == 'NN' and measure_only:
				# 	notes.append('We recommend using Neural Network -f NN.')
				# elif recommend_model == 'RF' and measure_only:
				# 	notes.append('We recommend using Random Forest -f RF.')

				if effort == 1:
					notes.append(
						"If predictor accuracy is insufficient, try using the effort option -e with a value of 5 or more to increase training time.")
			data_meter['start_time'] = spinner.start_time.timestamp()
			data_meter['end_time'] = time.time()
			session('data_meter', data_meter)
		except json.JSONDecodeError as decode_err:
			# TODO code 75 former
			logger.warning(f'data_meter returned _NOT_ json {meterout}')
			session("data_meter", {})
			warning("data_meter returned _NOT_ json", exc=decode_err)
			# print(str(decode_err))


def process_classmap(args_classmapping: str, remapping: str) -> str:
	"""
	Define the ultimate classmap object.
	"""
	classmap = "{}"
	if args_classmapping != "{}":
		classmap = args_classmapping
	if str(remapping) != "{}":
		classmap = str(remapping)
	if args_classmapping != "{}" and str(remapping) == "{}":
		session('class_mapping', json.loads(classmap.replace('\'', '\"')))
	else:
		session('class_mapping', remapping)
	return classmap


def check_license_terms(server, port, quiet) -> bool:
	""" returns True when daysleft or LICENSETYPE or LICENSEOK fail """
	violation = False
	dmn.Meter.dontconnect(server=server, port=port, quiet=quiet)
	logger.debug(f"PermissionsManager.daysleft()={dmn.PermissionsManager.daysleft()}")
	logger.debug(f"PermissionsManager.LICENSETYPE={dmn.PermissionsManager.LICENSETYPE}")
	logger.debug(f"PermissionsManager.LICENSEOK={dmn.PermissionsManager.LICENSEOK}")
	if dmn.PermissionsManager.daysleft() < 1:
		# code 104
		violation = True
		warning(f"License has expired {dmn.PermissionsManager.EXPIRATION.isoformat()}..")
		set_exit_code(104)
	if dmn.PermissionsManager.LICENSETYPE > 3:
		# code 103
		violation = True
		warning("Error validating license file.")
		set_exit_code(103)
	if not dmn.PermissionsManager.LICENSEOK:
		# code 105
		violation = True
		reporting.print_basic()
		critical(105, "License is terminated.")
		# sys.exit(105)
	return violation


def run_terminate_command(server, port):
	dmn.Meter.lightconnect(server, port)
	if dmn.Meter.terminate():
		note("All cloud processes terminated.")
		reporting.print_basic()
		raise BrainomeExit
		# sys.exit(0)
	else:
		# code 40
		critical(40, "Error: Cannot run terminate. Try again.")
		# sys.exit(40)


def run_wipe_command(server, port):
	dmn.Meter.lightconnect(server, port)
	if dmn.Meter.terminate() and dmn.Meter.wipe():
		note("All cloud files wiped.")
		reporting.print_basic()
		raise BrainomeExit
		# sys.exit(0)
	else:
		# code 41
		critical(41, "Error: Cannot run wipe. Try again.")
		# sys.exit(41)


def run_chpasswd_command(server, port):
	dmn.Meter.lightconnect(server, port)
	dmn.Meter.chpasswd(server, port)
	logger.debug("User password changed.")
	reporting.print_basic()
	raise BrainomeExit
	# sys.exit()


def run_logout_command():
	dmn.Meter.logout()
	logger.debug("User logged out.")
	reporting.print_basic()
	raise BrainomeExit
	# sys.exit()


def run_login_command(server, port, args_email, args_pswd):
	dmn.Meter.logout()
	dmn.Meter.lightconnect(server, port, user_email=args_email, user_pswd=args_pswd)
	note("User logged in.")
	reporting.print_basic()
	raise BrainomeExit
	# sys.exit()


def finish_cleanonly_mode(
	args_classmapping, inputfile,
	classmap, igncol, ignorelabels, n_attrs, n_classes, remapping, target):
	# shove these variables into the global context destine for the predictor a.py
	global mappingstr, targetstr, ignorelabelstr, ignorecolumnstr
	clean_report, mappingstr, targetstr, ignorelabelstr, ignorecolumnstr = \
		get_clean_report(
			inputfile,
			args_classmapping, classmap, remapping,
			ignorelabels, igncol, n_classes, n_attrs, target)
	# record clean_report
	session('clean_report', clean_report)  # save clean report into report
	# report("READY.", verbose_level=1)
	reporting.print_data_meter()
	raise BrainomeExit
	# sys.exit(0)


def check_license_limits(inputfile, n_attrs, n_instances) -> bool:
	""" returns True when dataset metrics exceed license dataset limits """
	violation = False
	limits_warning = ""  # no message...
	filesize_in_mb = os.path.getsize(inputfile) / 1048576  # MB = 1024.0 * 1024.0
	session('filesize_in_mb', "{:.4f}".format(filesize_in_mb))
	# testing max file size limit: zero means no limits
	if 0 < dmn.PermissionsManager.MAXFILESIZEMB < filesize_in_mb:
		violation = True
		limits_warning += f"\tData file size: {math.ceil(filesize_in_mb)} MB > {dmn.PermissionsManager.MAXFILESIZEMB} MB maximum file size\n"
		set_exit_code(53)
	# testing max instances limit: zero means no limits
	session('instances', str(n_instances))
	if 0 < dmn.PermissionsManager.MAXINSTANCES < n_instances:
		violation = True
		limits_warning += f"\tInstances: {n_instances} > {dmn.PermissionsManager.MAXINSTANCES} maximum instances.\n"
		set_exit_code(54)
	# testing max attributes limit: zero means no limits
	session('attributes', str(n_attrs))
	if 0 < dmn.PermissionsManager.MAXATTRIBS < n_attrs:
		violation = True
		limits_warning += f"\tAttributes: {n_attrs} > {dmn.PermissionsManager.MAXATTRIBS} maximum attributes."
		set_exit_code(55)
	if violation:
		warning(
			"Please upgrade your license to save your predictor and unmask attribute importance information by contacting sales@brainome.ai\n" + limits_warning)
	return violation


def process_dataset_to_clean(
	args_target, args_headerless, args_nsamples, args_ignorelabels, args_classmapping,
	ignore_columns_list, args_use_columns, inputfile, regression):
	preprocessesed = False
	subsampled = False
	try:
		"""
			SUBSAMPLE if -nsamples
			capture ogheader
			PREPROCESS if -target or -ignorecolumns or -ignorelabels
		"""
		fd1, tmpfile1 = tempfile.mkstemp()
		fd2, tmpfile2 = tempfile.mkstemp()
		if args_nsamples > 0:
			with Spinner("Sampling..."):
				subsampled = dmnu.subsample(inputfile, tmpfile2, int(args_nsamples), headerless=args_headerless)
			inputfile = tmpfile2
			if subsampled:
				note(
					"Note: Results on subsampled data may differ from original. Use -nsamples 0 to work on the entire data set.")
			else:
				warning(f"Warning: Attempted subsampling with {args_nsamples} samples but failed to reduce size.")

		ignore_labels_list = args_ignorelabels.split(',') if args_ignorelabels else []
		with Spinner("Cleaning...") as spinner:
			# retrieve header of file after concat and subsampled as ogheader
			header = get_csv_file_header(inputfile, args_headerless)

			n_classes, n_instances, n_attrs, remapping, processed_header, column_index_map, all_classes, class_counts \
				= cln.clean(
					inputfile, cleanfile, target=args_target, headerless=args_headerless,
					ignorecolumns=ignore_columns_list, use_columns_list=args_use_columns,
					ignorelabels=ignore_labels_list, alphanumeric=False, numeric=False, regression=regression)

			# checking for number of classes > 1
			n_ignored_classes = len(ignore_labels_list)
			if n_classes <= 1 and not regression:
				error_str = f'There must be at least two classes in the data after removing classes. The data contained {len(all_classes)} classes'
				if n_ignored_classes == 1:
					error_str += ' and 1 class was removed.'
				else:
					error_str += f' and {n_ignored_classes} classes were removed.'
				critical(67, error_str)
				# sys.exit(67)

			if not regression:
				# checking for singleton classes
				singletons = [label for label in class_counts if class_counts[label] == 1]
				if len(singletons) > 0:
					# if len(singletons) == 1:
					# 	error_str = f"\nEach class must occur at least twice in the data but the class \"{singletons[0]}\" has only one instance."
					# else:
					# 	error_str = f"\nEach class must occur at least twice in the data but the class \"{singletons[0]}\" and {len(singletons) - 1} others have only one instance."
					msg = f"\nYour data contains {len(singletons)} classes with only one instance and {n_classes} total classes. If this is not expected, the target column may have been "
					msg += "mis-specified. Would you like to continue? (y/N)  "
					rsp = spinner.ask(msg)
					if not rsp:
						critical(59, "Error: User abort.")
						# sys.exit(59)

				bad_ignored_classes = [clss for clss in ignore_labels_list if clss not in all_classes]
				if len(bad_ignored_classes) > 0:
					error_str = '\nThere were classes specified for removal that were not found in the input data.\n'
					error_str += f'Classes in the data: {all_classes}\n'
					error_str += f'Classes to be removed: {ignore_labels_list}\n'
					error_str += f'Classes to be removed not in the data: {bad_ignored_classes}'
					critical(68, error_str)
					# sys.exit(68)

			session('header', header)
			session('processed_header', processed_header)
			session('column_index_map', column_index_map)

		if args_classmapping != "{}" and remapping != {}:
			raise ValueError("Manual class mapping must be onto contiguous integers from 0 to n.")

		inputfile = cleanfile

	except MemoryError as memx:
		# code 53  MemoryError
		note(
			'Brainome can handle millions of instances and attributes. To increase your license limitations, please contact our sales team at sales@brainome.ai')
		critical(53, "MemoryError: ", exc=memx)
		# sys.exit(53)

	except ValueError as valx:
		# code 54  ValueError license restriction
		note(
			'Brainome can handle millions of instances and attributes. To increase your license limitations, please contact our sales team at sales@brainome.ai')
		critical(54, "ValueError: ", exc=valx)
		sys.exit(54)

	finally:
		try:  # putting these in try/except because of a Windows 10 glitch
			if os.path.exists(tmpfile1):
				os.remove(tmpfile1)
			if os.path.exists(tmpfile2):
				os.remove(tmpfile2)
		except OSError as ose:
			warning("Exception encountered while cleaning tmp file ", exc=ose)
			pass
	# normal return
	return column_index_map, ignore_labels_list, inputfile, n_attrs, n_classes,\
		n_instances, preprocessesed,\
		processed_header, remapping, subsampled


def is_args_classification(ARGS) -> bool:
	""" return True if args only work with classification """
	# TODO obsolete codes 109 - 115
	return ARGS.ignorelabels or\
		ARGS.biasmeter or\
		ARGS.balance or\
		ARGS.optimize != 'all' or\
		ARGS.nclasses or\
		ARGS.classmapping != '{}' or\
		ARGS.nopriming or\
		ARGS.attributerank > 0 or\
		ARGS.effort != 1 or\
		ARGS.stopat != 100 or\
		ARGS.regularization_strength != 0.001 or\
		ARGS.forcemodel in CLASSIFICATION_MODEL_TYPES or\
		ARGS.force_classify


def is_args_regression(args_forcemodel, args_force_regress) -> bool:
	""" return True if args only work with regression """
	# TODO add ARGS.degree to force PR
	return args_forcemodel in ["LR", "PR"] or\
		args_force_regress


def calculate_algorithm_type(ARGS, args_headerless, inputfile, target_column) -> str:
	""" returns CLASSIFICATION or REGRESSION """
	global trainfile
	try:
		if is_args_classification(ARGS):
			algorithm_type = "CLASSIFICATION"
			# note('Detected classification problem.')

		elif is_args_regression(ARGS.forcemodel, ARGS.force_regress):
			algorithm_type = "REGRESSION"

		elif is_dataset_regression(inputfile, args_headerless, target_column):
			algorithm_type = "REGRESSION"
			note('Detected regression problem.')
			if ARGS.verbosity > 1:
				note('To override, use -classify to force classification model.')
		else:
			note('Defaulted to classification problem.')
			algorithm_type = "CLASSIFICATION"
	except UnableToDetectError:
		note('Defaulted to classification problem.')
		algorithm_type = "CLASSIFICATION"
		if ARGS.verbosity > 1:
			note('To override, use -regress to force regression model.')
	return algorithm_type


def process_inputfiles(args_input: list, args_headerless: bool):
	""" takes args_input as an array of dataset paths.
		i) download any dataset URLs
		ii) concatenate datasets into

		inputfiles == [csv file names]
		inputfile == csv file name
	"""
	global trainfile
	inputfiles = []
	# URL and compressed file handling
	# try:
	session("input_files", args_input)
	# download urls/check dataset file name
	for uinput in args_input:
		if "://" in uinput:
			inputfiles.append(download_dataset_url(uinput))
		else:
			if os.path.exists(uinput):
				inputfiles.append(uinput)
			else:
				critical(49, f"File not found: {uinput}")
	# unpack gz files
	for filename in inputfiles:
		if filename.endswith(".gz"):
			with Spinner(f"Unpacking {filename}") as spinner:
				newfilename = os.path.basename('.'.join(filename.split('.')[:-1]))
				# challenge unpack overwrite
				if os.path.exists(newfilename):
					rsp = spinner.ask(
						f"\nOverwrite local file {newfilename} ? [y/N]")
					if not rsp:
						critical(49, f"User abort overwriting {newfilename}")
				# unpack
				with gzip.open(filename, 'rb') as f_in:
					with open(newfilename, 'wb') as f_out:
						shutil.copyfileobj(f_in, f_out)
				inputfiles[inputfiles.index(filename)] = newfilename
	# except BrainomeError as e:
	# 	# code 49
	# 	critical(49, "Error: " + str(e))
	# 	sys.exit(49)
	# determine inputfile and trainfile
	if len(inputfiles) > 1:
		report("Multiple input files: " + (" ".join(inputfiles)), verbose_level=2)
		inputfile = "mergedfiles.csv"
		trainfile = os.path.basename(os.path.basename(inputfiles[0]) + " et al.")
		dmnu.concatcsv(inputfile, inputfiles, args_headerless)
	else:
		inputfile = inputfiles[0]
		report("Input: " + inputfile, verbose_level=2)
		trainfile = os.path.basename(inputfile)
	return inputfile, trainfile


def download_dataset_url(dataset_url):
	""" download url, prompt if overwriting
	return local file name
	"""
	try:
		fname = urllib.request.urlopen(urllib.request.Request(dataset_url, method='HEAD')).info().get_filename()
		if fname is None:
			fname = dataset_url.split('/')[-1]
		with Spinner(f"Downloading {fname}") as spinner:
			if os.path.exists(fname):
				rsp = spinner.ask(f"Download from {dataset_url} overwrites existing file {fname}. OK? [y/N]")
				if not rsp:
					# TODO define error code for this
					critical(99, "User abort (overwriting output file).")
			urllib.request.urlretrieve(dataset_url, fname)
		return fname
	except URLError as url_error:
		critical("URL cannot be opened: " + str(dataset_url), exc=url_error)


def calculate_outputfile(args_output: str, safe_overwrite: bool, args_onnx: bool, args_language: bool) -> str:
	""" given an args_output filename, what does it mean???
	warn on overwrite
	returns output_file
	"""
	output_file = args_output  # outputfile will be onnx or out or py (never exe)
	if args_language == "exe":
		# code 45
		if output_file.endswith(".py") or output_file.endswith(".csv"):
			critical(45, "Error: Executable file cannot end in .py or .csv")

	elif args_onnx:
		# code 46
		if not output_file.endswith(".onnx"):
			critical(46, "Error: The output filename for onnx must be .onnx")

	# code 46
	elif output_file.endswith(".csv"):
		critical(46, "Error: To prevent potential loss of data, brainome will not create files ending with csv.")
		# sys.exit(46)

	# only warn about overwriting output file
	if not safe_overwrite and os.path.exists(output_file) and output_file != "a.py":
		warning(f"Warning: Overwriting existing output file {output_file}")

	# TODO remove code 47 & 48
	return output_file


def validate_dataset_cols(
	args_headerless: bool, args_target: str, args_ignorecolumns: str, args_importantcolumns: str, args_attributerank: int,
	csv_header: []):
	""" sets target and target_column: int
	"""
	return_ignore_columns = []
	target_column = ""		# placeholder
	# process target and target_column
	if args_headerless:
		if args_target and int(args_target) not in csv_header:
			critical(
				50,
				f"The file is headerless and the specified target column index {args_target} does not exist (valid indices are [0, ..., {len(csv_header) - 1}]).")
			# sys.exit(50)
		else:
			target_column = int(args_target) if args_target else len(csv_header) - 1

	else:		# not args_headerless:
		if args_target and args_target not in csv_header:
			critical(50, f"The specified target {args_target} could not be found in header.")
			# sys.exit(50)
		else:
			target_column = csv_header.index(args_target) if args_target else len(csv_header) - 1

	# process ignorecolumns
	if args_ignorecolumns != '':
		return_ignore_columns = args_ignorecolumns.split(',')
		# validate ignore columns
		for col in return_ignore_columns:
			if args_headerless:
				if int(col) >= len(csv_header):
					critical(100, "A provided ignore columns index is out of bounds")
					# sys.exit(100)
			else:		# not args_headerless
				if col not in csv_header:
					critical(100, f"ignore column {col} not found in csv header.")
					# sys.exit(100)
		if len(csv_header) - len(args_ignorecolumns.split(',')) <= 1:
			critical(51, "Error: Cannot ignore all features. Header length: " + str(len(csv_header)) + str(
				", Number of Ignored Columns: ") + str(len(args_ignorecolumns.split(','))))
			# sys.exit(51)

	# SETTING TARGET HERE
	target = csv_header[-1] if args_target == "" else args_target

	# process important columns
	if args_importantcolumns != "":
		for name in args_importantcolumns.split(','):
			if args_headerless:
				if int(name) not in csv_header:
					critical(58, f'Error: Feature {name} is not in the header.')
			else:
				if name not in csv_header:
					critical(58, f'Error: Feature {name} is not in the header.')
		if args_attributerank < 0:
			cols_to_keep = args_importantcolumns.split(',')
			cols_to_keep.append(str(target))
			# override user ignore columns with attribute ranked cols
			return_ignore_columns = [str(x) for x in csv_header if str(x) not in cols_to_keep]

	return str(target), target_column, return_ignore_columns


def build_model(ARGS, algorithm, n_instances, numseeds, outputfile):
	""" build a model
	>>>> STOPS ARGS PROPAGATION HERE <<<<<
	"""
	effort = ARGS.effort
	if algorithm == "SVM":
		build_SVM_model(ARGS.regularization_strength, effort, ARGS.forcesplit)

	# Decision Tree #################
	elif algorithm == "DT":
		build_DT_model(ARGS.nopriming, effort, ARGS.forcesplit, ARGS.stopat, ARGS.verbosity, n_instances)

	# Random Forest #################
	elif algorithm == "RF":
		build_RF_model(ARGS.nopriming, effort, ARGS.forcesplit)

	# Neural Net #########################
	elif algorithm == "NN":
		build_NN_model(
			ARGS.balance, ARGS.nopriming, effort, ARGS.forcesplit,
			ARGS.stopat, ARGS.verbosity, ARGS.onnx, ARGS.optimize,
			numseeds, outputfile)

	elif algorithm == "LR":
		build_LR_model(alpha=ARGS.lr_regularization_strength)

	else:
		# algorithm unknown
		# TODO need error code for unknown algorithm
		critical(999, f'Unknown algorithm {algorithm}')
	# record effort used
	session("effort", effort)


def build_LR_model(alpha):
	""" Build a LR Model """
	with Spinner("Building LR model..."):
		dmn.Meter.buildLRModel(alpha=alpha)

def build_NN_model(
	args_balance, args_nopriming, args_effort,
	args_forcesplit, args_stopat, args_verbosity, args_onnx, args_optimize,
	numseeds, outputfile):
	""" Build A NN model, """
	with Spinner("Architecting NN model..."):
		dmn.Meter.buildModel(rigor=numseeds, balance=args_balance)
	report(dmn.Meter.modelmeter(), 1)
	estimate_neural_net = {}
	if not args_nopriming:
		# if False:
		# 	with Spinner("Estimating time to prime model..."):
		# 		timep = dmn.Meter.estimatePrimingTime(json=bool(args_json))
		# 	if bool(args_json):
		# 		estimate_neural_net.update({"est_priming_time":timep})
		# 	else:
		# 		report("Estimated time to prime model: {0}".format(timep), verbose_level=1)
		with Spinner("Priming NN model..."):
			dmn.Meter.primeModel(target=args_stopat / 100.0, favor_class=args_optimize, balance=args_balance)
	if not args_nopriming and args_effort > 1:
		# if False:
		# 	with Spinner("Estimating training time..."):
		# 		timep = dmn.Meter.estimateRigorTime(rigor=args_effort, json=bool(args_json))
		# 	if bool(args_json):
		# 		estimate_neural_net.update({"est_training_time":timep})
		# 	else:
		# 		report("Estimated training time: {0}".format(timep), verbose_level=1)
		signal.signal(signal.SIGINT, ctrlchandler2)
		with Spinner("Training NN..."):
			dmn.Meter.rigorRun(
				rigor=args_effort, optimize_class=args_optimize, balance=args_balance,
				cleanfile=cleanfile, upload=False, forcesplit=args_forcesplit)
		signal.signal(signal.SIGINT, ctrlchandler)
	# record neural network time estimates
	session('estimate_neural_net', estimate_neural_net)
	# removed printModel as per #1505
	# if args_verbosity > 2:
	# 	report("NN Model created")
	# 	dmn.Meter.printModel()
	if args_onnx:
		with Spinner("Building ONNX graph..."):
			dmn.Meter.getONNXModel(outputfile, visualize=False)


def build_RF_model(args_nopriming, args_effort, args_forcesplit):
	""" build a RD model """
	with Spinner("Building RF model..."):
		dmn.Meter.buildXGBModel()
	if not args_nopriming and args_effort > 1:
		with Spinner("Training RF..."):
			dmn.Meter.rigorRun(rigor=args_effort, cleanfile=cleanfile, forcesplit=args_forcesplit, upload=False)
		signal.signal(signal.SIGINT, ctrlchandler)


def build_DT_model(args_nopriming, args_effort, args_forcesplit, args_stopat, args_verbosity, n_instances):
	"""
	Build a DT model
	"""
	with Spinner("Building DT classifier..."):
		dmn.Meter.buildMEModel(target=args_stopat / 100.0)
	if not args_nopriming and args_effort > 1:
		if args_verbosity > 0:
			estimateMETime(
				n_instances * args_effort * 10, verb="train")
		signal.signal(signal.SIGINT, ctrlchandler2)
		with Spinner("Training DT..."):
			dmn.Meter.rigorRun(rigor=args_effort, cleanfile=cleanfile, forcesplit=args_forcesplit, upload=False)
		signal.signal(signal.SIGINT, ctrlchandler)


def build_SVM_model(args_regularization_strength, args_effort, args_forcesplit):
	""" build SVM model
	uses ARGS.regularization_strength
	ARGS.effort,
	ARGS.forcesplit
	"""
	with Spinner("Building SVM classifier..."):
		dmn.Meter.buildSVM(C=args_regularization_strength)
	if args_effort > 1:
		signal.signal(signal.SIGINT, ctrlchandler2)
		with Spinner("Training SVM..."):
			dmn.Meter.rigorRun(rigor=args_effort, cleanfile=cleanfile, forcesplit=args_forcesplit, upload=False)
		signal.signal(signal.SIGINT, ctrlchandler)


def generate_predictor(
	args_headerless, args_input, args_classmapping, args_attributerank, args_ignorecolumns, args_ignorelabels, args_novalidation, args_optimize,
	algorithm, classmap, csv_header, igncol, important_column_list, ignorelabels,
	license_violation, n_attrs, n_classes, preprocessesed, regression, remapping, target,
	target_column, outputfile, starttime, sysargs):

	encrypted_model_file = ""  # placeholder

	with Spinner(f"Compiling {algorithm} predictor..."):
		jsonout = dmn.Meter.get_model_info()
		jsonout = jsonout.replace("'", '"')
		model_info = eval(jsonout)  # json.loads(jsonout)
		if 'critical_error' in model_info or len(model_info['errors']) > 0:
			error_type = model_info['errors'][0] or model_info['critical_error']
			critical(1, f'An exception of type {error_type} occured.')
			# sys.exit(1)

		ogheader = [str(x) for x in csv_header]

		if args_headerless:
			if target == "":
				importantidxs = sorted([int(ogheader[int(i)]) for i in important_column_list])
			else:
				target_idx = int(target)
				importantidxs_pre_shift = sorted([int(ogheader[int(i)]) for i in important_column_list])
				importantidxs = [x - 1 if x > target_idx else x for x in importantidxs_pre_shift]
		else:
			if target == "":
				importantidxs = sorted([ogheader.index(x) for x in important_column_list])
			else:
				target_idx = ogheader.index(target)
				importantidxs_pre_shift = sorted([ogheader.index(x) for x in important_column_list])
				importantidxs = [x - 1 if x > target_idx else x for x in importantidxs_pre_shift]

		predictor_vars = {
			'license_str': '',
			'header_str': '',
			'system_meter_str': '',
			'add_cleanfile_flag': True,
			'model_type': '\'' + algorithm + '\'',
			'trainfile': args_input,
			'mapping': remapping if remapping != {} else args_classmapping,
			'ignore_labels': ignorelabels,
			'ignore_cols': igncol,
			'target': f"\'{target}\'",
			'target_column': target_column,
			'important_idxs': importantidxs,
			'n_attrs': n_attrs,
			'expected_feature_cols': len(igncol) + len(importantidxs),
			'n_classes': n_classes,
			'column_mappings': model_info['column_mappings'],
			'model_cap': model_info['model_cap'],
			'energy_thresholds': model_info['energy_thresholds'],
			'leaf_labels': model_info['leaf_labels'],
			'default_label': model_info['default_label'],
			'list_of_cols_to_normalize': model_info['list_of_cols_to_normalize'],
			'pcatrue': model_info['pcatrue'],
			'whiten': model_info['whiten'],
			'start_label': model_info['start_label'],
			'n_boosters': model_info['n_boosters'],
			'w_h': model_info['w_h'],
			'b_h': model_info['b_h'],
			'w_o': model_info['w_o'],
			'b_o': model_info['b_o'],
			'pca_mean': model_info['pca_mean'],
			'pca_components': model_info['pca_components'],
			'explained_variance': model_info['explained_variance'],
			'n_output_logits': model_info['n_output_logits'],
			'preprocess_required': (args_ignorecolumns != "" and args_attributerank < 0) or target != "" or args_ignorelabels != "",
			'yes_children_dict': model_info['yes_children_dict'],
			'split_feats_dict': model_info['split_feats_dict'],
			'split_vals_dict': model_info['split_vals_dict'],
			'logits_dict': model_info['logits_dict'],
			'preprocess_in_clean': args_attributerank >= 0 and len(importantidxs) < n_attrs and target == "" and args_ignorelabels == "",
			'svm_coef': model_info['svm_coef'],
			'svm_intercept': model_info['svm_intercept'],
			'svm_ranking': model_info['svm_ranking'],
			'lr_coef': model_info['lr_coef'],
			'lr_intercept': model_info['lr_intercept'],
		}
	if args_novalidation:
		sys_meter_out = {}			# placeholders
		print_system_meter = "\n -novalidation"		# placeholder
		predictor_vars['add_cleanfile_flag'] = False
		predictor_vars['header_str'] = get_header(starttime, sysargs)
		predictor_vars['license_str'] = dmn.PermissionsManager.getLicenseString()
		if not license_violation:
			with open(outputfile, 'w+') as f:
				print(reporting.print_predictor(data=predictor_vars, regression=regression), file=f)
		else:
			note("Note: Not producing a predictor output file due to exceeded limits.")
	else:
		# session('predictor', predictor_vars)
		if not license_violation:
			with open(stubfile, 'w+') as f:
				print(reporting.print_predictor(data=predictor_vars, regression=regression), file=f)
		else:
			model_as_str = reporting.print_predictor(data=predictor_vars, regression=regression)
			model_as_str = model_as_str[model_as_str.find('import sys'):]
			model_encrypted = encrypt(model_as_str)
			fd, encrypted_model_file = tempfile.mkstemp()
			with open(encrypted_model_file, 'w+') as out:
				print(model_encrypted, end='', file=out)

		# do_upload = ((not preprocessesed) or (args_attributerank >= 0)) and (
		# 	not ((not preprocessesed) or (args_attributerank >= 0)))
		with Spinner(f"Validating {algorithm} predictor...") as spinner:
			system_meter_json = dmn.Meter.systemmeter(
				stubfile,
				json=True,			# TODO obsolete old json param
				optimize_class=args_optimize,
				cleandata=cleanfile,
				upload=False,		# former do_upload above
				model_as_str=encrypted_model_file,
				regression=regression,
			)
			try:
				# TODO Spinner is putting characters in the stdout channel
				if not system_meter_json:
					system_meter_json = '{"classes": 0}'		# most likely an error...
				if system_meter_json[0] != '{':
					system_meter_json = system_meter_json[system_meter_json.find("{"):]

				sys_meter_out = json.loads(system_meter_json)
				if not regression:
					# TODO move this to where it always gets populated issue #591
					if classmap == "{}":
						sys_meter_out['confusion_matrix_labels'] = \
							[str(i) for i in range(0, n_classes)]
					else:
						sys_meter_out['confusion_matrix_labels'] = \
							[i[0] for i in sorted(eval(classmap).items(), key=lambda x: x[1])]
					# populate classifier type from num classes
					num_classes = sys_meter_out['classes']
					if n_classes == 2:
						sys_meter_out["system_type"] = "Binary classifier"
					else:
						sys_meter_out["system_type"] = str(num_classes) + "-way classifier"
				sys_meter_out['start_time'] = spinner.start_time.timestamp()
				sys_meter_out['end_time'] = time.time()
				# map column indexes in attribute_ranking to original inputfile positions
				rf_ranking = sys_meter_out.get('attribute_ranking')
				if rf_ranking:
					if target == "":
						csv_indices_for_selected_cols = importantidxs
					else:
						csv_indices_for_selected_cols = importantidxs_pre_shift
					# csv_indices_for_selected_cols = \
					# 	[i for i, x in enumerate(csv_header) if str(x) not in [str(y) for y in igncol] and str(x) != str(target)]
					if license_violation:
						# mask out ranking of features with negative indexes
						new_ranking = {-(i + 1): rf_ranking[key] for i, key in enumerate(rf_ranking.keys())}
					else:
						new_ranking = \
							{csv_indices_for_selected_cols[int(key)]: rf_ranking[key] for key in rf_ranking}
					sys_meter_out['attribute_ranking'] = new_ranking

			except json.JSONDecodeError as decode_err:
				# TODO code 75 former
				logger.warning(f'system_meter returned _NOT_ json {system_meter_json}')
				session(f"system_meter_{algorithm}", {})
				warning(f"system_meter_{algorithm} returned _NOT_ json", exc=decode_err)
				return None, {}, ""

		# track progress system_meter_XX
		session(f"system_meter_{algorithm}", sys_meter_out)
		session("system_meter", sys_meter_out, overwrite=True)		# load into old system_meter so that the predictor can have stats
		session("algorithm", algorithm, overwrite=True)

		print_system_meter = reporting.render_system_meter()
		predictor_vars['add_cleanfile_flag'] = False
		predictor_vars['system_meter_str'] = '"""\n' + print_system_meter + '\n"""'
		predictor_vars['header_str'] = get_header(starttime, sysargs)
		predictor_vars['license_str'] = dmn.PermissionsManager.getLicenseString()
		if not license_violation:
			with open(outputfile, 'w+') as f:
				print(reporting.print_predictor(data=predictor_vars, regression=regression), file=f)
		else:
			note("Note: Not producing a predictor output file due to exceeded limits.")
	return encrypted_model_file, sys_meter_out, print_system_meter


""" global list of temp files for cleanup """
temp_files_to_cleanup = []


def defer_temp_file(temp_file):
	""" accumulate temp files for cleanup"""
	global temp_files_to_cleanup
	temp_files_to_cleanup.append(temp_file)


def clean_temp_files():
	""" clean up temporary files
	cleanfile, stubfile, mergedfiles.csv, model_file
	"""
	try:
		if not os.getenv('BTCDEBUG'):  # do not clean up if BTCDEBUG is set
			if os.path.exists(cleanfile):
				os.remove(cleanfile)
			if os.path.exists(stubfile):
				os.remove(stubfile)
			if os.path.exists("mergedfiles.csv"):
				os.remove("mergedfiles.csv")
			for file in temp_files_to_cleanup:
				if os.path.exists(file):
					os.remove(file)
	except OSError as cleanexp:
		logger.info("error cleaning temp files", exc_info=cleanexp)


def create_bias_meter(dmn, outputfile, algorithm):
	""" create the bias meter output
	"""
	bias_meter = {}		# initialize ffs
	with Spinner(f"Measuring {algorithm} bias..."):
		bias_out = dmn.Meter.biasmeter(outputfile, json=True)
		try:
			if not bias_out:
				logger.warning("biasmeter errored out.")
				return None
			# trim leading noise from json response
			if bias_out[0] != '{':
				bias_out = bias_out[bias_out.find("{"):]

			bias_meter = json.loads(bias_out)
		except json.JSONDecodeError as decode_err:
			warning("error decoding bias meter {0}".format(bias_out), exc=decode_err)
			bias_meter = {"error": "bias out decode error"}

		bias_meter['algorithm'] = algorithm
		return bias_meter


def create_binary_predictor(args_output, outputfile):
	""" using pyinstaller to create a binary executable from outputfile
	requires pyinstaller
	creates temp directory for working
	"""
	# TODO reconcile exe outputfile as a.py vs a.out
	with Spinner(f"Creating binary executable {outputfile}..."):
		import PyInstaller.__main__
		import pkg_resources
		builddir = tempfile.mkdtemp()
		commandline = [
			'--name=%s' % args_output,
			'--onefile',
			'--workpath=' + builddir,
			'--strip',
			'-y',
			'--clean',
			'--log-level=WARN',
			'--distpath=./',
			os.path.join(outputfile)]
		if os.path.exists("icon.ico"):
			commandline = commandline + ['-i=icon.ico']
		if os.path.exists("icon.icns"):
			commandline = commandline + ['-i=icon.icns']
		if os.path.exists("Info.plist"):
			commandline = commandline + ['--osx-bundle-identifier=Info.plist']
		if os.path.exists("Manifest.xml"):
			commandline = commandline + ['-m=Manifest.xml']
		try:
			PyInstaller.__main__.run(commandline)

			if os.path.exists(args_output + ".spec"):
				os.remove(args_output + ".spec")
			shutil.rmtree(builddir)

		except ModuleNotFoundError:
			logger.warning("pyinstaller not loaded. Please run pip install pyinstaller")

		except pkg_resources.DistributionNotFound:
			logger.warning("pyinstaller not loaded. Please run pip install pyinstaller")

		except ImportError:
			logger.warning("pyinstaller not loaded. Please run pip install pyinstaller")

		except OSError as file_err:
			logger.warning("error removing binary .spec file", exc_info=file_err)

		except Exception as ex:
			logger.warning("misc. error returned by pyinstaller", exc_info=ex)


def get_csv_file_header(input_file: str, is_headerless: bool):
	""" open inputfile and return a [str] or [integer] with all header names """
	with open(input_file) as f:
		if is_headerless:
			ncols = len(next(csv.reader(f), None))
			header = [i for i in range(ncols)]		# manufacture header 0, 1, 2, 3, ...
		else:
			header = next(csv.reader(f), None)		# extract first line from file
		return header


# used to start debugger in pycharm
if __name__ == '__main__':
	sys.exit(main(sys.argv[0:]))
