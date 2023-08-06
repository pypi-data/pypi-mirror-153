from typing import overload
import typing

import QuantConnect
import QuantConnect.Brokerages
import QuantConnect.Brokerages.GDAX
import QuantConnect.Brokerages.GDAX.Messages
import QuantConnect.Data
import QuantConnect.Data.Market
import QuantConnect.Interfaces
import QuantConnect.Orders
import QuantConnect.Packets
import QuantConnect.Securities
import System
import System.Collections.Concurrent
import System.Collections.Generic


class AuthenticationToken(System.Object):
    """Contains data used for authentication"""

    @property
    def Key(self) -> str:
        """The key"""
        ...

    @Key.setter
    def Key(self, value: str):
        """The key"""
        ...

    @property
    def Signature(self) -> str:
        """The hashed signature"""
        ...

    @Signature.setter
    def Signature(self, value: str):
        """The hashed signature"""
        ...

    @property
    def Timestamp(self) -> str:
        """The timestamp"""
        ...

    @Timestamp.setter
    def Timestamp(self, value: str):
        """The timestamp"""
        ...

    @property
    def Passphrase(self) -> str:
        """The pass phrase"""
        ...

    @Passphrase.setter
    def Passphrase(self, value: str):
        """The pass phrase"""
        ...


class GDAXFill(System.Object):
    """Tracks fill messages"""

    @property
    def Order(self) -> QuantConnect.Orders.Order:
        """The Lean order"""
        ...

    @property
    def OrderId(self) -> int:
        """Lean orderId"""
        ...

    @property
    def TotalQuantity(self) -> float:
        """Total amount executed across all fills"""
        ...

    @property
    def OrderQuantity(self) -> float:
        """Original order quantity"""
        ...

    def __init__(self, order: QuantConnect.Orders.Order) -> None:
        """Creates instance of GDAXFill"""
        ...

    def Add(self, msg: QuantConnect.Brokerages.GDAX.Messages.Fill) -> None:
        """Adds a trade message"""
        ...


class GDAXBrokerage(QuantConnect.Brokerages.BaseWebsocketsBrokerage):
    """Utility methods for GDAX brokerage"""

    SignHeader: str = "CB-ACCESS-SIGN"
    """Sign Header"""

    KeyHeader: str = "CB-ACCESS-KEY"
    """Key Header"""

    TimeHeader: str = "CB-ACCESS-TIMESTAMP"
    """Timestamp Header"""

    PassHeader: str = "CB-ACCESS-PASSPHRASE"
    """Passphrase header"""

    @property
    def IsConnected(self) -> bool:
        ...

    @property
    def FillSplit(self) -> System.Collections.Concurrent.ConcurrentDictionary[int, QuantConnect.Brokerages.GDAX.GDAXFill]:
        ...

    @FillSplit.setter
    def FillSplit(self, value: System.Collections.Concurrent.ConcurrentDictionary[int, QuantConnect.Brokerages.GDAX.GDAXFill]):
        ...

    @property
    def _aggregator(self) -> QuantConnect.Data.IDataAggregator:
        """
        Data Aggregator
        
        This field is protected.
        """
        ...

    @_aggregator.setter
    def _aggregator(self, value: QuantConnect.Data.IDataAggregator):
        """
        Data Aggregator
        
        This field is protected.
        """
        ...

    @property
    def ChannelNames(self) -> typing.List[str]:
        """This property is protected."""
        ...

    @overload
    def __init__(self, name: str) -> None:
        """
        Constructor for brokerage
        
        :param name: Name of brokerage
        """
        ...

    @overload
    def __init__(self, wssUrl: str, websocket: QuantConnect.Brokerages.IWebSocket, restClient: typing.Any, apiKey: str, apiSecret: str, passPhrase: str, algorithm: QuantConnect.Interfaces.IAlgorithm, priceProvider: QuantConnect.Interfaces.IPriceProvider, aggregator: QuantConnect.Data.IDataAggregator, job: QuantConnect.Packets.LiveNodePacket) -> None:
        """
        Constructor for brokerage
        
        :param wssUrl: websockets url
        :param websocket: instance of websockets client
        :param restClient: instance of rest client
        :param apiKey: api key
        :param apiSecret: api secret
        :param passPhrase: pass phrase
        :param algorithm: the algorithm instance is required to retreive account type
        :param priceProvider: The price provider for missing FX conversion rates
        :param aggregator: consolidate ticks
        :param job: The live job packet
        """
        ...

    def CancelOrder(self, order: QuantConnect.Orders.Order) -> bool:
        """Cancels an order"""
        ...

    def Connect(self) -> None:
        """Connects the client to the broker's remote servers"""
        ...

    def Disconnect(self) -> None:
        """Closes the websockets connection"""
        ...

    def Dispose(self) -> None:
        """Performs application-defined tasks associated with freeing, releasing, or resetting unmanaged resources."""
        ...

    def GetAccountHoldings(self) -> System.Collections.Generic.List[QuantConnect.Holding]:
        """Gets all open positions"""
        ...

    @overload
    def GetAuthenticationToken(self, request: typing.Any) -> QuantConnect.Brokerages.GDAX.AuthenticationToken:
        """
        Creates an auth token and adds to the request
        
        :param request: the rest request
        :returns: a token representing the request params.
        """
        ...

    @overload
    def GetAuthenticationToken(self, body: str, method: str, url: str) -> QuantConnect.Brokerages.GDAX.AuthenticationToken:
        """
        Creates an auth token to sign a request
        
        :param body: the request body as json
        :param method: the http method
        :param url: the request url
        """
        ...

    def GetCashBalance(self) -> System.Collections.Generic.List[QuantConnect.Securities.CashAmount]:
        """Gets the total account cash balance"""
        ...

    def GetHistory(self, request: QuantConnect.Data.HistoryRequest) -> System.Collections.Generic.IEnumerable[QuantConnect.Data.BaseData]:
        """
        Gets the history for the requested security
        
        :param request: The historical data request
        :returns: An enumerable of bars covering the span specified in the request.
        """
        ...

    def GetOpenOrders(self) -> System.Collections.Generic.List[QuantConnect.Orders.Order]:
        """Gets all orders not yet closed"""
        ...

    def GetTick(self, symbol: typing.Union[QuantConnect.Symbol, str]) -> QuantConnect.Data.Market.Tick:
        """Retrieves a price tick for a given symbol"""
        ...

    def Initialize(self, wssUrl: str, websocket: QuantConnect.Brokerages.IWebSocket, restClient: typing.Any, apiKey: str, apiSecret: str, passPhrase: str, algorithm: QuantConnect.Interfaces.IAlgorithm, priceProvider: QuantConnect.Interfaces.IPriceProvider, aggregator: QuantConnect.Data.IDataAggregator, job: QuantConnect.Packets.LiveNodePacket) -> None:
        """
        Initialize the instance of this class
        
        This method is protected.
        
        :param wssUrl: The web socket base url
        :param websocket: instance of websockets client
        :param restClient: instance of rest client
        :param apiKey: api key
        :param apiSecret: api secret
        :param passPhrase: pass phrase
        :param algorithm: the algorithm instance is required to retrieve account type
        :param priceProvider: The price provider for missing FX conversion rates
        :param aggregator: the aggregator for consolidating ticks
        :param job: The live job packet
        """
        ...

    def OnMessage(self, sender: typing.Any, webSocketMessage: QuantConnect.Brokerages.WebSocketMessage) -> None:
        """
        Wss message handler
        
        This method is protected.
        """
        ...

    def PlaceOrder(self, order: QuantConnect.Orders.Order) -> bool:
        """Creates a new order"""
        ...

    def PollTick(self, symbol: typing.Union[QuantConnect.Symbol, str]) -> None:
        """Poll for new tick to refresh conversion rate of non-USD denomination"""
        ...

    def Subscribe(self, symbols: System.Collections.Generic.IEnumerable[QuantConnect.Symbol]) -> bool:
        """
        Creates websocket message subscriptions for the supplied symbols
        
        This method is protected.
        """
        ...

    def Unsubscribe(self, symbols: System.Collections.Generic.IEnumerable[QuantConnect.Symbol]) -> bool:
        """Ends current subscriptions"""
        ...

    def UpdateOrder(self, order: QuantConnect.Orders.Order) -> bool:
        """This operation is not supported"""
        ...


