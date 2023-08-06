from typing import overload
import datetime
import typing

import QuantConnect
import QuantConnect.Brokerages
import QuantConnect.Brokerages.Tradier
import QuantConnect.Data
import QuantConnect.Interfaces
import QuantConnect.Orders
import QuantConnect.Packets
import QuantConnect.Securities
import System
import System.Collections.Generic

QuantConnect_Brokerages_Tradier__EventContainer_Callable = typing.TypeVar("QuantConnect_Brokerages_Tradier__EventContainer_Callable")
QuantConnect_Brokerages_Tradier__EventContainer_ReturnType = typing.TypeVar("QuantConnect_Brokerages_Tradier__EventContainer_ReturnType")


class TradierTimeSeries(System.Object):
    """One bar of historical Tradier data."""

    @property
    def Time(self) -> datetime.datetime:
        ...

    @Time.setter
    def Time(self, value: datetime.datetime):
        ...

    @property
    def Price(self) -> float:
        ...

    @Price.setter
    def Price(self, value: float):
        ...

    @property
    def Open(self) -> float:
        ...

    @Open.setter
    def Open(self, value: float):
        ...

    @property
    def High(self) -> float:
        ...

    @High.setter
    def High(self, value: float):
        ...

    @property
    def Low(self) -> float:
        ...

    @Low.setter
    def Low(self, value: float):
        ...

    @property
    def Close(self) -> float:
        ...

    @Close.setter
    def Close(self, value: float):
        ...

    @property
    def Volume(self) -> int:
        ...

    @Volume.setter
    def Volume(self, value: int):
        ...


class TradierTimeSeriesContainer(System.Object):
    """Container for timeseries array"""

    @property
    def TimeSeries(self) -> System.Collections.Generic.List[QuantConnect.Brokerages.Tradier.TradierTimeSeries]:
        ...

    @TimeSeries.setter
    def TimeSeries(self, value: System.Collections.Generic.List[QuantConnect.Brokerages.Tradier.TradierTimeSeries]):
        ...


class TradierQuote(System.Object):
    """Quote data from Tradier:"""

    @property
    def Symbol(self) -> str:
        ...

    @Symbol.setter
    def Symbol(self, value: str):
        ...

    @property
    def Description(self) -> str:
        ...

    @Description.setter
    def Description(self, value: str):
        ...

    @property
    def Exchange(self) -> str:
        ...

    @Exchange.setter
    def Exchange(self, value: str):
        ...

    @property
    def Type(self) -> str:
        ...

    @Type.setter
    def Type(self, value: str):
        ...

    @property
    def Last(self) -> float:
        ...

    @Last.setter
    def Last(self, value: float):
        ...

    @property
    def Change(self) -> float:
        ...

    @Change.setter
    def Change(self, value: float):
        ...

    @property
    def PercentageChange(self) -> float:
        ...

    @PercentageChange.setter
    def PercentageChange(self, value: float):
        ...

    @property
    def Volume(self) -> float:
        ...

    @Volume.setter
    def Volume(self, value: float):
        ...

    @property
    def AverageVolume(self) -> float:
        ...

    @AverageVolume.setter
    def AverageVolume(self, value: float):
        ...

    @property
    def LastVolume(self) -> float:
        ...

    @LastVolume.setter
    def LastVolume(self, value: float):
        ...

    @property
    def TradeDateUnix(self) -> int:
        ...

    @TradeDateUnix.setter
    def TradeDateUnix(self, value: int):
        ...

    @property
    def Open(self) -> typing.Optional[float]:
        ...

    @Open.setter
    def Open(self, value: typing.Optional[float]):
        ...

    @property
    def High(self) -> typing.Optional[float]:
        ...

    @High.setter
    def High(self, value: typing.Optional[float]):
        ...

    @property
    def Low(self) -> typing.Optional[float]:
        ...

    @Low.setter
    def Low(self, value: typing.Optional[float]):
        ...

    @property
    def Close(self) -> typing.Optional[float]:
        ...

    @Close.setter
    def Close(self, value: typing.Optional[float]):
        ...

    @property
    def PreviousClose(self) -> float:
        ...

    @PreviousClose.setter
    def PreviousClose(self, value: float):
        ...

    @property
    def Week52High(self) -> float:
        ...

    @Week52High.setter
    def Week52High(self, value: float):
        ...

    @property
    def Week52Low(self) -> float:
        ...

    @Week52Low.setter
    def Week52Low(self, value: float):
        ...

    @property
    def Bid(self) -> typing.Optional[float]:
        ...

    @Bid.setter
    def Bid(self, value: typing.Optional[float]):
        ...

    @property
    def BidSize(self) -> float:
        ...

    @BidSize.setter
    def BidSize(self, value: float):
        ...

    @property
    def BigExchange(self) -> str:
        ...

    @BigExchange.setter
    def BigExchange(self, value: str):
        ...

    @property
    def Ask(self) -> typing.Optional[float]:
        ...

    @Ask.setter
    def Ask(self, value: typing.Optional[float]):
        ...

    @property
    def AskSize(self) -> float:
        ...

    @AskSize.setter
    def AskSize(self, value: float):
        ...

    @property
    def AskExchange(self) -> str:
        ...

    @AskExchange.setter
    def AskExchange(self, value: str):
        ...

    def __init__(self) -> None:
        ...


class TradierQuoteContainer(System.Object):
    """Container for quotes:"""

    @property
    def Quotes(self) -> System.Collections.Generic.List[QuantConnect.Brokerages.Tradier.TradierQuote]:
        ...

    @Quotes.setter
    def Quotes(self, value: System.Collections.Generic.List[QuantConnect.Brokerages.Tradier.TradierQuote]):
        ...


class TradierHistoryBar(System.Object):
    """"Bar" for a history unit."""

    @property
    def Time(self) -> datetime.datetime:
        ...

    @Time.setter
    def Time(self, value: datetime.datetime):
        ...

    @property
    def Open(self) -> float:
        ...

    @Open.setter
    def Open(self, value: float):
        ...

    @property
    def High(self) -> float:
        ...

    @High.setter
    def High(self, value: float):
        ...

    @property
    def Low(self) -> float:
        ...

    @Low.setter
    def Low(self, value: float):
        ...

    @property
    def Close(self) -> float:
        ...

    @Close.setter
    def Close(self, value: float):
        ...

    @property
    def Volume(self) -> int:
        ...

    @Volume.setter
    def Volume(self, value: int):
        ...


class TradierHistoryDataContainer(System.Object):
    """Container for deserializing history classes"""

    @property
    def Data(self) -> System.Collections.Generic.List[QuantConnect.Brokerages.Tradier.TradierHistoryBar]:
        ...

    @Data.setter
    def Data(self, value: System.Collections.Generic.List[QuantConnect.Brokerages.Tradier.TradierHistoryBar]):
        ...


class TradierMarketStatus(System.Object):
    """Current market status description"""

    @property
    def Date(self) -> datetime.datetime:
        ...

    @Date.setter
    def Date(self, value: datetime.datetime):
        ...

    @property
    def Description(self) -> str:
        ...

    @Description.setter
    def Description(self, value: str):
        ...

    @property
    def NextChange(self) -> str:
        ...

    @NextChange.setter
    def NextChange(self, value: str):
        ...

    @property
    def State(self) -> str:
        ...

    @State.setter
    def State(self, value: str):
        ...

    @property
    def TimeStamp(self) -> int:
        ...

    @TimeStamp.setter
    def TimeStamp(self, value: int):
        ...


class TradierCalendarDayMarketHours(System.Object):
    """Start and finish time of market hours for this market."""

    @property
    def Start(self) -> datetime.datetime:
        ...

    @Start.setter
    def Start(self, value: datetime.datetime):
        ...

    @property
    def End(self) -> datetime.datetime:
        ...

    @End.setter
    def End(self, value: datetime.datetime):
        ...


