import pandas as pd

from learntools_dados_ufv.core import *
from scipy.stats import percentileofscore

# q1
class Q1(CodingProblem):
    _var = 'population_weight'
    _hint = 'Utilize a função `pd.read_csv` com o caminho do arquivos `pesos_populacao.csv`. Note que não há cabeçalhos no arquivo.'

    _solution = ''

    def check(self, population_weight):
        assert_isinstance(pd.Series, population_weight, name='population_weight')
        assert_series_equals(population_weight, pd.read_csv('./pesos_populacao.csv', header=None, squeeze=True), name='population_weight')

# q2 - a
class Q2A(CodingProblem):
    _var = 'sample_1_weight'
    _hint = 'Utilize a função `pd.read_csv` com o caminho do arquivos `pesos_amostra1.csv`. Note que não há cabeçalhos no arquivo.'

    _solution = ''

    def check(self, sample_1_weight):
        assert_isinstance(pd.Series, sample_1_weight, name='sample_1_weight')
        assert_series_equals(sample_1_weight, pd.read_csv('./pesos_amostra1.csv', header=None, squeeze=True), name='sample_1_weight')

# q2 - b
class Q2B(EqualityCheckProblem):
    _var = 'is_sample_1_from_population'
    _expected = True
    _hints = [
        'Calcule a média da população e da amostra, como no roteiro',
        'Após calcular as médias, calcule o erro padrão.',
        'Veja a diferença entre a média da amostra e da população, em erros padrão',
        'Existe algum valor estatístico de referência que conseguimos comparar pra ter uma certa certeza que uma amostra pertence a população?',
        'Salve o resultado em uma variável booleana, como `is_sample_1_from_population = False` ou `is_sample_1_from_population = True`'
    ]
    _solution = ''

# q2
Q2 = MultipartProblem(Q2A, Q2B)

# q3 - a
class Q3A(CodingProblem):
    _var = 'sample_2_weight'
    _hint = 'Utilize a função `pd.read_csv` com o caminho do arquivos `pesos_amostra2.csv`. Note que não há cabeçalhos no arquivo.'

    _solution = ''

    def check(self, sample_2_weight):
        assert_isinstance(pd.Series, sample_2_weight, name='sample_2_weight')
        assert_series_equals(sample_2_weight, pd.read_csv('./pesos_amostra2.csv', header=None, squeeze=True), name='sample_2_weight')

# q3 - b
class Q3B(EqualityCheckProblem):
    _var = 'is_sample_2_from_population'
    _expected = False
    _hints = [
        'Calcule a média da população e da amostra, como no roteiro',
        'Após calcular as médias, calcule o erro padrão.',
        'Veja a diferença entre a média da amostra e da população, em erros padrão',
        'Existe algum valor estatístico de referência que conseguimos comparar pra ter uma certa certeza que uma amostra pertence a população?',
        'Salve o resultado em uma variável booleana, como `is_sample_2_from_population = False` ou `is_sample_2_from_population = True`'
    ]
    _solution = ''

# q3
Q3 = MultipartProblem(Q3A, Q3B)

# q4 - a
class Q4A(CodingProblem):
    _var = 'sample_3_weight'
    _hint = 'Utilize a função `pd.read_csv` com o caminho do arquivos `pesos_amostra3.csv`. Note que não há cabeçalhos no arquivo.'

    _solution = ''

    def check(self, sample_3_weight):
        assert_isinstance(pd.Series, sample_3_weight, name='sample_3_weight')
        assert_series_equals(sample_3_weight, pd.read_csv('./pesos_amostra3.csv', header=None, squeeze=True), name='sample_3_weight')

# q4 - b
class Q4B(EqualityCheckProblem):
    _var = 'is_sample_3_from_population'
    _expected = False
    _hints = [
        'Calcule a média da população e da amostra, como no roteiro',
        'Após calcular as médias, calcule o erro padrão.',
        'Veja a diferença entre a média da amostra e da população, em erros padrão',
        'Existe algum valor estatístico de referência que conseguimos comparar pra ter uma certa certeza que uma amostra pertence a população?',
        'Salve o resultado em uma variável booleana, como `is_sample_3_from_population = False` ou `is_sample_3_from_population = True`'
    ]
    _solution = ''

# q4
Q4 = MultipartProblem(Q4A, Q4B)

# q5 - a
class Q5A(CodingProblem):
    _var = 'sample_4_weight'
    _hint = 'Utilize a função `pd.read_csv` com o caminho do arquivos `pesos_amostra4.csv`. Note que não há cabeçalhos no arquivo.'

    _solution = ''

    def check(self, sample_4_weight):
        assert_isinstance(pd.Series, sample_4_weight, name='sample_4_weight')
        assert_series_equals(sample_4_weight, pd.read_csv('./pesos_amostra4.csv', header=None, squeeze=True), name='sample_4_weight')

# q5 - b
class Q5B(EqualityCheckProblem):
    _var = 'is_sample_4_from_population'
    _expected = False
    _hints = [
        'Calcule a média da população e da amostra, como no roteiro',
        'Após calcular as médias, calcule o erro padrão.',
        'Veja a diferença entre a média da amostra e da população, em erros padrão',
        'Existe algum valor estatístico de referência que conseguimos comparar pra ter uma certa certeza que uma amostra pertence a população?',
        'Salve o resultado em uma variável booleana, como `is_sample_4_from_population = False` ou `is_sample_4_from_population = True`'
    ]
    _solution = ''

# q5
Q5 = MultipartProblem(Q5A, Q5B)

# q6
class Q6(ThoughtExperiment):
    _hints = [
        'Veja os resultados dessas amostras se pertencem a uma mesma população em comum, nas atividades anteriores.',
    ]
    _solution = ''

qvars = bind_exercises(globals(), [
    Q1,
    Q2,
    Q3,
    Q4,
    Q5,
    Q6
], var_format='q{n}')

__all__ = list(qvars)
