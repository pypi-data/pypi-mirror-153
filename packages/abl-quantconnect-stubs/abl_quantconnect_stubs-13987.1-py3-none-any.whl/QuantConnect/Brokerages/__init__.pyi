from typing import overload
import abc
import datetime
import typing

import QuantConnect
import QuantConnect.Benchmarks
import QuantConnect.Brokerages
import QuantConnect.Data.Market
import QuantConnect.Interfaces
import QuantConnect.Orders
import QuantConnect.Orders.Fees
import QuantConnect.Orders.Fills
import QuantConnect.Orders.Slippage
import QuantConnect.Packets
import QuantConnect.Securities
import System
import System.Collections.Generic


class BrokerageMessageType(System.Enum):
    """Specifies the type of message received from an IBrokerage implementation"""

    Information = 0
    """Informational message"""

    Warning = 1
    """Warning message"""

    Error = 2
    """Fatal error message, the algo will be stopped"""

    Reconnect = 3
    """Brokerage reconnected with remote server"""

    Disconnect = 4
    """Brokerage disconnected from remote server"""


class BrokerageMessageEvent(System.Object):
    """Represents a message received from a brokerage"""

    @property
    def Type(self) -> int:
        """
        Gets the type of brokerage message
        
        This property contains the int value of a member of the QuantConnect.Brokerages.BrokerageMessageType enum.
        """
        ...

    @Type.setter
    def Type(self, value: int):
        """
        Gets the type of brokerage message
        
        This property contains the int value of a member of the QuantConnect.Brokerages.BrokerageMessageType enum.
        """
        ...

    @property
    def Code(self) -> str:
        """Gets the brokerage specific code for this message, zero if no code was specified"""
        ...

    @Code.setter
    def Code(self, value: str):
        """Gets the brokerage specific code for this message, zero if no code was specified"""
        ...

    @property
    def Message(self) -> str:
        """Gets the message text received from the brokerage"""
        ...

    @Message.setter
    def Message(self, value: str):
        """Gets the message text received from the brokerage"""
        ...

    @overload
    def __init__(self, type: QuantConnect.Brokerages.BrokerageMessageType, code: int, message: str) -> None:
        """
        Initializes a new instance of the BrokerageMessageEvent class
        
        :param type: The type of brokerage message
        :param code: The brokerage specific code
        :param message: The message text received from the brokerage
        """
        ...

    @overload
    def __init__(self, type: QuantConnect.Brokerages.BrokerageMessageType, code: str, message: str) -> None:
        """
        Initializes a new instance of the BrokerageMessageEvent class
        
        :param type: The type of brokerage message
        :param code: The brokerage specific code
        :param message: The message text received from the brokerage
        """
        ...

    @staticmethod
    def Disconnected(message: str) -> QuantConnect.Brokerages.BrokerageMessageEvent:
        """
        Creates a new BrokerageMessageEvent to represent a disconnect message
        
        :param message: The message from the brokerage
        :returns: A brokerage disconnect message.
        """
        ...

    @staticmethod
    def Reconnected(message: str) -> QuantConnect.Brokerages.BrokerageMessageEvent:
        """
        Creates a new BrokerageMessageEvent to represent a reconnect message
        
        :param message: The message from the brokerage
        :returns: A brokerage reconnect message.
        """
        ...

    def ToString(self) -> str:
        """
        Returns a string that represents the current object.
        
        :returns: A string that represents the current object.
        """
        ...


class IBrokerageModel(metaclass=abc.ABCMeta):
    """Models brokerage transactions, fees, and order"""

    @property
    @abc.abstractmethod
    def AccountType(self) -> int:
        """
        Gets the account type used by this model
        
        This property contains the int value of a member of the QuantConnect.AccountType enum.
        """
        ...

    @property
    @abc.abstractmethod
    def RequiredFreeBuyingPowerPercent(self) -> float:
        """
        Gets the brokerages model percentage factor used to determine the required unused buying power for the account.
        From 1 to 0. Example: 0 means no unused buying power is required. 0.5 means 50% of the buying power should be left unused.
        """
        ...

    @property
    @abc.abstractmethod
    def DefaultMarkets(self) -> System.Collections.Generic.IReadOnlyDictionary[QuantConnect.SecurityType, str]:
        """Gets a map of the default markets to be used for each security type"""
        ...

    def ApplySplit(self, tickets: System.Collections.Generic.List[QuantConnect.Orders.OrderTicket], split: QuantConnect.Data.Market.Split) -> None:
        """
        Applies the split to the specified order ticket
        
        :param tickets: The open tickets matching the split event
        :param split: The split event data
        """
        ...

    def CanExecuteOrder(self, security: QuantConnect.Securities.Security, order: QuantConnect.Orders.Order) -> bool:
        """
        Returns true if the brokerage would be able to execute this order at this time assuming
        market prices are sufficient for the fill to take place. This is used to emulate the
        brokerage fills in backtesting and paper trading. For example some brokerages may not perform
        executions during extended market hours. This is not intended to be checking whether or not
        the exchange is open, that is handled in the Security.Exchange property.
        
        :param security: The security being ordered
        :param order: The order to test for execution
        :returns: True if the brokerage would be able to perform the execution, false otherwise.
        """
        ...

    def CanSubmitOrder(self, security: QuantConnect.Securities.Security, order: QuantConnect.Orders.Order, message: typing.Optional[QuantConnect.Brokerages.BrokerageMessageEvent]) -> typing.Union[bool, QuantConnect.Brokerages.BrokerageMessageEvent]:
        """
        Returns true if the brokerage could accept this order. This takes into account
        order type, security type, and order size limits.
        
        :param security: The security being ordered
        :param order: The order to be processed
        :param message: If this function returns false, a brokerage message detailing why the order may not be submitted
        :returns: True if the brokerage could process the order, false otherwise.
        """
        ...

    def CanUpdateOrder(self, security: QuantConnect.Securities.Security, order: QuantConnect.Orders.Order, request: QuantConnect.Orders.UpdateOrderRequest, message: typing.Optional[QuantConnect.Brokerages.BrokerageMessageEvent]) -> typing.Union[bool, QuantConnect.Brokerages.BrokerageMessageEvent]:
        """
        Returns true if the brokerage would allow updating the order as specified by the request
        
        :param security: The security of the order
        :param order: The order to be updated
        :param request: The requested updated to be made to the order
        :param message: If this function returns false, a brokerage message detailing why the order may not be updated
        :returns: True if the brokerage would allow updating the order, false otherwise.
        """
        ...

    def GetBenchmark(self, securities: QuantConnect.Securities.SecurityManager) -> QuantConnect.Benchmarks.IBenchmark:
        """
        Get the benchmark for this model
        
        :param securities: SecurityService to create the security with if needed
        :returns: The benchmark for this brokerage.
        """
        ...

    @overload
    def GetBuyingPowerModel(self, security: QuantConnect.Securities.Security) -> QuantConnect.Securities.IBuyingPowerModel:
        """
        Gets a new buying power model for the security
        
        :param security: The security to get a buying power model for
        :returns: The buying power model for this brokerage/security.
        """
        ...

    @overload
    def GetBuyingPowerModel(self, security: QuantConnect.Securities.Security, accountType: QuantConnect.AccountType) -> QuantConnect.Securities.IBuyingPowerModel:
        """
        Gets a new buying power model for the security
        
        Flagged deprecated and will remove December 1st 2018
        
        :param security: The security to get a buying power model for
        :param accountType: The account type
        :returns: The buying power model for this brokerage/security.
        """
        ...

    def GetFeeModel(self, security: QuantConnect.Securities.Security) -> QuantConnect.Orders.Fees.IFeeModel:
        """
        Gets a new fee model that represents this brokerage's fee structure
        
        :param security: The security to get a fee model for
        :returns: The new fee model for this brokerage.
        """
        ...

    def GetFillModel(self, security: QuantConnect.Securities.Security) -> QuantConnect.Orders.Fills.IFillModel:
        """
        Gets a new fill model that represents this brokerage's fill behavior
        
        :param security: The security to get fill model for
        :returns: The new fill model for this brokerage.
        """
        ...

    def GetLeverage(self, security: QuantConnect.Securities.Security) -> float:
        """
        Gets the brokerage's leverage for the specified security
        
        :param security: The security's whose leverage we seek
        :returns: The leverage for the specified security.
        """
        ...

    @overload
    def GetSettlementModel(self, security: QuantConnect.Securities.Security) -> QuantConnect.Securities.ISettlementModel:
        """
        Gets a new settlement model for the security
        
        :param security: The security to get a settlement model for
        :returns: The settlement model for this brokerage.
        """
        ...

    @overload
    def GetSettlementModel(self, security: QuantConnect.Securities.Security, accountType: QuantConnect.AccountType) -> QuantConnect.Securities.ISettlementModel:
        """
        Gets a new settlement model for the security
        
        Flagged deprecated and will remove December 1st 2018
        
        :param security: The security to get a settlement model for
        :param accountType: The account type
        :returns: The settlement model for this brokerage.
        """
        ...

    def GetShortableProvider(self) -> QuantConnect.Interfaces.IShortableProvider:
        """
        Gets the shortable provider
        
        :returns: Shortable provider.
        """
        ...

    def GetSlippageModel(self, security: QuantConnect.Securities.Security) -> QuantConnect.Orders.Slippage.ISlippageModel:
        """
        Gets a new slippage model that represents this brokerage's fill slippage behavior
        
        :param security: The security to get a slippage model for
        :returns: The new slippage model for this brokerage.
        """
        ...


