import pandas as pd

from learntools_dados_ufv.core import *

# q1
class Q1(CodingProblem):
    _var = 'series'
    _hint = 'Utilize a função `pd.Series` com uma lista de números aleatórios como argumento. A função `random.sample` pode ser útil...'

    _solution = ''
#     _solution = CS('''\
# # O segundo paramêtro da função range() não é inclusivo, por isso deve-se usar 1001 e não 1000.
# values = random.sample(range(-1000, 1001), 500)
# series = pd.Series(values)
# series
#     ''')

    def check(self, series):
        assert_isinstance(pd.Series, series, name=self._var)
        series_len = len(series)
        assert series_len == 500, ('Esperado que a variável `series` tenha uma série com 500 valores mas possui {}'.format(series_len))
        series_max = series.max()
        assert series_max <= 1000, ('Esperado que a variável `series` tenha uma série com um valor máximo de até **1000**, mas possui um valor máximo de **{}**'.format(series_max))
        series_min = series.min()
        assert series_min >= -1000, ('Esperado que a variável `series` tenha uma série com um valor mínimo de pelo menos **-1000**, mas possui um valor mínimo de **{}**'.format(series_min))

# q2
class Q2(CodingProblem):
    _vars = ['series', 'series_max']
    _hint = 'Utilize a função `.max()` da classe Series do Pandas'

    _solution = ''
#     _solution = CS('''\
# series_max = series.max()
# print(series_max)
#     ''')

    def check(self, series, series_max):
        assert_isinstance(int, series_max, name=self._var)
        correct_vaue = series.max()
        assert series_max == correct_vaue, ('A variável `series_max` (valor = `{}`) não possui o valor máximo da série `series`'.format(series_max))

# q3
class Q3(CodingProblem):
    _vars = ['series', 'series_min']
    _hint = 'Utilize a função `.min()` da classe Series do Pandas'

    _solution = ''
#     _solution = CS('''\
# series_min = series.min()
# print(series_min)
#     ''')

    def check(self, series, series_min):
        assert_isinstance(int, series_min, name=self._var)
        correct_vaue = series.min()
        assert series_min == correct_vaue, ('A variável `series_min` (valor = `{}`) não possui o valor mínimo da série `series`'.format(series_min))

# q4
class Q4(CodingProblem):
    _vars = ['series', 'series_positives']
    _hint = 'Faça o filtro de acesso à serie usando a sintaxe `series[filtro]`.'

    _solution = ''
#     _solution = CS('''\
# series_positives = series[series > 0]
# print(series_positives)
#     ''')

    def check(self, series, series_positives):
        assert_isinstance(pd.Series, series_positives, name=self._var)
        assert_series_equals(series_positives, series[series > 0])

# q5
class Q5(CodingProblem):
    _vars = ['series', 'series_odds']
    _hints = [
        'Faça o filtro de acesso à serie usando a sintaxe `series[filtro]`.',
        'Um dado é ímpar quando não é divsível por 2 (resto da divisão != 0)',
        'Você também pode usar a função `pd.Series.apply` passando uma função com o retorno se um dado item da série deve ser incluso na filtragem ou não'
    ]

    _solution = ''
#     _solution = CS('''\
# series_odds = series[series % 2 == 1]
# # ou...
# series_odds = series[series % 2 != 0]
# # ou...
# def is_even(number):
#     return (number % 2) != 0

# series_odds = series[series.apply(is_even)]

# print(series_odds)
#     ''')

    def check(self, series, series_odds):
        assert_isinstance(pd.Series, series_odds, name=self._var)
        assert_series_equals(series_odds, series[series % 2 == 1])

# q6
class Q6(CodingProblem):
    _vars = ['series', 'series_range']
    _hints = [
        'Faça o filtro de acesso à serie usando a sintaxe `series[filtro]`.',
        'Você pode usar a sintaxe de acesso à listas de python lista[n:m] onde n é o número inicial e m o final',
        'O número final de um range python é não inclusivo!'
    ]

    _solution = CS('''\
series_range = series[50:101]

print(series_odds)
    ''')

    def check(self, series, series_range):
        assert_isinstance(pd.Series, series_range, name=self._var)
        assert_series_equals(series_range, series[50:101])

