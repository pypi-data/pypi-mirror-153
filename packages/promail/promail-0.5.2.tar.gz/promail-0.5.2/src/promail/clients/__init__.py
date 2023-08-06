"""Email Clients."""
from .gmail import GmailClient
from .microsoft import HotmailClient
from .smtp_client import SmtpClient

try:
    from importlib.metadata import version, PackageNotFoundError  # type: ignore
except ImportError:  # pragma: no cover
    from importlib_metadata import version, PackageNotFoundError  # type: ignore

try:
    __version__ = version(__name__)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"

__all__ = ["email_manager", "gmail", "GmailClient", "HotmailClient", "SmtpClient"]
