from typing import overload
import datetime
import typing

import QuantConnect
import QuantConnect.Brokerages
import QuantConnect.Brokerages.Bitfinex
import QuantConnect.Data
import QuantConnect.Data.Market
import QuantConnect.Interfaces
import QuantConnect.Orders
import QuantConnect.Packets
import QuantConnect.Securities
import System
import System.Collections.Concurrent
import System.Collections.Generic


class BitfinexWebSocketWrapper(QuantConnect.Brokerages.WebSocketClientWrapper):
    """Wrapper class for a Bitfinex websocket connection"""

    @property
    def ConnectionId(self) -> str:
        """The unique Id for the connection"""
        ...

    @property
    def ConnectionHandler(self) -> QuantConnect.Brokerages.IConnectionHandler:
        """The handler for the connection"""
        ...

    def __init__(self, connectionHandler: QuantConnect.Brokerages.IConnectionHandler) -> None:
        """Initializes a new instance of the BitfinexWebSocketWrapper class."""
        ...


class BitfinexBrokerage(QuantConnect.Brokerages.BaseWebsocketsBrokerage, QuantConnect.Interfaces.IDataQueueHandler):
    """Utility methods for Bitfinex brokerage"""

    @property
    def UnixEpoch(self) -> datetime.datetime:
        """Unix Epoch"""
        ...

    ApiKeyHeader: str = "bfx-apikey"
    """ApiKey Header"""

    NonceHeader: str = "bfx-nonce"
    """Nonce Header"""

    SignatureHeader: str = "bfx-signature"
    """Signature Header"""

    @property
    def IsConnected(self) -> bool:
        ...

    @property
    def TickLocker(self) -> System.Object:
        """Locking object for the Ticks list in the data queue handler"""
        ...

    @overload
    def __init__(self) -> None:
        """Constructor for brokerage"""
        ...

    @overload
    def __init__(self, apiKey: str, apiSecret: str, algorithm: QuantConnect.Interfaces.IAlgorithm, priceProvider: QuantConnect.Interfaces.IPriceProvider, aggregator: QuantConnect.Data.IDataAggregator, job: QuantConnect.Packets.LiveNodePacket) -> None:
        """
        Constructor for brokerage
        
        :param apiKey: api key
        :param apiSecret: api secret
        :param algorithm: the algorithm instance is required to retrieve account type
        :param priceProvider: The price provider for missing FX conversion rates
        :param aggregator: consolidate ticks
        :param job: The live job packet
        """
        ...

    @overload
    def __init__(self, websocket: QuantConnect.Brokerages.IWebSocket, restClient: typing.Any, apiKey: str, apiSecret: str, algorithm: QuantConnect.Interfaces.IAlgorithm, priceProvider: QuantConnect.Interfaces.IPriceProvider, aggregator: QuantConnect.Data.IDataAggregator, job: QuantConnect.Packets.LiveNodePacket) -> None:
        """
        Constructor for brokerage
        
        :param websocket: instance of websockets client
        :param restClient: instance of rest client
        :param apiKey: api key
        :param apiSecret: api secret
        :param algorithm: the algorithm instance is required to retrieve account type
        :param priceProvider: The price provider for missing FX conversion rates
        :param aggregator: consolidate ticks
        :param job: The live job packet
        """
        ...

    def CancelOrder(self, order: QuantConnect.Orders.Order) -> bool:
        """
        Cancels the order with the specified ID
        
        :param order: The order to cancel
        :returns: True if the request was submitted for cancellation, false otherwise.
        """
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

    def GetCashBalance(self) -> System.Collections.Generic.List[QuantConnect.Securities.CashAmount]:
        """Gets the total account cash balance for specified account type"""
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

    def GetSubscribed(self) -> System.Collections.Generic.IEnumerable[QuantConnect.Symbol]:
        """
        Should be empty. BrokerageMultiWebSocketSubscriptionManager manages each BitfinexWebSocketWrapper individually
        
        This method is protected.
        """
        ...

    def GetTick(self, symbol: typing.Union[QuantConnect.Symbol, str]) -> QuantConnect.Data.Market.Tick:
        """Provides the current best bid and ask"""
        ...

    @overload
    def OnMessage(self, e: QuantConnect.Brokerages.BrokerageMessageEvent) -> None:
        ...

    @overload
    def OnMessage(self, sender: typing.Any, e: QuantConnect.Brokerages.WebSocketMessage) -> None:
        """
        Wss message handler
        
        This method is protected.
        """
        ...

    def PlaceOrder(self, order: QuantConnect.Orders.Order) -> bool:
        """
        Places a new order and assigns a new broker ID to the order
        
        :param order: The order to be placed
        :returns: True if the request for a new order has been placed, false otherwise.
        """
        ...

    def SetJob(self, job: QuantConnect.Packets.LiveNodePacket) -> None:
        ...

    @overload
    def Subscribe(self, dataConfig: QuantConnect.Data.SubscriptionDataConfig, newDataAvailableHandler: typing.Callable[[System.Object, System.EventArgs], None]) -> System.Collections.Generic.IEnumerator[QuantConnect.Data.BaseData]:
        """
        Subscribe to the specified configuration
        
        :param dataConfig: defines the parameters to subscribe to a data feed
        :param newDataAvailableHandler: handler to be fired on new data available
        :returns: The new enumerator for this subscription request.
        """
        ...

    @overload
    def Subscribe(self, symbols: System.Collections.Generic.IEnumerable[QuantConnect.Symbol]) -> bool:
        """
        Should be empty, Bitfinex brokerage manages his public channels including subscribe/unsubscribe/reconnect methods using BrokerageMultiWebSocketSubscriptionManager
        Not used in master
        
        This method is protected.
        """
        ...

    def SubscribeAuth(self) -> None:
        """Subscribes to the authenticated channels (using an single streaming channel)"""
        ...

    def Unsubscribe(self, dataConfig: QuantConnect.Data.SubscriptionDataConfig) -> None:
        """
        Removes the specified configuration
        
        :param dataConfig: Subscription config to be removed
        """
        ...

    def UpdateOrder(self, order: QuantConnect.Orders.Order) -> bool:
        """
        Updates the order with the same id
        
        :param order: The new order information
        :returns: True if the request was made for the order to be updated, false otherwise.
        """
        ...


class BitfinexWebSocketChannels(System.Collections.Concurrent.ConcurrentDictionary[int, QuantConnect.Data.Channel]):
    """Contains the channel mappings for a WebSocket connection"""

    def Contains(self, channel: QuantConnect.Data.Channel) -> bool:
        """
        Determines whether the dictionary contains a specific channel.
        
        :param channel: The channel
        :returns: true if the channel was found.
        """
        ...

    def GetChannelId(self, channel: QuantConnect.Data.Channel) -> int:
        """
        Returns the channel id for the given channel.
        
        :param channel: The channel
        :returns: The channel id.
        """
        ...


class BitfinexBrokerageFactory(QuantConnect.Brokerages.BrokerageFactory):
    """Factory method to create Bitfinex Websockets brokerage"""

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


