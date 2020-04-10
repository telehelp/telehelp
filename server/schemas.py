from schema import And
from schema import Optional
from schema import Regex
from schema import Schema
from schema import Use

REGISTRATION_SCHEMA = Schema(
    {
        "helperName": str,
        "zipCode": And(str, Regex(r"^[0-9]{5}$"), Use(int)),
        "phoneNumber": Regex(r"^[0]{1}\d{7,9}$|^[\+46]{3}\d{9}$"),
        "terms": bool,
    }
)
VERIFICATION_SCHEMA = Schema(
    {"verificationCode": Regex(r"^[0-9]{6}$"), "number": Regex(r"^[0]{1}\d{7,9}$|^[\+46]{3}\d{9}$")}
)
