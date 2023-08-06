import time
import re
from scrapeanything.utils.types import Types
from scrapeanything.utils.constants import *

class Scraper:

    def __del__(self):
        self.on_close()

    def wget(self, url, tries=0):
        try:
            if url is not None and tries < 3:
                self.parser = self.on_wget(url)
                return True
            else:
                return False
        except Exception as ex:
            tries += 1
            time.sleep(3)
            return self.wget(url, tries)

    def xPath(self, path, element=None, pos=0, dataType=None, prop=None, explode=None, condition=None, substring=None, transform=None, replace=None, join=None, timeout=0):
        if path is None or path == '':
            return None

        element = self.parser if element is None else element
        el = self.on_xPath(element=element, path=path, timeout=timeout)

        # step 1: extract xpath
        if el is None:
            return None
        elif isinstance(el, list) == True and dataType == WebScraper.Types.LIST:
            if pos == 0 or len(el) == 1:
                el = el[0]

        response = []
        for item in el:
            try:
                if prop == WebScraper.Properties.TEXT or prop == 'text()':
                    response.append(self.on_get_text(item))
                elif prop == WebScraper.Properties.HTML or prop == 'html()':
                    response.append(self.on_get_html(item))
                elif prop is not None:
                    response.append(self.on_get_attribute(item, prop))
                else:
                    response.append(item)
            except Exception as e:
                pass

        if len(response) == 1:
            el = response[0]
        elif pos is not None and len(response) > pos:
            el = response[pos]
        else:
            el = response

        primitive = (int, str, bool)
        if el is not None and (not isinstance(el, primitive) or not isinstance(el, primitive)):
            return el

        # step 2: apply functions
        options = dict(locals())
        for option in options:

            if option == WebScraper.Functions.SUBSTRING and substring is not None:
                el = self.substring(el, substring)
            if (option == WebScraper.Functions.EXPLODE) and explode is not None:
                el = self.explode(el, explode)
            if option == WebScraper.Functions.REPLACE and replace is not None:
                el = self.replace(el, replace)
            if option == WebScraper.Functions.JOIN and join is not None:
                el = self.join(el, join)

        # step 3 apply dataTypes
        if dataType is not None and '[' in dataType: # in the case dataType is a datetime with format (DATE[%Y-%m-%d %H:%M:%S])
            tokens = dataType.split('[')
            dataType = tokens[0]
            format = tokens[1][:-1]

        if dataType == WebScraper.Types.DATE:
            el = Types.to_date(el, format=format)
        if dataType == WebScraper.Types.PERCENTAGE:
            el = Types.to_number(el.replace('%', ''))
        if dataType == WebScraper.Types.BOOL:
            el = self.eval_condition(el, condition)
        if dataType == WebScraper.Types.MONEY:
            el = Types.to_money(el)
        if dataType == WebScraper.Types.NUMBER:
            el = Types.to_number(el)
        if dataType == WebScraper.Types.INTEGER:
            el = Types.to_integer(el)
        if dataType == WebScraper.Types.GEO:
            el = Types.to_geo(el)
        if dataType == WebScraper.Types.CHAR:
            el = Types.to_char(el)
        if dataType == WebScraper.Types.URL:
            base_url = Types.to_base_web(self.publisher.url)
            el = Types.to_normalized_url(base_url, el)

        if transform is not None:
            el = self.transform(el, transform)

        # clean string if element is not of ay complex type (WebElement, any object type, ...)
        primitive = (str) # (int, str, bool)
        if el is not None and isinstance(el, primitive):
            el = el.replace('\n', '').strip()

        return el

    def exists(self, path: str, element: any=None, timeout: int=0):
        return self.on_exists(path=path, element=element, timeout=timeout)

    def substring(self, el: any, substring: str):
        if substring is not None and el is not None:
            idx_separator1 = None
            idx_separator2 = None

            index = [m.start() for m in re.finditer('"', substring)][1]
            separator1 = substring[:index+1].replace('"', '', 9999).strip()
            separator2 = substring[index+2:].replace('"', '', 9999).strip()

            idx_separator1 = el.index(separator1) + len(separator1)
            idx_separator2 = el.index(separator2)

            if idx_separator1 is not None and idx_separator2 is not None:
                el = el[idx_separator1:idx_separator2]

        return el       

    def explode(self, el, explode):
        '''
        Description:
        Arguments:
        Returns:
        '''
        
        tokens = []
        separator_find = None
        separator_replace = None

        if explode is not None and el is not None:
            separators, indexes = explode.rsplit(',', 1)

            separators = separators.split(';')

            separator_find = separators[0].strip(' ').replace('"', '', 9999)
            if len(separators) > 1:
                separator_replace = separators[1].strip(' ').replace('"', '', 9999)


            for index in indexes.split(';'):
                index = int(index.strip(' '))
                if el is not None and separator_find in el:
                    el = el.split(separator_find)[index]
                else:
                    el = ''
                
                tokens.append(el)

        if separator_replace is None:
            separator_replace = ' '
        
        return separator_replace.join(tokens).strip(' ')

    def replace(self, el, replace):
        if replace is not None and el is not None:
            replace = replace.replace('; ', ';')
            tokens = [ token.replace('"', '') for token in replace.split(';') ]

        return el.replace(tokens[0], tokens[1])

    def join(self, el, separator):
        if type(el) is list and separator is not None and separator != '':
            el =  [ e for e in el if e is not None and e != '' ]
            return separator.join(el)
        else:
            return el

    def transform(self, el, transform):
        return el

        if transform is not None and el is not None:
            for couple in transform:
                from_value, to_value = couple
            return el # TODO
        else:
            return el

    def eval_condition(self, element, condition):
        return eval('element ' + condition)
        '''
        try:
            return eval('int(element) ' + condition)
        except Exception as e:
            return eval('element ' + condition)
        '''

    def enter_text(self, path: str, text: str, element: any=None, clear: bool=False, timeout: int=0):
        return self.on_enter_text(path=path, text=text, element=element, clear=clear, timeout=timeout)

    def click(self, path, element=None, timeout=0):
        return self.on_click(path=path, element=element, timeout=timeout)

    def back(self):
        self.on_back()

    def get_current_url(self):
        return self.on_get_current_url()

    def solve_captcha(self, path):
        self.on_solve_captcha(path)

    def get_css(self, element, prop):
        return self.on_get_css(element.scraper.parser, prop)

    def login(self, username_text=None, username=None, password_text=None, password=None):
        return self.on_login(username_text, username, password_text, password)

    def search(self, path=None, text=None):
        return self.on_search(path, text)

    def scroll_to_bottom(self):
        return self.on_scroll_to_bottom()

    def get_scroll_top(self):
        return self.on_get_scroll_top()

    def get_scroll_bottom(self):
        return self.on_get_scroll_bottom()

    def select(self, path: str, option: str) -> None:
        self.on_select(path=path, option=option)

    def get_image_from_canvas(self, path: str, local_path: str, element: any) -> str:
        return self.on_get_image_from_canvas(path=path, local_path=local_path, element=element)

    def switch_to(self, element: any) -> None:
        return self.on_switch_to(element=element)

    def close(self):
        self.on_close()