from schema import And
from schema import Optional
from schema import Regex
from schema import Schema
from schema import Use

REGISTRATION_SCHEMA = Schema(
    {
        "helperName": str,
        "zipCode": And(str, Regex(r"^[0-9]{5}$"), Use(int)),
        "phoneNumber": Regex(r"^(\d|\+){1}\d{9,12}$"),
        "terms": bool,
    }
)
VERIFICATION_SCHEMA = Schema(
    {"verificationCode": Regex(r"^[0-9]{6}$"), "number": Regex(r"^(\d|\+){1}\d{9,12}$")}
)