class DefaultBrokerageModel(System.Object, QuantConnect.Brokerages.IBrokerageModel):
    """
    Provides a default implementation of IBrokerageModel that allows all orders and uses
    the default transaction models
    """

    DefaultMarketMap: System.Collections.Generic.IReadOnlyDictionary[QuantConnect.SecurityType, str] = ...
    """The default markets for the backtesting brokerage"""

    @property
    def ShortableProvider(self) -> QuantConnect.Interfaces.IShortableProvider:
        """
        Determines whether the asset you want to short is shortable.
        The default is set to NullShortableProvider,
        which allows for infinite shorting of any asset. You can limit the
        quantity you can short for an asset class by setting this variable to
        your own implementation of IShortableProvider.
        
        This property is protected.
        """
        ...

    @ShortableProvider.setter
    def ShortableProvider(self, value: QuantConnect.Interfaces.IShortableProvider):
        """
        Determines whether the asset you want to short is shortable.
        The default is set to NullShortableProvider,
        which allows for infinite shorting of any asset. You can limit the
        quantity you can short for an asset class by setting this variable to
        your own implementation of IShortableProvider.
        
        This property is protected.
        """
        ...

    @property
    def AccountType(self) -> int:
        """
        Gets or sets the account type used by this model
        
        This property contains the int value of a member of the QuantConnect.AccountType enum.
        """
        ...

    @AccountType.setter
    def AccountType(self, value: int):
        """
        Gets or sets the account type used by this model
        
        This property contains the int value of a member of the QuantConnect.AccountType enum.
        """
        ...

    @property
    def RequiredFreeBuyingPowerPercent(self) -> float:
        """
        Gets the brokerages model percentage factor used to determine the required unused buying power for the account.
        From 1 to 0. Example: 0 means no unused buying power is required. 0.5 means 50% of the buying power should be left unused.
        """
        ...

    @property
    def DefaultMarkets(self) -> System.Collections.Generic.IReadOnlyDictionary[QuantConnect.SecurityType, str]:
        """Gets a map of the default markets to be used for each security type"""
        ...

    def __init__(self, accountType: QuantConnect.AccountType = ...) -> None:
        """
        Initializes a new instance of the DefaultBrokerageModel class
        
        :param accountType: The type of account to be modelled, defaults to QuantConnect.AccountType.Margin
        """
        ...

    def ApplySplit(self, tickets: System.Collections.Generic.List[QuantConnect.Orders.OrderTicket], split: QuantConnect.Data.Market.Split) -> None:
        """
        Applies the split to the specified order ticket
        
        :param tickets: The open tickets matching the split event
        :param split: The split event data
        """
        ...

    def CanExecuteOrder(self, security: QuantConnect.Securities.Security, order: QuantConnect.Orders.Order) -> bool:
        """
        Returns true if the brokerage would be able to execute this order at this time assuming
        market prices are sufficient for the fill to take place. This is used to emulate the
        brokerage fills in backtesting and paper trading. For example some brokerages may not perform
        executions during extended market hours. This is not intended to be checking whether or not
        the exchange is open, that is handled in the Security.Exchange property.
        
        :param security: The security being traded
        :param order: The order to test for execution
        :returns: True if the brokerage would be able to perform the execution, false otherwise.
        """
        ...

    def CanSubmitOrder(self, security: QuantConnect.Securities.Security, order: QuantConnect.Orders.Order, message: typing.Optional[QuantConnect.Brokerages.BrokerageMessageEvent]) -> typing.Union[bool, QuantConnect.Brokerages.BrokerageMessageEvent]:
        """
        Returns true if the brokerage could accept this order. This takes into account
        order type, security type, and order size limits.
        
        :param security: The security being ordered
        :param order: The order to be processed
        :param message: If this function returns false, a brokerage message detailing why the order may not be submitted
        :returns: True if the brokerage could process the order, false otherwise.
        """
        ...

    def CanUpdateOrder(self, security: QuantConnect.Securities.Security, order: QuantConnect.Orders.Order, request: QuantConnect.Orders.UpdateOrderRequest, message: typing.Optional[QuantConnect.Brokerages.BrokerageMessageEvent]) -> typing.Union[bool, QuantConnect.Brokerages.BrokerageMessageEvent]:
        """
        Returns true if the brokerage would allow updating the order as specified by the request
        
        :param security: The security of the order
        :param order: The order to be updated
        :param request: The requested update to be made to the order
        :param message: If this function returns false, a brokerage message detailing why the order may not be updated
        :returns: True if the brokerage would allow updating the order, false otherwise.
        """
        ...

    def GetBenchmark(self, securities: QuantConnect.Securities.SecurityManager) -> QuantConnect.Benchmarks.IBenchmark:
        """
        Get the benchmark for this model
        
        :param securities: SecurityService to create the security with if needed
        :returns: The benchmark for this brokerage.
        """
        ...

    @overload
    def GetBuyingPowerModel(self, security: QuantConnect.Securities.Security) -> QuantConnect.Securities.IBuyingPowerModel:
        """
        Gets a new buying power model for the security, returning the default model with the security's configured leverage.
        For cash accounts, leverage = 1 is used.
        
        :param security: The security to get a buying power model for
        :returns: The buying power model for this brokerage/security.
        """
        ...

    @overload
    def GetBuyingPowerModel(self, security: QuantConnect.Securities.Security, accountType: QuantConnect.AccountType) -> QuantConnect.Securities.IBuyingPowerModel:
        """
        Gets a new buying power model for the security
        
        Flagged deprecated and will remove December 1st 2018
        
        :param security: The security to get a buying power model for
        :param accountType: The account type
        :returns: The buying power model for this brokerage/security.
        """
        ...

    def GetFeeModel(self, security: QuantConnect.Securities.Security) -> QuantConnect.Orders.Fees.IFeeModel:
        """
        Gets a new fee model that represents this brokerage's fee structure
        
        :param security: The security to get a fee model for
        :returns: The new fee model for this brokerage.
        """
        ...

    def GetFillModel(self, security: QuantConnect.Securities.Security) -> QuantConnect.Orders.Fills.IFillModel:
        """
        Gets a new fill model that represents this brokerage's fill behavior
        
        :param security: The security to get fill model for
        :returns: The new fill model for this brokerage.
        """
        ...

    def GetLeverage(self, security: QuantConnect.Securities.Security) -> float:
        """
        Gets the brokerage's leverage for the specified security
        
        :param security: The security's whose leverage we seek
        :returns: The leverage for the specified security.
        """
        ...

    @overload
    def GetSettlementModel(self, security: QuantConnect.Securities.Security) -> QuantConnect.Securities.ISettlementModel:
        """
        Gets a new settlement model for the security
        
        :param security: The security to get a settlement model for
        :returns: The settlement model for this brokerage.
        """
        ...

    @overload
    def GetSettlementModel(self, security: QuantConnect.Securities.Security, accountType: QuantConnect.AccountType) -> QuantConnect.Securities.ISettlementModel:
        """
        Gets a new settlement model for the security
        
        Flagged deprecated and will remove December 1st 2018
        
        :param security: The security to get a settlement model for
        :param accountType: The account type
        :returns: The settlement model for this brokerage.
        """
        ...

    def GetShortableProvider(self) -> QuantConnect.Interfaces.IShortableProvider:
        """
        Gets the shortable provider
        
        :returns: Shortable provider.
        """
        ...

    def GetSlippageModel(self, security: QuantConnect.Securities.Security) -> QuantConnect.Orders.Slippage.ISlippageModel:
        """
        Gets a new slippage model that represents this brokerage's fill slippage behavior
        
        :param security: The security to get a slippage model for
        :returns: The new slippage model for this brokerage.
        """
        ...

    @staticmethod
    def IsValidOrderSize(security: QuantConnect.Securities.Security, orderQuantity: float, message: typing.Optional[QuantConnect.Brokerages.BrokerageMessageEvent]) -> typing.Union[bool, QuantConnect.Brokerages.BrokerageMessageEvent]:
        """
        Checks if the order quantity is valid, it means, the order size is bigger than the minimum size allowed
        
        :param security: The security of the order
        :param orderQuantity: The quantity of the order to be processed
        :param message: If this function returns false, a brokerage message detailing why the order may be invalid
        :returns: True if the order quantity is bigger than the minimum allowed, false otherwise.
        """
        ...


