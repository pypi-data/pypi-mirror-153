from typing import NamedTuple


class QuantplayInstrument(NamedTuple):
    """Common instrument model to be used across
    different exchanges and brokers.
    """

    symbol: str
    instrument_id: str
    instrument_type: str  # e.g EQ, CE, PE, FUT
    exchange: str  # e.g. NSE, NFO
    segment: str = ""  # e.g. NSE, NFO-OPT, NFO-FUT

    def __repr__(self):
        return "{} {} {} {} {}".format(
            self.symbol,
            self.instrument_id,
            self.instrument_type,
            self.exchange,
            self.segment,
        )

    def security_type(self):
        if self.instrument_type in ["CE", "PE"]:
            return "OPT"
        return self.instrument_type

    @classmethod
    def from_zerodha_instrument(cls, zerodha_instrument_dict):
        """Creates QuantplayInstrument from instrument dict returned by Zerodha API"""
        d = zerodha_instrument_dict
        return cls(
            d["tradingsymbol"],
            d["instrument_token"],
            d["instrument_type"],
            d["exchange"],
            d["segment"],
        )
