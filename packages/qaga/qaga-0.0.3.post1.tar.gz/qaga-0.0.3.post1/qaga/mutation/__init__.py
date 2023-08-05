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
"""This module contains all predefined classes to configure mutation, i.e. how a
genetic algorithm can improve the elements of its current population by an
individual local search.

This module uses the abstract factory pattern to allow encapsulated state and
isolated optimisation runs. Implementations of `Mutation` create
implementations of `Recombination`, that implement the actual functionality.

"""


from .mutation import Mutator, Mutation
from .identity_mutation import IdentityMutator, IdentityMutation
from .addition_mutation import AdditionMutator, AdditionMutation
from .sampler_mutation import SamplerMutator, SamplerMutation
from .reverse_annealing_mutation import ReverseAnnealingMutation
