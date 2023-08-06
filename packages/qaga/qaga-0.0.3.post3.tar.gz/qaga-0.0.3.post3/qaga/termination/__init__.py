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
"""This module contains all predefined classes to configure termination, i.e. if
a genetic algorithm should stop its iterative improvement of the population.

In general, one chooses one that guarantees termination, for instance after a
fix amount of iterations, and then combines it with (use case dependent) classes
that cover some early returns due to good population quality.

This module uses the abstract factory pattern to allow encapsulated state and
isolated optimisation runs. Implementations of `Termination` create
implementations of `Terminator`, that implement the actual functionality.

"""

from .termination import Terminator, Termination
from .generation_termination import GenerationTermination
from .and_termination import AndTerminator, AndTermination
from .or_termination import OrTerminator, OrTermination
from .lowest_energy_evaluation import LowestEnergyTerminator, LowestEnergyTermination
