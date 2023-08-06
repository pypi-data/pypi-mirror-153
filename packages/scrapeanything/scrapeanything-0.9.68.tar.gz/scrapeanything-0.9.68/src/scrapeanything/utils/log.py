from abc import ABC
from datetime import datetime
import pandas as pd

class Log(ABC):

    @staticmethod
    def trace(message: str, *args) -> None:
        '''
        Description: logs a trace message
        Arguments: message: message containing {i}, args: arguments replacing {i}
        Returns: None
        '''
        pass # Log.log(message, 'trace', *args)

    @staticmethod
    def info(message: str, *args) -> None:
        '''
        Description: logs an info message
        Arguments: message: message containing {i}, args: arguments replacing {i}
        Returns: None
        '''
        Log.log(message, 'info', *args)

    def warning(message: str, *args) -> None:
        '''
        Description: logs a warning message
        Arguments: message: message containing {i}, args: arguments replacing {i}
        Returns: None
        '''
        Log.log(message, 'warning', *args)

    def error(message: str, *args) -> None:
        '''
        Description: logs an error message
        Arguments: message: message containing {i}, args: arguments replacing {i}
        Returns: None
        '''
        Log.log(message, 'error', *args)

    def replace_params(message: str, *args) -> str:
        '''
        Description: given a string like "Today it is a good {0}", replaces {0} with its related variable
        Arguments: message: message containing {i}, str: related arguments
        Returns: message modified
        '''

        for i, arg in enumerate(args):
            if type(arg) is pd.Timestamp:
                message = message.replace('{' + str(i) + '}', str(arg))
            else:
                message = message.replace('{' + str(i) + '}', str(arg))

        return message 

    def log(*args) -> str:
        message = args[0]
        severity = args[1]
        message = Log.replace_params(message, *args[2:])

        msg = f'{datetime.now():%Y-%m-%d %H:%M:%S} - {severity}: {message}'
        print(msg)
        Log.log_on_file(msg=msg)
        
    def log_on_file(msg: str) -> None:
        f = open(f'./logs/log_{datetime.now():%Y-%m-%d}.log','a')
        f.write(msg)
        f.write('\n')
        f.close()