class Market:

    TIMINGS = {
        # In (hour, minute) format
        "NSE": {
            "start": (9, 15),
            "end": (15, 30),
        },
        "NFO": {
            "start": (9, 15),
            "end": (15, 30),
        },
    }

    EXCHANGE_MAPPINGS = {
        "NFO": {"EQ": "NSE", "FUT": "NFO", "OPT": "NFO"},
        "NSE": {"EQ": "NSE", "FUT": "NFO", "OPT": "NFO"},
    }

    INDEX_SYMBOL_TO_DERIVATIVE_SYMBOL_MAP = {
        "NIFTY 50": "NIFTY",
        "NIFTY FIN SERVICE": "FINNIFTY",
        "NIFTY BANK": "BANKNIFTY",
    }

    DERIVATIVE_SYMBOL_TO_INDEX_SYMBOL_MAP = {
        "NIFTY": "NIFTY 50",
        "FINNIFTY": "NIFTY FIN SERVICE",
        "BANKNIFTY": "NIFTY BANK",
    }
