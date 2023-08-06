from enum import Enum

class Integration:

    class Types(Enum):
        CSV = 'CSV'
        EXCEL = 'EXCEL'
        GOOGLESPREADSHEET = 'GOOGLE SPREADSHEET'

    class Modes(Enum):
        READ = 'READ'
        WRITE = 'WRITE'

class WebScraper:

    class Functions:
        SUBSTRING = 'substring'
        EXPLODE = 'explode'
        REPLACE = 'join'
        JOIN = 'join'

    class Types:
        PERCENTAGE = 'PERCENTAGE'
        BOOL = 'BOOL'
        MONEY = 'MONEY'
        NUMBER = 'NUMBER'
        INTEGER = 'INTEGER'
        GEO = 'GEO'
        CHAR = 'CHAR'
        URL = 'URL'
        LIST = 'LIST'
        DATE = 'DATE'
        JSON = 'JSON'
        STRING = 'STRING'

    class Properties:
        TEXT = 'text()'
        HTML = 'html()'

class Requests:

    class Methods(Enum):
        POST = 'POST'
        GET = 'GET'
        PUT = 'PUT'
    
    class ResponseTypes(Enum):
        TEXT = 'TEXT'
        JSON = 'JSON'
