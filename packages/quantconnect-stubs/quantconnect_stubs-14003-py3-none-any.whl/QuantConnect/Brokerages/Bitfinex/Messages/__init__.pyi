from typing import overload
import typing

import QuantConnect.Brokerages.Bitfinex.Messages
import System


class Wallet(System.Object):
    """Account wallet balance"""

    @property
    def Type(self) -> str:
        """Wallet name (exchange, margin, funding)"""
        ...

    @Type.setter
    def Type(self, value: str):
        """Wallet name (exchange, margin, funding)"""
        ...

    @property
    def Currency(self) -> str:
        """Currency (e.g. USD, ...)"""
        ...

    @Currency.setter
    def Currency(self, value: str):
        """Currency (e.g. USD, ...)"""
        ...

    @property
    def Balance(self) -> float:
        """Wallet balance"""
        ...

    @Balance.setter
    def Balance(self, value: float):
        """Wallet balance"""
        ...

    @property
    def UnsettledInterest(self) -> float:
        """Unsettled interest"""
        ...

    @UnsettledInterest.setter
    def UnsettledInterest(self, value: float):
        """Unsettled interest"""
        ...


class TradeExecutionUpdate(System.Object):
    """Trade execution event on the account."""

    @property
    def TradeId(self) -> int:
        """Trade database id"""
        ...

    @TradeId.setter
    def TradeId(self, value: int):
        """Trade database id"""
        ...

    @property
    def Symbol(self) -> str:
        """Symbol (tBTCUSD, …)"""
        ...

    @Symbol.setter
    def Symbol(self, value: str):
        """Symbol (tBTCUSD, …)"""
        ...

    @property
    def MtsCreate(self) -> int:
        """Execution timestamp"""
        ...

    @MtsCreate.setter
    def MtsCreate(self, value: int):
        """Execution timestamp"""
        ...

    @property
    def OrderId(self) -> int:
        """Order id"""
        ...

    @OrderId.setter
    def OrderId(self, value: int):
        """Order id"""
        ...

    @property
    def ExecAmount(self) -> float:
        """Positive means buy, negative means sell"""
        ...

    @ExecAmount.setter
    def ExecAmount(self, value: float):
        """Positive means buy, negative means sell"""
        ...

    @property
    def ExecPrice(self) -> float:
        """Execution price"""
        ...

    @ExecPrice.setter
    def ExecPrice(self, value: float):
        """Execution price"""
        ...

    @property
    def OrderType(self) -> str:
        """Order type"""
        ...

    @OrderType.setter
    def OrderType(self, value: str):
        """Order type"""
        ...

    @property
    def OrderPrice(self) -> float:
        """Order price"""
        ...

    @OrderPrice.setter
    def OrderPrice(self, value: float):
        """Order price"""
        ...

    @property
    def Maker(self) -> int:
        """1 if true, -1 if false"""
        ...

    @Maker.setter
    def Maker(self, value: int):
        """1 if true, -1 if false"""
        ...

    @property
    def Fee(self) -> float:
        """Fee ('tu' only)"""
        ...

    @Fee.setter
    def Fee(self, value: float):
        """Fee ('tu' only)"""
        ...

    @property
    def FeeCurrency(self) -> str:
        """Fee currency ('tu' only)"""
        ...

    @FeeCurrency.setter
    def FeeCurrency(self, value: str):
        """Fee currency ('tu' only)"""
        ...


class Ticker(System.Object):
    """A high level overview of the state of the market for a specified pair"""

    @property
    def Bid(self) -> float:
        """Price of last highest bid"""
        ...

    @Bid.setter
    def Bid(self, value: float):
        """Price of last highest bid"""
        ...

    @property
    def BidSize(self) -> float:
        """Sum of the 25 highest bid sizes"""
        ...

    @BidSize.setter
    def BidSize(self, value: float):
        """Sum of the 25 highest bid sizes"""
        ...

    @property
    def Ask(self) -> float:
        """Price of last lowest ask"""
        ...

    @Ask.setter
    def Ask(self, value: float):
        """Price of last lowest ask"""
        ...

    @property
    def AskSize(self) -> float:
        """Sum of the 25 lowest ask sizes"""
        ...

    @AskSize.setter
    def AskSize(self, value: float):
        """Sum of the 25 lowest ask sizes"""
        ...

    @property
    def DailyChange(self) -> float:
        """Amount that the last price has changed since yesterday"""
        ...

    @DailyChange.setter
    def DailyChange(self, value: float):
        """Amount that the last price has changed since yesterday"""
        ...

    @property
    def DailyChangeRelative(self) -> float:
        """Relative price change since yesterday (*100 for percentage change)"""
        ...

    @DailyChangeRelative.setter
    def DailyChangeRelative(self, value: float):
        """Relative price change since yesterday (*100 for percentage change)"""
        ...

    @property
    def LastPrice(self) -> float:
        """Price of the last trade"""
        ...

    @LastPrice.setter
    def LastPrice(self, value: float):
        """Price of the last trade"""
        ...

    @property
    def Volume(self) -> float:
        """Daily volume"""
        ...

    @Volume.setter
    def Volume(self, value: float):
        """Daily volume"""
        ...

    @property
    def High(self) -> float:
        """Daily high"""
        ...

    @High.setter
    def High(self, value: float):
        """Daily high"""
        ...

    @property
    def Low(self) -> float:
        """Daily low"""
        ...

    @Low.setter
    def Low(self, value: float):
        """Daily low"""
        ...


