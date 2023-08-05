"""
Base class for pretty printed objects.
"""
import abc


class PrettyPrinted(abc.ABC):
    """
    Base class for pretty-printed objects.
    """

    @classmethod
    def get_tabular(cls, size: int) -> str:
        """Get tabular offset with fixed size."""
        return ' ' * size

    @abc.abstractmethod
    def pretty_print(self, *_, **kwargs) -> str:
        """Get the pretty-print-ready representation."""
        pass
