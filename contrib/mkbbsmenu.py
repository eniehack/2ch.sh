import sys

from dataclasses import dataclass
from enum import Enum
from html.parser import HTMLParser
from typing import Optional

class State(Enum):
    NONE = 1
    B = 2
    A = 3

@dataclass
class Board:
    href: str
    name: str

class BBSMenuParser(HTMLParser):
    current_category: str = ""
    current_board: Optional[Board] = None
    state: State = State.NONE
    boards: list[tuple[str, Board]] = []

    def handle_starttag(self, tag, attrs):
        #print(f"starttag: {tag}, current state: {self.state}")
        if tag == "b": #and self.state == State.SECOND_BR:
            self.state = State.B
        elif tag == "a":
            self.state = State.A
            href = list(filter(lambda x: x[0] == "href", attrs))
            self.current_board = Board(href = href[0][1], name = "")
        #print(f"starttag: {tag}, changed state: {self.state}")

    def handle_data(self, data):
        #print(f"data, current: {self.state}, {self.current_category}, {self.current_board}")
        if self.state == State.B:
            self.current_category = data
            #print(f"changed cat: {self.current_category}, current: {self.state}")
        elif self.state == State.A:
            self.current_board.name = data
            #print(f"board: {self.current_board}, current: {self.state}, {self.current_category}")

    def handle_endtag(self, tag):
        if self.state == State.A:
            self.boards.append((self.current_category, self.current_board))
            self.current_board = None

        self.state = State.NONE
        #print(f"endtag: {tag}, current: {self.state}, {self.current_category}")


parser = BBSMenuParser()
parser.feed(sys.stdin.read())

#print(parser.boards)

for i in parser.boards:
    if i[0] is None or i[0] == "": continue
    print(f"\"{i[1].href}\",{i[0]},{i[1].name}")
