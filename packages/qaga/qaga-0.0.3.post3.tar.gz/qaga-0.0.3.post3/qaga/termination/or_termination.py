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


class OrTerminator(Terminator[ProblemType]):
    """Terminating an algorithm if any of multiple conditions holds.

    Args:
        children (List[Terminator[ProblemType]])

    """
    def __init__(self, children: List[Terminator[ProblemType]]):
        self._children = children

    def should_terminate(self, population: SampleSet) -> bool:
        """Checks if any child requests termination for the current
        population.

        Returns:
            `True` to terminate if any child returns `True`; `False` to
            proceed if all children return `False`.

        """
        return any(s.should_terminate(population) for s in self._children)


class OrTermination(Termination[ProblemType]):
    """Configuration of a selection of termination conditions.

    Only one termination condition must hold to halt.

    Args:
        children (List[Termination[ProblemType]])

    """
    def __init__(self, children: List[Termination[ProblemType]]):
        self._children = children

    def initialise(self, problem: ProblemType) -> Terminator[ProblemType]:
        """Problem-specific configuration of termination.

        Args:
            problem (ProblemType): A concrete problem instance,
                that is used to configure the children.

        Returns:
            An `OrTerminator[ProblemType]` that checks if any child condition holds.

        """
        return OrTerminator[ProblemType]([s.initialise(problem) for s in self._children])
