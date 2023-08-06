# Copyright (C) 2022 PlanQK
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
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from dataclasses import dataclass
from typing import TypeVar

from dimod import BinaryQuadraticModel

@dataclass
class Problem:
    """Base class for any problem to optimise.

    In general, it necessary that it contains a `dimod.BinaryQuadraticModel`
    encoding the actual problem, however, additional information can be added by
    interheritance to make use of domain knowledge.

    """
    bqm : BinaryQuadraticModel

ProblemType = TypeVar('ProblemType', bound=Problem)
"""TypeVariable of all subtypes of `Problem`.

Standardises the problem type all procedures use.

"""
