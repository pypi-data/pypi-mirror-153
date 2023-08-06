#!/usr/bin/env python
# encoding: utf-8

import os

from setuptools import setup


here = os.path.abspath(os.path.dirname(__file__))


tests_require = [
	]

setup(
		name = "cro-validate",
		version = "0.0.37",

		description = "CRO Validation Library",
		long_description = "",
		url = "https://github.com/crosoftware/cro_validate",
		license = "MIT",
		author_email = "develop@crosoftware.net",
		keywords = [],

		packages = [
				'cro_validate',
				'cro_validate.api',
				'cro_validate.classes',
				'cro_validate.enum',
				'cro_validate.input',
				'cro_validate.util'
			],

		namespace_packages = [
			],

		setup_requires = [
				'pytest-runner',
			],

		tests_require = tests_require,

		install_requires = [
			],

		extras_require = dict(
				development = tests_require + [
						'backlash',
						'waitress',
						'pudb',
						'ptpython',
						'ipython',
					],
			),

		zip_safe = True,

		entry_points = {
				}
	)
