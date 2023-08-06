"""Email Message Reader."""
import base64
import email
from email.message import EmailMessage
from email.policy import default

from promail.core.attachements.attachments import Attachments


class Message:
    """Email Message reader."""

    def __init__(self, msg: dict) -> None:
        """Initalises Message object.

        Args:
            msg: email message data containing id
        """
        self.msg = email.message_from_bytes(
            base64.urlsafe_b64decode(msg["raw"]), _class=EmailMessage, policy=default
        )
        self._attachments = None

    @property
    def html_body(self) -> str:
        """Get HTML Body of email."""
        return str(
            self.msg.get_body(  # type: ignore
                preferencelist=("related", "html", "plain")
            )
        )

    @property
    def plain_text(self):
        """Get Plain text body of email."""
        return str(self.msg.get_body(preferencelist=("plain",)))  # type: ignore

    @property
    def sender(self) -> str:
        """Get sender of email."""
        return self.msg.get("from")

    @property
    def cc(self) -> str:
        """Get emails cc'd."""
        return self.msg.get("cc")

    @property
    def bcc(self) -> str:
        """Get emails ccc'd."""
        return self.msg.get("bcc")

    @property
    def message_id(self) -> str:
        """Get Message ID of email."""
        return self.msg.get("message-id")

    @property
    def to(self) -> str:
        """Get to field of email."""
        return self.msg.get("to")

    @property
    def subject(self) -> str:
        """Get Subject of email."""
        return self.msg.get("subject")

    @property
    def date(self):
        """Get Date of Email."""
        return self.msg.get("date")

    @property
    def attachments(self):
        """Get Email Attachments."""
        if self._attachments is None:
            self._attachments = {}
            for email_message_attachment in self.msg.iter_attachments():
                if email_message_attachment.is_attachment():
                    self._attachments[
                        email_message_attachment.get_filename()
                    ] = Attachments(email_message_attachment)
        return self._attachments

    def data(self) -> dict:
        """Get all Email fields."""
        return {
            "attachments": self.attachments,
            "date": self.date,
            "subject": self.subject,
            "to": self.to,
            "message_id": self.message_id,
            "bcc": self.bcc,
            "cc": self.cc,
            "html_body": self.html_body,
            "plain_text": self.plain_text,
        }

    def __str__(self) -> str:
        """String representation."""
        return self.subject or ""
