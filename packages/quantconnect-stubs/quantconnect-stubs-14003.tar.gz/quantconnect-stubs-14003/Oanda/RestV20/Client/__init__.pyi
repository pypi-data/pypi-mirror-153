from typing import overload
import abc
import typing

import Oanda.RestV20.Client
import System
import System.Collections.Generic
import System.IO
import System.Threading.Tasks

IRestResponse = typing.Any
FileParameter = typing.Any

Oanda_RestV20_Client_ApiResponse_T = typing.TypeVar("Oanda_RestV20_Client_ApiResponse_T")


class ApiResponse(typing.Generic[Oanda_RestV20_Client_ApiResponse_T], System.Object):
    """API Response"""

    @property
    def StatusCode(self) -> int:
        """Gets or sets the status code (HTTP status code)"""
        ...

    @StatusCode.setter
    def StatusCode(self, value: int):
        """Gets or sets the status code (HTTP status code)"""
        ...

    @property
    def Headers(self) -> System.Collections.Generic.IDictionary[str, str]:
        """Gets or sets the HTTP headers"""
        ...

    @Headers.setter
    def Headers(self, value: System.Collections.Generic.IDictionary[str, str]):
        """Gets or sets the HTTP headers"""
        ...

    @property
    def Data(self) -> Oanda_RestV20_Client_ApiResponse_T:
        """Gets or sets the data (parsed HTTP body)"""
        ...

    @Data.setter
    def Data(self, value: Oanda_RestV20_Client_ApiResponse_T):
        """Gets or sets the data (parsed HTTP body)"""
        ...

    def __init__(self, statusCode: int, headers: System.Collections.Generic.IDictionary[str, str], data: Oanda_RestV20_Client_ApiResponse_T) -> None:
        """
        Initializes a new instance of the ApiResponse<T> class.
        
        :param statusCode: HTTP status code.
        :param headers: HTTP headers.
        :param data: Data (parsed HTTP body)
        """
        ...


class ApiException(System.Exception):
    """API Exception"""

    @property
    def ErrorCode(self) -> int:
        """Gets or sets the error code (HTTP status code)"""
        ...

    @ErrorCode.setter
    def ErrorCode(self, value: int):
        """Gets or sets the error code (HTTP status code)"""
        ...

    @property
    def ErrorContent(self) -> typing.Any:
        """Gets or sets the error content (body json object)"""
        ...

    @ErrorContent.setter
    def ErrorContent(self, value: typing.Any):
        """Gets or sets the error content (body json object)"""
        ...

    @overload
    def __init__(self) -> None:
        """Initializes a new instance of the ApiException class."""
        ...

    @overload
    def __init__(self, errorCode: int, message: str) -> None:
        """
        Initializes a new instance of the ApiException class.
        
        :param errorCode: HTTP status code.
        :param message: Error message.
        """
        ...

    @overload
    def __init__(self, errorCode: int, message: str, errorContent: typing.Any = None) -> None:
        """
        Initializes a new instance of the ApiException class.
        
        :param errorCode: HTTP status code.
        :param message: Error message.
        :param errorContent: Error content.
        """
        ...


