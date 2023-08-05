from typing import overload
import datetime
import typing

import System
import System.Buffers
import System.Buffers.Text


class Utf8Parser(System.Object):
    """Methods to parse common data types to Utf8 strings."""

    @staticmethod
    @overload
    def TryParse(source: System.ReadOnlySpan[int], value: typing.Optional[float], bytesConsumed: typing.Optional[int], standardFormat: str = ...) -> typing.Union[bool, float, int]:
        """
        Parses a Single at the start of a Utf8 string.
        
        :param source: The Utf8 string to parse
        :param value: Receives the parsed value
        :param bytesConsumed: On a successful parse, receives the length in bytes of the substring that was parsed
        :param standardFormat: Expected format of the Utf8 string
        :returns: true for success. "bytesConsumed" contains the length in bytes of the substring that was parsed. false if the string was not syntactically valid or an overflow or underflow occurred. "bytesConsumed" is set to 0.
        """
        ...

    @staticmethod
    @overload
    def TryParse(source: System.ReadOnlySpan[int], value: typing.Optional[float], bytesConsumed: typing.Optional[int], standardFormat: str = ...) -> typing.Union[bool, float, int]:
        """
        Parses a Double at the start of a Utf8 string.
        
        :param source: The Utf8 string to parse
        :param value: Receives the parsed value
        :param bytesConsumed: On a successful parse, receives the length in bytes of the substring that was parsed
        :param standardFormat: Expected format of the Utf8 string
        :returns: true for success. "bytesConsumed" contains the length in bytes of the substring that was parsed. false if the string was not syntactically valid or an overflow or underflow occurred. "bytesConsumed" is set to 0.
        """
        ...

    @staticmethod
    @overload
    def TryParse(source: System.ReadOnlySpan[int], value: typing.Optional[typing.Union[datetime.datetime, datetime.date]], bytesConsumed: typing.Optional[int], standardFormat: str = ...) -> typing.Union[bool, typing.Union[datetime.datetime, datetime.date], int]:
        """
        Parses a DateTime at the start of a Utf8 string.
        
        :param source: The Utf8 string to parse
        :param value: Receives the parsed value
        :param bytesConsumed: On a successful parse, receives the length in bytes of the substring that was parsed
        :param standardFormat: Expected format of the Utf8 string
        :returns: true for success. "bytesConsumed" contains the length in bytes of the substring that was parsed. false if the string was not syntactically valid or an overflow or underflow occurred. "bytesConsumed" is set to 0.
        """
        ...

    @staticmethod
    @overload
    def TryParse(source: System.ReadOnlySpan[int], value: typing.Optional[System.DateTimeOffset], bytesConsumed: typing.Optional[int], standardFormat: str = ...) -> typing.Union[bool, System.DateTimeOffset, int]:
        """
        Parses a DateTimeOffset at the start of a Utf8 string.
        
        :param source: The Utf8 string to parse
        :param value: Receives the parsed value
        :param bytesConsumed: On a successful parse, receives the length in bytes of the substring that was parsed
        :param standardFormat: Expected format of the Utf8 string
        :returns: true for success. "bytesConsumed" contains the length in bytes of the substring that was parsed. false if the string was not syntactically valid or an overflow or underflow occurred. "bytesConsumed" is set to 0.
        """
        ...

    @staticmethod
    @overload
    def TryParse(source: System.ReadOnlySpan[int], value: typing.Optional[datetime.timedelta], bytesConsumed: typing.Optional[int], standardFormat: str = ...) -> typing.Union[bool, datetime.timedelta, int]:
        """
        Parses a TimeSpan at the start of a Utf8 string.
        
        :param source: The Utf8 string to parse
        :param value: Receives the parsed value
        :param bytesConsumed: On a successful parse, receives the length in bytes of the substring that was parsed
        :param standardFormat: Expected format of the Utf8 string
        :returns: true for success. "bytesConsumed" contains the length in bytes of the substring that was parsed. false if the string was not syntactically valid or an overflow or underflow occurred. "bytesConsumed" is set to 0.
        """
        ...

    @staticmethod
    @overload
    def TryParse(source: System.ReadOnlySpan[int], value: typing.Optional[System.Guid], bytesConsumed: typing.Optional[int], standardFormat: str = ...) -> typing.Union[bool, System.Guid, int]:
        """
        Parses a Guid at the start of a Utf8 string.
        
        :param source: The Utf8 string to parse
        :param value: Receives the parsed value
        :param bytesConsumed: On a successful parse, receives the length in bytes of the substring that was parsed
        :param standardFormat: Expected format of the Utf8 string
        :returns: true for success. "bytesConsumed" contains the length in bytes of the substring that was parsed. false if the string was not syntactically valid or an overflow or underflow occurred. "bytesConsumed" is set to 0.
        """
        ...

    @staticmethod
    @overload
    def TryParse(source: System.ReadOnlySpan[int], value: typing.Optional[int], bytesConsumed: typing.Optional[int], standardFormat: str = ...) -> typing.Union[bool, int, int]:
        """
        Parses a Byte at the start of a Utf8 string.
        
        :param source: The Utf8 string to parse
        :param value: Receives the parsed value
        :param bytesConsumed: On a successful parse, receives the length in bytes of the substring that was parsed
        :param standardFormat: Expected format of the Utf8 string
        :returns: true for success. "bytesConsumed" contains the length in bytes of the substring that was parsed. false if the string was not syntactically valid or an overflow or underflow occurred. "bytesConsumed" is set to 0.
        """
        ...

    @staticmethod
    @overload
    def TryParse(source: System.ReadOnlySpan[int], value: typing.Optional[int], bytesConsumed: typing.Optional[int], standardFormat: str = ...) -> typing.Union[bool, int, int]:
        """
        Parses a UInt16 at the start of a Utf8 string.
        
        :param source: The Utf8 string to parse
        :param value: Receives the parsed value
        :param bytesConsumed: On a successful parse, receives the length in bytes of the substring that was parsed
        :param standardFormat: Expected format of the Utf8 string
        :returns: true for success. "bytesConsumed" contains the length in bytes of the substring that was parsed. false if the string was not syntactically valid or an overflow or underflow occurred. "bytesConsumed" is set to 0.
        """
        ...

    @staticmethod
    @overload
    def TryParse(source: System.ReadOnlySpan[int], value: typing.Optional[int], bytesConsumed: typing.Optional[int], standardFormat: str = ...) -> typing.Union[bool, int, int]:
        """
        Parses a UInt32 at the start of a Utf8 string.
        
        :param source: The Utf8 string to parse
        :param value: Receives the parsed value
        :param bytesConsumed: On a successful parse, receives the length in bytes of the substring that was parsed
        :param standardFormat: Expected format of the Utf8 string
        :returns: true for success. "bytesConsumed" contains the length in bytes of the substring that was parsed. false if the string was not syntactically valid or an overflow or underflow occurred. "bytesConsumed" is set to 0.
        """
        ...

    @staticmethod
    @overload
    def TryParse(source: System.ReadOnlySpan[int], value: typing.Optional[int], bytesConsumed: typing.Optional[int], standardFormat: str = ...) -> typing.Union[bool, int, int]:
        """
        Parses a UInt64 at the start of a Utf8 string.
        
        :param source: The Utf8 string to parse
        :param value: Receives the parsed value
        :param bytesConsumed: On a successful parse, receives the length in bytes of the substring that was parsed
        :param standardFormat: Expected format of the Utf8 string
        :returns: true for success. "bytesConsumed" contains the length in bytes of the substring that was parsed. false if the string was not syntactically valid or an overflow or underflow occurred. "bytesConsumed" is set to 0.
        """
        ...

    @staticmethod
    @overload
    def TryParse(source: System.ReadOnlySpan[int], value: typing.Optional[float], bytesConsumed: typing.Optional[int], standardFormat: str = ...) -> typing.Union[bool, float, int]:
        """
        Parses a Decimal at the start of a Utf8 string.
        
        :param source: The Utf8 string to parse
        :param value: Receives the parsed value
        :param bytesConsumed: On a successful parse, receives the length in bytes of the substring that was parsed
        :param standardFormat: Expected format of the Utf8 string
        :returns: true for success. "bytesConsumed" contains the length in bytes of the substring that was parsed. false if the string was not syntactically valid or an overflow or underflow occurred. "bytesConsumed" is set to 0.
        """
        ...

    @staticmethod
    @overload
    def TryParse(source: System.ReadOnlySpan[int], value: typing.Optional[int], bytesConsumed: typing.Optional[int], standardFormat: str = ...) -> typing.Union[bool, int, int]:
        """
        Parses a SByte at the start of a Utf8 string.
        
        :param source: The Utf8 string to parse
        :param value: Receives the parsed value
        :param bytesConsumed: On a successful parse, receives the length in bytes of the substring that was parsed
        :param standardFormat: Expected format of the Utf8 string
        :returns: true for success. "bytesConsumed" contains the length in bytes of the substring that was parsed. false if the string was not syntactically valid or an overflow or underflow occurred. "bytesConsumed" is set to 0.
        """
        ...

    @staticmethod
    @overload
    def TryParse(source: System.ReadOnlySpan[int], value: typing.Optional[int], bytesConsumed: typing.Optional[int], standardFormat: str = ...) -> typing.Union[bool, int, int]:
        """
        Parses an Int16 at the start of a Utf8 string.
        
        :param source: The Utf8 string to parse
        :param value: Receives the parsed value
        :param bytesConsumed: On a successful parse, receives the length in bytes of the substring that was parsed
        :param standardFormat: Expected format of the Utf8 string
        :returns: true for success. "bytesConsumed" contains the length in bytes of the substring that was parsed. false if the string was not syntactically valid or an overflow or underflow occurred. "bytesConsumed" is set to 0.
        """
        ...

    @staticmethod
    @overload
    def TryParse(source: System.ReadOnlySpan[int], value: typing.Optional[int], bytesConsumed: typing.Optional[int], standardFormat: str = ...) -> typing.Union[bool, int, int]:
        """
        Parses an Int32 at the start of a Utf8 string.
        
        :param source: The Utf8 string to parse
        :param value: Receives the parsed value
        :param bytesConsumed: On a successful parse, receives the length in bytes of the substring that was parsed
        :param standardFormat: Expected format of the Utf8 string
        :returns: true for success. "bytesConsumed" contains the length in bytes of the substring that was parsed. false if the string was not syntactically valid or an overflow or underflow occurred. "bytesConsumed" is set to 0.
        """
        ...

    @staticmethod
    @overload
    def TryParse(source: System.ReadOnlySpan[int], value: typing.Optional[int], bytesConsumed: typing.Optional[int], standardFormat: str = ...) -> typing.Union[bool, int, int]:
        """
        Parses an Int64 at the start of a Utf8 string.
        
        :param source: The Utf8 string to parse
        :param value: Receives the parsed value
        :param bytesConsumed: On a successful parse, receives the length in bytes of the substring that was parsed
        :param standardFormat: Expected format of the Utf8 string
        :returns: true for success. "bytesConsumed" contains the length in bytes of the substring that was parsed. false if the string was not syntactically valid or an overflow or underflow occurred. "bytesConsumed" is set to 0.
        """
        ...

    @staticmethod
    @overload
    def TryParse(source: System.ReadOnlySpan[int], value: typing.Optional[bool], bytesConsumed: typing.Optional[int], standardFormat: str = ...) -> typing.Union[bool, bool, int]:
        """
        Parses a Boolean at the start of a Utf8 string.
        
        :param source: The Utf8 string to parse
        :param value: Receives the parsed value
        :param bytesConsumed: On a successful parse, receives the length in bytes of the substring that was parsed
        :param standardFormat: Expected format of the Utf8 string
        :returns: true for success. "bytesConsumed" contains the length in bytes of the substring that was parsed. false if the string was not syntactically valid or an overflow or underflow occurred. "bytesConsumed" is set to 0.
        """
        ...


