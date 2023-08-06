"""Email Filter implementation for Gmail."""
import re
from typing import Optional

from promail.filters.email_filter import EmailFilter


class GmailFilter(EmailFilter):
    """Email Filter Generates a query string used to query the email backend.

    Email filter is used by the email client to store
    which emails have been run with which filters.
    The Filter uses `name` and `version` to uniquely identify itself.
    Queries based on: https://seosly.com/gmail-search-operators/
    """

    TIME_FRAMES = {
        "d": "Day",
        "m": "Month",
        "y": "Year",
    }

    def _validate(self) -> None:
        fields = "newer_than", "older_than"
        for field in fields:
            value = getattr(self, f"_{field}")
            if value is None:
                continue
            value = value.strip().lower()
            if len(value) < 2:
                raise IndexError(
                    f"{value} is not valid for{field} is expected to be either None "
                    f"or a string representing the number of a time period. "
                    f"example: 6d for 6 days. valid options are: {self.TIME_FRAMES}"
                )

            elif value[-1] not in self.TIME_FRAMES.keys():
                raise ValueError(
                    f"{value} is not valid for{field},"
                    f"string must end in one of the following values: "
                    f"{list(self.TIME_FRAMES.keys())} "
                )
            elif not value[:-1].isdigit():
                raise ValueError(
                    f"{value} is not valid for{field}, "
                    f"expecting value to begin with a number"
                )

    @staticmethod
    def _join_tuple(term: str, data: Optional[tuple], seperator: str):
        if data is None:
            return ""
        if seperator == "OR":
            return " OR ".join([f"{term}:{d}" for d in data])
        elif seperator == " ":
            return f"{term}:(" + seperator.join([f"{d}" for d in data]) + ")"

    @staticmethod
    def _get_boalean(term: str, value: tuple, data: Optional[bool]):
        if data is None:
            return ""

        elif data:
            return f"{term}:{value[1]}"

        else:
            return f"{term}:{value[2]}"

    @staticmethod
    def _get_string(term: str, data: Optional[str]):
        if data is None:
            return ""
        return f"{term}:{data}"

    @staticmethod
    def _get_date(term, date):
        if date is None:
            return ""
        return f"{term}:{date.strftime('%G/%m/%d')}"

    @staticmethod
    def _get_toggle(term, data):
        """Format toggle."""
        if data:
            return f"{term}:{data}"
        return ""

    @property
    def sender(self):
        """Search query based on sender."""
        return self._join_tuple("from", self._sender, seperator="OR")

    @property
    def read(self):
        """Search query based on read."""
        return self._get_boalean("read", ["read", "unread"], self._read)

    @property
    def newer_than(self):
        """Search query based on newer_than."""
        return self._get_string("newer_than", self._newer_than)

    @property
    def not_sender(self):
        """Search query based on not_sender."""
        return self._join_tuple("NOT from", self._not_sender, seperator="OR")

    @property
    def older_than(self):
        """Search query based on older_than."""
        return self._get_string("older_than", self._older_than)

    @property
    def phrase(self):
        """Search query based on phrase."""
        if self._phrase is None:
            return ""
        return self._join_tuple(
            "", tuple([f'"{phrase}"' for phrase in self._phrase]), seperator="AND"
        )

    @property
    def size(self):
        """Search query based on size."""
        return "" if self._size is None else f"size:{self._size}"

    @property
    def size_larger(self):
        """Search query based on size_larger."""
        return self._get_string("larger", self._size_larger)

    @property
    def size_smaller(self):
        """Search query based on size_smaller."""
        return self._get_string("larger", self._size_smaller)

    @property
    def sent_after(self):
        """Search query based on sent_after."""
        return self._get_date("after", self._sent_after)

    @property
    def sent_before(self):
        """Search query based on sent_before."""
        return self._get_date("before", self._sent_after)

    @property
    def starred(self):
        """Search query based on starred."""
        data = True if self._starred else None
        return self._get_toggle("starred", data)

    @property
    def keyword(self):
        """Search query based on keyword."""
        if self._keyword is None:
            return ""
        else:
            return "(" + " ".join(self._keyword) + ")"

    @property
    def important(self):
        """Search query based on important."""
        if self._important is None:
            return ""
        return self._get_toggle("is", "important")

    @property
    def filename(self):
        """Search query based on filename."""
        return self._join_tuple("filename", self._filename, "OR")

    @property
    def category(self):
        """Search query based on category."""
        return self._get_string("category", self._category)

    @property
    def bcc(self):
        """Search query based on bcc."""
        return self._join_tuple("bcc", self._bcc, "AND")

    @property
    def around(self):
        """Search query based on around."""
        if self._around is None:
            return ""
        return (
            f"{self._around['first_term']}"
            "AROUND {self._around['apart']} "
            "{self._around['second_term']}"
        )

    @property
    def attachment(self):
        """Search query based on attachment."""
        return self._get_toggle("has", "attachment" if self._attachment else None)

    @property
    def label(self):
        """Search query based on label."""
        return self._get_string("label", self._label)

    @property
    def folder(self):
        """Search query based on folder."""
        return self._get_string("folder", self._folder)

    @property
    def cc(self):
        """Search query based on cc."""
        return self._join_tuple("cc", self._cc, "AND")

    @property
    def to(self):
        """Search query based on to."""
        return self._join_tuple("to", self._to, "AND")

    def get_filter_string(self) -> str:
        """Creates string to query email based on parameters."""
        return re.sub(
            " +",
            " ",
            " ".join(
                (
                    self.around,
                    self.attachment,
                    self.bcc,
                    self.category,
                    self.cc,
                    self.filename,
                    self.folder,
                    self.important,
                    self.keyword,
                    self.label,
                    self.newer_than,
                    self.not_sender,
                    self.older_than,
                    self.phrase,
                    self.read,
                    self.sender,
                    self.sent_after,
                    self.sent_before,
                    self.size,
                    self.size_larger,
                    self.size_smaller,
                    self.starred,
                    self.to,
                )
            ).strip(),
        )

    def filter_results(self, messages):
        """Removes messages in self.processed."""
        return filter(lambda msg: msg["id"] not in self.processed, messages)


# a = GmailFilter(
#     load_processed=True,
#     sender=("Antoinewood@gmail.com", "sue"),
#     older_than="99d",
#     sent_after=datetime.now(),
# )
#
# print(a.get_filter_string())
# # l = list(set(a.__dict__.keys()))
# # l.sort()
# # for value in l:
# #     print(
# #         f"self.{value.strip('_')}", end = ", "
# #     )
