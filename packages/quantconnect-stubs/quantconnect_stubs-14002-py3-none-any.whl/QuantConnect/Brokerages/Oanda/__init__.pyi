from typing import overload
import abc
import datetime
import typing

import QuantConnect
import QuantConnect.Brokerages
import QuantConnect.Brokerages.Oanda
import QuantConnect.Data
import QuantConnect.Data.Market
import QuantConnect.Interfaces
import QuantConnect.Orders
import QuantConnect.Packets
import QuantConnect.Securities
import System
import System.Collections.Concurrent
import System.Collections.Generic


class OandaSymbolMapper(System.Object, QuantConnect.Brokerages.ISymbolMapper):
    """Provides the mapping between Lean symbols and Oanda symbols."""

    KnownTickers: System.Collections.Generic.HashSet[str] = ...
    """The list of known Oanda symbols."""

    def GetBrokerageSecurityType(self, brokerageSymbol: str) -> int:
        """
        Returns the security type for an Oanda symbol
        
        :param brokerageSymbol: The Oanda symbol
        :returns: The security type. This method returns the int value of a member of the QuantConnect.SecurityType enum.
        """
        ...

    def GetBrokerageSymbol(self, symbol: typing.Union[QuantConnect.Symbol, str]) -> str:
        """
        Converts a Lean symbol instance to an Oanda symbol
        
        :param symbol: A Lean symbol instance
        :returns: The Oanda symbol.
        """
        ...

    def GetLeanSecurityType(self, leanSymbol: str) -> int:
        """
        Returns the security type for a Lean symbol
        
        :param leanSymbol: The Lean symbol
        :returns: The security type. This method returns the int value of a member of the QuantConnect.SecurityType enum.
        """
        ...

    def GetLeanSymbol(self, brokerageSymbol: str, securityType: QuantConnect.SecurityType, market: str, expirationDate: typing.Union[datetime.datetime, datetime.date] = ..., strike: float = 0, optionRight: QuantConnect.OptionRight = 0) -> QuantConnect.Symbol:
        """
        Converts an Oanda symbol to a Lean symbol instance
        
        :param brokerageSymbol: The Oanda symbol
        :param securityType: The security type
        :param market: The market
        :param expirationDate: Expiration date of the security(if applicable)
        :param strike: The strike of the security (if applicable)
        :param optionRight: The option right of the security (if applicable)
        :returns: A new Lean Symbol instance.
        """
        ...

    def IsKnownBrokerageSymbol(self, brokerageSymbol: str) -> bool:
        """
        Checks if the symbol is supported by Oanda
        
        :param brokerageSymbol: The Oanda symbol
        :returns: True if Oanda supports the symbol.
        """
        ...

    def IsKnownLeanSymbol(self, symbol: typing.Union[QuantConnect.Symbol, str]) -> bool:
        """
        Checks if the symbol is supported by Oanda
        
        :param symbol: The Lean symbol
        :returns: True if Oanda supports the symbol.
        """
        ...


class Environment(System.Enum):
    """Represents different environments available for the REST API."""

    Practice = 0
    """A stable environment; recommended for testing with your fxTrade Practice account and your personal access token."""

    Trade = 1
    """A stable environment; recommended for production-ready code to execute with your fxTrade account and your personal access token."""