class AlphaStreamsBrokerageModel(QuantConnect.Brokerages.DefaultBrokerageModel):
    """Provides properties specific to Alpha Streams"""

    def __init__(self, accountType: QuantConnect.AccountType = ...) -> None:
        """
        Initializes a new instance of the AlphaStreamsBrokerageModel class
        
        :param accountType: The type of account to be modelled, defaults to AccountType.Margin does not accept AccountType.Cash.
        """
        ...

    def GetFeeModel(self, security: QuantConnect.Securities.Security) -> QuantConnect.Orders.Fees.IFeeModel:
        """
        Gets a new fee model that represents this brokerage's fee structure
        
        :param security: The security to get a fee model for
        :returns: The new fee model for this brokerage.
        """
        ...

    def GetLeverage(self, security: QuantConnect.Securities.Security) -> float:
        """
        Gets the brokerage's leverage for the specified security
        
        :param security: The security's whose leverage we seek
        :returns: The leverage for the specified security.
        """
        ...

    def GetSettlementModel(self, security: QuantConnect.Securities.Security) -> QuantConnect.Securities.ISettlementModel:
        """
        Gets a new settlement model for the security
        
        :param security: The security to get a settlement model for
        :returns: The settlement model for this brokerage.
        """
        ...

    def GetSlippageModel(self, security: QuantConnect.Securities.Security) -> QuantConnect.Orders.Slippage.ISlippageModel:
        """
        Gets a new slippage model that represents this brokerage's fill slippage behavior
        
        :param security: The security to get a slippage model for
        :returns: The new slippage model for this brokerage.
        """
        ...


class AtreyuBrokerageModel(QuantConnect.Brokerages.DefaultBrokerageModel):
    """Provides Atreyu specific properties"""

    DefaultMarketMap: System.Collections.Generic.IReadOnlyDictionary[QuantConnect.SecurityType, str] = ...
    """The default markets for Trading Technologies"""

    @property
    def DefaultMarkets(self) -> System.Collections.Generic.IReadOnlyDictionary[QuantConnect.SecurityType, str]:
        """Gets a map of the default markets to be used for each security type"""
        ...

    def __init__(self, accountType: QuantConnect.AccountType = ...) -> None:
        """Creates a new instance"""
        ...

    def CanSubmitOrder(self, security: QuantConnect.Securities.Security, order: QuantConnect.Orders.Order, message: typing.Optional[QuantConnect.Brokerages.BrokerageMessageEvent]) -> typing.Union[bool, QuantConnect.Brokerages.BrokerageMessageEvent]:
        """
        Returns true if the brokerage could accept this order.
        
        :param security: The security being ordered
        :param order: The order to be processed
        :param message: If this function returns false, a brokerage message detailing why the order may not be submitted
        :returns: True if the brokerage could process the order, false otherwise.
        """
        ...

    def CanUpdateOrder(self, security: QuantConnect.Securities.Security, order: QuantConnect.Orders.Order, request: QuantConnect.Orders.UpdateOrderRequest, message: typing.Optional[QuantConnect.Brokerages.BrokerageMessageEvent]) -> typing.Union[bool, QuantConnect.Brokerages.BrokerageMessageEvent]:
        """
        Returns true if the brokerage would allow updating the order as specified by the request
        
        :param security: The security of the order
        :param order: The order to be updated
        :param request: The requested update to be made to the order
        :param message: If this function returns false, a brokerage message detailing why the order may not be updated
        :returns: True if the brokerage would allow updating the order, false otherwise.
        """
        ...

    def GetBenchmark(self, securities: QuantConnect.Securities.SecurityManager) -> QuantConnect.Benchmarks.IBenchmark:
        """
        Get the benchmark for this model
        
        :param securities: SecurityService to create the security with if needed
        :returns: The benchmark for this brokerage.
        """
        ...

    def GetFeeModel(self, security: QuantConnect.Securities.Security) -> QuantConnect.Orders.Fees.IFeeModel:
        """
        Provides Atreyu fee model
        
        :param security: The security to get a fee model for
        :returns: The new fee model for this brokerage.
        """
        ...

    def GetShortableProvider(self) -> QuantConnect.Interfaces.IShortableProvider:
        """
        Gets the shortable provider
        
        :returns: Shortable provider.
        """
        ...


class BinanceBrokerageModel(QuantConnect.Brokerages.DefaultBrokerageModel):
    """Provides Binance specific properties"""

    @property
    def MarketName(self) -> str:
        """
        Market name
        
        This property is protected.
        """
        ...

    @property
    def DefaultMarkets(self) -> System.Collections.Generic.IReadOnlyDictionary[QuantConnect.SecurityType, str]:
        """Gets a map of the default markets to be used for each security type"""
        ...

    def __init__(self, accountType: QuantConnect.AccountType = ...) -> None:
        """
        Initializes a new instance of the BinanceBrokerageModel class
        
        :param accountType: The type of account to be modeled, defaults to AccountType.Cash
        """
        ...

    def CanSubmitOrder(self, security: QuantConnect.Securities.Security, order: QuantConnect.Orders.Order, message: typing.Optional[QuantConnect.Brokerages.BrokerageMessageEvent]) -> typing.Union[bool, QuantConnect.Brokerages.BrokerageMessageEvent]:
        """
        Returns true if the brokerage could accept this order. This takes into account
        order type, security type, and order size limits.
        
        :param security: The security of the order
        :param order: The order to be processed
        :param message: If this function returns false, a brokerage message detailing why the order may not be submitted
        :returns: True if the brokerage could process the order, false otherwise.
        """
        ...

    def CanUpdateOrder(self, security: QuantConnect.Securities.Security, order: QuantConnect.Orders.Order, request: QuantConnect.Orders.UpdateOrderRequest, message: typing.Optional[QuantConnect.Brokerages.BrokerageMessageEvent]) -> typing.Union[bool, QuantConnect.Brokerages.BrokerageMessageEvent]:
        """
        Binance does not support update of orders
        
        :param security: The security of the order
        :param order: The order to be updated
        :param request: The requested update to be made to the order
        :param message: If this function returns false, a brokerage message detailing why the order may not be updated
        :returns: Binance does not support update of orders, so it will always return false.
        """
        ...

    def GetBenchmark(self, securities: QuantConnect.Securities.SecurityManager) -> QuantConnect.Benchmarks.IBenchmark:
        """
        Get the benchmark for this model
        
        :param securities: SecurityService to create the security with if needed
        :returns: The benchmark for this brokerage.
        """
        ...

    @staticmethod
    def GetDefaultMarkets(marketName: str) -> System.Collections.Generic.IReadOnlyDictionary[QuantConnect.SecurityType, str]:
        """This method is protected."""
        ...

    def GetFeeModel(self, security: QuantConnect.Securities.Security) -> QuantConnect.Orders.Fees.IFeeModel:
        """Provides Binance fee model"""
        ...

    def GetLeverage(self, security: QuantConnect.Securities.Security) -> float:
        """Binance global leverage rule"""
        ...


