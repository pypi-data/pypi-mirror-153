import bokeh.io as bio
import bokeh.models as bm
import pandas as pd
import typing as typ

from pacifico_devel.util.reportTemplate.src.core.Plot.Table.Table import Table


class TableDefault(Table):

    def makePlot(self,
                 df: pd.DataFrame,
                 title: str,
                 backend: str,
                 shape: typ.Tuple[int, int]) -> bm.DataTable:
        """
        Renders the plot both the HTML and saves the .png.

        Args:
            df:
            title:
            backend:
            shape:

        Returns:

        """
        columns = [bm.TableColumn(field=col, title=col)
                   for col in df.columns]
        source = bm.ColumnDataSource(df)
        dataTable = bm.DataTable(source=source,
                                 columns=columns,
                                 fit_columns=True,
                                 selectable=True,
                                 sortable=True)
        dataTable.name = title

        self._saveImageFile(dataTable)
        return dataTable


if __name__ == '__main__':
    from pacifico_devel.util.reportTemplate.src.util.testing import makeRandomCategoricalDf

    df = makeRandomCategoricalDf(shape=(20, 3))

    bp = TableDefault()
    ps = bp.makePlot(df=df)
    bio.show(ps)
