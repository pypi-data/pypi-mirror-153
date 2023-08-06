from dataclasses import dataclass


@dataclass
class InstrumentExchange:
    instrument: str
    to_instrument: str

    def invert(self):
        return InstrumentExchange(self.to_instrument, self.instrument)

    def __iter__(self):
        return iter((self.instrument, self.to_instrument))

    def __repr__(self):
        return f'{self.instrument}/{self.to_instrument}'