class BinanceUSBrokerageModel(QuantConnect.Brokerages.BinanceBrokerageModel):
    """Provides Binance.US specific properties"""

    @property
    def MarketName(self) -> str:
        """
        Market name
        
        This property is protected.
        """
        ...

    @property
    def DefaultMarkets(self) -> System.Collections.Generic.IReadOnlyDictionary[QuantConnect.SecurityType, str]:
        """Gets a map of the default markets to be used for each security type"""
        ...

    def __init__(self, accountType: QuantConnect.AccountType = ...) -> None:
        """
        Initializes a new instance of the BinanceBrokerageModel class
        
        :param accountType: The type of account to be modeled, defaults to AccountType.Cash
        """
        ...

    def GetLeverage(self, security: QuantConnect.Securities.Security) -> float:
        """Binance global leverage rule"""
        ...


class BitfinexBrokerageModel(QuantConnect.Brokerages.DefaultBrokerageModel):
    """Provides Bitfinex specific properties"""

    @property
    def DefaultMarkets(self) -> System.Collections.Generic.IReadOnlyDictionary[QuantConnect.SecurityType, str]:
        """Gets a map of the default markets to be used for each security type"""
        ...

    def __init__(self, accountType: QuantConnect.AccountType = ...) -> None:
        """
        Initializes a new instance of the BitfinexBrokerageModel class
        
        :param accountType: The type of account to be modeled, defaults to AccountType.Margin
        """
        ...

    def CanSubmitOrder(self, security: QuantConnect.Securities.Security, order: QuantConnect.Orders.Order, message: typing.Optional[QuantConnect.Brokerages.BrokerageMessageEvent]) -> typing.Union[bool, QuantConnect.Brokerages.BrokerageMessageEvent]:
        """
        Returns true if the brokerage could accept this order. This takes into account
        order type, security type, and order size limits.
        
        :param security: The security of the order
        :param order: The order to be processed
        :param message: If this function returns false, a brokerage message detailing why the order may not be submitted
        :returns: True if the brokerage could process the order, false otherwise.
        """
        ...

    def CanUpdateOrder(self, security: QuantConnect.Securities.Security, order: QuantConnect.Orders.Order, request: QuantConnect.Orders.UpdateOrderRequest, message: typing.Optional[QuantConnect.Brokerages.BrokerageMessageEvent]) -> typing.Union[bool, QuantConnect.Brokerages.BrokerageMessageEvent]:
        """
        Checks whether an order can be updated or not in the Bitfinex brokerage model
        
        :param security: The security of the order
        :param order: The order to be updated
        :param request: The update request
        :param message: If this function returns false, a brokerage message detailing why the order may not be updated
        :returns: True if the update requested quantity is valid, false otherwise.
        """
        ...

    def GetBenchmark(self, securities: QuantConnect.Securities.SecurityManager) -> QuantConnect.Benchmarks.IBenchmark:
        """
        Get the benchmark for this model
        
        :param securities: SecurityService to create the security with if needed
        :returns: The benchmark for this brokerage.
        """
        ...

    def GetFeeModel(self, security: QuantConnect.Securities.Security) -> QuantConnect.Orders.Fees.IFeeModel:
        """Provides Bitfinex fee model"""
        ...

    def GetLeverage(self, security: QuantConnect.Securities.Security) -> float:
        """Bitfinex global leverage rule"""
        ...


class BrokerageFactoryAttribute(System.Attribute):
    """Represents the brokerage factory type required to load a data queue handler"""

    @property
    def Type(self) -> typing.Type:
        """The type of the brokerage factory"""
        ...

    @Type.setter
    def Type(self, value: typing.Type):
        """The type of the brokerage factory"""
        ...

    def __init__(self, type: typing.Type) -> None:
        """
        Creates a new instance of the BrokerageFactoryAttribute class
        
        :param type: The brokerage factory type
        """
        ...


class BrokerageName(System.Enum):
    """Specifices what transaction model and submit/execution rules to use"""

    Default = 0
    """Transaction and submit/execution rules will be the default as initialized"""

    QuantConnectBrokerage = ...
    """
    Transaction and submit/execution rules will be the default as initialized
    Alternate naming for default brokerage
    """

    InteractiveBrokersBrokerage = 2
    """Transaction and submit/execution rules will use interactive brokers models"""

    TradierBrokerage = 3
    """Transaction and submit/execution rules will use tradier models"""

    OandaBrokerage = 4
    """Transaction and submit/execution rules will use oanda models"""

    FxcmBrokerage = 5
    """Transaction and submit/execution rules will use fxcm models"""

    Bitfinex = 6
    """Transaction and submit/execution rules will use bitfinex models"""

    Binance = 7
    """Transaction and submit/execution rules will use binance models"""

    GDAX = 12
    """Transaction and submit/execution rules will use gdax models"""

    Alpaca = 9
    """Transaction and submit/execution rules will use alpaca models"""

    AlphaStreams = 10
    """Transaction and submit/execution rules will use AlphaStream models"""

    Zerodha = 11
    """Transaction and submit/execution rules will use Zerodha models"""

    Samco = 12
    """Transaction and submit/execution rules will use Samco models"""

    Atreyu = 13
    """Transaction and submit/execution rules will use atreyu models"""

    TradingTechnologies = 14
    """Transaction and submit/execution rules will use TradingTechnologies models"""

    Kraken = 15
    """Transaction and submit/execution rules will use Kraken models"""

    FTX = 16
    """Transaction and submit/execution rules will use ftx models"""

    FTXUS = 17
    """Transaction and submit/execution rules will use ftx us models"""

    Exante = 18
    """Transaction and submit/execution rules will use Exante models"""

    BinanceUS = 19
    """Transaction and submit/execution rules will use Binance.US models"""


class IBrokerageMessageHandler(metaclass=abc.ABCMeta):
    """
    Provides an plugin point to allow algorithms to directly handle the messages
    that come from their brokerage
    """

    def Handle(self, message: QuantConnect.Brokerages.BrokerageMessageEvent) -> None:
        """
        Handles the message
        
        :param message: The message to be handled
        """
        ...


class DefaultBrokerageMessageHandler(System.Object, QuantConnect.Brokerages.IBrokerageMessageHandler):
    """
    Provides a default implementation o IBrokerageMessageHandler that will forward
    messages as follows:
    Information -> IResultHandler.Debug
    Warning     -> IResultHandler.Error && IApi.SendUserEmail
    Error       -> IResultHandler.Error && IAlgorithm.RunTimeError
    """

    def __init__(self, algorithm: QuantConnect.Interfaces.IAlgorithm, job: QuantConnect.Packets.AlgorithmNodePacket, api: QuantConnect.Interfaces.IApi, initialDelay: typing.Optional[datetime.timedelta] = None, openThreshold: typing.Optional[datetime.timedelta] = None) -> None:
        """
        Initializes a new instance of the DefaultBrokerageMessageHandler class
        
        :param algorithm: The running algorithm
        :param job: The job that produced the algorithm
        :param api: The api for the algorithm
        :param openThreshold: Defines how long before market open to re-check for brokerage reconnect message
        """
        ...

    def Handle(self, message: QuantConnect.Brokerages.BrokerageMessageEvent) -> None:
        """
        Handles the message
        
        :param message: The message to be handled
        """
        ...


class DelistingNotificationEventArgs(System.Object):
    """Event arguments class for the IBrokerage.DelistingNotification event"""

    @property
    def Symbol(self) -> QuantConnect.Symbol:
        """Gets the option symbol which has received a notification"""
        ...

    def __init__(self, symbol: typing.Union[QuantConnect.Symbol, str]) -> None:
        """
        Initializes a new instance of the DelistingNotificationEventArgs class
        
        :param symbol: The symbol
        """
        ...


class DowngradeErrorCodeToWarningBrokerageMessageHandler(System.Object, QuantConnect.Brokerages.IBrokerageMessageHandler):
    """Provides an implementation of IBrokerageMessageHandler that converts specified error codes into warnings"""

    def __init__(self, brokerageMessageHandler: QuantConnect.Brokerages.IBrokerageMessageHandler, errorCodesToIgnore: typing.List[str]) -> None:
        """
        Initializes a new instance of the DowngradeErrorCodeToWarningBrokerageMessageHandler class
        
        :param brokerageMessageHandler: The brokerage message handler to be wrapped
        :param errorCodesToIgnore: The error codes to convert to warning messages
        """
        ...

    def Handle(self, message: QuantConnect.Brokerages.BrokerageMessageEvent) -> None:
        """
        Handles the message
        
        :param message: The message to be handled
        """
        ...


