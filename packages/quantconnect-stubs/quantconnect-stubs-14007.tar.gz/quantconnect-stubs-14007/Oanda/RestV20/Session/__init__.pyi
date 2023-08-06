from typing import overload
import abc
import typing

import Oanda.RestV20.Session
import QuantConnect.Brokerages.Oanda
import System
import System.Collections.Generic

Oanda_RestV20_Session__EventContainer_Callable = typing.TypeVar("Oanda_RestV20_Session__EventContainer_Callable")
Oanda_RestV20_Session__EventContainer_ReturnType = typing.TypeVar("Oanda_RestV20_Session__EventContainer_ReturnType")


class StreamSession(System.Object, metaclass=abc.ABCMeta):
    """StreamSession abstract class used to model streaming sessions"""

    @property
    def DataReceived(self) -> _EventContainer[typing.Callable[[str], None], None]:
        """The event fired when a new message is received"""
        ...

    @DataReceived.setter
    def DataReceived(self, value: _EventContainer[typing.Callable[[str], None], None]):
        """The event fired when a new message is received"""
        ...

    def DataHandler(self, data: str) -> None:
        """The delegate for the DataReceived event handler"""
        ...

    def GetSession(self) -> typing.Any:
        """
        Returns the started session
        
        This method is protected.
        """
        ...

    def StartSession(self) -> None:
        """Starts the session"""
        ...

    def StopSession(self) -> None:
        """Stops the session"""
        ...


class PricingStreamSession(Oanda.RestV20.Session.StreamSession):
    """Pricing streaming session"""

    def __init__(self, api: QuantConnect.Brokerages.Oanda.OandaRestApiV20, instruments: System.Collections.Generic.List[str]) -> None:
        """
        Creates an instance of the PricingStreamSession class
        
        :param api: The Rest API instance
        :param instruments: The list of instruments
        """
        ...

    def GetSession(self) -> typing.Any:
        """
        Returns the started session
        
        This method is protected.
        """
        ...


class TransactionStreamSession(Oanda.RestV20.Session.StreamSession):
    """Transaction streaming session"""

    def __init__(self, api: QuantConnect.Brokerages.Oanda.OandaRestApiV20) -> None:
        """Creates an instance of the TransactionStreamSession class"""
        ...

    def GetSession(self) -> typing.Any:
        """
        Returns the started session
        
        This method is protected.
        """
        ...


class _EventContainer(typing.Generic[Oanda_RestV20_Session__EventContainer_Callable, Oanda_RestV20_Session__EventContainer_ReturnType]):
    """This class is used to provide accurate autocomplete on events and cannot be imported."""

    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> Oanda_RestV20_Session__EventContainer_ReturnType:
        """Fires the event."""
        ...

    def __iadd__(self, item: Oanda_RestV20_Session__EventContainer_Callable) -> None:
        """Registers an event handler."""
        ...

    def __isub__(self, item: Oanda_RestV20_Session__EventContainer_Callable) -> None:
        """Unregisters an event handler."""
        ...


