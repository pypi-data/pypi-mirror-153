import pandas as pd

class Csv:
    
    def __init__(self):
        pass

    def import_data(self, filename):
        pass

    def export_data(self, data: any, filename: str, separator: str) -> None:
        df = pd.DataFrame(data)
        df.to_csv(filename, sep=',', encoding='utf-8')