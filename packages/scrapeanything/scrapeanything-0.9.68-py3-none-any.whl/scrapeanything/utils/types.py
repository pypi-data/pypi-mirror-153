from datetime import datetime
from decimal import Decimal
import sys
import re
import unicodedata
from money import Money

class Types:
    @staticmethod
    def is_primitive(value: any) -> bool:
        primitive = (int, float, str, bool, datetime)
        return type(value) in primitive

    @staticmethod
    def to_class(module_name: str, class_name: str) -> any:
        return getattr(sys.modules[module_name], class_name)

    @staticmethod
    def to_date(value: str, format: str) -> datetime:
        return datetime.strptime(value, format)

    @staticmethod
    def to_number(value: any) -> float:
        if value is None:
            return None
        else:
            if bool(re.search(r'\d', value)) == True:
                value = ''.join(i for i in value if i.isdigit() or i in [ ',', '.', '-' ])
                value = value[0] + value[1:].replace('-', '', 999) # if it is a negative number, remove all '-' except the first '-' (i.e. -10)
                value = value.replace(',', '.')
                return float(value)
            else:
                return None

    @staticmethod
    def to_integer(value: any) -> int:
        value = Types.to_number(value)
        return int(value)

    @staticmethod
    def to_currency(value: any) -> str:
        value = Money(amount=value, currency='EUR')
        return str(value)

    @staticmethod
    def to_geo(value: any) -> int:
        if value is not None:
            return value.replace(',', '')
        else:
            return None

    @staticmethod
    def to_money(value: any) -> Decimal:
        if value is not None:
            thousand_seaparator = '.'
            decimal_separator = ','
            currency_sign = '€'
            value = value.replace(unicodedata.lookup(currency_sign), '').replace(thousand_seaparator, '').replace(decimal_separator, '.').strip()

            values = value.split(' ')
            value = None
            for v in values:
                if Types.to_number(v) is not None:
                    value = v               

            if value is not None and value.isnumeric():
                return Decimal(value)
            else:
                return None
        else:
            return None

    @staticmethod
    def to_char(value: any) -> str:
        if value is None:
            return None
        else:
            return value.strip()

    @staticmethod
    def to_list(klist: list) -> list:
        return [item for sublist in klist for item in sublist]

    @staticmethod
    def to_dict(obj: any, columns: list) -> dict:
        dictionary = {}
        for attr in dir(obj):
            if attr in columns:
                dictionary[attr] = getattr(obj, attr)

        return dictionary