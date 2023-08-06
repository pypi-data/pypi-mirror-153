import sqlite3
import pandas as pd

from learntools_dados_ufv.core import *

class WeatherDfCreation(EqualityCheckProblem):
    _var = 'df'
    _expected = (
            pd.read_csv('./weatherHistory.csv'),
    )
    _hint = 'Use a função `read_csv` do Pandas para ler o arquivo e construir o DataFrame.'
    _solution = CS(
            "df = pd.read_csv('./weatherHistory.csv')"
    )


qvars = bind_exercises(globals(), [
    WeatherDfCreation
])

__all__ = list(qvars)
