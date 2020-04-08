from schema import Schema, And, Use, Optional, Regex

REGISTRATION_SCHEMA = Schema({'helperName': str, 'zipCode': And(str, Regex("^[0-9]{5}$"), Use(int)), 'phoneNumber': Regex("^(\d|\+){1}\d{9,12}$"), 'terms': bool })
VERIFICATION_SCHEMA = Schema({'verificationCode':  Regex("^[0-9]{6}$"), 'number': Regex("^(\d|\+){1}\d{9,12}$")})