class ExanteBrokerageModel(QuantConnect.Brokerages.DefaultBrokerageModel):
    """Exante Brokerage Model Implementation for Back Testing."""

    def __init__(self, accountType: QuantConnect.AccountType = ...) -> None:
        """
        Constructor for Exante brokerage model
        
        :param accountType: Cash or Margin
        """
        ...

    def CanSubmitOrder(self, security: QuantConnect.Securities.Security, order: QuantConnect.Orders.Order, message: typing.Optional[QuantConnect.Brokerages.BrokerageMessageEvent]) -> typing.Union[bool, QuantConnect.Brokerages.BrokerageMessageEvent]:
        """
        Returns true if the brokerage could accept this order. This takes into account
        order type, security type, and order size limits.
        
        :param security: The security being ordered
        :param order: The order to be processed
        :param message: If this function returns false, a brokerage message detailing why the order may not be submitted
        :returns: True if the brokerage could process the order, false otherwise.
        """
        ...

    def GetBenchmark(self, securities: QuantConnect.Securities.SecurityManager) -> QuantConnect.Benchmarks.IBenchmark:
        """
        Get the benchmark for this model
        
        :param securities: SecurityService to create the security with if needed
        :returns: The benchmark for this brokerage.
        """
        ...

    def GetFeeModel(self, security: QuantConnect.Securities.Security) -> QuantConnect.Orders.Fees.IFeeModel:
        """
        Gets a new fee model that represents this brokerage's fee structure
        
        :param security: The security to get a fee model for
        :returns: The new fee model for this brokerage.
        """
        ...

    def GetLeverage(self, security: QuantConnect.Securities.Security) -> float:
        """
        Exante global leverage rule
        
        :param security: The security's whose leverage we seek
        :returns: The leverage for the specified security.
        """
        ...


class FTXBrokerageModel(QuantConnect.Brokerages.DefaultBrokerageModel):
    """FTX Brokerage model"""

    @property
    def MarketName(self) -> str:
        """
        market name
        
        This property is protected.
        """
        ...

    @property
    def DefaultMarkets(self) -> System.Collections.Generic.IReadOnlyDictionary[QuantConnect.SecurityType, str]:
        """Gets a map of the default markets to be used for each security type"""
        ...

    def __init__(self, accountType: QuantConnect.AccountType = ...) -> None:
        """
        Creates an instance of FTXBrokerageModel class
        
        :param accountType: Cash or Margin
        """
        ...

    def CanSubmitOrder(self, security: QuantConnect.Securities.Security, order: QuantConnect.Orders.Order, message: typing.Optional[QuantConnect.Brokerages.BrokerageMessageEvent]) -> typing.Union[bool, QuantConnect.Brokerages.BrokerageMessageEvent]:
        """
        Returns true if the brokerage could accept this order. This takes into account
        order type, security type, and order size limits.
        
        :param security: The security of the order
        :param order: The order to be processed
        :param message: If this function returns false, a brokerage message detailing why the order may not be submitted
        :returns: True if the brokerage could process the order, false otherwise.
        """
        ...

    def CanUpdateOrder(self, security: QuantConnect.Securities.Security, order: QuantConnect.Orders.Order, request: QuantConnect.Orders.UpdateOrderRequest, message: typing.Optional[QuantConnect.Brokerages.BrokerageMessageEvent]) -> typing.Union[bool, QuantConnect.Brokerages.BrokerageMessageEvent]:
        """
        Please note that the order's queue priority will be reset, and the order ID of the modified order will be different from that of the original order.
        Also note: this is implemented as cancelling and replacing your order.
        There's a chance that the order meant to be cancelled gets filled and its replacement still gets placed.
        
        :param security: The security of the order
        :param order: The order to be updated
        :param request: The requested update to be made to the order
        :param message: If this function returns false, a brokerage message detailing why the order may not be updated
        :returns: True if the brokerage would allow updating the order, false otherwise.
        """
        ...

    def GetBenchmark(self, securities: QuantConnect.Securities.SecurityManager) -> QuantConnect.Benchmarks.IBenchmark:
        """
        Get the benchmark for this model
        
        :param securities: SecurityService to create the security with if needed
        :returns: The benchmark for this brokerage.
        """
        ...

    @staticmethod
    def GetDefaultMarkets(market: str) -> System.Collections.Generic.IReadOnlyDictionary[QuantConnect.SecurityType, str]:
        """This method is protected."""
        ...

    def GetFeeModel(self, security: QuantConnect.Securities.Security) -> QuantConnect.Orders.Fees.IFeeModel:
        """
        Provides FTX fee model
        
        :param security: The security to get a fee model for
        :returns: The new fee model for this brokerage.
        """
        ...

    def GetLeverage(self, security: QuantConnect.Securities.Security) -> float:
        """
        Gets the brokerage's leverage for the specified security
        
        :param security: The security's whose leverage we seek
        :returns: The leverage for the specified security.
        """
        ...


class FTXUSBrokerageModel(QuantConnect.Brokerages.FTXBrokerageModel):
    """FTX.US Brokerage model"""

    @property
    def MarketName(self) -> str:
        """
        Market name
        
        This property is protected.
        """
        ...

    @property
    def DefaultMarkets(self) -> System.Collections.Generic.IReadOnlyDictionary[QuantConnect.SecurityType, str]:
        """Gets a map of the default markets to be used for each security type"""
        ...

    def __init__(self, accountType: QuantConnect.AccountType = ...) -> None:
        """
        Creates an instance of FTXUSBrokerageModel class
        
        :param accountType: Cash or Margin
        """
        ...

    def GetFeeModel(self, security: QuantConnect.Securities.Security) -> QuantConnect.Orders.Fees.IFeeModel:
        """
        Provides FTX.US fee model
        
        :param security: The security to get a fee model for
        :returns: The new fee model for this brokerage.
        """
        ...


class FxcmBrokerageModel(QuantConnect.Brokerages.DefaultBrokerageModel):
    """Provides FXCM specific properties"""

    DefaultMarketMap: System.Collections.Generic.IReadOnlyDictionary[QuantConnect.SecurityType, str] = ...
    """The default markets for the fxcm brokerage"""

    @property
    def DefaultMarkets(self) -> System.Collections.Generic.IReadOnlyDictionary[QuantConnect.SecurityType, str]:
        """Gets a map of the default markets to be used for each security type"""
        ...

    def __init__(self, accountType: QuantConnect.AccountType = ...) -> None:
        """
        Initializes a new instance of the DefaultBrokerageModel class
        
        :param accountType: The type of account to be modelled, defaults to AccountType.Margin
        """
        ...

    def CanSubmitOrder(self, security: QuantConnect.Securities.Security, order: QuantConnect.Orders.Order, message: typing.Optional[QuantConnect.Brokerages.BrokerageMessageEvent]) -> typing.Union[bool, QuantConnect.Brokerages.BrokerageMessageEvent]:
        """
        Returns true if the brokerage could accept this order. This takes into account
        order type, security type, and order size limits.
        
        :param order: The order to be processed
        :param message: If this function returns false, a brokerage message detailing why the order may not be submitted
        :returns: True if the brokerage could process the order, false otherwise.
        """
        ...

    def CanUpdateOrder(self, security: QuantConnect.Securities.Security, order: QuantConnect.Orders.Order, request: QuantConnect.Orders.UpdateOrderRequest, message: typing.Optional[QuantConnect.Brokerages.BrokerageMessageEvent]) -> typing.Union[bool, QuantConnect.Brokerages.BrokerageMessageEvent]:
        """
        Returns true if the brokerage would allow updating the order as specified by the request
        
        :param security: The security of the order
        :param order: The order to be updated
        :param request: The requested update to be made to the order
        :param message: If this function returns false, a brokerage message detailing why the order may not be updated
        :returns: True if the brokerage would allow updating the order, false otherwise.
        """
        ...

    def GetBenchmark(self, securities: QuantConnect.Securities.SecurityManager) -> QuantConnect.Benchmarks.IBenchmark:
        """
        Get the benchmark for this model
        
        :param securities: SecurityService to create the security with if needed
        :returns: The benchmark for this brokerage.
        """
        ...

    def GetFeeModel(self, security: QuantConnect.Securities.Security) -> QuantConnect.Orders.Fees.IFeeModel:
        """
        Gets a new fee model that represents this brokerage's fee structure
        
        :param security: The security to get a fee model for
        :returns: The new fee model for this brokerage.
        """
        ...

    def GetSettlementModel(self, security: QuantConnect.Securities.Security) -> QuantConnect.Securities.ISettlementModel:
        """
        Gets a new settlement model for the security
        
        :param security: The security to get a settlement model for
        :returns: The settlement model for this brokerage.
        """
        ...

    def GetSlippageModel(self, security: QuantConnect.Securities.Security) -> QuantConnect.Orders.Slippage.ISlippageModel:
        """
        Gets a new slippage model that represents this brokerage's fill slippage behavior
        
        :param security: The security to get a slippage model for
        :returns: The new slippage model for this brokerage.
        """
        ...


