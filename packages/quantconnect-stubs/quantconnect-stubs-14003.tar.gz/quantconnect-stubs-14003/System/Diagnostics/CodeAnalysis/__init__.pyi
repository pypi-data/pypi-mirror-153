from typing import overload
import System
import System.Diagnostics.CodeAnalysis


class ConstantExpectedAttribute(System.Attribute):
    """Indicates that the specified method parameter expects a constant."""

    @property
    def Min(self) -> System.Object:
        """Indicates the minimum bound of the expected constant, inclusive."""
        ...

    @Min.setter
    def Min(self, value: System.Object):
        """Indicates the minimum bound of the expected constant, inclusive."""
        ...

    @property
    def Max(self) -> System.Object:
        """Indicates the maximum bound of the expected constant, inclusive."""
        ...

    @Max.setter
    def Max(self, value: System.Object):
        """Indicates the maximum bound of the expected constant, inclusive."""
        ...


class ExcludeFromCodeCoverageAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def Justification(self) -> str:
        """Gets or sets the justification for excluding the member from code coverage."""
        ...

    @Justification.setter
    def Justification(self, value: str):
        """Gets or sets the justification for excluding the member from code coverage."""
        ...

    def __init__(self) -> None:
        ...


class SuppressMessageAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def Category(self) -> str:
        ...

    @property
    def CheckId(self) -> str:
        ...

    @property
    def Scope(self) -> str:
        ...

    @Scope.setter
    def Scope(self, value: str):
        ...

    @property
    def Target(self) -> str:
        ...

    @Target.setter
    def Target(self, value: str):
        ...

    @property
    def MessageId(self) -> str:
        ...

    @MessageId.setter
    def MessageId(self, value: str):
        ...

    @property
    def Justification(self) -> str:
        ...

    @Justification.setter
    def Justification(self, value: str):
        ...

    def __init__(self, category: str, checkId: str) -> None:
        ...