class OandaRestApiBase(QuantConnect.Brokerages.Brokerage, QuantConnect.Interfaces.IDataQueueHandler, metaclass=abc.ABCMeta):
    """Oanda REST API base class"""

    @property
    def Locker(self) -> System.Object:
        """
        This lock is used to sync 'PlaceOrder' and callback 'OnTransactionDataReceived'
        
        This field is protected.
        """
        ...

    @property
    def PendingFilledMarketOrders(self) -> System.Collections.Concurrent.ConcurrentDictionary[int, QuantConnect.Orders.OrderStatus]:
        """
        This container is used to keep pending to be filled market orders, so when the callback comes in we send the filled event
        
        This field is protected.
        """
        ...

    @property
    def PricingConnectionHandler(self) -> QuantConnect.Brokerages.IConnectionHandler:
        """
        The connection handler for pricing
        
        This field is protected.
        """
        ...

    @property
    def TransactionsConnectionHandler(self) -> QuantConnect.Brokerages.IConnectionHandler:
        """
        The connection handler for transactions
        
        This field is protected.
        """
        ...

    @property
    def SubscribedSymbols(self) -> System.Collections.Generic.IEnumerable[QuantConnect.Symbol]:
        """
        The list of currently subscribed symbols
        
        This property is protected.
        """
        ...

    @property
    def SymbolMapper(self) -> QuantConnect.Brokerages.Oanda.OandaSymbolMapper:
        """
        The symbol mapper
        
        This field is protected.
        """
        ...

    @SymbolMapper.setter
    def SymbolMapper(self, value: QuantConnect.Brokerages.Oanda.OandaSymbolMapper):
        """
        The symbol mapper
        
        This field is protected.
        """
        ...

    @property
    def OrderProvider(self) -> QuantConnect.Securities.IOrderProvider:
        """
        The order provider
        
        This field is protected.
        """
        ...

    @OrderProvider.setter
    def OrderProvider(self, value: QuantConnect.Securities.IOrderProvider):
        """
        The order provider
        
        This field is protected.
        """
        ...

    @property
    def SecurityProvider(self) -> QuantConnect.Securities.ISecurityProvider:
        """
        The security provider
        
        This field is protected.
        """
        ...

    @SecurityProvider.setter
    def SecurityProvider(self, value: QuantConnect.Securities.ISecurityProvider):
        """
        The security provider
        
        This field is protected.
        """
        ...

    @property
    def Aggregator(self) -> QuantConnect.Data.IDataAggregator:
        """
        The data aggregator
        
        This field is protected.
        """
        ...

    @Aggregator.setter
    def Aggregator(self, value: QuantConnect.Data.IDataAggregator):
        """
        The data aggregator
        
        This field is protected.
        """
        ...

    @property
    def Environment(self) -> QuantConnect.Brokerages.Oanda.Environment:
        """
        The Oanda enviroment
        
        This field is protected.
        """
        ...

    @Environment.setter
    def Environment(self, value: QuantConnect.Brokerages.Oanda.Environment):
        """
        The Oanda enviroment
        
        This field is protected.
        """
        ...

    @property
    def AccessToken(self) -> str:
        """
        The Oanda access token
        
        This field is protected.
        """
        ...

    @AccessToken.setter
    def AccessToken(self, value: str):
        """
        The Oanda access token
        
        This field is protected.
        """
        ...

    @property
    def AccountId(self) -> str:
        """
        The Oanda account ID
        
        This field is protected.
        """
        ...

    @AccountId.setter
    def AccountId(self, value: str):
        """
        The Oanda account ID
        
        This field is protected.
        """
        ...

    @property
    def Agent(self) -> str:
        """
        The Oanda agent string
        
        This field is protected.
        """
        ...

    @Agent.setter
    def Agent(self, value: str):
        """
        The Oanda agent string
        
        This field is protected.
        """
        ...

    OandaAgentKey: str = "OANDA-Agent"
    """
    The HTTP header key for Oanda agent
    
    This field is protected.
    """

    OandaAgentDefaultValue: str = "QuantConnect/0.0.0 (LEAN)"
    """The default HTTP header value for Oanda agent"""

    @property
    def IsConnected(self) -> bool:
        """Returns true if we're currently connected to the broker"""
        ...

    def __init__(self, symbolMapper: QuantConnect.Brokerages.Oanda.OandaSymbolMapper, orderProvider: QuantConnect.Securities.IOrderProvider, securityProvider: QuantConnect.Securities.ISecurityProvider, aggregator: QuantConnect.Data.IDataAggregator, environment: QuantConnect.Brokerages.Oanda.Environment, accessToken: str, accountId: str, agent: str) -> None:
        """
        Initializes a new instance of the OandaRestApiBase class.
        
        This method is protected.
        
        :param symbolMapper: The symbol mapper.
        :param orderProvider: The order provider.
        :param securityProvider: The holdings provider.
        :param aggregator: Consolidate ticks
        :param environment: The Oanda environment (Trade or Practice)
        :param accessToken: The Oanda access token (can be the user's personal access token or the access token obtained with OAuth by QC on behalf of the user)
        :param accountId: The account identifier.
        :param agent: The Oanda agent string
        """
        ...

    def Connect(self) -> None:
        """Connects the client to the broker's remote servers"""
        ...

    def Disconnect(self) -> None:
        """Disconnects the client from the broker's remote servers"""
        ...

    def Dispose(self) -> None:
        """Dispose of the brokerage instance"""
        ...

    def DownloadQuoteBars(self, symbol: typing.Union[QuantConnect.Symbol, str], startTimeUtc: typing.Union[datetime.datetime, datetime.date], endTimeUtc: typing.Union[datetime.datetime, datetime.date], resolution: QuantConnect.Resolution, requestedTimeZone: typing.Any) -> System.Collections.Generic.IEnumerable[QuantConnect.Data.Market.QuoteBar]:
        """
        Downloads a list of QuoteBars at the requested resolution
        
        :param symbol: The symbol
        :param startTimeUtc: The starting time (UTC)
        :param endTimeUtc: The ending time (UTC)
        :param resolution: The requested resolution
        :param requestedTimeZone: The requested timezone for the data
        :returns: The list of bars.
        """
        ...

    def DownloadTradeBars(self, symbol: typing.Union[QuantConnect.Symbol, str], startTimeUtc: typing.Union[datetime.datetime, datetime.date], endTimeUtc: typing.Union[datetime.datetime, datetime.date], resolution: QuantConnect.Resolution, requestedTimeZone: typing.Any) -> System.Collections.Generic.IEnumerable[QuantConnect.Data.Market.TradeBar]:
        """
        Downloads a list of TradeBars at the requested resolution
        
        :param symbol: The symbol
        :param startTimeUtc: The starting time (UTC)
        :param endTimeUtc: The ending time (UTC)
        :param resolution: The requested resolution
        :param requestedTimeZone: The requested timezone for the data
        :returns: The list of bars.
        """
        ...

    def EmitTick(self, tick: QuantConnect.Data.Market.Tick) -> None:
        """
        Emit ticks
        
        This method is protected.
        
        :param tick: The new tick to emit
        """
        ...

    def GetAccountBaseCurrency(self) -> str:
        """Gets the account base currency"""
        ...

    def GetInstrumentList(self) -> System.Collections.Generic.List[str]:
        """Gets the list of available tradable instruments/products from Oanda"""
        ...

    def GetRates(self, instruments: System.Collections.Generic.List[str]) -> System.Collections.Generic.Dictionary[str, QuantConnect.Data.Market.Tick]:
        """
        Retrieves the current rate for each of a list of instruments
        
        :param instruments: the list of instruments to check
        :returns: Dictionary containing the current quotes for each instrument.
        """
        ...

    def SetJob(self, job: QuantConnect.Packets.LiveNodePacket) -> None:
        """
        Sets the job we're subscribing for
        
        :param job: Job we're subscribing for
        """
        ...

    def StartPricingStream(self, instruments: System.Collections.Generic.List[str]) -> None:
        """Starts streaming prices for a list of instruments"""
        ...

    def StartTransactionStream(self) -> None:
        """Starts streaming transactions for the active account"""
        ...

    def StopPricingStream(self) -> None:
        """Stops streaming prices for all instruments"""
        ...

    def StopTransactionStream(self) -> None:
        """Stops streaming transactions for the active account"""
        ...

    def Subscribe(self, dataConfig: QuantConnect.Data.SubscriptionDataConfig, newDataAvailableHandler: typing.Callable[[System.Object, System.EventArgs], None]) -> System.Collections.Generic.IEnumerator[QuantConnect.Data.BaseData]:
        """
        Subscribe to the specified configuration
        
        :param dataConfig: defines the parameters to subscribe to a data feed
        :param newDataAvailableHandler: handler to be fired on new data available
        :returns: The new enumerator for this subscription request.
        """
        ...

    def SubscribeSymbols(self, symbolsToSubscribe: System.Collections.Generic.IEnumerable[QuantConnect.Symbol]) -> None:
        """
        Subscribes to the requested symbols (using a single streaming session)
        
        This method is protected.
        
        :param symbolsToSubscribe: The list of symbols to subscribe
        """
        ...

    def Unsubscribe(self, dataConfig: QuantConnect.Data.SubscriptionDataConfig) -> None:
        """
        Removes the specified configuration
        
        :param dataConfig: Subscription config to be removed
        """
        ...