class TradierCalendarDay(System.Object):
    """Single days properties from the calendar:"""

    @property
    def Date(self) -> datetime.datetime:
        ...

    @Date.setter
    def Date(self, value: datetime.datetime):
        ...

    @property
    def Status(self) -> str:
        ...

    @Status.setter
    def Status(self, value: str):
        ...

    @property
    def Description(self) -> str:
        ...

    @Description.setter
    def Description(self, value: str):
        ...

    @property
    def Premarket(self) -> QuantConnect.Brokerages.Tradier.TradierCalendarDayMarketHours:
        ...

    @Premarket.setter
    def Premarket(self, value: QuantConnect.Brokerages.Tradier.TradierCalendarDayMarketHours):
        ...

    @property
    def Open(self) -> QuantConnect.Brokerages.Tradier.TradierCalendarDayMarketHours:
        ...

    @Open.setter
    def Open(self, value: QuantConnect.Brokerages.Tradier.TradierCalendarDayMarketHours):
        ...

    @property
    def Postmarket(self) -> QuantConnect.Brokerages.Tradier.TradierCalendarDayMarketHours:
        ...

    @Postmarket.setter
    def Postmarket(self, value: QuantConnect.Brokerages.Tradier.TradierCalendarDayMarketHours):
        ...


class TradierCalendarDayContainer(System.Object):
    """Container for the days array:"""

    @property
    def Days(self) -> System.Collections.Generic.List[QuantConnect.Brokerages.Tradier.TradierCalendarDay]:
        ...

    @Days.setter
    def Days(self, value: System.Collections.Generic.List[QuantConnect.Brokerages.Tradier.TradierCalendarDay]):
        ...


class TradierCalendarStatus(System.Object):
    """Calendar status:"""

    @property
    def Days(self) -> QuantConnect.Brokerages.Tradier.TradierCalendarDayContainer:
        ...

    @Days.setter
    def Days(self, value: QuantConnect.Brokerages.Tradier.TradierCalendarDayContainer):
        ...

    @property
    def Month(self) -> int:
        ...

    @Month.setter
    def Month(self, value: int):
        ...

    @property
    def Year(self) -> int:
        ...

    @Year.setter
    def Year(self, value: int):
        ...


class TradierSearchResult(System.Object):
    """One search result from API"""

    @property
    def Symbol(self) -> str:
        ...

    @Symbol.setter
    def Symbol(self, value: str):
        ...

    @property
    def Exchange(self) -> str:
        ...

    @Exchange.setter
    def Exchange(self, value: str):
        ...

    @property
    def Type(self) -> str:
        ...

    @Type.setter
    def Type(self, value: str):
        ...

    @property
    def Description(self) -> str:
        ...

    @Description.setter
    def Description(self, value: str):
        ...


class TradierSearchContainer(System.Object):
    """Tradier Search Container for Deserialization:"""

    @property
    def Results(self) -> System.Collections.Generic.List[QuantConnect.Brokerages.Tradier.TradierSearchResult]:
        ...

    @Results.setter
    def Results(self, value: System.Collections.Generic.List[QuantConnect.Brokerages.Tradier.TradierSearchResult]):
        ...


class TradierStreamSession(System.Object):
    """Create a new stream session"""

    @property
    def SessionId(self) -> str:
        ...

    @SessionId.setter
    def SessionId(self, value: str):
        ...

    @property
    def Url(self) -> str:
        ...

    @Url.setter
    def Url(self, value: str):
        ...


class TradierStreamData(System.Object):
    """One data packet from a tradier stream:"""

    @property
    def Type(self) -> str:
        ...

    @Type.setter
    def Type(self, value: str):
        ...

    @property
    def UnixDate(self) -> str:
        ...

    @UnixDate.setter
    def UnixDate(self, value: str):
        ...

    @property
    def Symbol(self) -> str:
        ...

    @Symbol.setter
    def Symbol(self, value: str):
        ...

    @property
    def SummaryOpen(self) -> float:
        ...

    @SummaryOpen.setter
    def SummaryOpen(self, value: float):
        ...

    @property
    def SummaryHigh(self) -> float:
        ...

    @SummaryHigh.setter
    def SummaryHigh(self, value: float):
        ...

    @property
    def SummaryLow(self) -> float:
        ...

    @SummaryLow.setter
    def SummaryLow(self, value: float):
        ...

    @property
    def SummaryClose(self) -> float:
        ...

    @SummaryClose.setter
    def SummaryClose(self, value: float):
        ...

    @property
    def BidPrice(self) -> float:
        ...

    @BidPrice.setter
    def BidPrice(self, value: float):
        ...

    @property
    def BidSize(self) -> int:
        ...

    @BidSize.setter
    def BidSize(self, value: int):
        ...

    @property
    def BidExchange(self) -> str:
        ...

    @BidExchange.setter
    def BidExchange(self, value: str):
        ...

    @property
    def BidDateUnix(self) -> int:
        ...

    @BidDateUnix.setter
    def BidDateUnix(self, value: int):
        ...

    @property
    def TradePrice(self) -> float:
        ...

    @TradePrice.setter
    def TradePrice(self, value: float):
        ...

    @property
    def TradeSize(self) -> float:
        ...

    @TradeSize.setter
    def TradeSize(self, value: float):
        ...

    @property
    def TradeExchange(self) -> str:
        ...

    @TradeExchange.setter
    def TradeExchange(self, value: str):
        ...

    @property
    def TradeCVol(self) -> int:
        ...

    @TradeCVol.setter
    def TradeCVol(self, value: int):
        ...

    @property
    def AskPrice(self) -> float:
        ...

    @AskPrice.setter
    def AskPrice(self, value: float):
        ...

    @property
    def AskSize(self) -> int:
        ...

    @AskSize.setter
    def AskSize(self, value: int):
        ...

    @property
    def AskExchange(self) -> str:
        ...

    @AskExchange.setter
    def AskExchange(self, value: str):
        ...

    @property
    def AskDateUnix(self) -> int:
        ...

    @AskDateUnix.setter
    def AskDateUnix(self, value: int):
        ...

    def GetTickTimestamp(self) -> datetime.datetime:
        """Gets the tick timestamp (UTC)"""
        ...


class TradierEventType(System.Enum):
    """Tradier event type:"""

    Trade = 0

    Journal = 1

    Option = 2

    Dividend = 3


class TradierEventDetail(System.Object):
    """Common base class for events detail information:"""

    @property
    def Description(self) -> str:
        ...

    @Description.setter
    def Description(self, value: str):
        ...

    @property
    def Quantity(self) -> float:
        ...

    @Quantity.setter
    def Quantity(self, value: float):
        ...

    def __init__(self) -> None:
        ...


class TradierTradeType(System.Enum):
    """Market type of the trade:"""

    Equity = 0

    Option = 1


class TradierTradeEvent(QuantConnect.Brokerages.Tradier.TradierEventDetail):
    """Trade event in history for tradier:"""

    @property
    def Commission(self) -> float:
        ...

    @Commission.setter
    def Commission(self, value: float):
        ...

    @property
    def Price(self) -> float:
        ...

    @Price.setter
    def Price(self, value: float):
        ...

    @property
    def Symbol(self) -> str:
        ...

    @Symbol.setter
    def Symbol(self, value: str):
        ...

    @property
    def TradeType(self) -> QuantConnect.Brokerages.Tradier.TradierTradeType:
        ...

    @TradeType.setter
    def TradeType(self, value: QuantConnect.Brokerages.Tradier.TradierTradeType):
        ...

    def __init__(self) -> None:
        ...


class TradierJournalEvent(QuantConnect.Brokerages.Tradier.TradierEventDetail):
    """Journal event in history:"""

    def __init__(self) -> None:
        ...


class TradierOptionStatus(System.Enum):
    """Tradier options status"""

    Exercise = 0

    Expired = 1

    Assignment = 2


class TradierOptionEvent(QuantConnect.Brokerages.Tradier.TradierEventDetail):
    """Option event record in history:"""

    @property
    def Type(self) -> QuantConnect.Brokerages.Tradier.TradierOptionStatus:
        ...

    @Type.setter
    def Type(self, value: QuantConnect.Brokerages.Tradier.TradierOptionStatus):
        ...

    def __init__(self) -> None:
        ...