class GDAXBrokerageModel(QuantConnect.Brokerages.DefaultBrokerageModel):
    """Provides GDAX specific properties"""

    def __init__(self, accountType: QuantConnect.AccountType = ...) -> None:
        """
        Initializes a new instance of the GDAXBrokerageModel class
        
        :param accountType: The type of account to be modelled, defaults to AccountType.Cash
        """
        ...

    def CanSubmitOrder(self, security: QuantConnect.Securities.Security, order: QuantConnect.Orders.Order, message: typing.Optional[QuantConnect.Brokerages.BrokerageMessageEvent]) -> typing.Union[bool, QuantConnect.Brokerages.BrokerageMessageEvent]:
        """
        Evaluates whether exchange will accept order. Will reject order update
        
        :param security: The security of the order
        :param order: The order to be processed
        :param message: If this function returns false, a brokerage message detailing why the order may not be submitted
        :returns: True if the brokerage could process the order, false otherwise.
        """
        ...

    def CanUpdateOrder(self, security: QuantConnect.Securities.Security, order: QuantConnect.Orders.Order, request: QuantConnect.Orders.UpdateOrderRequest, message: typing.Optional[QuantConnect.Brokerages.BrokerageMessageEvent]) -> typing.Union[bool, QuantConnect.Brokerages.BrokerageMessageEvent]:
        """
        Gdax does not support update of orders
        
        :param security: The security of the order
        :param order: The order to be updated
        :param request: The requested update to be made to the order
        :param message: If this function returns false, a brokerage message detailing why the order may not be updated
        :returns: GDAX does not support update of orders, so it will always return false.
        """
        ...

    def GetBenchmark(self, securities: QuantConnect.Securities.SecurityManager) -> QuantConnect.Benchmarks.IBenchmark:
        """
        Get the benchmark for this model
        
        :param securities: SecurityService to create the security with if needed
        :returns: The benchmark for this brokerage.
        """
        ...

    def GetBuyingPowerModel(self, security: QuantConnect.Securities.Security) -> QuantConnect.Securities.IBuyingPowerModel:
        """
        Gets a new buying power model for the security, returning the default model with the security's configured leverage.
        For cash accounts, leverage = 1 is used.
        
        :param security: The security to get a buying power model for
        :returns: The buying power model for this brokerage/security.
        """
        ...

    def GetFeeModel(self, security: QuantConnect.Securities.Security) -> QuantConnect.Orders.Fees.IFeeModel:
        """Provides GDAX fee model"""
        ...

    def GetFillModel(self, security: QuantConnect.Securities.Security) -> QuantConnect.Orders.Fills.IFillModel:
        """
        GDAX fills order using the latest Trade or Quote data
        
        :param security: The security to get fill model for
        :returns: The new fill model for this brokerage.
        """
        ...

    def GetLeverage(self, security: QuantConnect.Securities.Security) -> float:
        """GDAX global leverage rule"""
        ...


class BrokerageModel(System.Object):
    """Provides factory method for creating an IBrokerageModel from the BrokerageName enum"""

    @staticmethod
    def Create(orderProvider: QuantConnect.Securities.IOrderProvider, brokerage: QuantConnect.Brokerages.BrokerageName, accountType: QuantConnect.AccountType) -> QuantConnect.Brokerages.IBrokerageModel:
        """
        Creates a new IBrokerageModel for the specified BrokerageName
        
        :param orderProvider: The order provider
        :param brokerage: The name of the brokerage
        :param accountType: The account type
        :returns: The model for the specified brokerage.
        """
        ...


class InteractiveBrokersBrokerageModel(QuantConnect.Brokerages.DefaultBrokerageModel):
    """Provides properties specific to interactive brokers"""

    DefaultMarketMap: System.Collections.Generic.IReadOnlyDictionary[QuantConnect.SecurityType, str] = ...
    """The default markets for the IB brokerage"""

    @property
    def DefaultMarkets(self) -> System.Collections.Generic.IReadOnlyDictionary[QuantConnect.SecurityType, str]:
        """Gets a map of the default markets to be used for each security type"""
        ...

    def __init__(self, accountType: QuantConnect.AccountType = ...) -> None:
        """
        Initializes a new instance of the InteractiveBrokersBrokerageModel class
        
        :param accountType: The type of account to be modelled, defaults to AccountType.Margin
        """
        ...

    def CanExecuteOrder(self, security: QuantConnect.Securities.Security, order: QuantConnect.Orders.Order) -> bool:
        """
        Returns true if the brokerage would be able to execute this order at this time assuming
        market prices are sufficient for the fill to take place. This is used to emulate the
        brokerage fills in backtesting and paper trading. For example some brokerages may not perform
        executions during extended market hours. This is not intended to be checking whether or not
        the exchange is open, that is handled in the Security.Exchange property.
        
        :param order: The order to test for execution
        :returns: True if the brokerage would be able to perform the execution, false otherwise.
        """
        ...

    def CanSubmitOrder(self, security: QuantConnect.Securities.Security, order: QuantConnect.Orders.Order, message: typing.Optional[QuantConnect.Brokerages.BrokerageMessageEvent]) -> typing.Union[bool, QuantConnect.Brokerages.BrokerageMessageEvent]:
        """
        Returns true if the brokerage could accept this order. This takes into account
        order type, security type, and order size limits.
        
        :param security: The security being ordered
        :param order: The order to be processed
        :param message: If this function returns false, a brokerage message detailing why the order may not be submitted
        :returns: True if the brokerage could process the order, false otherwise.
        """
        ...

    def CanUpdateOrder(self, security: QuantConnect.Securities.Security, order: QuantConnect.Orders.Order, request: QuantConnect.Orders.UpdateOrderRequest, message: typing.Optional[QuantConnect.Brokerages.BrokerageMessageEvent]) -> typing.Union[bool, QuantConnect.Brokerages.BrokerageMessageEvent]:
        """
        Returns true if the brokerage would allow updating the order as specified by the request
        
        :param security: The security of the order
        :param order: The order to be updated
        :param request: The requested update to be made to the order
        :param message: If this function returns false, a brokerage message detailing why the order may not be updated
        :returns: True if the brokerage would allow updating the order, false otherwise.
        """
        ...

    def GetBenchmark(self, securities: QuantConnect.Securities.SecurityManager) -> QuantConnect.Benchmarks.IBenchmark:
        """
        Get the benchmark for this model
        
        :param securities: SecurityService to create the security with if needed
        :returns: The benchmark for this brokerage.
        """
        ...

    def GetFeeModel(self, security: QuantConnect.Securities.Security) -> QuantConnect.Orders.Fees.IFeeModel:
        """
        Gets a new fee model that represents this brokerage's fee structure
        
        :param security: The security to get a fee model for
        :returns: The new fee model for this brokerage.
        """
        ...


class KrakenBrokerageModel(QuantConnect.Brokerages.DefaultBrokerageModel):
    """Kraken Brokerage model"""

    @property
    def DefaultMarkets(self) -> System.Collections.Generic.IReadOnlyDictionary[QuantConnect.SecurityType, str]:
        """Gets a map of the default markets to be used for each security type"""
        ...

    @property
    def CoinLeverage(self) -> System.Collections.Generic.IReadOnlyDictionary[str, float]:
        """Leverage map of different coins"""
        ...

    def __init__(self, accountType: QuantConnect.AccountType = ...) -> None:
        """
        Constructor for Kraken brokerage model
        
        :param accountType: Cash or Margin
        """
        ...

    def CanSubmitOrder(self, security: QuantConnect.Securities.Security, order: QuantConnect.Orders.Order, message: typing.Optional[QuantConnect.Brokerages.BrokerageMessageEvent]) -> typing.Union[bool, QuantConnect.Brokerages.BrokerageMessageEvent]:
        """
        Returns true if the brokerage could accept this order. This takes into account
        order type, security type, and order size limits.
        
        :param security: The security of the order
        :param order: The order to be processed
        :param message: If this function returns false, a brokerage message detailing why the order may not be submitted
        :returns: True if the brokerage could process the order, false otherwise.
        """
        ...

    def CanUpdateOrder(self, security: QuantConnect.Securities.Security, order: QuantConnect.Orders.Order, request: QuantConnect.Orders.UpdateOrderRequest, message: typing.Optional[QuantConnect.Brokerages.BrokerageMessageEvent]) -> typing.Union[bool, QuantConnect.Brokerages.BrokerageMessageEvent]:
        """
        Kraken does not support update of orders
        
        :param security: Security
        :param order: Order that should be updated
        :param request: Update request
        :param message: Outgoing message
        :returns: Always false as Kraken does not support update of orders.
        """
        ...

    def GetBenchmark(self, securities: QuantConnect.Securities.SecurityManager) -> QuantConnect.Benchmarks.IBenchmark:
        """
        Get the benchmark for this model
        
        :param securities: SecurityService to create the security with if needed
        :returns: The benchmark for this brokerage.
        """
        ...

    def GetFeeModel(self, security: QuantConnect.Securities.Security) -> QuantConnect.Orders.Fees.IFeeModel:
        """
        Provides Kraken fee model
        
        :param security: Security
        :returns: Kraken fee model.
        """
        ...

    def GetLeverage(self, security: QuantConnect.Securities.Security) -> float:
        """Kraken global leverage rule"""
        ...


