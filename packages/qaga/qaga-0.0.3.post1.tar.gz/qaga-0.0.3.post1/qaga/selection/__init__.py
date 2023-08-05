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
"""This module contains all predefined classes to configure selection, i.e. how
a genetic algorithm prepares a population to serve as input for the next generation.

Usually, it implements pruning to prevent large populations with bad individuals
and improve run time performance. In addition, one can use it to increase
diversity of population or even to integrate more constraints.

This module uses the abstract factory pattern to allow encapsulated state and
isolated optimisation runs. Implementations of `Selection` create
implementations of `Selector`, that implement the actual functionality.

"""

from .selection import Selector, Selection
from .identity_selection import IdentitySelector, IdentitySelection
from .truncation_selection import TruncationSelector, TruncationSelection
from .refilling_selection import RefillingSelector, RefillingSelection
from .pareto_selection import ParetoSelector, ParetoSelection