class TradierEvent(System.Object):
    """Tradier event model:"""

    @property
    def Amount(self) -> float:
        ...

    @Amount.setter
    def Amount(self, value: float):
        ...

    @property
    def Date(self) -> datetime.datetime:
        ...

    @Date.setter
    def Date(self, value: datetime.datetime):
        ...

    @property
    def Type(self) -> QuantConnect.Brokerages.Tradier.TradierEventType:
        ...

    @Type.setter
    def Type(self, value: QuantConnect.Brokerages.Tradier.TradierEventType):
        ...

    @property
    def TradeEvent(self) -> QuantConnect.Brokerages.Tradier.TradierTradeEvent:
        ...

    @TradeEvent.setter
    def TradeEvent(self, value: QuantConnect.Brokerages.Tradier.TradierTradeEvent):
        ...

    @property
    def JournalEvent(self) -> QuantConnect.Brokerages.Tradier.TradierJournalEvent:
        ...

    @JournalEvent.setter
    def JournalEvent(self, value: QuantConnect.Brokerages.Tradier.TradierJournalEvent):
        ...

    @property
    def OptionEvent(self) -> QuantConnect.Brokerages.Tradier.TradierOptionEvent:
        ...

    @OptionEvent.setter
    def OptionEvent(self, value: QuantConnect.Brokerages.Tradier.TradierOptionEvent):
        ...

    @property
    def DividendEvent(self) -> QuantConnect.Brokerages.Tradier.TradierOptionEvent:
        ...

    @DividendEvent.setter
    def DividendEvent(self, value: QuantConnect.Brokerages.Tradier.TradierOptionEvent):
        ...


class TradierEvents(System.Object):
    """Events array container."""

    @property
    def Events(self) -> System.Collections.Generic.List[QuantConnect.Brokerages.Tradier.TradierEvent]:
        ...

    @Events.setter
    def Events(self, value: System.Collections.Generic.List[QuantConnect.Brokerages.Tradier.TradierEvent]):
        ...

    def __init__(self) -> None:
        ...


class TradierEventContainer(System.Object):
    """Tradier deserialization container for history"""

    @property
    def TradierEvents(self) -> QuantConnect.Brokerages.Tradier.TradierEvents:
        ...

    @TradierEvents.setter
    def TradierEvents(self, value: QuantConnect.Brokerages.Tradier.TradierEvents):
        ...

    def __init__(self) -> None:
        ...


class TradierDividendEvent(QuantConnect.Brokerages.Tradier.TradierEventDetail):
    """Dividend event in history:"""

    def __init__(self) -> None:
        ...