class OandaBrokerageModel(QuantConnect.Brokerages.DefaultBrokerageModel):
    """Oanda Brokerage Model Implementation for Back Testing."""

    DefaultMarketMap: System.Collections.Generic.IReadOnlyDictionary[QuantConnect.SecurityType, str] = ...
    """The default markets for the fxcm brokerage"""

    @property
    def DefaultMarkets(self) -> System.Collections.Generic.IReadOnlyDictionary[QuantConnect.SecurityType, str]:
        """Gets a map of the default markets to be used for each security type"""
        ...

    def __init__(self, accountType: QuantConnect.AccountType = ...) -> None:
        """
        Initializes a new instance of the DefaultBrokerageModel class
        
        :param accountType: The type of account to be modelled, defaults to AccountType.Margin
        """
        ...

    def CanSubmitOrder(self, security: QuantConnect.Securities.Security, order: QuantConnect.Orders.Order, message: typing.Optional[QuantConnect.Brokerages.BrokerageMessageEvent]) -> typing.Union[bool, QuantConnect.Brokerages.BrokerageMessageEvent]:
        """
        Returns true if the brokerage could accept this order. This takes into account
        order type, security type, and order size limits.
        
        :param order: The order to be processed
        :param message: If this function returns false, a brokerage message detailing why the order may not be submitted
        :returns: True if the brokerage could process the order, false otherwise.
        """
        ...

    def GetBenchmark(self, securities: QuantConnect.Securities.SecurityManager) -> QuantConnect.Benchmarks.IBenchmark:
        """
        Get the benchmark for this model
        
        :param securities: SecurityService to create the security with if needed
        :returns: The benchmark for this brokerage.
        """
        ...

    def GetFeeModel(self, security: QuantConnect.Securities.Security) -> QuantConnect.Orders.Fees.IFeeModel:
        """
        Gets a new fee model that represents this brokerage's fee structure
        
        :param security: The security to get a fee model for
        :returns: The new fee model for this brokerage.
        """
        ...

    def GetSettlementModel(self, security: QuantConnect.Securities.Security) -> QuantConnect.Securities.ISettlementModel:
        """
        Gets a new settlement model for the security
        
        :param security: The security to get a settlement model for
        :returns: The settlement model for this brokerage.
        """
        ...

    def GetSlippageModel(self, security: QuantConnect.Securities.Security) -> QuantConnect.Orders.Slippage.ISlippageModel:
        """
        Gets a new slippage model that represents this brokerage's fill slippage behavior
        
        :param security: The security to get a slippage model for
        :returns: The new slippage model for this brokerage.
        """
        ...


class OptionNotificationEventArgs(System.EventArgs):
    """Event arguments class for the IBrokerage.OptionNotification event"""

    @property
    def Symbol(self) -> QuantConnect.Symbol:
        """Gets the option symbol which has received a notification"""
        ...

    @property
    def Position(self) -> float:
        """Gets the new option position (positive for long, zero for flat, negative for short)"""
        ...

    def __init__(self, symbol: typing.Union[QuantConnect.Symbol, str], position: float) -> None:
        """
        Initializes a new instance of the OptionNotificationEventArgs class
        
        :param symbol: The symbol
        :param position: The new option position
        """
        ...


class SamcoBrokerageModel(QuantConnect.Brokerages.DefaultBrokerageModel):
    """Brokerage Model implementation for Samco"""

    @property
    def DefaultMarkets(self) -> System.Collections.Generic.IReadOnlyDictionary[QuantConnect.SecurityType, str]:
        """Gets a map of the default markets to be used for each security type"""
        ...

    def __init__(self, accountType: QuantConnect.AccountType = ...) -> None:
        """
        Initializes a new instance of the SamcoBrokerageModel class
        
        :param accountType: The type of account to be modelled, defaults to AccountType.Margin
        """
        ...

    def CanExecuteOrder(self, security: QuantConnect.Securities.Security, order: QuantConnect.Orders.Order) -> bool:
        """
        Returns true if the brokerage would be able to execute this order at this time assuming
        market prices are sufficient for the fill to take place. This is used to emulate the
        brokerage fills in backtesting and paper trading. For example some brokerages may not
        perform executions during extended market hours. This is not intended to be checking
        whether or not the exchange is open, that is handled in the Security.Exchange property.
        
        :param order: The order to test for execution
        :returns: True if the brokerage would be able to perform the execution, false otherwise.
        """
        ...

    def CanSubmitOrder(self, security: QuantConnect.Securities.Security, order: QuantConnect.Orders.Order, message: typing.Optional[QuantConnect.Brokerages.BrokerageMessageEvent]) -> typing.Union[bool, QuantConnect.Brokerages.BrokerageMessageEvent]:
        """
        Returns true if the brokerage could accept this order. This takes into account order
        type, security type, and order size limits.
        
        :param security: The security being ordered
        :param order: The order to be processed
        :param message: If this function returns false, a brokerage message detailing why the order may not be submitted
        :returns: True if the brokerage could process the order, false otherwise.
        """
        ...

    def CanUpdateOrder(self, security: QuantConnect.Securities.Security, order: QuantConnect.Orders.Order, request: QuantConnect.Orders.UpdateOrderRequest, message: typing.Optional[QuantConnect.Brokerages.BrokerageMessageEvent]) -> typing.Union[bool, QuantConnect.Brokerages.BrokerageMessageEvent]:
        """
        Returns true if the brokerage would allow updating the order as specified by the request
        
        :param security: The security of the order
        :param order: The order to be updated
        :param request: The requested update to be made to the order
        :param message: If this function returns false, a brokerage message detailing why the order may not be updated
        :returns: True if the brokerage would allow updating the order, false otherwise.
        """
        ...

    def GetBenchmark(self, securities: QuantConnect.Securities.SecurityManager) -> QuantConnect.Benchmarks.IBenchmark:
        """
        Get the benchmark for this model
        
        :param securities: SecurityService to create the security with if needed
        :returns: The benchmark for this brokerage.
        """
        ...

    def GetFeeModel(self, security: QuantConnect.Securities.Security) -> QuantConnect.Orders.Fees.IFeeModel:
        """Provides Samco fee model"""
        ...

    def GetLeverage(self, security: QuantConnect.Securities.Security) -> float:
        """Samco global leverage rule"""
        ...


