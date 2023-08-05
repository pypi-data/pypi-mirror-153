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
"""This module contains all predefined classes to configure recombination, i.e.
how a genetic algorithm can improve its popultion quality by combining
individuals. In fact, it is implements information exchange between solution
candidates.

This module uses the abstract factory pattern to allow encapsulated state and
isolated optimisation runs. Implementations of `Recombination` create
implementations of `Recombinator`, that implement the actual functionality.
"""

from .recombination import Recombinator, Recombination
from .addition_recombination import AdditionRecombinator, AdditionRecombination
from .identity_recombination import IdentityRecombination, IdentityRecombinator
from .random_bits_recombination import RandomBitsRecombinator, RandomBitsRecombination
from .random_cluster_recombination import RandomClusterRecombinator, RandomClusterRecombination