class TradierBrokerageFactory(QuantConnect.Brokerages.BrokerageFactory):
    """Provides an implementations of IBrokerageFactory that produces a TradierBrokerage"""

    class Configuration(System.Object):
        """Gets tradier values from configuration"""

        UseSandbox: bool
        """Gets whether to use the developer sandbox or not"""

        Environment: str
        """Gets whether to use the developer sandbox (paper mode) or live mode"""

        AccountId: str
        """Gets the account ID to be used when instantiating a brokerage"""

        AccessToken: str
        """Gets the access token from configuration"""

    @property
    def BrokerageData(self) -> System.Collections.Generic.Dictionary[str, str]:
        """Gets the brokerage data required to run the brokerage from configuration/disk"""
        ...

    def __init__(self) -> None:
        """Initializes a new instance of he TradierBrokerageFactory class"""
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
        Gets a new instance of the TradierBrokerageModel
        
        :param orderProvider: The order provider
        """
        ...


class TradierAccountType(System.Enum):
    """Tradier account type:"""

    DayTrader = 0

    Cash = 1

    Margin = 2


class TradierAccountTypeCash(System.Object):
    """Account Type Margin Settings:"""

    @property
    def Sweep(self) -> int:
        ...

    @Sweep.setter
    def Sweep(self, value: int):
        ...

    @property
    def CashAvailable(self) -> float:
        ...

    @CashAvailable.setter
    def CashAvailable(self, value: float):
        ...

    @property
    def UnsettledFunds(self) -> float:
        ...

    @UnsettledFunds.setter
    def UnsettledFunds(self, value: float):
        ...

    def __init__(self) -> None:
        ...


class TradierAccountTypeSettings(System.Object):
    """Common Account Settings."""

    @property
    def FedCall(self) -> float:
        ...

    @FedCall.setter
    def FedCall(self, value: float):
        ...

    @property
    def MaintenanceCall(self) -> float:
        ...

    @MaintenanceCall.setter
    def MaintenanceCall(self, value: float):
        ...

    @property
    def StockBuyingPower(self) -> float:
        ...

    @StockBuyingPower.setter
    def StockBuyingPower(self, value: float):
        ...

    @property
    def OptionBuyingPower(self) -> float:
        ...

    @OptionBuyingPower.setter
    def OptionBuyingPower(self, value: float):
        ...

    @property
    def StockShortValue(self) -> float:
        ...

    @StockShortValue.setter
    def StockShortValue(self, value: float):
        ...

    def __init__(self) -> None:
        ...


class TradierAccountTypeDayTrader(QuantConnect.Brokerages.Tradier.TradierAccountTypeSettings):
    """Account Type Day Trader Settings:"""

    @property
    def DayTradeBuyingPower(self) -> float:
        ...

    @DayTradeBuyingPower.setter
    def DayTradeBuyingPower(self, value: float):
        ...

    def __init__(self) -> None:
        ...


class TradierAccountTypeMargin(QuantConnect.Brokerages.Tradier.TradierAccountTypeSettings):
    """Account Type Margin Settings:"""

    @property
    def Sweep(self) -> int:
        ...

    @Sweep.setter
    def Sweep(self, value: int):
        ...

    def __init__(self) -> None:
        ...


class TradierBalanceDetails(System.Object):
    """Trader Balance Detail:"""

    @property
    def AccountNumber(self) -> str:
        ...

    @AccountNumber.setter
    def AccountNumber(self, value: str):
        ...

    @property
    def Type(self) -> QuantConnect.Brokerages.Tradier.TradierAccountType:
        ...

    @Type.setter
    def Type(self, value: QuantConnect.Brokerages.Tradier.TradierAccountType):
        ...

    @property
    def CashAvailable(self) -> float:
        ...

    @CashAvailable.setter
    def CashAvailable(self, value: float):
        ...

    @property
    def ClosingProfitLoss(self) -> float:
        ...

    @ClosingProfitLoss.setter
    def ClosingProfitLoss(self, value: float):
        ...

    @property
    def CurrentRequirement(self) -> float:
        ...

    @CurrentRequirement.setter
    def CurrentRequirement(self, value: float):
        ...

    @property
    def DividendBalance(self) -> float:
        ...

    @DividendBalance.setter
    def DividendBalance(self, value: float):
        ...

    @property
    def Equity(self) -> float:
        ...

    @Equity.setter
    def Equity(self, value: float):
        ...

    @property
    def LongLiquidValue(self) -> float:
        ...

    @LongLiquidValue.setter
    def LongLiquidValue(self, value: float):
        ...

    @property
    def LongMarketValue(self) -> float:
        ...

    @LongMarketValue.setter
    def LongMarketValue(self, value: float):
        ...

    @property
    def MarketValue(self) -> float:
        ...

    @MarketValue.setter
    def MarketValue(self, value: float):
        ...

    @property
    def NetValue(self) -> float:
        ...

    @NetValue.setter
    def NetValue(self, value: float):
        ...

    @property
    def OpenProfitLoss(self) -> float:
        ...

    @OpenProfitLoss.setter
    def OpenProfitLoss(self, value: float):
        ...

    @property
    def OptionLongValue(self) -> float:
        ...

    @OptionLongValue.setter
    def OptionLongValue(self, value: float):
        ...

    @property
    def OptionRequirement(self) -> float:
        ...

    @OptionRequirement.setter
    def OptionRequirement(self, value: float):
        ...

    @property
    def OptionShortValue(self) -> float:
        ...

    @OptionShortValue.setter
    def OptionShortValue(self, value: float):
        ...

    @property
    def PendingCash(self) -> float:
        ...

    @PendingCash.setter
    def PendingCash(self, value: float):
        ...

    @property
    def PendingOrdersCount(self) -> int:
        ...

    @PendingOrdersCount.setter
    def PendingOrdersCount(self, value: int):
        ...

    @property
    def ShortLiquidValue(self) -> float:
        ...

    @ShortLiquidValue.setter
    def ShortLiquidValue(self, value: float):
        ...

    @property
    def ShortMarketValue(self) -> float:
        ...

    @ShortMarketValue.setter
    def ShortMarketValue(self, value: float):
        ...

    @property
    def StockLongValue(self) -> float:
        ...

    @StockLongValue.setter
    def StockLongValue(self, value: float):
        ...

    @property
    def UnclearedFunds(self) -> float:
        ...

    @UnclearedFunds.setter
    def UnclearedFunds(self, value: float):
        ...

    @property
    def UnsettledFunds(self) -> float:
        ...

    @UnsettledFunds.setter
    def UnsettledFunds(self, value: float):
        ...

    @property
    def TotalCash(self) -> float:
        ...

    @TotalCash.setter
    def TotalCash(self, value: float):
        ...

    @property
    def TotalEquity(self) -> float:
        ...

    @TotalEquity.setter
    def TotalEquity(self, value: float):
        ...

    @property
    def CashTypeSettings(self) -> QuantConnect.Brokerages.Tradier.TradierAccountTypeCash:
        ...

    @CashTypeSettings.setter
    def CashTypeSettings(self, value: QuantConnect.Brokerages.Tradier.TradierAccountTypeCash):
        ...

    @property
    def PatternTraderTypeSettings(self) -> QuantConnect.Brokerages.Tradier.TradierAccountTypeDayTrader:
        ...

    @PatternTraderTypeSettings.setter
    def PatternTraderTypeSettings(self, value: QuantConnect.Brokerages.Tradier.TradierAccountTypeDayTrader):
        ...

    @property
    def MarginTypeSettings(self) -> QuantConnect.Brokerages.Tradier.TradierAccountTypeMargin:
        ...

    @MarginTypeSettings.setter
    def MarginTypeSettings(self, value: QuantConnect.Brokerages.Tradier.TradierAccountTypeMargin):
        ...


class TradierBalance(System.Object):
    """Inside "Account" User-account balance information."""

    @property
    def Balances(self) -> QuantConnect.Brokerages.Tradier.TradierBalanceDetails:
        ...

    @Balances.setter
    def Balances(self, value: QuantConnect.Brokerages.Tradier.TradierBalanceDetails):
        ...


class TradierPosition(System.Object):
    """Individual Tradier position model."""

    @property
    def Id(self) -> int:
        ...

    @Id.setter
    def Id(self, value: int):
        ...

    @property
    def DateAcquired(self) -> datetime.datetime:
        ...

    @DateAcquired.setter
    def DateAcquired(self, value: datetime.datetime):
        ...

    @property
    def Quantity(self) -> int:
        ...

    @Quantity.setter
    def Quantity(self, value: int):
        ...

    @property
    def CostBasis(self) -> float:
        ...

    @CostBasis.setter
    def CostBasis(self, value: float):
        ...

    @property
    def Symbol(self) -> str:
        ...

    @Symbol.setter
    def Symbol(self, value: str):
        ...


class TradierPositions(System.Object):
    """Position array container."""

    @property
    def Positions(self) -> System.Collections.Generic.List[QuantConnect.Brokerages.Tradier.TradierPosition]:
        ...

    @Positions.setter
    def Positions(self, value: System.Collections.Generic.List[QuantConnect.Brokerages.Tradier.TradierPosition]):
        ...

    def __init__(self) -> None:
        ...


class TradierPositionsContainer(System.Object):
    """Empty class for deserializing positions held."""

    @property
    def TradierPositions(self) -> QuantConnect.Brokerages.Tradier.TradierPositions:
        ...

    @TradierPositions.setter
    def TradierPositions(self, value: QuantConnect.Brokerages.Tradier.TradierPositions):
        ...

    def __init__(self) -> None:
        ...


class TradierUserAccount(System.Object):
    """Account only settings for a tradier user:"""

    @property
    def AccountNumber(self) -> int:
        ...

    @AccountNumber.setter
    def AccountNumber(self, value: int):
        ...

    @property
    def DayTrader(self) -> bool:
        ...

    @DayTrader.setter
    def DayTrader(self, value: bool):
        ...

    @property
    def OptionLevel(self) -> int:
        ...

    @OptionLevel.setter
    def OptionLevel(self, value: int):
        ...

    @property
    def Type(self) -> int:
        """This property contains the int value of a member of the QuantConnect.Brokerages.Tradier.TradierAccountType enum."""
        ...

    @Type.setter
    def Type(self, value: int):
        """This property contains the int value of a member of the QuantConnect.Brokerages.Tradier.TradierAccountType enum."""
        ...

    @property
    def LastUpdated(self) -> datetime.datetime:
        ...

    @LastUpdated.setter
    def LastUpdated(self, value: datetime.datetime):
        ...

    @property
    def Status(self) -> int:
        """This property contains the int value of a member of the QuantConnect.Brokerages.Tradier.TradierAccountStatus enum."""
        ...

    @Status.setter
    def Status(self, value: int):
        """This property contains the int value of a member of the QuantConnect.Brokerages.Tradier.TradierAccountStatus enum."""
        ...

    @property
    def Classification(self) -> int:
        """This property contains the int value of a member of the QuantConnect.Brokerages.Tradier.TradierAccountClassification enum."""
        ...

    @Classification.setter
    def Classification(self, value: int):
        """This property contains the int value of a member of the QuantConnect.Brokerages.Tradier.TradierAccountClassification enum."""
        ...

    def __init__(self) -> None:
        """Create a new account:"""
        ...


class TradierUser(System.Object):
    """User profile array:"""

    @property
    def Id(self) -> str:
        ...

    @Id.setter
    def Id(self, value: str):
        ...

    @property
    def Name(self) -> str:
        ...

    @Name.setter
    def Name(self, value: str):
        ...

    @property
    def Accounts(self) -> System.Collections.Generic.List[QuantConnect.Brokerages.Tradier.TradierUserAccount]:
        ...

    @Accounts.setter
    def Accounts(self, value: System.Collections.Generic.List[QuantConnect.Brokerages.Tradier.TradierUserAccount]):
        ...

    def __init__(self) -> None:
        ...


class TradierOrderType(System.Enum):
    """Tradier order type: (market, limit, stop, stop_limit or market) //credit, debit, even"""

    Limit = 0

    Market = 1

    StopLimit = 2

    StopMarket = 3

    Credit = 4

    Debit = 5

    Even = 6


class TradierOrderDirection(System.Enum):
    """
    Direction of the order
    (buy, buy_to_open, buy_to_cover, buy_to_close, sell, sell_short, sell_to_open, sell_to_close)
    """

    Buy = 0

    SellShort = 1

    Sell = 2

    BuyToCover = 3

    SellToOpen = 4

    SellToClose = 5

    BuyToClose = 6

    BuyToOpen = 7

    # Cannot convert to Python: None = 8


class TradierOrderStatus(System.Enum):
    """
    Status of the tradier order.
     (filled, canceled, open, expired, rejected, pending, partially_filled, submitted)
    """

    Filled = 0

    Canceled = 1

    Open = 2

    Expired = 3

    Rejected = 4

    Pending = 5

    PartiallyFilled = 6

    Submitted = 7


class TradierOrderDuration(System.Enum):
    """Length of the order offer."""

    GTC = 0

    Day = 1

    Pre = 2

    Post = 3


class TradierOrderClass(System.Enum):
    """Class of the order."""

    Equity = 0

    Option = 1

    Multileg = 2

    Combo = 3


