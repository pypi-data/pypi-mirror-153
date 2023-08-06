from typing import overload
import System
import System.Net.Security


class SslPolicyErrors(System.Enum):
    """This class has no documentation."""

    # Cannot convert to Python: None = ...

    RemoteCertificateNotAvailable = ...

    RemoteCertificateNameMismatch = ...

    RemoteCertificateChainErrors = ...


class AuthenticationLevel(System.Enum):
    """This class has no documentation."""

    # Cannot convert to Python: None = 0

    MutualAuthRequested = 1

    MutualAuthRequired = 2