class ApiClient(System.Object):
    """API client is mainly responsible for making the HTTP call to the API backend."""

    Default: Oanda.RestV20.Client.ApiClient
    """
    Gets or sets the default API client for making HTTP calls.
    
    ApiClient.Default is deprecated, please use 'Configuration.Default.ApiClient' instead.
    """

    @property
    def Configuration(self) -> Oanda.RestV20.Client.Configuration:
        """Gets or sets the Configuration."""
        ...

    @Configuration.setter
    def Configuration(self, value: Oanda.RestV20.Client.Configuration):
        """Gets or sets the Configuration."""
        ...

    @property
    def RestClient(self) -> typing.Any:
        """Gets or sets the RestClient."""
        ...

    @RestClient.setter
    def RestClient(self, value: typing.Any):
        """Gets or sets the RestClient."""
        ...

    @overload
    def __init__(self) -> None:
        """
        Initializes a new instance of the ApiClient class
        with default configuration and base path (https://localhost/v3).
        """
        ...

    @overload
    def __init__(self, config: Oanda.RestV20.Client.Configuration = None) -> None:
        """
        Initializes a new instance of the ApiClient class
        with default base path (https://localhost/v3).
        
        :param config: An instance of Configuration.
        """
        ...

    @overload
    def __init__(self, basePath: str = "https://localhost/v3") -> None:
        """
        Initializes a new instance of the ApiClient class
        with default configuration.
        
        :param basePath: The base path.
        """
        ...

    @staticmethod
    def Base64Encode(text: str) -> str:
        """
        Encode string in base64 format.
        
        :param text: String to be encoded.
        :returns: Encoded string.
        """
        ...

    def CallApi(self, path: str, method: typing.Any, queryParams: System.Collections.Generic.Dictionary[str, str], postBody: typing.Any, headerParams: System.Collections.Generic.Dictionary[str, str], formParams: System.Collections.Generic.Dictionary[str, str], fileParams: System.Collections.Generic.Dictionary[str, FileParameter], pathParams: System.Collections.Generic.Dictionary[str, str], contentType: str) -> System.Object:
        """
        Makes the HTTP request (Sync).
        
        :param path: URL path.
        :param method: HTTP method.
        :param queryParams: Query parameters.
        :param postBody: HTTP body (POST request).
        :param headerParams: Header parameters.
        :param formParams: Form parameters.
        :param fileParams: File parameters.
        :param pathParams: Path parameters.
        :param contentType: Content Type of the request
        :returns: Object.
        """
        ...

    def CallApiAsync(self, path: str, method: typing.Any, queryParams: System.Collections.Generic.Dictionary[str, str], postBody: typing.Any, headerParams: System.Collections.Generic.Dictionary[str, str], formParams: System.Collections.Generic.Dictionary[str, str], fileParams: System.Collections.Generic.Dictionary[str, FileParameter], pathParams: System.Collections.Generic.Dictionary[str, str], contentType: str) -> System.Threading.Tasks.Task[System.Object]:
        """
        Makes the asynchronous HTTP request.
        
        :param path: URL path.
        :param method: HTTP method.
        :param queryParams: Query parameters.
        :param postBody: HTTP body (POST request).
        :param headerParams: Header parameters.
        :param formParams: Form parameters.
        :param fileParams: File parameters.
        :param pathParams: Path parameters.
        :param contentType: Content type.
        :returns: The Task instance.
        """
        ...

    @staticmethod
    def ConvertType(source: typing.Any, dest: typing.Type) -> typing.Any:
        """
        Dynamically cast the object into target type.
        Ref: http://stackoverflow.com/questions/4925718/c-dynamic-runtime-cast
        
        :param source: Object to be casted
        :param dest: Target type
        :returns: Casted object.
        """
        ...

    def Deserialize(self, response: typing.Any, type: typing.Type) -> System.Object:
        """
        Deserialize the JSON string into a proper object.
        
        :param response: The HTTP response.
        :param type: Object type.
        :returns: Object representation of the JSON string.
        """
        ...

    def EscapeString(self, str: str) -> str:
        """
        Escape string (url-encoded).
        
        :param str: String to be escaped.
        :returns: Escaped string.
        """
        ...

    def InterceptRequest(self, request: typing.Any) -> None:
        """
        Allows for extending request processing for ApiClient generated code.
        
        :param request: The RestSharp request object
        """
        ...

    def InterceptResponse(self, request: typing.Any, response: typing.Any) -> None:
        """
        Allows for extending response processing for ApiClient generated code.
        
        :param request: The RestSharp request object
        :param response: The RestSharp response object
        """
        ...

    def ParameterToFile(self, name: str, stream: System.IO.Stream) -> typing.Any:
        """
        Create FileParameter based on Stream.
        
        :param name: Parameter name.
        :param stream: Input stream.
        :returns: FileParameter.
        """
        ...

    def ParameterToString(self, obj: typing.Any) -> str:
        """
        If parameter is DateTime, output in a formatted string (default ISO 8601), customizable with Configuration.DateTime.
        If parameter is a list, join the list with ",".
        Otherwise just return the string.
        
        :param obj: The parameter (header, path, query, form).
        :returns: Formatted string.
        """
        ...

    @staticmethod
    def ReadAsBytes(input: System.IO.Stream) -> typing.List[int]:
        """
        Convert stream to byte array
        Credit/Ref: http://stackoverflow.com/a/221941/677735
        
        :param input: Input stream to be converted
        :returns: Byte array.
        """
        ...

    @staticmethod
    def SanitizeFilename(filename: str) -> str:
        """
        Sanitize filename by removing the path
        
        :param filename: Filename
        :returns: Filename.
        """
        ...

    def SelectHeaderAccept(self, accepts: typing.List[str]) -> str:
        """
        Select the Accept header's value from the given accepts array:
        if JSON exists in the given array, use it;
        otherwise use all of them (joining into a string)
        
        :param accepts: The accepts array to select from.
        :returns: The Accept header to use.
        """
        ...

    def SelectHeaderContentType(self, contentTypes: typing.List[str]) -> str:
        """
        Select the Content-Type header's value from the given content-type array:
        if JSON exists in the given array, use it;
        otherwise use the first one defined in 'consumes'
        
        :param contentTypes: The Content-Type array to select from.
        :returns: The Content-Type header to use.
        """
        ...

    def Serialize(self, obj: typing.Any) -> str:
        """
        Serialize an input (model) into JSON string
        
        :param obj: Object.
        :returns: JSON string.
        """
        ...

    @staticmethod
    def UrlEncode(input: str) -> str:
        """
        URL encode a string
        Credit/Ref: https://github.com/restsharp/RestSharp/blob/master/RestSharp/Extensions/StringExtensions.cs#L50
        
        :param input: String to be URL encoded
        :returns: Byte array.
        """
        ...


