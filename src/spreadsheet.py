import pandas as pd
from openpyxl.worksheet.table import Table, TableStyleInfo
from typing import Any, Literal
from pathlib import Path


class Spreadsheet:
    def __init__(self) -> None:
        self.__df = pd.DataFrame({
            'símbolos': [],
            'nomes': [],
            'preços': []
        })

    @property
    def df(self) -> pd.DataFrame:
        return self.__df

    @df.setter
    def df(self, df: Any) -> None:
        self.__df = df

    def add_row(self, simbol: str, name: str, price: float) -> None:
        """
            Add new values for spreadsheet
        """
        price_f = 'R$ ' + str(price).replace(',', '').replace('.', ',')
        self.df.loc[len(self.df)] = [simbol, name, price_f]

    def save(self, f_name: str, f_type: Literal['csv', 'xlsx']) -> None:
        """
            save and format excel
        """
        root_p = Path('.')
        spreadsheet_dir = root_p / 'spreadsheet'

        assert spreadsheet_dir.exists(), 'required "spreadsheet" folder at root path'

        with pd.ExcelWriter(str((spreadsheet_dir / f'{f_name}.{f_type}').absolute()), engine='openpyxl') as writer:
            self.df.to_excel(writer, sheet_name='nomes', index=False)

            worksheet = writer.sheets['nomes']
            num_rows, num_cols = self.df.shape

            # Define the table reference range
            ref = f"A1:{chr(65 + num_cols - 1)}{num_rows + 1}"

            # Create and style the table
            table = Table(displayName="stockExchangeTable", ref=ref)
            style = TableStyleInfo(
                name="TableStyleMedium9",
                showFirstColumn=False,
                showLastColumn=False,
                showRowStripes=True,
                showColumnStripes=True
            )
            table.tableStyleInfo = style
            worksheet.add_table(table)

            # Adjust column widths based on content
            for col in worksheet.columns:
                max_length = 0
                # Get the column letter (e.g., "A", "B")
                col_letter = col[0].column_letter

                for cell in col:
                    try:
                        # Check the length of cell value, convert to string if needed
                        max_length = max(max_length, len(str(cell.value)))
                    except:
                        pass

                # Set column width, adding padding for aesthetics
                adjusted_width = (max_length + 2)
                worksheet.column_dimensions[col_letter].width = adjusted_width


if __name__ == '__main__':
    excel = Spreadsheet()