class Utf8Formatter(System.Object):
    """Methods to format common data types as Utf8 strings."""

    @staticmethod
    @overload
    def TryFormat(value: bool, destination: System.Span[int], bytesWritten: typing.Optional[int], format: System.Buffers.StandardFormat = ...) -> typing.Union[bool, int]:
        """
        Formats a Boolean as a UTF8 string.
        
        :param value: Value to format
        :param destination: Buffer to write the UTF8-formatted value to
        :param bytesWritten: Receives the length of the formatted text in bytes
        :param format: The standard format to use
        :returns: true for success. "bytesWritten" contains the length of the formatted text in bytes. false if buffer was too short. Iteratively increase the size of the buffer and retry until it succeeds.
        """
        ...

    @staticmethod
    @overload
    def TryFormat(value: float, destination: System.Span[int], bytesWritten: typing.Optional[int], format: System.Buffers.StandardFormat = ...) -> typing.Union[bool, int]:
        """
        Formats a Decimal as a UTF8 string.
        
        :param value: Value to format
        :param destination: Buffer to write the UTF8-formatted value to
        :param bytesWritten: Receives the length of the formatted text in bytes
        :param format: The standard format to use
        :returns: true for success. "bytesWritten" contains the length of the formatted text in bytes. false if buffer was too short. Iteratively increase the size of the buffer and retry until it succeeds.
        """
        ...

    @staticmethod
    @overload
    def TryFormat(value: System.Guid, destination: System.Span[int], bytesWritten: typing.Optional[int], format: System.Buffers.StandardFormat = ...) -> typing.Union[bool, int]:
        ...

    @staticmethod
    @overload
    def TryFormat(value: int, destination: System.Span[int], bytesWritten: typing.Optional[int], format: System.Buffers.StandardFormat = ...) -> typing.Union[bool, int]:
        """
        Formats a Byte as a UTF8 string.
        
        :param value: Value to format
        :param destination: Buffer to write the UTF8-formatted value to
        :param bytesWritten: Receives the length of the formatted text in bytes
        :param format: The standard format to use
        :returns: true for success. "bytesWritten" contains the length of the formatted text in bytes. false if buffer was too short. Iteratively increase the size of the buffer and retry until it succeeds.
        """
        ...

    @staticmethod
    @overload
    def TryFormat(value: int, destination: System.Span[int], bytesWritten: typing.Optional[int], format: System.Buffers.StandardFormat = ...) -> typing.Union[bool, int]:
        """
        Formats an SByte as a UTF8 string.
        
        :param value: Value to format
        :param destination: Buffer to write the UTF8-formatted value to
        :param bytesWritten: Receives the length of the formatted text in bytes
        :param format: The standard format to use
        :returns: true for success. "bytesWritten" contains the length of the formatted text in bytes. false if buffer was too short. Iteratively increase the size of the buffer and retry until it succeeds.
        """
        ...

    @staticmethod
    @overload
    def TryFormat(value: int, destination: System.Span[int], bytesWritten: typing.Optional[int], format: System.Buffers.StandardFormat = ...) -> typing.Union[bool, int]:
        """
        Formats a Unt16 as a UTF8 string.
        
        :param value: Value to format
        :param destination: Buffer to write the UTF8-formatted value to
        :param bytesWritten: Receives the length of the formatted text in bytes
        :param format: The standard format to use
        :returns: true for success. "bytesWritten" contains the length of the formatted text in bytes. false if buffer was too short. Iteratively increase the size of the buffer and retry until it succeeds.
        """
        ...

    @staticmethod
    @overload
    def TryFormat(value: int, destination: System.Span[int], bytesWritten: typing.Optional[int], format: System.Buffers.StandardFormat = ...) -> typing.Union[bool, int]:
        """
        Formats an Int16 as a UTF8 string.
        
        :param value: Value to format
        :param destination: Buffer to write the UTF8-formatted value to
        :param bytesWritten: Receives the length of the formatted text in bytes
        :param format: The standard format to use
        :returns: true for success. "bytesWritten" contains the length of the formatted text in bytes. false if buffer was too short. Iteratively increase the size of the buffer and retry until it succeeds.
        """
        ...

    @staticmethod
    @overload
    def TryFormat(value: int, destination: System.Span[int], bytesWritten: typing.Optional[int], format: System.Buffers.StandardFormat = ...) -> typing.Union[bool, int]:
        """
        Formats a UInt32 as a UTF8 string.
        
        :param value: Value to format
        :param destination: Buffer to write the UTF8-formatted value to
        :param bytesWritten: Receives the length of the formatted text in bytes
        :param format: The standard format to use
        :returns: true for success. "bytesWritten" contains the length of the formatted text in bytes. false if buffer was too short. Iteratively increase the size of the buffer and retry until it succeeds.
        """
        ...

    @staticmethod
    @overload
    def TryFormat(value: int, destination: System.Span[int], bytesWritten: typing.Optional[int], format: System.Buffers.StandardFormat = ...) -> typing.Union[bool, int]:
        """
        Formats an Int32 as a UTF8 string.
        
        :param value: Value to format
        :param destination: Buffer to write the UTF8-formatted value to
        :param bytesWritten: Receives the length of the formatted text in bytes
        :param format: The standard format to use
        :returns: true for success. "bytesWritten" contains the length of the formatted text in bytes. false if buffer was too short. Iteratively increase the size of the buffer and retry until it succeeds.
        """
        ...

    @staticmethod
    @overload
    def TryFormat(value: int, destination: System.Span[int], bytesWritten: typing.Optional[int], format: System.Buffers.StandardFormat = ...) -> typing.Union[bool, int]:
        """
        Formats a UInt64 as a UTF8 string.
        
        :param value: Value to format
        :param destination: Buffer to write the UTF8-formatted value to
        :param bytesWritten: Receives the length of the formatted text in bytes
        :param format: The standard format to use
        :returns: true for success. "bytesWritten" contains the length of the formatted text in bytes. false if buffer was too short. Iteratively increase the size of the buffer and retry until it succeeds.
        """
        ...

    @staticmethod
    @overload
    def TryFormat(value: int, destination: System.Span[int], bytesWritten: typing.Optional[int], format: System.Buffers.StandardFormat = ...) -> typing.Union[bool, int]:
        """
        Formats an Int64 as a UTF8 string.
        
        :param value: Value to format
        :param destination: Buffer to write the UTF8-formatted value to
        :param bytesWritten: Receives the length of the formatted text in bytes
        :param format: The standard format to use
        :returns: true for success. "bytesWritten" contains the length of the formatted text in bytes. false if buffer was too short. Iteratively increase the size of the buffer and retry until it succeeds.
        """
        ...

    @staticmethod
    @overload
    def TryFormat(value: datetime.timedelta, destination: System.Span[int], bytesWritten: typing.Optional[int], format: System.Buffers.StandardFormat = ...) -> typing.Union[bool, int]:
        """
        Formats a TimeSpan as a UTF8 string.
        
        :param value: Value to format
        :param destination: Buffer to write the UTF8-formatted value to
        :param bytesWritten: Receives the length of the formatted text in bytes
        :param format: The standard format to use
        :returns: true for success. "bytesWritten" contains the length of the formatted text in bytes. false if buffer was too short. Iteratively increase the size of the buffer and retry until it succeeds.
        """
        ...

    @staticmethod
    @overload
    def TryFormat(value: System.DateTimeOffset, destination: System.Span[int], bytesWritten: typing.Optional[int], format: System.Buffers.StandardFormat = ...) -> typing.Union[bool, int]:
        """
        Formats a DateTimeOffset as a UTF8 string.
        
        :param value: Value to format
        :param destination: Buffer to write the UTF8-formatted value to
        :param bytesWritten: Receives the length of the formatted text in bytes
        :param format: The standard format to use
        :returns: true for success. "bytesWritten" contains the length of the formatted text in bytes. false if buffer was too short. Iteratively increase the size of the buffer and retry until it succeeds.
        """
        ...

    @staticmethod
    @overload
    def TryFormat(value: typing.Union[datetime.datetime, datetime.date], destination: System.Span[int], bytesWritten: typing.Optional[int], format: System.Buffers.StandardFormat = ...) -> typing.Union[bool, int]:
        """
        Formats a DateTime as a UTF8 string.
        
        :param value: Value to format
        :param destination: Buffer to write the UTF8-formatted value to
        :param bytesWritten: Receives the length of the formatted text in bytes
        :param format: The standard format to use
        :returns: true for success. "bytesWritten" contains the length of the formatted text in bytes. false if buffer was too short. Iteratively increase the size of the buffer and retry until it succeeds.
        """
        ...

    @staticmethod
    @overload
    def TryFormat(value: float, destination: System.Span[int], bytesWritten: typing.Optional[int], format: System.Buffers.StandardFormat = ...) -> typing.Union[bool, int]:
        """
        Formats a Double as a UTF8 string.
        
        :param value: Value to format
        :param destination: Buffer to write the UTF8-formatted value to
        :param bytesWritten: Receives the length of the formatted text in bytes
        :param format: The standard format to use
        :returns: true for success. "bytesWritten" contains the length of the formatted text in bytes. false if buffer was too short. Iteratively increase the size of the buffer and retry until it succeeds.
        """
        ...

    @staticmethod
    @overload
    def TryFormat(value: float, destination: System.Span[int], bytesWritten: typing.Optional[int], format: System.Buffers.StandardFormat = ...) -> typing.Union[bool, int]:
        """
        Formats a Single as a UTF8 string.
        
        :param value: Value to format
        :param destination: Buffer to write the UTF8-formatted value to
        :param bytesWritten: Receives the length of the formatted text in bytes
        :param format: The standard format to use
        :returns: true for success. "bytesWritten" contains the length of the formatted text in bytes. false if buffer was too short. Iteratively increase the size of the buffer and retry until it succeeds.
        """
        ...


