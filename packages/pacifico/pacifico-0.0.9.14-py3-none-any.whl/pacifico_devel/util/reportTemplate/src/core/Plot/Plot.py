# from abc import ABCMeta, abstractmethod
import abc
import pathlib as pth
import bokeh.io as bio
import pandas as pd
import pandas.api.types as pdt
import typing as typ
import dataframe_image as dfi
import altair as alt

import bokeh.plotting as bpl
import bokeh.models as bm
import altair.vegalite.v4.api as altapi
import pandas.io.formats.style as pdst

from pacifico_devel.util.reportTemplate.src.core.Style.Style import Style
import pacifico_devel.util.reportTemplate.src.util.Enumerations as renm

import pacifico_devel.util.lexikon.src.core.Translator as trl
import pacifico_devel.util.lexikon.src.util.Enumerations as lenm

from pacifico_devel.util.reportTemplate.src.util.Patches import ScreenshotPatch

MultiDisplay = typ.Union[bpl.Figure, bm.DataTable, altapi.Chart, pdst.Styler]


class Plot(metaclass=abc.ABCMeta):
    """
    Abstract class for all necessary plots
    """
    _BOKEH_THEME_PATH = pth.Path(__file__).parents[1] / "Style" / "bokeh_themes" / "pacifico_theme.yml"
    _TEMP_ROOT = pth.Path(__file__).parent / "tmp"

    def __init__(self,
                 languageInput: lenm.Language,
                 languageOutput: lenm.Language,
                 style: typ.Optional[Style] = None):
        alt.data_transformers.disable_max_rows()
        self._languageInput = languageInput
        self._languageOutput = languageOutput
        self._style = style
        self._pathImage = self._makePathImage()

    @abc.abstractmethod
    def makePlot(self,
                 df: pd.DataFrame,
                 title: str,
                 backend: typ.Union[str, renm.Backend],
                 shape: typ.Tuple[int, int]) -> MultiDisplay:
        """
        Renders plot and saves it to temp folder.

        Args:
            df:
            title:
            backend:
            shape:

        Returns:

        """
        pass

    @property
    def pathImage(self) -> pth.Path:
        """
        Path in which the image of the plot will be saved.

        Returns:

        """
        return self._pathImage

    def _translateDataFrame(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Translates all strings in dataframe.

        Args:
            df:

        Returns:

        """
        dfAux = df.copy()
        if pdt.is_string_dtype(dfAux.index):
            dfAux.index = trl.Translator.translate(text=dfAux.index,
                                                   languageInput=self._languageInput,
                                                   languageOutput=self._languageOutput)

        if dfAux.index.name is None:
            dfAux.index.name = trl.Translator.translate(text="index",
                                                        languageInput=lenm.Language.English_US,
                                                        languageOutput=self._languageOutput)
        else:
            dfAux.index.name = trl.Translator.translate(text=dfAux.index.name,
                                                        languageInput=self._languageInput,
                                                        languageOutput=self._languageOutput)

        if pdt.is_string_dtype(dfAux.columns):
            dfAux.columns = trl.Translator.translate(text=dfAux.columns,
                                                     languageInput=self._languageInput,
                                                     languageOutput=self._languageOutput)
        for col in dfAux.columns:
            if pdt.is_string_dtype(dfAux[col]):
                dfAux[col] = trl.Translator.translate(text=dfAux[col],
                                                      languageInput=self._languageInput,
                                                      languageOutput=self._languageOutput)
        return dfAux

    def _translateString(self, s: str) -> str:
        """
        Translates a single string.

        Args:
            s:

        Returns:

        """
        return trl.Translator.translate(text=s,
                                        languageInput=self._languageInput,
                                        languageOutput=self._languageOutput)

    def deleteImageFile(self) -> None:
        """
        Deletes plot image file.

        Returns:

        """
        self._pathImage.unlink()

    def hoverTools(self):
        """
        Hover tools for plot HTML.

        Returns:

        """
        pass

    def _saveImageFile(self,
                       Display: MultiDisplay) -> None:
        """
        Saves Image of plot to 'tmp' folder.

        Args:
            Display:

        Returns:

        """
        if isinstance(Display, (bpl.Figure, bm.DataTable)):
            bio.export_png(Display,
                           filename=self._pathImage)
        elif isinstance(Display, altapi.Chart):
            Display.save(fp=self._makePathImage())
        elif isinstance(Display, pdst.Styler):
            ScreenshotPatch.patch()  # Monkey patch for chrome screenshots server
            print(f"SAVING TABLE TO: {self._pathImage} ...")
            dfi.export(obj=Display,
                       filename=str(self._pathImage))
            print(f"SAVING TABLE TO: {self._pathImage} ... DONE!")

        else:
            raise ValueError(f"Display of type {type(Display)} cannot be saved.")

    @classmethod
    def _makePathImage(cls) -> pth.Path:
        idxMax = cls._getMaximumDigit()

        if idxMax is None:
            plotIdx = 0
        else:
            plotIdx = idxMax + 1

        fileName = f"plot_{plotIdx}.png"
        return cls._TEMP_ROOT / fileName

    @classmethod
    def _getMaximumDigit(cls) -> typ.Optional[int]:
        digits = [cls._digitFromFileName(filePath.stem)
                  for filePath in cls._TEMP_ROOT.glob("*.png")]
        digits = [x
                  for x in digits
                  if x is not None]
        if len(digits) > 0:
            return max(digits)
        return None

    @staticmethod
    def _digitFromFileName(s: str) -> typ.Optional[int]:
        base = s.split("_")[-1]
        if base.isnumeric():
            return int(base)
        return None


if __name__ == '__main__':
    print("/n")
    p = pth.Path(__file__).parent / "tmp"
    print(p)
    for x in p.glob("*.png"):
        print(x)
