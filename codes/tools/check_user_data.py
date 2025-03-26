import re


def validate_tw_id(personal_id):
    pattern = r"^[A-Z][12]\d{8}$"
    return bool(re.match(pattern, personal_id))

def validate_phone(phone_number):
    pattern = r"^09\d{8}$"
    return bool(re.match(pattern, phone_number))

def validate_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(pattern, email))

