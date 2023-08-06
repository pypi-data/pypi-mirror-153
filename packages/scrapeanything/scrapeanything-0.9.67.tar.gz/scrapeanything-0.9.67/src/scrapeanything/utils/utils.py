from abc import abstractmethod
import importlib

class Utils:

    @staticmethod
    def write_to_file(filename: str, text: str) -> None:
        with open(filename, 'a') as fd:
            fd.write(f'{text}')

    @staticmethod
    def instantiate(module_name: str, class_name: str, args=None) -> any:
        module = importlib.import_module(module_name)
        class_ = getattr(module, class_name)
        if args is not None:
            return class_(**args)
        else:
            return class_()

    @staticmethod
    def import_module(module_name: str) -> None:
        # The file gets executed upon import, as expected.
        importlib.import_module(module_name)

    @staticmethod
    def distinct(elements: list) -> list:
        distinct_elements = []

        for element in elements:
            if element not in distinct_elements:
                distinct_elements.append(element)
        
        return distinct_elements

    @staticmethod
    def find(obj: any, key: str) -> any:
        if isinstance(obj, dict):
            if key in obj: return obj[key]
            for k, v in obj.items():
                if isinstance(v, dict) and k == key.split('.')[0]:
                    item = Utils.find(v, '.'.join(key.split('.')[1:]))
                    if item is not None:
                        return item
        else:
            return Utils.rgetattr(obj, key)

    def rgetattr(obj: any, attr: str, *args) -> any:
        '''
        Description:
        Arguments:
        Returns:
        '''

        def _rgetattr(obj: any, attrs: list) -> any:
            # TODO: this is from sqlalchemy. There should not be any reference to SqlAlchemy here in this class
            for attr in attrs:
                obj = getattr(obj, attr, *args)
            
            return obj

        def _getattr(obj: any, attr: str) -> any:
            return getattr(obj, attr, *args)
        
        if attr.find('.') > -1:
            return _rgetattr(obj=obj, attrs=attr.split('.'))
            # return functools.reduce(_getattr, [obj] + attr.split('.')) # recursively gets the property value given a request like object.child.property
        else:
            return _getattr(obj, attr)