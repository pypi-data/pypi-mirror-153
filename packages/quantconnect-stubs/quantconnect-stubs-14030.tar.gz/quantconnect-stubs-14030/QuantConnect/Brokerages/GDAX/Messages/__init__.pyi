from typing import overload
import datetime
import typing

import QuantConnect.Brokerages.GDAX.Messages
import System
import System.Collections.Generic


class BaseMessage(System.Object):
    """This class has no documentation."""

    @property
    def Type(self) -> str:
        ...

    @Type.setter
    def Type(self, value: str):
        ...

    @property
    def Sequence(self) -> int:
        ...

    @Sequence.setter
    def Sequence(self, value: int):
        ...

    @property
    def Time(self) -> datetime.datetime:
        ...

    @Time.setter
    def Time(self, value: datetime.datetime):
        ...

    @property
    def ProductId(self) -> str:
        ...

    @ProductId.setter
    def ProductId(self, value: str):
        ...


class Done(QuantConnect.Brokerages.GDAX.Messages.BaseMessage):
    """This class has no documentation."""

    @property
    def Price(self) -> float:
        ...

    @Price.setter
    def Price(self, value: float):
        ...

    @property
    def OrderId(self) -> str:
        ...

    @OrderId.setter
    def OrderId(self, value: str):
        ...

    @property
    def Reason(self) -> str:
        ...

    @Reason.setter
    def Reason(self, value: str):
        ...

    @property
    def Side(self) -> str:
        ...

    @Side.setter
    def Side(self, value: str):
        ...

    @property
    def RemainingSize(self) -> float:
        ...

    @RemainingSize.setter
    def RemainingSize(self, value: float):
        ...


class Matched(QuantConnect.Brokerages.GDAX.Messages.BaseMessage):
    """This class has no documentation."""

    @property
    def TradeId(self) -> int:
        ...

    @TradeId.setter
    def TradeId(self, value: int):
        ...

    @property
    def MakerOrderId(self) -> str:
        ...

    @MakerOrderId.setter
    def MakerOrderId(self, value: str):
        ...

    @property
    def TakerOrderId(self) -> str:
        ...

    @TakerOrderId.setter
    def TakerOrderId(self, value: str):
        ...

    @property
    def Size(self) -> float:
        ...

    @Size.setter
    def Size(self, value: float):
        ...

    @property
    def Price(self) -> float:
        ...

    @Price.setter
    def Price(self, value: float):
        ...

    @property
    def Side(self) -> str:
        ...

    @Side.setter
    def Side(self, value: str):
        ...

    @property
    def TakerUserId(self) -> str:
        ...

    @TakerUserId.setter
    def TakerUserId(self, value: str):
        ...

    @property
    def UserId(self) -> str:
        ...

    @UserId.setter
    def UserId(self, value: str):
        ...

    @property
    def TakerProfileId(self) -> str:
        ...

    @TakerProfileId.setter
    def TakerProfileId(self, value: str):
        ...

    @property
    def ProfileId(self) -> str:
        ...

    @ProfileId.setter
    def ProfileId(self, value: str):
        ...


class Heartbeat(QuantConnect.Brokerages.GDAX.Messages.BaseMessage):
    """This class has no documentation."""

    @property
    def LastTradeId(self) -> int:
        ...

    @LastTradeId.setter
    def LastTradeId(self, value: int):
        ...


class Error(QuantConnect.Brokerages.GDAX.Messages.BaseMessage):
    """This class has no documentation."""

    @property
    def Message(self) -> str:
        ...

    @Message.setter
    def Message(self, value: str):
        ...

    @property
    def Reason(self) -> str:
        ...

    @Reason.setter
    def Reason(self, value: str):
        ...


class Subscribe(System.Object):
    """This class has no documentation."""

    @property
    def Type(self) -> str:
        ...

    @Type.setter
    def Type(self, value: str):
        ...

    @property
    def ProductIds(self) -> System.Collections.Generic.IList[str]:
        ...

    @ProductIds.setter
    def ProductIds(self, value: System.Collections.Generic.IList[str]):
        ...

    @property
    def Signature(self) -> str:
        ...

    @Signature.setter
    def Signature(self, value: str):
        ...

    @property
    def Key(self) -> str:
        ...

    @Key.setter
    def Key(self, value: str):
        ...

    @property
    def Passphrase(self) -> str:
        ...

    @Passphrase.setter
    def Passphrase(self, value: str):
        ...

    @property
    def Timestamp(self) -> str:
        ...

    @Timestamp.setter
    def Timestamp(self, value: str):
        ...