class GDAXBrokerageFactory(QuantConnect.Brokerages.BrokerageFactory):
    """Factory method to create GDAX Websockets brokerage"""

    @property
    def BrokerageData(self) -> System.Collections.Generic.Dictionary[str, str]:
        """provides brokerage connection data"""
        ...

    def __init__(self) -> None:
        """Factory constructor"""
        ...

    def CreateBrokerage(self, job: QuantConnect.Packets.LiveNodePacket, algorithm: QuantConnect.Interfaces.IAlgorithm) -> QuantConnect.Interfaces.IBrokerage:
        """Create the Brokerage instance"""
        ...

    def Dispose(self) -> None:
        """Not required"""
        ...

    def GetBrokerageModel(self, orderProvider: QuantConnect.Securities.IOrderProvider) -> QuantConnect.Brokerages.IBrokerageModel:
        """
        The brokerage model
        
        :param orderProvider: The order provider
        """
        ...


class GDAXDataQueueHandler(QuantConnect.Brokerages.GDAX.GDAXBrokerage, QuantConnect.Interfaces.IDataQueueHandler):
    """An implementation of IDataQueueHandler for GDAX"""

    @property
    def ChannelNames(self) -> typing.List[str]:
        """
        The list of websocket channels to subscribe
        
        This property is protected.
        """
        ...

    @overload
    def __init__(self) -> None:
        """Constructor for brokerage"""
        ...

    @overload
    def __init__(self, wssUrl: str, websocket: QuantConnect.Brokerages.IWebSocket, restClient: typing.Any, apiKey: str, apiSecret: str, passPhrase: str, algorithm: QuantConnect.Interfaces.IAlgorithm, priceProvider: QuantConnect.Interfaces.IPriceProvider, aggregator: QuantConnect.Data.IDataAggregator, job: QuantConnect.Packets.LiveNodePacket) -> None:
        """Initializes a new instance of the GDAXDataQueueHandler class"""
        ...

    def SetJob(self, job: QuantConnect.Packets.LiveNodePacket) -> None:
        """
        Sets the job we're subscribing for
        
        :param job: Job we're subscribing for
        """
        ...

    def Subscribe(self, dataConfig: QuantConnect.Data.SubscriptionDataConfig, newDataAvailableHandler: typing.Callable[[System.Object, System.EventArgs], None]) -> System.Collections.Generic.IEnumerator[QuantConnect.Data.BaseData]:
        """
        Subscribe to the specified configuration
        
        :param dataConfig: defines the parameters to subscribe to a data feed
        :param newDataAvailableHandler: handler to be fired on new data available
        :returns: The new enumerator for this subscription request.
        """
        ...

    def Unsubscribe(self, dataConfig: QuantConnect.Data.SubscriptionDataConfig) -> None:
        """
        Removes the specified configuration
        
        :param dataConfig: Subscription config to be removed
        """
        ...


