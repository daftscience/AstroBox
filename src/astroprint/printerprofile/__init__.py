# coding=utf-8
__author__ = "Daniel Arroyo. 3DaGogo, Inc <daniel@3dagogo.com>"
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'

# singleton
_instance = None

def printerProfileManager():
	global _instance
	if _instance is None:
		_instance = PrinterProfileManager()
	return _instance

import os
import yaml
import logging

from octoprint.settings import settings

class PrinterProfileManager(object):
	def __init__(self):
		self._settings = settings()
		self._infoFile = self._settings.get(['printerParameters', 'infoFile']) or "%s/printer-profile.yaml" % os.path.dirname(self._settings._configfile)
		self._logger = logging.getLogger(__name__)

		self.data = {
			'extruder_count': 1,
			'heated_bed': True
		}

		if not os.path.isfile(self._infoFile):
			open(self._infoFile, 'w').close()

		if self._infoFile:
			config = None
			with open(self._infoFile, "r") as f:
				config = yaml.safe_load(f)

			def merge_dict(a,b):
				for key in b:
					if isinstance(b[key], dict):
						merge_dict(a[key], b[key])
					else:
						a[key] = b[key]

			if config:
				merge_dict(self.data, config)

	def save(self):
		with open(self._infoFile, "wb") as infoFile:
			yaml.safe_dump(self.data, infoFile, default_flow_style=False, indent="    ", allow_unicode=True)

	def set(self, changes):
		for k in changes:
			if k in self.data:
				self.data[k] = self._clean(k, changes[k])
			else:
				this._logger.error("trying to set unkonwn printer profile field %s to %s" % (k, str(changes[k])))

	def _clean(self, field, value):
		if field == 'extruder_count':
			return int(value)
		elif field == 'heated_bed':
			return bool(value)
