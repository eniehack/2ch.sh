from __future__ import annotations

import csv
import sys
import io
from dataclasses import dataclass
from enum import Enum
from html.parser import HTMLParser
from signal import SIG_DFL, SIGPIPE, signal
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import ClassVar


class State(Enum):
    NONE = 1
    B = 2
    A = 3


@dataclass
class Board:
    href: str | None
    name: str


class BBSMenuParser(HTMLParser):
    current_category: str = ""
    current_board: Board | None = None
    state: State = State.NONE
    boards: ClassVar[list[tuple[str, Board | None]]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        # print(f"starttag: {tag}, current state: {self.state}")
        if tag == "b":  # and self.state == State.SECOND_BR:
            self.state = State.B
        elif tag == "a":
            self.state = State.A
            href = list(filter(lambda x: x[0] == "href", attrs))
            self.current_board = Board(href=href[0][1], name="")
        # print(f"starttag: {tag}, changed state: {self.state}")

    def handle_data(self, data: str) -> None:
        # print(f"data, current: {self.state}, {self.current_category}, {self.current_board}")
        if self.state == State.B:
            self.current_category = data
            # print(f"changed cat: {self.current_category}, current: {self.state}")
        elif self.state == State.A:
            if self.current_board is not None:
                self.current_board.name = data
            # print(f"board: {self.current_board}, current: {self.state}, {self.current_category}")

    def handle_endtag(self, tag: str) -> None:
        if self.state == State.A:
            if self.boards is not None:
                self.boards.append((self.current_category, self.current_board))
            self.current_board = None

        self.state = State.NONE
        # print(f"endtag: {tag}, current: {self.state}, {self.current_category}")


if __name__ == "__main__":
    # Avoid `BrokenPipeError` when running `... | head`
    signal(SIGPIPE, SIG_DFL)

    # Avoid `UnicodeDecodeError`
    if isinstance(sys.stdin, io.TextIOWrapper):
        sys.stdin.reconfigure(encoding="shift-jis")

    parser = BBSMenuParser()
    parser.feed(sys.stdin.read())

    # print(parser.boards)

    writer = csv.writer(sys.stdout, quoting=csv.QUOTE_ALL)
    for category, board in parser.boards:
        if not category or not board:
            continue
        writer.writerow((board.href, category, board.name))
