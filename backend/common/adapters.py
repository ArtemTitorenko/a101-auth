import phonenumbers
from sqlalchemy_utils import PhoneNumber


class PhoneNumberAdapter(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(dict(test="test"))

    @classmethod
    def validate(cls, v):
        try:
            phone_number = None
            if isinstance(v, str) and len(v) > 0:
                phone_number = phonenumbers.parse(v, None)
                return phonenumbers.format_number(
                    phone_number, phonenumbers.PhoneNumberFormat.E164
                )
            if isinstance(v, PhoneNumber):
                return phonenumbers.format_number(
                    v, phonenumbers.PhoneNumberFormat.E164
                )
        except phonenumbers.phonenumberutil.NumberParseException:
            raise ValueError("Некорректный номер телефона")
        return ""

    def __repr__(self):
        return f"PhoneNumberType"