class OandaBrokerage(QuantConnect.Brokerages.Brokerage, QuantConnect.Interfaces.IDataQueueHandler):
    """Oanda Brokerage implementation"""

    MaxBarsPerRequest: int = 5000
    """The maximum number of bars per historical data request"""

    @property
    def IsConnected(self) -> bool:
        ...

    @property
    def AccountBaseCurrency(self) -> str:
        """Returns the brokerage account's base currency"""
        ...

    @AccountBaseCurrency.setter
    def AccountBaseCurrency(self, value: str):
        """Returns the brokerage account's base currency"""
        ...

    @overload
    def __init__(self) -> None:
        """Initializes a new instance of the OandaBrokerage class."""
        ...

    @overload
    def __init__(self, orderProvider: QuantConnect.Securities.IOrderProvider, securityProvider: QuantConnect.Securities.ISecurityProvider, aggregator: QuantConnect.Data.IDataAggregator, environment: QuantConnect.Brokerages.Oanda.Environment, accessToken: str, accountId: str, agent: str = ...) -> None:
        """
        Initializes a new instance of the OandaBrokerage class.
        
        :param orderProvider: The order provider.
        :param securityProvider: The holdings provider.
        :param aggregator: consolidate ticks
        :param environment: The Oanda environment (Trade or Practice)
        :param accessToken: The Oanda access token (can be the user's personal access token or the access token obtained with OAuth by QC on behalf of the user)
        :param accountId: The account identifier.
        :param agent: The Oanda agent string
        """
        ...

    def CancelOrder(self, order: QuantConnect.Orders.Order) -> bool:
        """
        Cancels the order with the specified ID
        
        :param order: The order to cancel
        :returns: True if the request was made for the order to be canceled, false otherwise.
        """
        ...

    def Connect(self) -> None:
        """Connects the client to the broker's remote servers"""
        ...

    def Disconnect(self) -> None:
        """Disconnects the client from the broker's remote servers"""
        ...

    def DownloadQuoteBars(self, symbol: typing.Union[QuantConnect.Symbol, str], startTimeUtc: typing.Union[datetime.datetime, datetime.date], endTimeUtc: typing.Union[datetime.datetime, datetime.date], resolution: QuantConnect.Resolution, requestedTimeZone: typing.Any) -> System.Collections.Generic.IEnumerable[QuantConnect.Data.Market.QuoteBar]:
        """
        Downloads a list of QuoteBars at the requested resolution
        
        :param symbol: The symbol
        :param startTimeUtc: The starting time (UTC)
        :param endTimeUtc: The ending time (UTC)
        :param resolution: The requested resolution
        :param requestedTimeZone: The requested timezone for the data
        :returns: The list of bars.
        """
        ...

    def DownloadTradeBars(self, symbol: typing.Union[QuantConnect.Symbol, str], startTimeUtc: typing.Union[datetime.datetime, datetime.date], endTimeUtc: typing.Union[datetime.datetime, datetime.date], resolution: QuantConnect.Resolution, requestedTimeZone: typing.Any) -> System.Collections.Generic.IEnumerable[QuantConnect.Data.Market.TradeBar]:
        """
        Downloads a list of TradeBars at the requested resolution
        
        :param symbol: The symbol
        :param startTimeUtc: The starting time (UTC)
        :param endTimeUtc: The ending time (UTC)
        :param resolution: The requested resolution
        :param requestedTimeZone: The requested timezone for the data
        :returns: The list of bars.
        """
        ...

    def GetAccountHoldings(self) -> System.Collections.Generic.List[QuantConnect.Holding]:
        """
        Gets all holdings for the account
        
        :returns: The current holdings from the account.
        """
        ...

    def GetCashBalance(self) -> System.Collections.Generic.List[QuantConnect.Securities.CashAmount]:
        """
        Gets the current cash balance for each currency held in the brokerage account
        
        :returns: The current cash balance for each currency available for trading.
        """
        ...

    @staticmethod
    def GetDateTimeFromString(time: str) -> datetime.datetime:
        ...

    def GetHistory(self, request: QuantConnect.Data.HistoryRequest) -> System.Collections.Generic.IEnumerable[QuantConnect.Data.BaseData]:
        """
        Gets the history for the requested security
        
        :param request: The historical data request
        :returns: An enumerable of bars covering the span specified in the request.
        """
        ...

    def GetOpenOrders(self) -> System.Collections.Generic.List[QuantConnect.Orders.Order]:
        """
        Gets all open orders on the account.
        NOTE: The order objects returned do not have QC order IDs.
        
        :returns: The open orders returned from Oanda.
        """
        ...

    def GetRates(self, instrument: str) -> QuantConnect.Data.Market.Tick:
        """
        Retrieves the current quotes for an instrument
        
        :param instrument: the instrument to check
        :returns: Returns a Tick object with the current bid/ask prices for the instrument.
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

    def UpdateOrder(self, order: QuantConnect.Orders.Order) -> bool:
        """
        Updates the order with the same id
        
        :param order: The new order information
        :returns: True if the request was made for the order to be updated, false otherwise.
        """
        ...


class Server(System.Enum):
    """Represents the server instance that we will be performing the RESTful call."""

    Account = 0
    """The account"""

    Rates = 1
    """The rates"""

    StreamingRates = 2
    """The streaming rates"""

    StreamingEvents = 3
    """The streaming events"""


class OandaBrokerageFactory(QuantConnect.Brokerages.BrokerageFactory):
    """Provides an implementations of IBrokerageFactory that produces a OandaBrokerage"""

    @property
    def BrokerageData(self) -> System.Collections.Generic.Dictionary[str, str]:
        """Gets the brokerage data required to run the brokerage from configuration/disk"""
        ...

    def __init__(self) -> None:
        """Initializes a new instance of the OandaBrokerageFactory class."""
        ...

    def CreateBrokerage(self, job: QuantConnect.Packets.LiveNodePacket, algorithm: QuantConnect.Interfaces.IAlgorithm) -> QuantConnect.Interfaces.IBrokerage:
        """
        Creates a new IBrokerage instance
        
        :param job: The job packet to create the brokerage for
        :param algorithm: The algorithm instance
        :returns: A new brokerage instance.
        """
        ...

    def Dispose(self) -> None:
        """Performs application-defined tasks associated with freeing, releasing, or resetting unmanaged resources."""
        ...

    def GetBrokerageModel(self, orderProvider: QuantConnect.Securities.IOrderProvider) -> QuantConnect.Brokerages.IBrokerageModel:
        """
        Gets a new instance of the OandaBrokerageModel
        
        :param orderProvider: The order provider
        """
        ...


class OandaRestApiV20(QuantConnect.Brokerages.Oanda.OandaRestApiBase):
    """Oanda REST API v20 implementation"""

    def __init__(self, symbolMapper: QuantConnect.Brokerages.Oanda.OandaSymbolMapper, orderProvider: QuantConnect.Securities.IOrderProvider, securityProvider: QuantConnect.Securities.ISecurityProvider, aggregator: QuantConnect.Data.IDataAggregator, environment: QuantConnect.Brokerages.Oanda.Environment, accessToken: str, accountId: str, agent: str) -> None:
        """
        Initializes a new instance of the OandaRestApiV20 class.
        
        :param symbolMapper: The symbol mapper.
        :param orderProvider: The order provider.
        :param securityProvider: The holdings provider.
        :param aggregator: Consolidate ticks.
        :param environment: The Oanda environment (Trade or Practice)
        :param accessToken: The Oanda access token (can be the user's personal access token or the access token obtained with OAuth by QC on behalf of the user)
        :param accountId: The account identifier.
        :param agent: The Oanda agent string
        """
        ...

    def CancelOrder(self, order: QuantConnect.Orders.Order) -> bool:
        """
        Cancels the order with the specified ID
        
        :param order: The order to cancel
        :returns: True if the request was made for the order to be canceled, false otherwise.
        """
        ...

    def DownloadQuoteBars(self, symbol: typing.Union[QuantConnect.Symbol, str], startTimeUtc: typing.Union[datetime.datetime, datetime.date], endTimeUtc: typing.Union[datetime.datetime, datetime.date], resolution: QuantConnect.Resolution, requestedTimeZone: typing.Any) -> System.Collections.Generic.IEnumerable[QuantConnect.Data.Market.QuoteBar]:
        """
        Downloads a list of QuoteBars at the requested resolution
        
        :param symbol: The symbol
        :param startTimeUtc: The starting time (UTC)
        :param endTimeUtc: The ending time (UTC)
        :param resolution: The requested resolution
        :param requestedTimeZone: The requested timezone for the data
        :returns: The list of bars.
        """
        ...

    def DownloadTradeBars(self, symbol: typing.Union[QuantConnect.Symbol, str], startTimeUtc: typing.Union[datetime.datetime, datetime.date], endTimeUtc: typing.Union[datetime.datetime, datetime.date], resolution: QuantConnect.Resolution, requestedTimeZone: typing.Any) -> System.Collections.Generic.IEnumerable[QuantConnect.Data.Market.TradeBar]:
        """
        Downloads a list of TradeBars at the requested resolution
        
        :param symbol: The symbol
        :param startTimeUtc: The starting time (UTC)
        :param endTimeUtc: The ending time (UTC)
        :param resolution: The requested resolution
        :param requestedTimeZone: The requested timezone for the data
        :returns: The list of bars.
        """
        ...

    def GetAccountBaseCurrency(self) -> str:
        """Gets the account base currency"""
        ...

    def GetAccountHoldings(self) -> System.Collections.Generic.List[QuantConnect.Holding]:
        """
        Gets all holdings for the account
        
        :returns: The current holdings from the account.
        """
        ...

    def GetCashBalance(self) -> System.Collections.Generic.List[QuantConnect.Securities.CashAmount]:
        """
        Gets the current cash balance for each currency held in the brokerage account
        
        :returns: The current cash balance for each currency available for trading.
        """
        ...

    def GetInstrumentList(self) -> System.Collections.Generic.List[str]:
        """Gets the list of available tradable instruments/products from Oanda"""
        ...

    def GetOpenOrders(self) -> System.Collections.Generic.List[QuantConnect.Orders.Order]:
        """
        Gets all open orders on the account.
        NOTE: The order objects returned do not have QC order IDs.
        
        :returns: The open orders returned from Oanda.
        """
        ...

    def GetRates(self, instruments: System.Collections.Generic.List[str]) -> System.Collections.Generic.Dictionary[str, QuantConnect.Data.Market.Tick]:
        """
        Retrieves the current rate for each of a list of instruments
        
        :param instruments: the list of instruments to check
        :returns: Dictionary containing the current quotes for each instrument.
        """
        ...

    def PlaceOrder(self, order: QuantConnect.Orders.Order) -> bool:
        """
        Places a new order and assigns a new broker ID to the order
        
        :param order: The order to be placed
        :returns: True if the request for a new order has been placed, false otherwise.
        """
        ...

    def StartEventsSession(self) -> typing.Any:
        """
        Initializes a streaming events session which will stream events for the given accounts
        
        :returns: the WebResponse object that can be used to retrieve the events as they stream.
        """
        ...

    def StartPricingStream(self, instruments: System.Collections.Generic.List[str]) -> None:
        """Starts streaming prices for a list of instruments"""
        ...

    def StartRatesSession(self, instruments: System.Collections.Generic.List[str]) -> typing.Any:
        """
        Initializes a streaming rates session with the given instruments on the given account
        
        :param instruments: list of instruments to stream rates for
        :returns: the WebResponse object that can be used to retrieve the rates as they stream.
        """
        ...

    def StartTransactionStream(self) -> None:
        """Starts streaming transactions for the active account"""
        ...

    def StopPricingStream(self) -> None:
        """Stops streaming prices for all instruments"""
        ...

    def StopTransactionStream(self) -> None:
        """Stops streaming transactions for the active account"""
        ...

    def UpdateOrder(self, order: QuantConnect.Orders.Order) -> bool:
        """
        Updates the order with the same id
        
        :param order: The new order information
        :returns: True if the request was made for the order to be updated, false otherwise.
        """
        ...


