"""Abstract Classes for Inbound and outbound mail."""
import abc
import mimetypes
import os
from email.message import EmailMessage
from typing import Callable, List, Optional

from promail.core.embedded_attachments import EmbeddedAttachments
from promail.core.messages.messages import Message
from promail.filters.email_filter import EmailFilter


class EmailManager:
    """Super class inherited by OutBoundInbound manager."""

    def __init__(self, account):
        """Initializes email manager."""
        self._account = account


class OutBoundManager(abc.ABC, EmailManager):
    """Outbound Mail class template."""

    def __init__(self, account):
        """Initializes OutBoundManager."""
        super(OutBoundManager, self).__init__(account)

    def send_email(
        self,
        recipients: str = "",
        cc: str = "",
        bcc: str = "",
        subject: str = "",
        htmltext: str = "",
        plaintext: str = "",
        embedded_attachments: Optional[List[EmbeddedAttachments]] = None,
        attachements: Optional[list] = None,
    ) -> None:
        """Send an email."""
        pass

    @staticmethod
    def guess_types(path: str) -> tuple:
        """Will attempt to guess ctype, subtype and maintype of file.

        Based on https://docs.python.org/3/library/email.examples.html

        Args:
            path: path to attachment file

        Returns:
            tuple: maintype, subtype of file
        """
        ctype, encoding = mimetypes.guess_type(path)
        if ctype is None or encoding is not None:
            # No guess could be made, or the file is encoded (compressed), so
            # use a generic bag-of-bits type.
            ctype = "application/octet-stream"
        maintype, subtype = ctype.split("/", 1)
        return maintype, subtype

    def add_attachments(self, msg: EmailMessage, attachments: list) -> None:
        """Add attachment to email."""
        for path in attachments:
            filename = os.path.basename(path)
            maintype, subtype = self.guess_types(path)
            with open(path, "rb") as fp:
                msg.add_attachment(
                    fp.read(), maintype=maintype, subtype=subtype, filename=filename
                )

    def create_message(
        self,
        recipients: str = "",
        cc: str = "",
        bcc: str = "",
        subject: str = "",
        htmltext: str = "",
        plaintext: str = "",
        embedded_attachments: Optional[List[EmbeddedAttachments]] = None,
        attachements: Optional[list] = None,
    ) -> EmailMessage:
        """Create Email Message."""
        if attachements is None:
            attachements = []
        if embedded_attachments is None:
            embedded_attachments = []
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = self._account
        msg["To"] = recipients
        msg["Cc"] = cc
        msg["Bcc"] = bcc
        msg.set_content(plaintext)
        msg.add_alternative(htmltext, subtype="html")
        for embedded_attachment in embedded_attachments:
            maintype, subtype = self.guess_types(embedded_attachment.filepath)
            msg.get_payload()[1].add_related(
                embedded_attachment.read(),
                maintype,
                subtype,
                cid=embedded_attachment.cid,
            )

        self.add_attachments(msg, attachements)
        return msg


class InBoundManager(abc.ABC):
    """InBound Mail class template."""

    def __init__(self, account):
        """Initializes Inbound Email manager."""
        self._registered_functions: dict = {}
        self._last_email = None
        self._filter_class = None
        super(InBoundManager, self).__init__(account)

    @property
    def registered_functions(self) -> dict:
        """Get Dictionary of (key) filters and (value) registered functions."""
        return self._registered_functions

    def retrieve_last_items(self: object, max_items: int = 100) -> List[Message]:
        """Get a list of last n items received in inbox.

        Args:
            max_items: The Maximum number of items to return

        Raises:
            NotImplementedError: If not implemented by subclass.
        """
        raise NotImplementedError(__name__ + " not Implemented")

    def _process_filter_messages(
        self,
        email_filter: EmailFilter,
        page_size: int = 100,
        page_token: Optional[str] = None,
    ):
        """Queries Email Server for new messages.

         That match filter requisites passes each matched message
         to their registered functions.

        Args:
            email_filter: Email Filter Object, must be a key
                of self._registered_functions.
            page_size: Number of emails to pull per query,
                max number platform dependent (GMAIL: 500).
            page_token: Pagenation Token
                (may not be used on all platforms).

        Raises:
            NotImplementedError: If not implemented by subclass.
        """
        raise NotImplementedError

    def process(self, page_size: int = 100) -> None:
        """Process all filters."""
        for email_filter in self._registered_functions:
            self._process_filter_messages(
                email_filter, page_size=page_size, page_token=None
            )

    def register(self, **filter_args):
        """Registers a listener function."""

        def decorator(func: Callable):
            def wrapper(email: EmailMessage):
                func(email)

            f = self._filter_class(**filter_args)

            if f not in self._registered_functions:
                self._registered_functions[f] = set()
            self._registered_functions[f].add(wrapper)

        return decorator