class TradierOrderLeg(System.Object):
    """Leg of a tradier order:"""

    @property
    def Type(self) -> QuantConnect.Brokerages.Tradier.TradierOrderType:
        ...

    @Type.setter
    def Type(self, value: QuantConnect.Brokerages.Tradier.TradierOrderType):
        ...

    @property
    def Symbol(self) -> str:
        ...

    @Symbol.setter
    def Symbol(self, value: str):
        ...

    @property
    def Direction(self) -> QuantConnect.Brokerages.Tradier.TradierOrderDirection:
        ...

    @Direction.setter
    def Direction(self, value: QuantConnect.Brokerages.Tradier.TradierOrderDirection):
        ...

    @property
    def Quantity(self) -> float:
        ...

    @Quantity.setter
    def Quantity(self, value: float):
        ...

    @property
    def Status(self) -> QuantConnect.Brokerages.Tradier.TradierOrderStatus:
        ...

    @Status.setter
    def Status(self, value: QuantConnect.Brokerages.Tradier.TradierOrderStatus):
        ...

    @property
    def Duration(self) -> QuantConnect.Brokerages.Tradier.TradierOrderDuration:
        ...

    @Duration.setter
    def Duration(self, value: QuantConnect.Brokerages.Tradier.TradierOrderDuration):
        ...

    @property
    def Price(self) -> float:
        ...

    @Price.setter
    def Price(self, value: float):
        ...

    @property
    def AverageFillPrice(self) -> float:
        ...

    @AverageFillPrice.setter
    def AverageFillPrice(self, value: float):
        ...

    @property
    def QuantityExecuted(self) -> float:
        ...

    @QuantityExecuted.setter
    def QuantityExecuted(self, value: float):
        ...

    @property
    def LastFillPrice(self) -> float:
        ...

    @LastFillPrice.setter
    def LastFillPrice(self, value: float):
        ...

    @property
    def LastFillQuantity(self) -> float:
        ...

    @LastFillQuantity.setter
    def LastFillQuantity(self, value: float):
        ...

    @property
    def RemainingQuantity(self) -> float:
        ...

    @RemainingQuantity.setter
    def RemainingQuantity(self, value: float):
        ...

    @property
    def CreatedDate(self) -> datetime.datetime:
        ...

    @CreatedDate.setter
    def CreatedDate(self, value: datetime.datetime):
        ...

    @property
    def TransacionDate(self) -> datetime.datetime:
        ...

    @TransacionDate.setter
    def TransacionDate(self, value: datetime.datetime):
        ...

    def __init__(self) -> None:
        ...


class TradierOrder(System.Object):
    """Intraday or pending order for user"""

    @property
    def Id(self) -> int:
        ...

    @Id.setter
    def Id(self, value: int):
        ...

    @property
    def Type(self) -> QuantConnect.Brokerages.Tradier.TradierOrderType:
        ...

    @Type.setter
    def Type(self, value: QuantConnect.Brokerages.Tradier.TradierOrderType):
        ...

    @property
    def Symbol(self) -> str:
        ...

    @Symbol.setter
    def Symbol(self, value: str):
        ...

    @property
    def OptionSymbol(self) -> str:
        ...

    @OptionSymbol.setter
    def OptionSymbol(self, value: str):
        ...

    @property
    def Direction(self) -> QuantConnect.Brokerages.Tradier.TradierOrderDirection:
        ...

    @Direction.setter
    def Direction(self, value: QuantConnect.Brokerages.Tradier.TradierOrderDirection):
        ...

    @property
    def Quantity(self) -> float:
        ...

    @Quantity.setter
    def Quantity(self, value: float):
        ...

    @property
    def Status(self) -> QuantConnect.Brokerages.Tradier.TradierOrderStatus:
        ...

    @Status.setter
    def Status(self, value: QuantConnect.Brokerages.Tradier.TradierOrderStatus):
        ...

    @property
    def Duration(self) -> QuantConnect.Brokerages.Tradier.TradierOrderDuration:
        ...

    @Duration.setter
    def Duration(self, value: QuantConnect.Brokerages.Tradier.TradierOrderDuration):
        ...

    @property
    def Price(self) -> float:
        ...

    @Price.setter
    def Price(self, value: float):
        ...

    @property
    def AverageFillPrice(self) -> float:
        ...

    @AverageFillPrice.setter
    def AverageFillPrice(self, value: float):
        ...

    @property
    def QuantityExecuted(self) -> float:
        ...

    @QuantityExecuted.setter
    def QuantityExecuted(self, value: float):
        ...

    @property
    def LastFillPrice(self) -> float:
        ...

    @LastFillPrice.setter
    def LastFillPrice(self, value: float):
        ...

    @property
    def LastFillQuantity(self) -> float:
        ...

    @LastFillQuantity.setter
    def LastFillQuantity(self, value: float):
        ...

    @property
    def RemainingQuantity(self) -> float:
        ...

    @RemainingQuantity.setter
    def RemainingQuantity(self, value: float):
        ...

    @property
    def CreatedDate(self) -> datetime.datetime:
        ...

    @CreatedDate.setter
    def CreatedDate(self, value: datetime.datetime):
        ...

    @property
    def TransactionDate(self) -> datetime.datetime:
        ...

    @TransactionDate.setter
    def TransactionDate(self, value: datetime.datetime):
        ...

    @property
    def Class(self) -> QuantConnect.Brokerages.Tradier.TradierOrderClass:
        ...

    @Class.setter
    def Class(self, value: QuantConnect.Brokerages.Tradier.TradierOrderClass):
        ...

    @property
    def NumberOfLegs(self) -> int:
        ...

    @NumberOfLegs.setter
    def NumberOfLegs(self, value: int):
        ...

    @property
    def Legs(self) -> System.Collections.Generic.List[QuantConnect.Brokerages.Tradier.TradierOrderLeg]:
        ...

    @Legs.setter
    def Legs(self, value: System.Collections.Generic.List[QuantConnect.Brokerages.Tradier.TradierOrderLeg]):
        ...

    def __init__(self) -> None:
        ...


class TradierOptionType(System.Enum):
    """Tradier option type"""

    Put = 0

    Call = 1


class TradierOrderDetailed(QuantConnect.Brokerages.Tradier.TradierOrder):
    """Detailed order type."""

    @property
    def Exchange(self) -> str:
        ...

    @Exchange.setter
    def Exchange(self, value: str):
        ...

    @property
    def ExecutionExchange(self) -> str:
        ...

    @ExecutionExchange.setter
    def ExecutionExchange(self, value: str):
        ...

    @property
    def OptionType(self) -> QuantConnect.Brokerages.Tradier.TradierOptionType:
        ...

    @OptionType.setter
    def OptionType(self, value: QuantConnect.Brokerages.Tradier.TradierOptionType):
        ...

    @property
    def OptionExpirationDate(self) -> datetime.datetime:
        ...

    @OptionExpirationDate.setter
    def OptionExpirationDate(self, value: datetime.datetime):
        ...

    @property
    def StopPrice(self) -> float:
        ...

    @StopPrice.setter
    def StopPrice(self, value: float):
        ...


class TradierOrderResponseOrder(System.Object):
    """Order response when purchasing equity."""

    @property
    def Id(self) -> int:
        ...

    @Id.setter
    def Id(self, value: int):
        ...

    @property
    def PartnerId(self) -> str:
        ...

    @PartnerId.setter
    def PartnerId(self, value: str):
        ...

    @property
    def Status(self) -> str:
        ...

    @Status.setter
    def Status(self, value: str):
        ...


class TradierOrderResponseError(System.Object):
    """Errors result from an order request."""

    @property
    def Errors(self) -> System.Collections.Generic.List[str]:
        ...

    @Errors.setter
    def Errors(self, value: System.Collections.Generic.List[str]):
        ...


class TradierOrderResponse(System.Object):
    """Deserialization wrapper for order response:"""

    @property
    def Order(self) -> QuantConnect.Brokerages.Tradier.TradierOrderResponseOrder:
        ...

    @Order.setter
    def Order(self, value: QuantConnect.Brokerages.Tradier.TradierOrderResponseOrder):
        ...

    @property
    def Errors(self) -> QuantConnect.Brokerages.Tradier.TradierOrderResponseError:
        ...

    @Errors.setter
    def Errors(self, value: QuantConnect.Brokerages.Tradier.TradierOrderResponseError):
        ...


class TradierTimeSeriesIntervals(System.Enum):
    """TradeBar windows for Tradier's data histories"""

    Tick = 0

    OneMinute = 1

    FiveMinutes = 2

    FifteenMinutes = 3


class TradierHistoricalDataIntervals(System.Enum):
    """Historical data intervals for tradier requests:"""

    Daily = 0

    Weekly = 1

    Monthly = 2


