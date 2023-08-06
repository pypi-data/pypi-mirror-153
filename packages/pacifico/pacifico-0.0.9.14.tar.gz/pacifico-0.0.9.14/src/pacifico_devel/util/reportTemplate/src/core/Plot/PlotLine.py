import typing as typ
import bokeh.plotting as bpl
import bokeh.themes as bt
import bokeh.models as bm
import pandas as pd
import altair as alt

from pacifico_devel.util.reportTemplate.src.util.PacificoPlotColors import PacificoPlotColors
from pacifico_devel.util.reportTemplate.src.core.Plot.Plot import Plot
import pacifico_devel.util.reportTemplate.src.util.Enumerations as renm

import pacifico_devel.util.lexikon.src.util.Enumerations as lenm


class PlotLine(Plot):
    _DATE_TIME_FORMAT = lenm.Language.English_US.dateFormatString()

    def _makePlotBokeh(self,
                       df: pd.DataFrame,
                       title: str,
                       shape: typ.Tuple[int, int]) -> bpl.Figure:
        ps = bpl.figure(width=shape[0],
                        height=shape[1],
                        toolbar_location=None)
        bpl.curdoc().theme = bt.Theme(filename=self._BOKEH_THEME_PATH)
        ps.title = title
        if pd.api.types.is_datetime64_any_dtype(df.index):
            ps.xaxis[0].formatter = bm.DatetimeTickFormatter(years=self._DATE_TIME_FORMAT,
                                                             months=self._DATE_TIME_FORMAT,
                                                             days=self._DATE_TIME_FORMAT)
        for colName, color in zip(df.columns,
                                  PacificoPlotColors):
            if pd.api.types.is_numeric_dtype(df[colName]):
                data = df[[colName]]
                ps.line(x="index",
                        y=colName,
                        legend_label=colName,
                        color=color.getCodeString(),
                        source=data,
                        line_width=2)
        self._saveImageFile(ps)
        return ps

    def _makePlotAltair(self,
                        df: pd.DataFrame,
                        title: str,
                        shape: typ.Tuple[int, int]) -> bpl.Figure:
        indexName = df.index.name
        data = df[[colName
                   for colName in df.columns
                   if pd.api.types.is_numeric_dtype(df[colName])]]
        data = data.reset_index()

        varName = self._translateString("series")
        valueName = self._translateString("value")

        data = data.melt(id_vars=data.columns[0],
                         var_name=varName,
                         value_name=valueName)
        colorScale = alt.Scale(domain=data[varName].unique(),
                               range=[c.getCodeString()
                                      for c in PacificoPlotColors]
                               )

        # print(f"DATA: {data}")
        ps = alt.Chart(data).mark_line().encode(x=indexName,
                                                y=valueName,
                                                color=alt.Color(varName, scale=colorScale))
        ps = ps.properties(title=title,
                           width=shape[0],
                           height=shape[1])

        # kwargsTitle = {"font": "klartext mono",
        #                "color": PacificoPlotColors.BLUE.getCodeString()}
        # kwargsAxis = {"title" + k.capitalize(): v
        #               for k, v in kwargsTitle.items()}
        #
        # ps = ps.configure_title(**kwargsTitle).configure_axis(**kwargsAxis)

        self._saveImageFile(ps)
        return ps

    def makePlot(self,
                 df: pd.DataFrame,
                 title: str,
                 shape: typ.Tuple[int, int],
                 backend: typ.Union[str, renm.Backend] = "bokeh"
                 ) -> bpl.Figure:

        dfAux = self._translateDataFrame(df)

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


if __name__ == '__main__':
    from pacifico_devel.util.reportTemplate.src.util.testing import makeRandomCategoricalDf

    df = makeRandomCategoricalDf(shape=(20, 3))  # .reset_index()

    print(df)

    bp = PlotLine(languageInput=lenm.Language.Spanish,
                  languageOutput=lenm.Language.French)
    ps = bp.makePlot(df=df,
                     backend="altair",
                     title="LINE PLOT",
                     shape=(1000, 1000)
                     )
    # bio.show(ps)
    # bp.deleteImageFile()