class Order(System.Object):
    """Bitfinex Order"""

    @property
    def Id(self) -> int:
        """Order ID"""
        ...

    @Id.setter
    def Id(self, value: int):
        """Order ID"""
        ...

    @property
    def GroupId(self) -> int:
        """Group ID"""
        ...

    @GroupId.setter
    def GroupId(self, value: int):
        """Group ID"""
        ...

    @property
    def ClientOrderId(self) -> int:
        """Client Order ID"""
        ...

    @ClientOrderId.setter
    def ClientOrderId(self, value: int):
        """Client Order ID"""
        ...

    @property
    def Symbol(self) -> str:
        """Pair (tBTCUSD, …)"""
        ...

    @Symbol.setter
    def Symbol(self, value: str):
        """Pair (tBTCUSD, …)"""
        ...

    @property
    def MtsCreate(self) -> int:
        """Millisecond timestamp of creation"""
        ...

    @MtsCreate.setter
    def MtsCreate(self, value: int):
        """Millisecond timestamp of creation"""
        ...

    @property
    def MtsUpdate(self) -> int:
        """Millisecond timestamp of update"""
        ...

    @MtsUpdate.setter
    def MtsUpdate(self, value: int):
        """Millisecond timestamp of update"""
        ...

    @property
    def Amount(self) -> float:
        """Positive means buy, negative means sell."""
        ...

    @Amount.setter
    def Amount(self, value: float):
        """Positive means buy, negative means sell."""
        ...

    @property
    def AmountOrig(self) -> float:
        """Original amount"""
        ...

    @AmountOrig.setter
    def AmountOrig(self, value: float):
        """Original amount"""
        ...

    @property
    def Type(self) -> str:
        """
        The type of the order:
        - LIMIT, MARKET, STOP, STOP LIMIT, TRAILING STOP,
        - EXCHANGE MARKET, EXCHANGE LIMIT, EXCHANGE STOP, EXCHANGE STOP LIMIT,
        - EXCHANGE TRAILING STOP, FOK, EXCHANGE FOK, IOC, EXCHANGE IOC.
        """
        ...

    @Type.setter
    def Type(self, value: str):
        """
        The type of the order:
        - LIMIT, MARKET, STOP, STOP LIMIT, TRAILING STOP,
        - EXCHANGE MARKET, EXCHANGE LIMIT, EXCHANGE STOP, EXCHANGE STOP LIMIT,
        - EXCHANGE TRAILING STOP, FOK, EXCHANGE FOK, IOC, EXCHANGE IOC.
        """
        ...

    @property
    def TypePrev(self) -> str:
        """Previous order type"""
        ...

    @TypePrev.setter
    def TypePrev(self, value: str):
        """Previous order type"""
        ...

    @property
    def Flags(self) -> int:
        """Active flags for order"""
        ...

    @Flags.setter
    def Flags(self, value: int):
        """Active flags for order"""
        ...

    @property
    def Status(self) -> str:
        """
        Order Status:
        - ACTIVE,
        - EXECUTED @ PRICE(AMOUNT) e.g. "EXECUTED @ 107.6(-0.2)",
        - PARTIALLY FILLED @ PRICE(AMOUNT),
        - INSUFFICIENT MARGIN was: PARTIALLY FILLED @ PRICE(AMOUNT),
        - CANCELED,
        - CANCELED was: PARTIALLY FILLED @ PRICE(AMOUNT),
        - RSN_DUST (amount is less than 0.00000001),
        - RSN_PAUSE (trading is paused / paused due to AMPL rebase event)
        """
        ...

    @Status.setter
    def Status(self, value: str):
        """
        Order Status:
        - ACTIVE,
        - EXECUTED @ PRICE(AMOUNT) e.g. "EXECUTED @ 107.6(-0.2)",
        - PARTIALLY FILLED @ PRICE(AMOUNT),
        - INSUFFICIENT MARGIN was: PARTIALLY FILLED @ PRICE(AMOUNT),
        - CANCELED,
        - CANCELED was: PARTIALLY FILLED @ PRICE(AMOUNT),
        - RSN_DUST (amount is less than 0.00000001),
        - RSN_PAUSE (trading is paused / paused due to AMPL rebase event)
        """
        ...

    @property
    def Price(self) -> float:
        """Price"""
        ...

    @Price.setter
    def Price(self, value: float):
        """Price"""
        ...

    @property
    def PriceAvg(self) -> float:
        """Average price"""
        ...

    @PriceAvg.setter
    def PriceAvg(self, value: float):
        """Average price"""
        ...

    @property
    def PriceTrailing(self) -> float:
        """The trailing price"""
        ...

    @PriceTrailing.setter
    def PriceTrailing(self, value: float):
        """The trailing price"""
        ...

    @property
    def PriceAuxLimit(self) -> float:
        """Auxiliary Limit price (for STOP LIMIT)"""
        ...

    @PriceAuxLimit.setter
    def PriceAuxLimit(self, value: float):
        """Auxiliary Limit price (for STOP LIMIT)"""
        ...

    @property
    def Hidden(self) -> int:
        """1 if Hidden, 0 if not hidden"""
        ...

    @Hidden.setter
    def Hidden(self, value: int):
        """1 if Hidden, 0 if not hidden"""
        ...

    @property
    def PlacedId(self) -> int:
        """If another order caused this order to be placed (OCO) this will be that other order's ID"""
        ...

    @PlacedId.setter
    def PlacedId(self, value: int):
        """If another order caused this order to be placed (OCO) this will be that other order's ID"""
        ...

    @property
    def IsExchange(self) -> bool:
        """If this is exchange order"""
        ...