class TradierGainLoss(System.Object):
    """Account only settings for a tradier user:"""

    @property
    def CloseDate(self) -> datetime.datetime:
        ...

    @CloseDate.setter
    def CloseDate(self, value: datetime.datetime):
        ...

    @property
    def OpenDate(self) -> datetime.datetime:
        ...

    @OpenDate.setter
    def OpenDate(self, value: datetime.datetime):
        ...

    @property
    def Cost(self) -> float:
        ...

    @Cost.setter
    def Cost(self, value: float):
        ...

    @property
    def GainLoss(self) -> float:
        ...

    @GainLoss.setter
    def GainLoss(self, value: float):
        ...

    @property
    def GainLossPercentage(self) -> float:
        ...

    @GainLossPercentage.setter
    def GainLossPercentage(self, value: float):
        ...

    @property
    def Proceeds(self) -> float:
        ...

    @Proceeds.setter
    def Proceeds(self, value: float):
        ...

    @property
    def Quantity(self) -> float:
        ...

    @Quantity.setter
    def Quantity(self, value: float):
        ...

    @property
    def Symbol(self) -> str:
        ...

    @Symbol.setter
    def Symbol(self, value: str):
        ...

    @property
    def Term(self) -> float:
        ...

    @Term.setter
    def Term(self, value: float):
        ...

    def __init__(self) -> None:
        """Closed position trade summary"""
        ...


