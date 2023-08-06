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

from abc import ABC, abstractmethod
from typing import Generic

from dimod import SampleSet

from ..problem import ProblemType


class Startup(Generic[ProblemType], ABC):
    """Interface for creating the initial population.
    """
    @abstractmethod
    def startup(self, problem: ProblemType) -> SampleSet:
        """Creates a population.

        Args:
            problem (ProblemType): The problem for which a
                population is created.

        Returns:
            A non-empty `dimod.SampleSet` that shares the same variable type and
            amount of qubits with `problem`.

        """
