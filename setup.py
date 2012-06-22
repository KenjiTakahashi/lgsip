# -*- coding: utf-8 -*-
# This is a part of lgsip @ http://github.com/KenjiTakahashi/lgsip/
# Karol "Kenji Takahashi" Wozniak (C) 2012
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup

setup(
    name='lgsip',
    version='0.1',
    description='Logic Gate Simulator In Python.',
    long_description=open('README.rst').read(),
    author='Karol "Kenji Takahashi" Woźniak',
    author_email='wozniakk@gmail.com',
    license='GPL3',
    url='http://github.com/KenjiTakahashi/lgsip',
    packages=[
        'lgsip',
        'lgsip.engine',
        'lgsip.engine.gates',
        'lgsip.frontend',
        'lgsip.frontend.gates'
    ],
    package_data={
        '': ['langs/*.qm', '*/*.rst']
    },
    scripts=['scripts/lgsip'],
    classifiers=[f.strip() for f in """
    Development Status :: 4 - Beta
    Environment :: Win32 (MS Windows)
    Environment :: X11 Applications :: Qt
    Intended Audience :: End Users/Desktop
    License :: OSI Approved :: GNU General Public License (GPL)
    Natural Language :: English
    Natural Language :: Polish
    Operating System :: OS Independent
    Programming Language :: Python :: 3
    """.splitlines() if f.strip()]
)