class TradierBrokerage(QuantConnect.Brokerages.BaseWebsocketsBrokerage, QuantConnect.Interfaces.IDataQueueHandler, QuantConnect.Interfaces.IDataQueueUniverseProvider, QuantConnect.Interfaces.IHistoryProvider):
    """
    Tradier Class:
     - Handle authentication.
     - Data requests.
     - Rate limiting.
     - Placing orders.
     - Getting user data.
    """

    @property
    def AccountBaseCurrency(self) -> str:
        """Returns the brokerage account's base currency"""
        ...

    @AccountBaseCurrency.setter
    def AccountBaseCurrency(self, value: str):
        """Returns the brokerage account's base currency"""
        ...

    @property
    def IsConnected(self) -> bool:
        ...

    @property
    def InvalidConfigurationDetected(self) -> _EventContainer[typing.Callable[[System.Object, QuantConnect.InvalidConfigurationDetectedEventArgs], None], None]:
        ...

    @InvalidConfigurationDetected.setter
    def InvalidConfigurationDetected(self, value: _EventContainer[typing.Callable[[System.Object, QuantConnect.InvalidConfigurationDetectedEventArgs], None], None]):
        ...

    @property
    def NumericalPrecisionLimited(self) -> _EventContainer[typing.Callable[[System.Object, QuantConnect.NumericalPrecisionLimitedEventArgs], None], None]:
        """Event fired when the numerical precision in the factor file has been limited"""
        ...

    @NumericalPrecisionLimited.setter
    def NumericalPrecisionLimited(self, value: _EventContainer[typing.Callable[[System.Object, QuantConnect.NumericalPrecisionLimitedEventArgs], None], None]):
        """Event fired when the numerical precision in the factor file has been limited"""
        ...

    @property
    def DownloadFailed(self) -> _EventContainer[typing.Callable[[System.Object, QuantConnect.DownloadFailedEventArgs], None], None]:
        """Event fired when there was an error downloading a remote file"""
        ...

    @DownloadFailed.setter
    def DownloadFailed(self, value: _EventContainer[typing.Callable[[System.Object, QuantConnect.DownloadFailedEventArgs], None], None]):
        """Event fired when there was an error downloading a remote file"""
        ...

    @property
    def ReaderErrorDetected(self) -> _EventContainer[typing.Callable[[System.Object, QuantConnect.ReaderErrorDetectedEventArgs], None], None]:
        """Event fired when there was an error reading the data"""
        ...

    @ReaderErrorDetected.setter
    def ReaderErrorDetected(self, value: _EventContainer[typing.Callable[[System.Object, QuantConnect.ReaderErrorDetectedEventArgs], None], None]):
        """Event fired when there was an error reading the data"""
        ...

    @property
    def StartDateLimited(self) -> _EventContainer[typing.Callable[[System.Object, QuantConnect.StartDateLimitedEventArgs], None], None]:
        """Event fired when the start date has been limited"""
        ...

    @StartDateLimited.setter
    def StartDateLimited(self, value: _EventContainer[typing.Callable[[System.Object, QuantConnect.StartDateLimitedEventArgs], None], None]):
        """Event fired when the start date has been limited"""
        ...

    @property
    def DataPointCount(self) -> int:
        ...

    @DataPointCount.setter
    def DataPointCount(self, value: int):
        ...

    @overload
    def __init__(self) -> None:
        """Create a new Tradier Object:"""
        ...

    @overload
    def __init__(self, algorithm: QuantConnect.Interfaces.IAlgorithm, orderProvider: QuantConnect.Securities.IOrderProvider, securityProvider: QuantConnect.Securities.ISecurityProvider, aggregator: QuantConnect.Data.IDataAggregator, useSandbox: bool, accountId: str, accessToken: str) -> None:
        """Create a new Tradier Object:"""
        ...

    @overload
    def CancelOrder(self, orderId: int) -> QuantConnect.Brokerages.Tradier.TradierOrderResponse:
        """Cancel the order with this account and id number"""
        ...

    @overload
    def CancelOrder(self, order: QuantConnect.Orders.Order) -> bool:
        """
        Cancels the order with the specified ID
        
        :param order: The order to cancel
        :returns: True if the request was made for the order to be canceled, false otherwise.
        """
        ...

    def CanPerformSelection(self) -> bool:
        """
        Returns whether selection can take place or not.
        
        :returns: True if selection can take place.
        """
        ...

    def ChangeOrder(self, orderId: int, type: QuantConnect.Brokerages.Tradier.TradierOrderType = ..., duration: QuantConnect.Brokerages.Tradier.TradierOrderDuration = ..., price: float = 0, stop: float = 0) -> QuantConnect.Brokerages.Tradier.TradierOrderResponse:
        """Update an exiting Tradier Order:"""
        ...

    @staticmethod
    def ConvertDirection(direction: QuantConnect.Orders.OrderDirection, securityType: QuantConnect.SecurityType, holdingQuantity: float) -> int:
        """
        Converts the QC order direction to a tradier order direction
        
        This method is protected.
        
        :returns: This method returns the int value of a member of the QuantConnect.Brokerages.Tradier.TradierOrderDirection enum.
        """
        ...

    def ConvertHolding(self, position: QuantConnect.Brokerages.Tradier.TradierPosition) -> QuantConnect.Holding:
        """
        Converts the tradier position into a qc holding
        
        This method is protected.
        """
        ...

    def ConvertOrder(self, order: QuantConnect.Brokerages.Tradier.TradierOrder) -> QuantConnect.Orders.Order:
        """
        Converts the specified tradier order into a qc order.
        The 'task' will have a value if we needed to issue a rest call for the stop price, otherwise it will be null
        
        This method is protected.
        """
        ...

    @overload
    def ConvertOrderType(self, type: QuantConnect.Orders.OrderType) -> int:
        """
        Converts the qc order type into a tradier order type
        
        This method is protected.
        
        :returns: This method returns the int value of a member of the QuantConnect.Brokerages.Tradier.TradierOrderType enum.
        """
        ...

    @staticmethod
    @overload
    def ConvertOrderType(order: QuantConnect.Orders.Order) -> int:
        """
        Converts the qc order type into a tradier order type
        
        This method is protected.
        
        :returns: This method returns the int value of a member of the QuantConnect.Brokerages.Tradier.TradierOrderType enum.
        """
        ...

    def ConvertQuantity(self, order: QuantConnect.Brokerages.Tradier.TradierOrder) -> int:
        """
        Converts the tradier order quantity into a qc quantity
        
        This method is protected.
        """
        ...

    @overload
    def ConvertStatus(self, status: QuantConnect.Brokerages.Tradier.TradierOrderStatus) -> int:
        """
        Converts the tradier order status into a qc order status
        
        This method is protected.
        
        :returns: This method returns the int value of a member of the QuantConnect.Orders.OrderStatus enum.
        """
        ...

    @overload
    def ConvertStatus(self, status: QuantConnect.Orders.OrderStatus) -> int:
        """
        Converts the qc order status into a tradier order status
        
        This method is protected.
        
        :returns: This method returns the int value of a member of the QuantConnect.Brokerages.Tradier.TradierOrderStatus enum.
        """
        ...

    def Disconnect(self) -> None:
        """Disconnects the client from the broker's remote servers"""
        ...

    def Dispose(self) -> None:
        """Dispose of the brokerage instance"""
        ...

    def GetAccountEvents(self) -> System.Collections.Generic.List[QuantConnect.Brokerages.Tradier.TradierEvent]:
        """Get a list of historical events for this account:"""
        ...

    def GetAccountHoldings(self) -> System.Collections.Generic.List[QuantConnect.Holding]:
        """
        Gets all holdings for the account
        
        :returns: The current holdings from the account.
        """
        ...

    def GetBalanceDetails(self) -> QuantConnect.Brokerages.Tradier.TradierBalanceDetails:
        """
        Get all the users balance information:
        
        :returns: Balance.
        """
        ...

    def GetCashBalance(self) -> System.Collections.Generic.List[QuantConnect.Securities.CashAmount]:
        """
        Gets the current cash balance for each currency held in the brokerage account
        
        :returns: The current cash balance for each currency available for trading.
        """
        ...

    def GetGainLoss(self) -> System.Collections.Generic.List[QuantConnect.Brokerages.Tradier.TradierGainLoss]:
        """GainLoss of recent trades for this account:"""
        ...

    def GetHistoricalData(self, symbol: typing.Union[QuantConnect.Symbol, str], start: typing.Union[datetime.datetime, datetime.date], end: typing.Union[datetime.datetime, datetime.date], interval: QuantConnect.Brokerages.Tradier.TradierHistoricalDataIntervals = ...) -> System.Collections.Generic.List[QuantConnect.Brokerages.Tradier.TradierHistoryBar]:
        """Get full daily, weekly or monthly bars of historical periods:"""
        ...

    def GetHistory(self, requests: System.Collections.Generic.IEnumerable[QuantConnect.Data.HistoryRequest], sliceTimeZone: typing.Any) -> System.Collections.Generic.IEnumerable[QuantConnect.Data.Slice]:
        """
        Gets the history for the requested securities
        
        :param requests: The historical data requests
        :param sliceTimeZone: The time zone used when time stamping the slice instances
        :returns: An enumerable of the slices of data covering the span specified in each request.
        """
        ...

    @staticmethod
    def GetLimitPrice(order: QuantConnect.Orders.Order) -> float:
        """
        Gets the limit price used in API calls with tradier from the specified qc order instance
        
        This method is protected.
        """
        ...

    def GetMarketCalendar(self, month: int, year: int) -> System.Collections.Generic.List[QuantConnect.Brokerages.Tradier.TradierCalendarDay]:
        """Get the list of days status for this calendar month, year:"""
        ...

    def GetMarketStatus(self) -> QuantConnect.Brokerages.Tradier.TradierMarketStatus:
        """Get the current market status"""
        ...

    def GetOpenOrders(self) -> System.Collections.Generic.List[QuantConnect.Orders.Order]:
        """
        Gets all open orders on the account.
        NOTE: The order objects returned do not have QC order IDs.
        
        :returns: The open orders returned from IB.
        """
        ...

    def GetOrder(self, orderId: int) -> QuantConnect.Brokerages.Tradier.TradierOrderDetailed:
        """Get information about a specific order: accounts/{account_id}/orders/{id}"""
        ...

    @staticmethod
    def GetOrderDuration(timeInForce: QuantConnect.Orders.TimeInForce) -> int:
        """
        Converts the qc order duration into a tradier order duration
        
        This method is protected.
        
        :returns: This method returns the int value of a member of the QuantConnect.Brokerages.Tradier.TradierOrderDuration enum.
        """
        ...

    def GetPositions(self) -> System.Collections.Generic.List[QuantConnect.Brokerages.Tradier.TradierPosition]:
        """
        Get a list of the tradier positions for this account:
        
        :returns: Array of the symbols we hold.
        """
        ...

    def GetQuotes(self, symbols: System.Collections.Generic.List[str]) -> System.Collections.Generic.List[QuantConnect.Brokerages.Tradier.TradierQuote]:
        """List of quotes for symbols"""
        ...

    @staticmethod
    def GetStopPrice(order: QuantConnect.Orders.Order) -> float:
        """
        Gets the stop price used in API calls with tradier from the specified qc order instance
        
        This method is protected.
        """
        ...

    def GetTimeSeries(self, symbol: typing.Union[QuantConnect.Symbol, str], start: typing.Union[datetime.datetime, datetime.date], end: typing.Union[datetime.datetime, datetime.date], interval: QuantConnect.Brokerages.Tradier.TradierTimeSeriesIntervals) -> System.Collections.Generic.List[QuantConnect.Brokerages.Tradier.TradierTimeSeries]:
        """Get the historical bars for this period"""
        ...

    def GetUserProfile(self) -> QuantConnect.Brokerages.Tradier.TradierUser:
        """
        Using this auth token get the tradier user:
        
        :returns: Tradier user model:.
        """
        ...

    def Initialize(self, parameters: QuantConnect.Data.HistoryProviderInitializeParameters) -> None:
        """
        Initializes this history provider to work for the specified job
        
        :param parameters: The initialization parameters
        """
        ...

    @staticmethod
    def IsShort(direction: QuantConnect.Brokerages.Tradier.TradierOrderDirection) -> bool:
        """
        Returns true if the specified tradier order direction represents a short position
        
        This method is protected.
        """
        ...

    def LookUpSymbol(self, query: str, includeIndexes: bool = True) -> System.Collections.Generic.List[QuantConnect.Brokerages.Tradier.TradierSearchResult]:
        """Get the list of days status for this calendar month, year:"""
        ...

    def LookupSymbols(self, symbol: typing.Union[QuantConnect.Symbol, str], includeExpired: bool, securityCurrency: str = None) -> System.Collections.Generic.IEnumerable[QuantConnect.Symbol]:
        """
        Method returns a collection of Symbols that are available at the data source.
        
        :param symbol: Symbol to lookup
        :param includeExpired: Include expired contracts
        :param securityCurrency: Expected security currency(if any)
        :returns: Enumerable of Symbols, that are associated with the provided Symbol.
        """
        ...

    def OnDownloadFailed(self, e: QuantConnect.DownloadFailedEventArgs) -> None:
        """
        Event invocator for the DownloadFailed event
        
        This method is protected.
        
        :param e: Event arguments for the DownloadFailed event
        """
        ...

    def OnInvalidConfigurationDetected(self, e: QuantConnect.InvalidConfigurationDetectedEventArgs) -> None:
        """
        Event invocator for the InvalidConfigurationDetected event
        
        This method is protected.
        
        :param e: Event arguments for the InvalidConfigurationDetected event
        """
        ...

    @overload
    def OnMessage(self, e: QuantConnect.Brokerages.BrokerageMessageEvent) -> None:
        """
        Event invocator for the Message event
        
        This method is protected.
        
        :param e: The error
        """
        ...

    @overload
    def OnMessage(self, sender: typing.Any, webSocketMessage: QuantConnect.Brokerages.WebSocketMessage) -> None:
        """
        Handles websocket received messages
        
        This method is protected.
        """
        ...

    def OnNumericalPrecisionLimited(self, e: QuantConnect.NumericalPrecisionLimitedEventArgs) -> None:
        """
        Event invocator for the NumericalPrecisionLimited event
        
        This method is protected.
        
        :param e: Event arguments for the NumericalPrecisionLimited event
        """
        ...

    def OnReaderErrorDetected(self, e: QuantConnect.ReaderErrorDetectedEventArgs) -> None:
        """
        Event invocator for the ReaderErrorDetected event
        
        This method is protected.
        
        :param e: Event arguments for the ReaderErrorDetected event
        """
        ...

    def OrderCrossesZero(self, order: QuantConnect.Orders.Order) -> bool:
        """
        Determines whether or not the specified order will bring us across the zero line for holdings
        
        This method is protected.
        """
        ...

    @staticmethod
    def OrderIsClosed(order: QuantConnect.Brokerages.Tradier.TradierOrder) -> bool:
        """
        Returns true if the specified order is considered close, otherwise false
        
        This method is protected.
        """
        ...

    @staticmethod
    def OrderIsOpen(order: QuantConnect.Brokerages.Tradier.TradierOrder) -> bool:
        """This method is protected."""
        ...

    def PlaceOrder(self, order: QuantConnect.Orders.Order) -> bool:
        """
        Places a new order and assigns a new broker ID to the order
        
        :param order: The order to be placed
        :returns: True if the request for a new order has been placed, false otherwise.
        """
        ...

    def Search(self, query: str, includeIndexes: bool = True) -> System.Collections.Generic.List[QuantConnect.Brokerages.Tradier.TradierSearchResult]:
        """Get the list of days status for this calendar month, year:"""
        ...

    def SetJob(self, job: QuantConnect.Packets.LiveNodePacket) -> None:
        """
        Sets the job we're subscribing for
        
        :param job: Job we're subscribing for
        """
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
        """This method is protected."""
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


