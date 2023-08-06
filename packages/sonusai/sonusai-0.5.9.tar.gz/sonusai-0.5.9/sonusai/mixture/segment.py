from dataclasses import dataclass


@dataclass
class Segment:
    start: int
    length: int

    def get_slice(self) -> slice:
        return slice(self.start, self.start + self.length)

    def trim_start(self, amount: int) -> None:
        self.trim_length(amount)
        self.start += amount

    def trim_length(self, amount: int) -> None:
        if amount >= self.length:
            raise ValueError(f'trim amount greater than or equal to length')
        self.length -= amount