class Open(QuantConnect.Brokerages.GDAX.Messages.BaseMessage):
    """This class has no documentation."""

    @property
    def OrderId(self) -> str:
        ...

    @OrderId.setter
    def OrderId(self, value: str):
        ...

    @property
    def Price(self) -> float:
        ...

    @Price.setter
    def Price(self, value: float):
        ...

    @property
    def RemainingSize(self) -> float:
        ...

    @RemainingSize.setter
    def RemainingSize(self, value: float):
        ...

    @property
    def Side(self) -> str:
        ...

    @Side.setter
    def Side(self, value: str):
        ...


class Change(QuantConnect.Brokerages.GDAX.Messages.Open):
    """This class has no documentation."""

    @property
    def NewFunds(self) -> float:
        ...

    @NewFunds.setter
    def NewFunds(self, value: float):
        ...

    @property
    def OldFunds(self) -> float:
        ...

    @OldFunds.setter
    def OldFunds(self, value: float):
        ...


class Order(System.Object):
    """This class has no documentation."""

    @property
    def Id(self) -> str:
        ...

    @Id.setter
    def Id(self, value: str):
        ...

    @property
    def Price(self) -> float:
        ...

    @Price.setter
    def Price(self, value: float):
        ...

    @property
    def Size(self) -> float:
        ...

    @Size.setter
    def Size(self, value: float):
        ...

    @property
    def ProductId(self) -> str:
        ...

    @ProductId.setter
    def ProductId(self, value: str):
        ...

    @property
    def Side(self) -> str:
        ...

    @Side.setter
    def Side(self, value: str):
        ...

    @property
    def Stp(self) -> str:
        ...

    @Stp.setter
    def Stp(self, value: str):
        ...

    @property
    def Type(self) -> str:
        ...

    @Type.setter
    def Type(self, value: str):
        ...

    @property
    def TimeInForce(self) -> str:
        ...

    @TimeInForce.setter
    def TimeInForce(self, value: str):
        ...

    @property
    def PostOnly(self) -> bool:
        ...

    @PostOnly.setter
    def PostOnly(self, value: bool):
        ...

    @property
    def RejectReason(self) -> str:
        ...

    @RejectReason.setter
    def RejectReason(self, value: str):
        ...

    @property
    def FillFees(self) -> float:
        ...

    @FillFees.setter
    def FillFees(self, value: float):
        ...

    @property
    def FilledSize(self) -> float:
        ...

    @FilledSize.setter
    def FilledSize(self, value: float):
        ...

    @property
    def ExecutedValue(self) -> float:
        ...

    @ExecutedValue.setter
    def ExecutedValue(self, value: float):
        ...

    @property
    def Status(self) -> str:
        ...

    @Status.setter
    def Status(self, value: str):
        ...

    @property
    def Settled(self) -> bool:
        ...

    @Settled.setter
    def Settled(self, value: bool):
        ...

    @property
    def Stop(self) -> str:
        ...

    @Stop.setter
    def Stop(self, value: str):
        ...

    @property
    def StopPrice(self) -> float:
        ...

    @StopPrice.setter
    def StopPrice(self, value: float):
        ...


class Fill(System.Object):
    """This class has no documentation."""

    @property
    def CreatedAt(self) -> datetime.datetime:
        ...

    @CreatedAt.setter
    def CreatedAt(self, value: datetime.datetime):
        ...

    @property
    def TradeId(self) -> int:
        ...

    @TradeId.setter
    def TradeId(self, value: int):
        ...

    @property
    def ProductId(self) -> str:
        ...

    @ProductId.setter
    def ProductId(self, value: str):
        ...

    @property
    def OrderId(self) -> str:
        ...

    @OrderId.setter
    def OrderId(self, value: str):
        ...

    @property
    def UserId(self) -> str:
        ...

    @UserId.setter
    def UserId(self, value: str):
        ...

    @property
    def ProfileId(self) -> str:
        ...

    @ProfileId.setter
    def ProfileId(self, value: str):
        ...

    @property
    def Liquidity(self) -> str:
        ...

    @Liquidity.setter
    def Liquidity(self, value: str):
        ...

    @property
    def Price(self) -> float:
        ...

    @Price.setter
    def Price(self, value: float):
        ...

    @property
    def Size(self) -> float:
        ...

    @Size.setter
    def Size(self, value: float):
        ...

    @property
    def Fee(self) -> float:
        ...

    @Fee.setter
    def Fee(self, value: float):
        ...

    @property
    def Side(self) -> str:
        ...

    @Side.setter
    def Side(self, value: str):
        ...

    @property
    def Settled(self) -> bool:
        ...

    @Settled.setter
    def Settled(self, value: bool):
        ...

    @property
    def UsdVolume(self) -> float:
        ...

    @UsdVolume.setter
    def UsdVolume(self, value: float):
        ...