class TokenResponse(System.Object):
    """Token response model from QuantConnect terminal"""

    @property
    def AccessToken(self) -> str:
        ...

    @AccessToken.setter
    def AccessToken(self, value: str):
        ...

    @property
    def RefreshToken(self) -> str:
        ...

    @RefreshToken.setter
    def RefreshToken(self, value: str):
        ...

    @property
    def ExpiresIn(self) -> int:
        ...

    @ExpiresIn.setter
    def ExpiresIn(self, value: int):
        ...

    @property
    def Scope(self) -> str:
        ...

    @Scope.setter
    def Scope(self, value: str):
        ...

    @property
    def IssuedAt(self) -> datetime.datetime:
        ...

    @IssuedAt.setter
    def IssuedAt(self, value: datetime.datetime):
        ...

    @property
    def Success(self) -> bool:
        ...

    @Success.setter
    def Success(self, value: bool):
        ...

    def __init__(self) -> None:
        """Default constructor:"""
        ...


class TradierUserContainer(System.Object):
    """Model for a TradierUser returned from the API."""

    @property
    def Profile(self) -> QuantConnect.Brokerages.Tradier.TradierUser:
        ...

    @Profile.setter
    def Profile(self, value: QuantConnect.Brokerages.Tradier.TradierUser):
        ...

    def __init__(self) -> None:
        ...


class TradierApiRequestType(System.Enum):
    """Rate limiting categorization"""

    Standard = 0

    Data = 1

    Orders = 2


class TradierAccountStatus(System.Enum):
    """Account status flag."""

    New = 0

    Approved = 1

    Closed = 2


class TradierOptionExpirationType(System.Enum):
    """Tradier options expiration"""

    Standard = 0

    Weekly = 1


class TradierAccountClassification(System.Enum):
    """Account classification"""

    Individual = 0

    IRA = 1

    Roth_Ira = 2

    Joint = 3

    Entity = 4


class TradierGainLossClosed(System.Object):
    """Gain loss class"""

    @property
    def ClosedPositions(self) -> System.Collections.Generic.List[QuantConnect.Brokerages.Tradier.TradierGainLoss]:
        ...

    @ClosedPositions.setter
    def ClosedPositions(self, value: System.Collections.Generic.List[QuantConnect.Brokerages.Tradier.TradierGainLoss]):
        ...


class TradierGainLossContainer(System.Object):
    """Gain loss parent class for deserialization"""

    @property
    def GainLossClosed(self) -> QuantConnect.Brokerages.Tradier.TradierGainLossClosed:
        ...

    @GainLossClosed.setter
    def GainLossClosed(self, value: QuantConnect.Brokerages.Tradier.TradierGainLossClosed):
        ...

    def __init__(self) -> None:
        ...


class TradierSymbolMapper(System.Object, QuantConnect.Brokerages.ISymbolMapper):
    """Provides the mapping between Lean symbols and Tradier symbols."""

    def GetBrokerageSymbol(self, symbol: typing.Union[QuantConnect.Symbol, str]) -> str:
        """
        Converts a Lean symbol instance to a Tradier symbol
        
        :param symbol: A Lean symbol instance
        :returns: The Tradier symbol.
        """
        ...

    @overload
    def GetLeanSymbol(self, brokerageSymbol: str, securityType: QuantConnect.SecurityType, market: str, expirationDate: typing.Union[datetime.datetime, datetime.date] = ..., strike: float = 0, optionRight: QuantConnect.OptionRight = ...) -> QuantConnect.Symbol:
        """
        Converts a Tradier symbol to a Lean symbol instance
        
        :param brokerageSymbol: The Tradier symbol
        :param securityType: The security type
        :param market: The market
        :param expirationDate: Expiration date of the security(if applicable)
        :param strike: The strike of the security (if applicable)
        :param optionRight: The option right of the security (if applicable)
        :returns: A new Lean Symbol instance.
        """
        ...

    @overload
    def GetLeanSymbol(self, brokerageSymbol: str) -> QuantConnect.Symbol:
        """
        Converts a Tradier symbol to a Lean symbol instance
        
        :param brokerageSymbol: The Tradier symbol
        :returns: A new Lean Symbol instance.
        """
        ...


class TradierFaultDetail(System.Object):
    """Error code associated with this fault."""

    @property
    def ErrorCode(self) -> str:
        ...

    @ErrorCode.setter
    def ErrorCode(self, value: str):
        ...

    def __init__(self) -> None:
        ...


class TradierFault(System.Object):
    """
    Tradier fault object:
    {"fault":{"faultstring":"Access Token expired","detail":{"errorcode":"keymanagement.service.access_token_expired"}}}
    """

    @property
    def Description(self) -> str:
        ...

    @Description.setter
    def Description(self, value: str):
        ...

    @property
    def Details(self) -> QuantConnect.Brokerages.Tradier.TradierFaultDetail:
        ...

    @Details.setter
    def Details(self, value: QuantConnect.Brokerages.Tradier.TradierFaultDetail):
        ...

    def __init__(self) -> None:
        ...


class TradierFaultContainer(System.Object):
    """Wrapper container for fault:"""

    @property
    def Fault(self) -> QuantConnect.Brokerages.Tradier.TradierFault:
        ...

    @Fault.setter
    def Fault(self, value: QuantConnect.Brokerages.Tradier.TradierFault):
        ...

    def __init__(self) -> None:
        ...


class TradierOrders(System.Object):
    """Order container class"""

    @property
    def Orders(self) -> System.Collections.Generic.List[QuantConnect.Brokerages.Tradier.TradierOrder]:
        ...

    @Orders.setter
    def Orders(self, value: System.Collections.Generic.List[QuantConnect.Brokerages.Tradier.TradierOrder]):
        ...

    def __init__(self) -> None:
        ...


class TradierOrdersContainer(System.Object):
    """Order parent class for deserialization"""

    @property
    def Orders(self) -> QuantConnect.Brokerages.Tradier.TradierOrders:
        ...

    @Orders.setter
    def Orders(self, value: QuantConnect.Brokerages.Tradier.TradierOrders):
        ...

    def __init__(self) -> None:
        ...


class TradierOrderDetailedContainer(System.Object):
    """Detailed order parent class"""

    @property
    def DetailedOrder(self) -> QuantConnect.Brokerages.Tradier.TradierOrderDetailed:
        ...

    @DetailedOrder.setter
    def DetailedOrder(self, value: QuantConnect.Brokerages.Tradier.TradierOrderDetailed):
        ...


class _EventContainer(typing.Generic[QuantConnect_Brokerages_Tradier__EventContainer_Callable, QuantConnect_Brokerages_Tradier__EventContainer_ReturnType]):
    """This class is used to provide accurate autocomplete on events and cannot be imported."""

    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> QuantConnect_Brokerages_Tradier__EventContainer_ReturnType:
        """Fires the event."""
        ...

    def __iadd__(self, item: QuantConnect_Brokerages_Tradier__EventContainer_Callable) -> None:
        """Registers an event handler."""
        ...

    def __isub__(self, item: QuantConnect_Brokerages_Tradier__EventContainer_Callable) -> None:
        """Unregisters an event handler."""
        ...


