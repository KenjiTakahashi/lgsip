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


class Error(Exception):
    def __str__(self):
        return repr(self.message)


class NotEnoughInputsError(Error):
    def __init__(self):
        self.message = "There need to be at least 2 inputs for a gate."


class NagativeNumOfInputsError(Error):
    def __init__(self):
        self.message = "Number of inputs to add/remove should be positive."


class InvalidInputIndexError(Error):
    def __init__(self):
        self.message = "The specified input does not exist."


class WireExistsError(Error):
    def __init__(self):
        self.message = "The specified wire already exists."


class IOConnectedError(Error):
    def __init__(self):
        self.message = "The specified input/output is already connected."
