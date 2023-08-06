from abc import ABC, abstractmethod
from typing import Generic

from dimod import SampleSet
from ..problem import ProblemType


class Selector(Generic[ProblemType], ABC):
    """Interface for pruning a population.

    """
    @abstractmethod
    def select(self, population: SampleSet) -> SampleSet:
        """Prunes a population.

        Args:
            population (dimod.SampleSet): Nonempty population to be modified.

        Returns:
            A nonempty `dimod.SampleSet`.
        """
        pass


class Selection(Generic[ProblemType], ABC):
    """Interface to configure selection procedure of a genetic algorithm.

    It determines how the population of the previous iteration is adjusted
    before the next iteration.

    """
    @abstractmethod
    def initialise(self, problem: ProblemType) -> Selector[ProblemType]:
        """Problem-specific configuration of selection.

        Args:
            problem (ProblemType): A concrete problem instance,
                for which a bespoke selection can be prepared.

        Returns:
            A `Selector[ProblemType]` implementation.
        """