class TradierBrokerageModel(QuantConnect.Brokerages.DefaultBrokerageModel):
    """Provides tradier specific properties"""

    def __init__(self, accountType: QuantConnect.AccountType = ...) -> None:
        """
        Initializes a new instance of the DefaultBrokerageModel class
        
        :param accountType: The type of account to be modeled, defaults to QuantConnect.AccountType.Margin
        """
        ...

    def ApplySplit(self, tickets: System.Collections.Generic.List[QuantConnect.Orders.OrderTicket], split: QuantConnect.Data.Market.Split) -> None:
        """
        Applies the split to the specified order ticket
        
        :param tickets: The open tickets matching the split event
        :param split: The split event data
        """
        ...

    def CanExecuteOrder(self, security: QuantConnect.Securities.Security, order: QuantConnect.Orders.Order) -> bool:
        """
        Returns true if the brokerage would be able to execute this order at this time assuming
        market prices are sufficient for the fill to take place. This is used to emulate the
        brokerage fills in backtesting and paper trading. For example some brokerages may not perform
        executions during extended market hours. This is not intended to be checking whether or not
        the exchange is open, that is handled in the Security.Exchange property.
        
        :param security: The security being ordered
        :param order: The order to test for execution
        :returns: True if the brokerage would be able to perform the execution, false otherwise.
        """
        ...

    def CanSubmitOrder(self, security: QuantConnect.Securities.Security, order: QuantConnect.Orders.Order, message: typing.Optional[QuantConnect.Brokerages.BrokerageMessageEvent]) -> typing.Union[bool, QuantConnect.Brokerages.BrokerageMessageEvent]:
        """
        Returns true if the brokerage could accept this order. This takes into account
        order type, security type, and order size limits.
        
        :param security: The security of the order
        :param order: The order to be processed
        :param message: If this function returns false, a brokerage message detailing why the order may not be submitted
        :returns: True if the brokerage could process the order, false otherwise.
        """
        ...

    def CanUpdateOrder(self, security: QuantConnect.Securities.Security, order: QuantConnect.Orders.Order, request: QuantConnect.Orders.UpdateOrderRequest, message: typing.Optional[QuantConnect.Brokerages.BrokerageMessageEvent]) -> typing.Union[bool, QuantConnect.Brokerages.BrokerageMessageEvent]:
        """
        Returns true if the brokerage would allow updating the order as specified by the request
        
        :param security: The security of the order
        :param order: The order to be updated
        :param request: The requested update to be made to the order
        :param message: If this function returns false, a brokerage message detailing why the order may not be updated
        :returns: True if the brokerage would allow updating the order, false otherwise.
        """
        ...

    def GetFeeModel(self, security: QuantConnect.Securities.Security) -> QuantConnect.Orders.Fees.IFeeModel:
        """
        Gets a new fee model that represents this brokerage's fee structure
        
        :param security: The security to get a fee model for
        :returns: The new fee model for this brokerage.
        """
        ...

    def GetSlippageModel(self, security: QuantConnect.Securities.Security) -> QuantConnect.Orders.Slippage.ISlippageModel:
        """
        Gets a new slippage model that represents this brokerage's fill slippage behavior
        
        :param security: The security to get a slippage model for
        :returns: The new slippage model for this brokerage.
        """
        ...


class TradingTechnologiesBrokerageModel(QuantConnect.Brokerages.DefaultBrokerageModel):
    """Provides properties specific to Trading Technologies"""

    DefaultMarketMap: System.Collections.Generic.IReadOnlyDictionary[QuantConnect.SecurityType, str] = ...
    """The default markets for Trading Technologies"""

    @property
    def DefaultMarkets(self) -> System.Collections.Generic.IReadOnlyDictionary[QuantConnect.SecurityType, str]:
        """Gets a map of the default markets to be used for each security type"""
        ...

    def __init__(self, accountType: QuantConnect.AccountType = ...) -> None:
        """
        Initializes a new instance of the TradingTechnologiesBrokerageModel class
        
        :param accountType: The type of account to be modelled, defaults to AccountType.Margin
        """
        ...

    def CanExecuteOrder(self, security: QuantConnect.Securities.Security, order: QuantConnect.Orders.Order) -> bool:
        """
        Returns true if the brokerage would be able to execute this order at this time assuming
        market prices are sufficient for the fill to take place. This is used to emulate the
        brokerage fills in backtesting and paper trading. For example some brokerages may not perform
        executions during extended market hours. This is not intended to be checking whether or not
        the exchange is open, that is handled in the Security.Exchange property.
        
        :param order: The order to test for execution
        :returns: True if the brokerage would be able to perform the execution, false otherwise.
        """
        ...

    def CanSubmitOrder(self, security: QuantConnect.Securities.Security, order: QuantConnect.Orders.Order, message: typing.Optional[QuantConnect.Brokerages.BrokerageMessageEvent]) -> typing.Union[bool, QuantConnect.Brokerages.BrokerageMessageEvent]:
        """
        Returns true if the brokerage could accept this order. This takes into account
        order type, security type, and order size limits.
        
        :param security: The security being ordered
        :param order: The order to be processed
        :param message: If this function returns false, a brokerage message detailing why the order may not be submitted
        :returns: True if the brokerage could process the order, false otherwise.
        """
        ...

    def CanUpdateOrder(self, security: QuantConnect.Securities.Security, order: QuantConnect.Orders.Order, request: QuantConnect.Orders.UpdateOrderRequest, message: typing.Optional[QuantConnect.Brokerages.BrokerageMessageEvent]) -> typing.Union[bool, QuantConnect.Brokerages.BrokerageMessageEvent]:
        """
        Returns true if the brokerage would allow updating the order as specified by the request
        
        :param security: The security of the order
        :param order: The order to be updated
        :param request: The requested update to be made to the order
        :param message: If this function returns false, a brokerage message detailing why the order may not be updated
        :returns: True if the brokerage would allow updating the order, false otherwise.
        """
        ...

    def GetBenchmark(self, securities: QuantConnect.Securities.SecurityManager) -> QuantConnect.Benchmarks.IBenchmark:
        """
        Get the benchmark for this model
        
        :param securities: SecurityService to create the security with if needed
        :returns: The benchmark for this brokerage.
        """
        ...

    def GetFeeModel(self, security: QuantConnect.Securities.Security) -> QuantConnect.Orders.Fees.IFeeModel:
        """
        Gets a new fee model that represents this brokerage's fee structure
        
        :param security: The security to get a fee model for
        :returns: The new fee model for this brokerage.
        """
        ...


class ZerodhaBrokerageModel(QuantConnect.Brokerages.DefaultBrokerageModel):
    """Brokerage Model implementation for Zerodha"""

    @property
    def DefaultMarkets(self) -> System.Collections.Generic.IReadOnlyDictionary[QuantConnect.SecurityType, str]:
        """Gets a map of the default markets to be used for each security type"""
        ...

    def __init__(self, accountType: QuantConnect.AccountType = ...) -> None:
        """
        Initializes a new instance of the ZerodhaBrokerageModel class
        
        :param accountType: The type of account to be modelled, defaults to AccountType.Margin
        """
        ...

    def CanExecuteOrder(self, security: QuantConnect.Securities.Security, order: QuantConnect.Orders.Order) -> bool:
        """
        Returns true if the brokerage would be able to execute this order at this time assuming
        market prices are sufficient for the fill to take place. This is used to emulate the
        brokerage fills in backtesting and paper trading. For example some brokerages may not perform
        executions during extended market hours. This is not intended to be checking whether or not
        the exchange is open, that is handled in the Security.Exchange property.
        
        :param order: The order to test for execution
        :returns: True if the brokerage would be able to perform the execution, false otherwise.
        """
        ...

    def CanSubmitOrder(self, security: QuantConnect.Securities.Security, order: QuantConnect.Orders.Order, message: typing.Optional[QuantConnect.Brokerages.BrokerageMessageEvent]) -> typing.Union[bool, QuantConnect.Brokerages.BrokerageMessageEvent]:
        """
        Returns true if the brokerage could accept this order. This takes into account
        order type, security type, and order size limits.
        
        :param security: The security being ordered
        :param order: The order to be processed
        :param message: If this function returns false, a brokerage message detailing why the order may not be submitted
        :returns: True if the brokerage could process the order, false otherwise.
        """
        ...

    def CanUpdateOrder(self, security: QuantConnect.Securities.Security, order: QuantConnect.Orders.Order, request: QuantConnect.Orders.UpdateOrderRequest, message: typing.Optional[QuantConnect.Brokerages.BrokerageMessageEvent]) -> typing.Union[bool, QuantConnect.Brokerages.BrokerageMessageEvent]:
        """
        Returns true if the brokerage would allow updating the order as specified by the request
        
        :param security: The security of the order
        :param order: The order to be updated
        :param request: The requested update to be made to the order
        :param message: If this function returns false, a brokerage message detailing why the order may not be updated
        :returns: True if the brokerage would allow updating the order, false otherwise.
        """
        ...

    def GetFeeModel(self, security: QuantConnect.Securities.Security) -> QuantConnect.Orders.Fees.IFeeModel:
        """Provides Zerodha fee model"""
        ...

    def GetLeverage(self, security: QuantConnect.Securities.Security) -> float:
        """Zerodha global leverage rule"""
        ...


