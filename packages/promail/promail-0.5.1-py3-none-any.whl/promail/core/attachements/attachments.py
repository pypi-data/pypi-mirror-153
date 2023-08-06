"""Email Attachments."""
import email
from email.message import EmailMessage
from io import BytesIO


class Attachments:
    """Email Attachment Reader."""

    manager = email.contentmanager.raw_data_manager

    def __init__(self, email_attachment: EmailMessage):
        """Initializes Email Attachment."""
        self.email_attachment = email_attachment

    @property
    def filename(self):
        """Get filename."""
        return self.email_attachment.get_filename()

    def save_file(self, path):
        """Saves file to path provided."""
        with open(path, "wb") as file:
            file.write(self.email_attachment.get_content(content_manager=self.manager))

    def get_data(self) -> BytesIO:
        """Get file data as an inmemory as a BytesIO file-like object."""
        obj = BytesIO()
        obj.write(self.email_attachment.get_content(content_manager=self.manager))
        obj.seek(0)
        return obj

    def __str__(self):
        """Get string representation."""
        return self.filename

    def __repr__(self):
        """Get repr representation."""
        return f"Attachments({self.__str__()})"
