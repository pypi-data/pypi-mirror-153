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

from dimod import SampleSet
from typing import List

from .termination import Terminator, Termination
from ..problem import ProblemType


class AndTerminator(Terminator[ProblemType]):
    """Terminating an algorithm only if multiple conditions hold.

    Args:
        children (List[Terminator[ProblemType]])

    """
    def __init__(self, children: List[Terminator[ProblemType]]):
        self._children = children

    def should_terminate(self, population: SampleSet) -> bool:
        """Checks if all children request termination for the current
        population.

        Returns:
            `True` to terminate if all children return `True`; `False` to
            proceed if any child returns `False`.

        """

        return all(s.should_terminate(population) for s in self._children)


class AndTermination(Termination[ProblemType]):
    """Composition of multiple termination configurations.

    All termination condition must hold to halt.

    Args:
        children (List[Termination])
    """
    def __init__(self, children: List[Termination]):
        self._children = children

    def initialise(self, problem: ProblemType) -> Terminator[ProblemType]:
        """Problem-specific configuration of termination.

        Args:
            problem (ProblemType): A concrete problem instance,
                that is used to configure the children.

        Returns:
            An `AndTerminator[ProblemType]` that checks all children conditions.

        """
        return AndTerminator([s.initialise(problem) for s in self._children])