class Configuration(System.Object):
    """Represents a set of configuration settings"""

    Version: str = "1.0.0"
    """Version of the package."""

    Default: Oanda.RestV20.Client.Configuration = ...
    """Gets or sets the default Configuration."""

    DefaultExceptionFactory: typing.Callable[[str, IRestResponse], System.Exception] = ...
    """Default creation of exceptions for a given method name and response object"""

    @property
    def Timeout(self) -> int:
        """Gets or sets the HTTP timeout (milliseconds) of ApiClient. Default to 100000 milliseconds."""
        ...

    @Timeout.setter
    def Timeout(self, value: int):
        """Gets or sets the HTTP timeout (milliseconds) of ApiClient. Default to 100000 milliseconds."""
        ...

    @property
    def ApiClient(self) -> Oanda.RestV20.Client.ApiClient:
        """Gets or sets the default API client for making HTTP calls."""
        ...

    @ApiClient.setter
    def ApiClient(self, value: Oanda.RestV20.Client.ApiClient):
        """Gets or sets the default API client for making HTTP calls."""
        ...

    @property
    def DefaultHeader(self) -> System.Collections.Generic.Dictionary[str, str]:
        """Gets or sets the default header."""
        ...

    @DefaultHeader.setter
    def DefaultHeader(self, value: System.Collections.Generic.Dictionary[str, str]):
        """Gets or sets the default header."""
        ...

    @property
    def UserAgent(self) -> str:
        """Gets or sets the HTTP user agent."""
        ...

    @UserAgent.setter
    def UserAgent(self, value: str):
        """Gets or sets the HTTP user agent."""
        ...

    @property
    def Username(self) -> str:
        """Gets or sets the username (HTTP basic authentication)."""
        ...

    @Username.setter
    def Username(self, value: str):
        """Gets or sets the username (HTTP basic authentication)."""
        ...

    @property
    def Password(self) -> str:
        """Gets or sets the password (HTTP basic authentication)."""
        ...

    @Password.setter
    def Password(self, value: str):
        """Gets or sets the password (HTTP basic authentication)."""
        ...

    @property
    def AccessToken(self) -> str:
        """Gets or sets the access token for OAuth2 authentication."""
        ...

    @AccessToken.setter
    def AccessToken(self, value: str):
        """Gets or sets the access token for OAuth2 authentication."""
        ...

    @property
    def ApiKey(self) -> System.Collections.Generic.Dictionary[str, str]:
        """Gets or sets the API key based on the authentication name."""
        ...

    @ApiKey.setter
    def ApiKey(self, value: System.Collections.Generic.Dictionary[str, str]):
        """Gets or sets the API key based on the authentication name."""
        ...

    @property
    def ApiKeyPrefix(self) -> System.Collections.Generic.Dictionary[str, str]:
        """Gets or sets the prefix (e.g. Token) of the API key based on the authentication name."""
        ...

    @ApiKeyPrefix.setter
    def ApiKeyPrefix(self, value: System.Collections.Generic.Dictionary[str, str]):
        """Gets or sets the prefix (e.g. Token) of the API key based on the authentication name."""
        ...

    @property
    def TempFolderPath(self) -> str:
        """Gets or sets the temporary folder path to store the files downloaded from the server."""
        ...

    @TempFolderPath.setter
    def TempFolderPath(self, value: str):
        """Gets or sets the temporary folder path to store the files downloaded from the server."""
        ...

    @property
    def DateTimeFormat(self) -> str:
        """
        Gets or sets the the date time format used when serializing in the ApiClient
        By default, it's set to ISO 8601 - "o", for others see:
        https://msdn.microsoft.com/en-us/library/az4se3k1(v=vs.110).aspx
        and https://msdn.microsoft.com/en-us/library/8kb3ddd4(v=vs.110).aspx
        No validation is done to ensure that the string you're providing is valid
        """
        ...

    @DateTimeFormat.setter
    def DateTimeFormat(self, value: str):
        """
        Gets or sets the the date time format used when serializing in the ApiClient
        By default, it's set to ISO 8601 - "o", for others see:
        https://msdn.microsoft.com/en-us/library/az4se3k1(v=vs.110).aspx
        and https://msdn.microsoft.com/en-us/library/8kb3ddd4(v=vs.110).aspx
        No validation is done to ensure that the string you're providing is valid
        """
        ...

    @overload
    def __init__(self, apiClient: Oanda.RestV20.Client.ApiClient = None, defaultHeader: System.Collections.Generic.Dictionary[str, str] = None, username: str = None, password: str = None, accessToken: str = None, apiKey: System.Collections.Generic.Dictionary[str, str] = None, apiKeyPrefix: System.Collections.Generic.Dictionary[str, str] = None, tempFolderPath: str = None, dateTimeFormat: str = None, timeout: int = 100000, userAgent: str = "Swagger-Codegen/1.0.0/csharp") -> None:
        """
        Initializes a new instance of the Configuration class with different settings
        
        :param apiClient: Api client
        :param defaultHeader: Dictionary of default HTTP header
        :param username: Username
        :param password: Password
        :param accessToken: accessToken
        :param apiKey: Dictionary of API key
        :param apiKeyPrefix: Dictionary of API key prefix
        :param tempFolderPath: Temp folder path
        :param dateTimeFormat: DateTime format string
        :param timeout: HTTP connection timeout (in milliseconds)
        :param userAgent: HTTP user agent
        """
        ...

    @overload
    def __init__(self, apiClient: Oanda.RestV20.Client.ApiClient) -> None:
        """
        Initializes a new instance of the Configuration class.
        
        :param apiClient: Api client.
        """
        ...

    def AddApiKey(self, key: str, value: str) -> None:
        """
        Add Api Key Header.
        
        :param key: Api Key name.
        :param value: Api Key value.
        """
        ...

    def AddApiKeyPrefix(self, key: str, value: str) -> None:
        """
        Sets the API key prefix.
        
        :param key: Api Key name.
        :param value: Api Key value.
        """
        ...

    def AddDefaultHeader(self, key: str, value: str) -> None:
        """
        Add default header.
        
        :param key: Header field name.
        :param value: Header field value.
        """
        ...

    def GetApiKeyWithPrefix(self, apiKeyIdentifier: str) -> str:
        """
        Get the API key with prefix.
        
        :param apiKeyIdentifier: API key identifier (authentication scheme).
        :returns: API key with prefix.
        """
        ...

    def setApiClientUsingDefault(self, apiClient: Oanda.RestV20.Client.ApiClient = None) -> None:
        """
        Set the ApiClient using Default or ApiClient instance.
        
        :param apiClient: An instance of ApiClient.
        """
        ...

    @staticmethod
    def ToDebugReport() -> str:
        """Returns a string with essential information for debugging."""
        ...


class IApiAccessor(metaclass=abc.ABCMeta):
    """Represents configuration aspects required to interact with the API endpoints."""

    @property
    @abc.abstractmethod
    def Configuration(self) -> Oanda.RestV20.Client.Configuration:
        """Gets or sets the configuration object"""
        ...

    @Configuration.setter
    @abc.abstractmethod
    def Configuration(self, value: Oanda.RestV20.Client.Configuration):
        """Gets or sets the configuration object"""
        ...

    @property
    @abc.abstractmethod
    def ExceptionFactory(self) -> typing.Callable[[str, IRestResponse], System.Exception]:
        """Provides a factory method hook for the creation of exceptions."""
        ...

    @ExceptionFactory.setter
    @abc.abstractmethod
    def ExceptionFactory(self, value: typing.Callable[[str, IRestResponse], System.Exception]):
        """Provides a factory method hook for the creation of exceptions."""
        ...

    def GetBasePath(self) -> str:
        """Gets the base path of the API client."""
        ...


