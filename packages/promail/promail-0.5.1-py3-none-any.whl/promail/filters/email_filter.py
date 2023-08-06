"""Email Filter."""

import abc
import hashlib
import os.path
import pickle
from datetime import datetime
from typing import Optional


class EmailFilter(abc.ABC):
    """Email Filter Generates a query string used to query the email backend.

    Email filter is used by the email client to store
    which emails have been run with which filters.
    The Filter uses `name` and `version` to uniquely identify itself.
    Queries based on: https://seosly.com/gmail-search-operators/
    """

    def __init__(
        self,
        name: str,
        run_completed: bool = False,
        around: Optional[dict] = None,
        attachment: Optional[bool] = None,
        bcc: Optional[tuple] = None,
        category: Optional[str] = None,
        cc: Optional[tuple] = None,
        filename: Optional[tuple] = None,
        folder: Optional[tuple] = None,
        important: Optional[bool] = None,
        label: Optional[tuple] = None,
        keyword: Optional[tuple] = None,
        newer_than: Optional[str] = None,
        not_sender: Optional[tuple] = None,
        older_than: Optional[str] = None,
        phrase: Optional[tuple] = None,
        sender: Optional[tuple] = None,
        size: Optional[int] = None,
        size_larger: Optional[str] = None,
        size_smaller: Optional[str] = None,
        sent_after: Optional[datetime] = None,
        sent_before: Optional[datetime] = None,
        starred: Optional[bool] = None,
        to: Optional[tuple] = None,
        read: Optional[bool] = None,
        version: Optional[str] = None,
    ):
        """Initializes email filter.

        Args:
            name: User defined name of filter.
                The name along with version is used to identify
                the filter internally to check which messages
                have been already run with a particular filter.
            run_completed: If True it will include messages
                that have already been processed.
            around: Will check body text for first term,
                within apart words of second term
                requires dictionary in form of
                {"first_term": "Term", "apart": 20, "second_term": "Other"}
            attachment: True will filter only emails with attachments,
                False without attachments, None will show all.
            bcc: Will look for emails that include terms in bcc,
                expects tuple of strings if more than one term
                provided will search based on "OR"
            category: filter on category
            cc: filter on cc
            filename: filter on filename
            folder: filter on folder
            important: filter on if important
            label: filter on label
            keyword: filter on keyword
            newer_than: filter on newer than
            not_sender: filter our senders
            older_than: filter older than
            phrase: filter by including phrase
            sender: filter on sender
            size: Minimum size of email in bytes
            size_larger: filter on size
            size_smaller: filter size
            sent_after: filter on date sent
            sent_before: filter on date sent
            starred: filter if starred
            to: filter on to fieled
            read: filter on if read
            version: Version will control whether
        """
        self.name = name
        self._newer_than = newer_than
        self._not_sender = not_sender
        self._older_than = older_than
        self._phrase = phrase
        self._size = size
        self._size_larger = size_larger
        self._size_smaller = size_smaller
        self._sent_after = sent_after
        self._sent_before = sent_before
        self._starred = starred
        self._keyword = keyword
        self._important = important
        self._filename = filename
        self._category = category
        self._bcc = bcc
        self._around = around
        self._attachment = attachment
        self._label = label
        self._folder = folder
        self._cc = cc
        self._to = to
        self._read = read
        self._sender = sender
        self._version = version

        self.save_folder = "processed_emails"

        self._validate()
        if run_completed:
            self.processed = set()
        else:
            self.processed = self.load_processed_ids()

    def _validate(self):
        """Validates inputs."""
        pass

    def filter_results(self, messages):
        """Removes messages in self.processed."""
        raise NotImplementedError

    @property
    def processed_filename(self):
        """Relative path to pickle file."""
        return f"{self.save_folder}/{hash(self)}.bin"

    def __hash__(self) -> int:
        """Hash based on name, version."""
        fields = (
            self.name,
            self._version,
        )
        return int(hashlib.md5(str(fields).encode()).hexdigest(), 16)

    def load_processed_ids(self):
        """Loads A Set of ids that have been processed with this filter."""
        try:
            with open(self.processed_filename, "rb") as file:
                return pickle.load(file)
        except FileNotFoundError:
            return set()

    def add_processed(self, email_id: str) -> None:
        """Add Message to list of processed Messages."""
        self.processed.add(email_id)
        if not os.path.exists(self.save_folder):
            os.makedirs(self.save_folder)
        with open(self.processed_filename, "wb") as file:
            pickle.dump(self.processed, file)

    def get_filter_string(self) -> str:
        """Creates string to query email based on parameters.

        Returns: Query String.

        Raises:
            NotImplementedError: method not implemented.
        """
        raise NotImplementedError(__name__ + " not implemented")

    @property
    def sender(self):
        """Search query based on sender."""
        raise NotImplementedError(__name__ + " not implemented")

    @property
    def read(self):
        """Search query based on read."""
        raise NotImplementedError(__name__ + " not implemented")

    @property
    def newer_than(self):
        """Search query based on newer_than."""
        raise NotImplementedError(__name__ + " not implemented")

    @property
    def not_sender(self):
        """Search query based on not_sender."""
        raise NotImplementedError(__name__ + " not implemented")

    @property
    def older_than(self):
        """Search query based on older_than."""
        raise NotImplementedError(__name__ + " not implemented")

    @property
    def phrase(self):
        """Search query based on phrase."""
        raise NotImplementedError(__name__ + " not implemented")

    @property
    def size(self):
        """Search query based on size."""
        raise NotImplementedError(__name__ + " not implemented")

    @property
    def size_larger(self):
        """Search query based on size_larger."""
        raise NotImplementedError(__name__ + " not implemented")

    @property
    def size_smaller(self):
        """Search query based on size_smaller."""
        raise NotImplementedError(__name__ + " not implemented")

    @property
    def sent_after(self):
        """Search query based on sent_after."""
        raise NotImplementedError(__name__ + " not implemented")

    @property
    def sent_before(self):
        """Search query based on sent_before."""
        raise NotImplementedError(__name__ + " not implemented")

    @property
    def starred(self):
        """Search query based on starred."""
        raise NotImplementedError(__name__ + " not implemented")

    @property
    def keyword(self):
        """Search query based on keyword."""
        raise NotImplementedError(__name__ + " not implemented")

    @property
    def important(self):
        """Search query based on important."""
        raise NotImplementedError(__name__ + " not implemented")

    @property
    def filename(self):
        """Search query based on filename."""
        raise NotImplementedError(__name__ + " not implemented")

    @property
    def category(self):
        """Search query based on category."""
        raise NotImplementedError(__name__ + " not implemented")

    @property
    def bcc(self):
        """Search query based on bcc."""
        raise NotImplementedError(__name__ + " not implemented")

    @property
    def around(self):
        """Search query based on around."""
        raise NotImplementedError(__name__ + " not implemented")

    @property
    def attachment(self):
        """Search query based on attachment."""
        raise NotImplementedError(__name__ + " not implemented")

    @property
    def label(self):
        """Search query based on label."""
        raise NotImplementedError(__name__ + " not implemented")

    @property
    def folder(self):
        """Search query based on folder."""
        raise NotImplementedError(__name__ + " not implemented")

    @property
    def cc(self):
        """Search query based on cc."""
        raise NotImplementedError(__name__ + " not implemented")

    @property
    def to(self):
        """Search query based on to."""
        raise NotImplementedError(__name__ + " not implemented")