class Position(System.Object):
    """Bitfinex position"""

    @property
    def Symbol(self) -> str:
        """Pair (tBTCUSD, …)."""
        ...

    @Symbol.setter
    def Symbol(self, value: str):
        """Pair (tBTCUSD, …)."""
        ...

    @property
    def Status(self) -> str:
        """Status (ACTIVE, CLOSED)."""
        ...

    @Status.setter
    def Status(self, value: str):
        """Status (ACTIVE, CLOSED)."""
        ...

    @property
    def Amount(self) -> float:
        """Size of the position. A positive value indicates a long position; a negative value indicates a short position."""
        ...

    @Amount.setter
    def Amount(self, value: float):
        """Size of the position. A positive value indicates a long position; a negative value indicates a short position."""
        ...

    @property
    def BasePrice(self) -> float:
        """Base price of the position. (Average traded price of the previous orders of the position)"""
        ...

    @BasePrice.setter
    def BasePrice(self, value: float):
        """Base price of the position. (Average traded price of the previous orders of the position)"""
        ...

    @property
    def MarginFunding(self) -> float:
        """The amount of funding being used for this position."""
        ...

    @MarginFunding.setter
    def MarginFunding(self, value: float):
        """The amount of funding being used for this position."""
        ...

    @property
    def MarginFundingType(self) -> int:
        """0 for daily, 1 for term."""
        ...

    @MarginFundingType.setter
    def MarginFundingType(self, value: int):
        """0 for daily, 1 for term."""
        ...

    @property
    def ProfitLoss(self) -> float:
        """Profit & Loss"""
        ...

    @ProfitLoss.setter
    def ProfitLoss(self, value: float):
        """Profit & Loss"""
        ...

    @property
    def ProfitLossPerc(self) -> float:
        """Profit & Loss Percentage"""
        ...

    @ProfitLossPerc.setter
    def ProfitLossPerc(self, value: float):
        """Profit & Loss Percentage"""
        ...

    @property
    def PriceLiq(self) -> float:
        """Liquidation price"""
        ...

    @PriceLiq.setter
    def PriceLiq(self, value: float):
        """Liquidation price"""
        ...

    @property
    def Leverage(self) -> float:
        """Leverage used for the position"""
        ...

    @Leverage.setter
    def Leverage(self, value: float):
        """Leverage used for the position"""
        ...

    @property
    def PositionId(self) -> int:
        """Position ID"""
        ...

    @PositionId.setter
    def PositionId(self, value: int):
        """Position ID"""
        ...

    @property
    def MtsCreate(self) -> int:
        """Millisecond timestamp of creation"""
        ...

    @MtsCreate.setter
    def MtsCreate(self, value: int):
        """Millisecond timestamp of creation"""
        ...

    @property
    def MtsUpdate(self) -> int:
        """Millisecond timestamp of update"""
        ...

    @MtsUpdate.setter
    def MtsUpdate(self, value: int):
        """Millisecond timestamp of update"""
        ...

    @property
    def Type(self) -> int:
        """Identifies the type of position, 0 = Margin position, 1 = Derivatives position"""
        ...

    @Type.setter
    def Type(self, value: int):
        """Identifies the type of position, 0 = Margin position, 1 = Derivatives position"""
        ...

    @property
    def Collateral(self) -> float:
        """The amount of collateral applied to the open position"""
        ...

    @Collateral.setter
    def Collateral(self, value: float):
        """The amount of collateral applied to the open position"""
        ...

    @property
    def CollateralMin(self) -> float:
        """The minimum amount of collateral required for the position"""
        ...

    @CollateralMin.setter
    def CollateralMin(self, value: float):
        """The minimum amount of collateral required for the position"""
        ...

    @property
    def Meta(self) -> System.Object:
        """Additional meta information about the position (JSON string)"""
        ...

    @Meta.setter
    def Meta(self, value: System.Object):
        """Additional meta information about the position (JSON string)"""
        ...