# q7
class Q7(CodingProblem):
    _vars = ['series', 'series_even_size']
    _hints = [
        'Faça o filtro de acesso à serie usando a sintaxe `series[filtro]`.',
        'Um dado é par quando é divsível por 2 (resto da divisão == 0)',
        'Você pode usar a mesma função python para saber o tamanho de uma lista, ou utilizar uma propridade `size` do `pd.Series`.'
    ]

    _solution = ''
#     _solution = CS('''\
# series_even_size = series[series % 2 == 0].size

# print(series_even_size)
#     ''')

    def check(self, series, series_even_size):
        assert_isinstance(int, series_even_size, name=self._var)
        assert series_even_size == series[series % 2 == 0].size

# q8
class Q8(CodingProblem):
    _vars = ['series', 'series_high_values_size']
    _hints = [
        'Faça o filtro de acesso à serie usando a sintaxe `series[filtro]`.',
        'Você pode usar a mesma função python para saber o tamanho de uma lista, ou utilizar uma propridade `size` do `pd.Series`.'
    ]

    _solution = ''
#     _solution = CS('''\
# series_high_values_size = series[series > 500].size

# print(series_high_values_size)
#     ''')

    def check(self, series, series_high_values_size):
        assert_isinstance(int, series_high_values_size, name=self._var)
        assert series_high_values_size == series[series > 500].size

# q9
class Q9(CodingProblem):
    _vars = ['series', 'series_subset_values']
    _hints = [
        'Faça o filtro de acesso à serie usando a sintaxe `series[filtro]`. Você pode usar múltiplas condições no filtro usando operadores booleanos.',
        'Talvez você precise utilizar parenteses para isolar os filtros...',
    ]

    _solution = ''
#     _solution = CS('''\
# series_subset_values = series[(series > 500) & (series < 700)]

# print(series_subset_values)
#     ''')

    def check(self, series, series_subset_values):
        assert_isinstance(pd.Series, series_subset_values, name=self._var)
        assert_series_equals(series_subset_values, series[(series > 500) & (series < 700)])

# q10
class Q10(CodingProblem):
    _vars = ['series', 'series_sqrt_values']
    _hint = 'Talvez a função `pd.Series.apply` seja útil... Ou talvez você possa fazer operações matemáticas diretamente na série...'

    _solution = ''
#     _solution = CS('''\
# series_sqrt_values = series ** 0.5

# print(series_sqrt_values)
#     ''')

    def check(self, series, series_sqrt_values):
        assert_isinstance(pd.Series, series_sqrt_values, name=self._var)
        assert_series_equals(series_sqrt_values, series ** 0.5)


# q11.a
class Q11A(CodingProblem):
    _var = 'grades'
    _hint = 'Utilize a função `pd.Series` com uma lista de números como argumento. A função `random.sample` pode ser útil...'

    _solution = ''
#     _solution = CS('''\
# # Você vai precisar criar sua própria estratégia para os valores `values`.
# grades = pd.Series(values)
#         ''')

    def check(self, grades):
        assert_isinstance(pd.Series, grades, name=self._var)

# q11.b
class Q11B(ThoughtExperiment):
    _hint = 'Que tal você olhar nos exercícios de 1 a 10? Pense como um pedagogo ou diretor da escola. Quais informações, mesmo que simples, você iria querer saber sobre seus alunos?'
    # _solution = ('Séries em Pandas possui várias funções úteis, para recuperar valores máximos, mínimos, média, mediana, etc. Essas informações são ricas em qualidade dependendo do contexto, mesmo que simples!')
    _solution = ''

# q11.c
class Q11C(ThoughtExperiment):
    _hint = 'Pense em quais respostas sobre o contexto de turmas de 5ª série apresentado uma série **não** consegue responder?'
    # _solution = ('Séries são úteis, mas são limitadas. Você não consegue extrair informação sobre turmas individuais, por exemplo. Essa questão é para debatermos, então não há bem uma resposta correta. Pense em mais limitações!')
    _solution = ''

# q11
Q11 = MultipartProblem(Q11A, Q11B, Q11C)

qvars = bind_exercises(globals(), [
    Q1,
    Q2,
    Q3,
    Q4,
    Q5,
    Q6,
    Q7,
    Q8,
    Q9,
    Q10,
    Q11,
], var_format='q{n}')

__all__ = list(qvars)
