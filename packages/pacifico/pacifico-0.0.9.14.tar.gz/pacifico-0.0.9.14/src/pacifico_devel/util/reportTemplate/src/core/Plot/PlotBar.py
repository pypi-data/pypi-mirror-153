import bokeh.io as bio
import bokeh.plotting as bpl
# from bokeh.models import ColumnDataSource, DataTable, TableColumn
import bokeh.themes as bt
import pandas as pd
import typing as typ
import altair as alt

from pacifico_devel.util.reportTemplate.src.util.PacificoPlotColors import PacificoPlotColors
from pacifico_devel.util.reportTemplate.src.core.Plot.Plot import Plot

import pacifico_devel.util.reportTemplate.src.util.Enumerations as renm


class PlotBar(Plot):

    def _makePlotBokeh(self,
                       df: pd.DataFrame,
                       title: str,
                       shape: typ.Tuple[int, int]):

        categoriesColumn = df.columns[0]
        valuesColumn = df.columns[1]

        df["barchart_color"] = df[valuesColumn].apply(self._colorMap)

        ps = bpl.figure(width=shape[0],
                        height=shape[1],
                        y_range=df.sort_values(valuesColumn,
                                               ascending=True)[categoriesColumn],
                        toolbar_location=None)
        bpl.curdoc().theme = bt.Theme(filename=self._BOKEH_THEME_PATH)
        ps.title = title

        ps.hbar(y=categoriesColumn,
                left=0,
                right=valuesColumn,
                height=0.5,
                color="barchart_color",
                source=df)

        self._saveImageFile(ps)

        return ps

    def _makePlotAltair(self,
                        df: pd.DataFrame,
                        title: str,
                        shape: typ.Tuple[int, int]) -> bpl.Figure:

        categoriesColumn = df.columns[0]
        valuesColumn = df.columns[1]

        # colorScale = alt.Scale(domain=df[valuesColumn],
        #                        range=df[valuesColumn].apply(self._colorMap)
        #                        )
        df["barchart_color"] = df[valuesColumn].apply(self._colorMap)

        ps = alt.Chart(df).mark_bar().encode(x=valuesColumn,
                                             y=alt.Y(categoriesColumn, sort="-x"),
                                             color=alt.Color("barchart_color:N", scale=None))
        ps = ps.properties(title=title,
                           width=shape[0],
                           height=shape[1])

        self._saveImageFile(ps)
        return ps

    def makePlot(self,
                 df: pd.DataFrame,
                 title: str,
                 shape: typ.Tuple[int, int],
                 backend: typ.Union[str, renm.Backend] = "bokeh") -> bpl.Figure:

        dfAux = self._translateDataFrame(df)

        assert (isinstance(dfAux, pd.DataFrame))
        assert (dfAux.shape[1] <= 2)

        if dfAux.shape[1] == 1:
            dfAux = dfAux.reset_index()
        if isinstance(backend, str):
            backend = renm.Backend[backend.upper()]

        if backend is renm.Backend.BOKEH:
            return self._makePlotBokeh(df=dfAux,
                                       title=title,
                                       shape=shape)
        elif backend is renm.Backend.ALTAIR:
            return self._makePlotAltair(df=dfAux,
                                        title=title,
                                        shape=shape)
        raise NotImplementedError(f"Backend {backend.name} not implemented.")

    @staticmethod
    def _colorMap(x: float):
        if x > 0:
            return PacificoPlotColors.BLUE.getCodeString()
        return PacificoPlotColors.PINK.getCodeString()


# def plot(self, series: pd.Series):
#     fig = plt.figure(title="this",
#                      x_axis_label="x axis",
#                      y_axis_label="y axis")
#     colors = None
#     # plot.bar(df.column, s: pd.Series)
#     for k, v in zip(series.index, series):
#         color = PacificoColors.getColor[]
#         fig.bar(k, v, legend_label=k, color=color)
#     formatAxesTickers(fig)
#     makeLegendStyle(fig)
#     style(plot)  # not colors or legends
#     hoverTools(plot)
#     return plot

if __name__ == '__main__':
    from pacifico_devel.util.reportTemplate.src.util.testing import makeRandomCategoricalDf

    df = makeRandomCategoricalDf(shape=(20, 3))

    df.rename(columns={"value_0": "value"}, inplace=True)

    bp = PlotBar()
    ps = bp.makePlot(df=df,
                     title="",
                     shape=(1 / 2, 1))
    bio.show(ps)
    # bp.deleteImageFile()