class Account(System.Object):
    """This class has no documentation."""

    @property
    def Id(self) -> str:
        ...

    @Id.setter
    def Id(self, value: str):
        ...

    @property
    def Currency(self) -> str:
        ...

    @Currency.setter
    def Currency(self, value: str):
        ...

    @property
    def Balance(self) -> float:
        ...

    @Balance.setter
    def Balance(self, value: float):
        ...

    @property
    def Hold(self) -> float:
        ...

    @Hold.setter
    def Hold(self, value: float):
        ...

    @property
    def Available(self) -> float:
        ...

    @Available.setter
    def Available(self, value: float):
        ...

    @property
    def ProfileId(self) -> str:
        ...

    @ProfileId.setter
    def ProfileId(self, value: str):
        ...


class Tick(System.Object):
    """This class has no documentation."""

    @property
    def ProductId(self) -> str:
        ...

    @ProductId.setter
    def ProductId(self, value: str):
        ...

    @property
    def TradeId(self) -> str:
        ...

    @TradeId.setter
    def TradeId(self, value: str):
        ...

    @property
    def Price(self) -> float:
        ...

    @Price.setter
    def Price(self, value: float):
        ...

    @property
    def Size(self) -> float:
        ...

    @Size.setter
    def Size(self, value: float):
        ...

    @property
    def Bid(self) -> float:
        ...

    @Bid.setter
    def Bid(self, value: float):
        ...

    @property
    def Ask(self) -> float:
        ...

    @Ask.setter
    def Ask(self, value: float):
        ...

    @property
    def Volume(self) -> float:
        ...

    @Volume.setter
    def Volume(self, value: float):
        ...

    @property
    def Time(self) -> datetime.datetime:
        ...

    @Time.setter
    def Time(self, value: datetime.datetime):
        ...


class Ticker(QuantConnect.Brokerages.GDAX.Messages.BaseMessage):
    """This class has no documentation."""

    @property
    def TradeId(self) -> str:
        ...

    @TradeId.setter
    def TradeId(self, value: str):
        ...

    @property
    def LastSize(self) -> float:
        ...

    @LastSize.setter
    def LastSize(self, value: float):
        ...

    @property
    def BestBid(self) -> float:
        ...

    @BestBid.setter
    def BestBid(self, value: float):
        ...

    @property
    def BestAsk(self) -> float:
        ...

    @BestAsk.setter
    def BestAsk(self, value: float):
        ...

    @property
    def Price(self) -> float:
        ...

    @Price.setter
    def Price(self, value: float):
        ...

    @property
    def Side(self) -> str:
        ...

    @Side.setter
    def Side(self, value: str):
        ...


class Snapshot(QuantConnect.Brokerages.GDAX.Messages.BaseMessage):
    """This class has no documentation."""

    @property
    def Bids(self) -> System.Collections.Generic.List[typing.List[str]]:
        ...

    @Bids.setter
    def Bids(self, value: System.Collections.Generic.List[typing.List[str]]):
        ...

    @property
    def Asks(self) -> System.Collections.Generic.List[typing.List[str]]:
        ...

    @Asks.setter
    def Asks(self, value: System.Collections.Generic.List[typing.List[str]]):
        ...


class L2Update(QuantConnect.Brokerages.GDAX.Messages.BaseMessage):
    """This class has no documentation."""

    @property
    def Changes(self) -> System.Collections.Generic.List[typing.List[str]]:
        ...

    @Changes.setter
    def Changes(self, value: System.Collections.Generic.List[typing.List[str]]):
        ...