class BaseMessage(System.Object):
    """This class has no documentation."""

    @property
    def Event(self) -> str:
        ...

    @Event.setter
    def Event(self, value: str):
        ...


class ErrorMessage(QuantConnect.Brokerages.Bitfinex.Messages.BaseMessage):
    """This class has no documentation."""

    @property
    def Message(self) -> str:
        ...

    @Message.setter
    def Message(self, value: str):
        ...

    @property
    def Code(self) -> int:
        ...

    @Code.setter
    def Code(self, value: int):
        ...

    @property
    def Level(self) -> str:
        """10301 : Already subscribed"""
        ...


class ChannelSubscription(QuantConnect.Brokerages.Bitfinex.Messages.BaseMessage):
    """This class has no documentation."""

    @property
    def Channel(self) -> str:
        ...

    @Channel.setter
    def Channel(self, value: str):
        ...

    @property
    def ChannelId(self) -> int:
        ...

    @ChannelId.setter
    def ChannelId(self, value: int):
        ...

    @property
    def Symbol(self) -> str:
        ...

    @Symbol.setter
    def Symbol(self, value: str):
        ...


class ChannelUnsubscribing(QuantConnect.Brokerages.Bitfinex.Messages.BaseMessage):
    """This class has no documentation."""

    @property
    def Status(self) -> str:
        ...

    @Status.setter
    def Status(self, value: str):
        ...

    @property
    def ChannelId(self) -> int:
        ...

    @ChannelId.setter
    def ChannelId(self, value: int):
        ...


class AuthResponseMessage(QuantConnect.Brokerages.Bitfinex.Messages.BaseMessage):
    """This class has no documentation."""

    @property
    def Status(self) -> str:
        ...

    @Status.setter
    def Status(self, value: str):
        ...


class Candle(System.Object):
    """This class has no documentation."""

    @property
    def Timestamp(self) -> int:
        ...

    @Timestamp.setter
    def Timestamp(self, value: int):
        ...

    @property
    def Open(self) -> float:
        ...

    @Open.setter
    def Open(self, value: float):
        ...

    @property
    def Close(self) -> float:
        ...

    @Close.setter
    def Close(self, value: float):
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
    def Volume(self) -> float:
        ...

    @Volume.setter
    def Volume(self, value: float):
        ...

    @overload
    def __init__(self) -> None:
        ...

    @overload
    def __init__(self, msts: int, close: float) -> None:
        ...

    @overload
    def __init__(self, entries: typing.List[System.Object]) -> None:
        ...


class OrderFlags(System.Object):
    """Bitfinex Order Flags"""

    Hidden: int = 64
    """The hidden order option ensures an order does not appear in the order book; thus does not influence other market participants."""

    Close: int = 512
    """Close position if position present."""

    ReduceOnly: int = 1024
    """Ensures that the executed order does not flip the opened position."""

    PostOnly: int = 4096
    """The post-only limit order option ensures the limit order will be added to the order book and not match with a pre-existing order."""

    Oco: int = 16384
    """
    The one cancels other order option allows you to place a pair of orders stipulating that if one order is executed fully or partially,
    then the other is automatically canceled.
    """

    NoVarRates: int = 524288
    """Excludes variable rate funding offers from matching against this order, if on margin"""


