import pandas as pd

from learntools_dados_ufv.core import *
from scipy.stats import percentileofscore

# q1
class Q1(CodingProblem):
    _vars = ['men_height_series', 'women_height_series']
    _hint = 'Utilize a função `pd.Series` com o caminho dos arquivos `altura_homens.csv` e `altura_mulheres.csv`. Note que não há cabeçalhos no arquivo.'

    _solution = ''

    def check(self, men_height_series, women_height_series):
        assert_isinstance(pd.Series, men_height_series, name='men_height_series')
        assert_series_equals(men_height_series, pd.read_csv('./altura_homens.csv', header=None, squeeze=True), name='men_height_series')
        assert_isinstance(pd.Series, women_height_series, name='women_height_series')
        assert_series_equals(women_height_series, pd.read_csv('./altura_mulheres.csv', header=None, squeeze=True), name='women_height_series')

# q2
class Q2(CodingProblem):
    _vars = ['men_height_series', 'women_height_series', 'men_min_height', 'men_max_height', 'women_min_height', 'women_max_height']
    _hint = 'Utilize a função `.max()` e `.min()` da classe Series do Pandas'
    _solution = ''

    def check(self, 
            men_height_series,
            women_height_series,
            men_min_height,
            men_max_height,
            women_min_height,
            women_max_height
        ):
        assert_isinstance(float, men_min_height, name='men_min_height')
        assert_isinstance(float, men_max_height, name='men_max_height')
        assert_isinstance(float, women_min_height, name='women_min_height')
        assert_isinstance(float, women_max_height, name='women_max_height')
        assert men_min_height == men_height_series.min(), ('A variável `men_min_height` (valor = `{}`) não possui o valor mínimo da Series `men_height_series`'.format(men_min_height))
        assert men_max_height == men_height_series.max(), ('A variável `men_max_height` (valor = `{}`) não possui o valor máximo da Series `men_height_series`'.format(men_max_height))
        assert women_min_height == women_height_series.min(), ('A variável `women_min_height` (valor = `{}`) não possui o valor mínimo da Series `women_height_series`'.format(women_min_height))
        assert women_max_height == women_height_series.max(), ('A variável `women_max_height` (valor = `{}`) não possui o valor máximo da Series `women_height_series`'.format(women_max_height))

# q3
class Q3(CodingProblem):
    _vars = ['men_height_series', 'women_height_series', 'men_mean_height', 'women_mean_height']
    _hint = 'Utilize a função `.mean()` da classe Series do Pandas'

    _solution = ''

    def check(self,
            men_height_series,
            women_height_series,
            men_mean_height,
            women_mean_height
        ):
        assert_isinstance(float, men_mean_height, name='men_mean_height')
        assert_isinstance(float, women_mean_height, name='women_mean_height')
        assert men_mean_height == men_height_series.mean(), ('A variável `men_mean_height` (valor = `{}`) não possui o valor da média da Series `men_height_series`'.format(men_mean_height))
        assert women_mean_height == women_height_series.mean(), ('A variável `women_mean_height` (valor = `{}`) não possui o valor da média da Series `women_height_series`'.format(women_mean_height))

# q4
class Q4(CodingProblem):
    _vars = ['men_height_series', 'women_height_series', 'men_median_height', 'women_median_height']
    _hint = 'Utilize a função `.median()` da classe Series do Pandas'

    _solution = ''

    def check(self,
            men_height_series,
            women_height_series,
            men_median_height,
            women_median_height
        ):
        assert_isinstance(float, men_median_height, name='men_median_height')
        assert_isinstance(float, women_median_height, name='women_median_height')
        assert men_median_height == men_height_series.median(), ('A variável `men_median_height` (valor = `{}`) não possui o valor da mediana da Series `men_height_series`'.format(men_median_height))
        assert women_median_height == women_height_series.median(), ('A variável `women_median_height` (valor = `{}`) não possui o valor da mediana da Series `women_height_series`'.format(women_median_height))

# q5
class Q5(CodingProblem):
    _vars = ['men_height_series', 'women_height_series', 'men_std_height', 'women_std_height']
    _hint = 'Utilize a função `.std()` da classe Series do Pandas'

    _solution = ''

    def check(self,
            men_height_series,
            women_height_series,
            men_std_height,
            women_std_height
        ):
        assert_isinstance(float, men_std_height, name='men_std_height')
        assert_isinstance(float, women_std_height, name='women_std_height')
        assert men_std_height == men_height_series.std(), ('A variável `men_std_height` (valor = `{}`) não possui o valor do desvio padrão da Series `men_height_series`'.format(men_std_height))
        assert women_std_height == women_height_series.std(), ('A variável `women_std_height` (valor = `{}`) não possui o valor do desvio padrão da Series `women_height_series`'.format(women_std_height))

# q6
class Q6(CodingProblem):
    _vars = ['men_height_series', 'men_shorter_160cm_perc']
    _hints = [
        'Faça o filtro de acesso à serie usando a sintaxe `series[filtro]`.',
        'Divida o total filtrado pelo total da base para ter a proporção',
        'Não esqueça de multiplicar o resultado da divisão por 100...'
    ]

    _solution = ''

    def check(self,
            men_height_series,
            men_shorter_160cm_perc
        ):
        assert_isinstance(float, men_shorter_160cm_perc, name='men_shorter_160cm_perc')
        assert men_shorter_160cm_perc <= 100 and men_shorter_160cm_perc >= 0, ('A variável `men_shorter_160cm_perc` deve possuir um valor entre 0 e 100.')
        men_shorter_160cm = men_height_series[men_height_series < 160]
        result = 100 * (len(men_shorter_160cm) / len(men_height_series))
        assert men_shorter_160cm_perc == result, ('A variável `men_shorter_160cm_perc` (valor = `{}`) não possui o valor do percentual de homens com altura menor que 160cm da Series `men_height_series`'.format(men_shorter_160cm_perc))

# q7
class Q7(CodingProblem):
    _vars = ['women_height_series', 'women_taller_180cm_perc']
    _hints = [
        'Faça o filtro de acesso à serie usando a sintaxe `series[filtro]`.',
        'Divida o total filtrado pelo total da base para ter a proporção',
        'Não esqueça de multiplicar o resultado da divisão por 100...'
    ]

    _solution = ''

    def check(self,
            women_height_series,
            women_taller_180cm_perc
        ):
        assert_isinstance(float, women_taller_180cm_perc, name='women_taller_180cm_perc')
        assert women_taller_180cm_perc <= 100 and women_taller_180cm_perc >= 0, ('A variável `women_taller_180cm_perc` deve possuir um valor entre 0 e 100.')
        women_taller_180cm = women_height_series[women_height_series > 180]
        result = 100 * (len(women_taller_180cm) / len(women_height_series))
        assert women_taller_180cm_perc == result, ('A variável `women_taller_180cm_perc` (valor = `{}`) não possui o valor do percentual de homens com altura menor que 160cm da Series `women_height_series`'.format(women_taller_180cm_perc))

# q8
class Q8(CodingProblem):
    _vars = ['men_height_series', 'men_185cm_percentile']
    _hints = [
        'Pesquise sobre a função `percentileofscore` do pacote SciPy',
        'Realmente use a função `percentileofscore` do pacote SciPy'
    ]

    _solution = ''

    def check(self,
            men_height_series,
            men_185cm_percentile
        ):
        assert_isinstance(float, men_185cm_percentile, name='men_185cm_percentile')
        result = percentileofscore(men_height_series, 185)
        assert men_185cm_percentile == result, ('A variável `men_185cm_percentile` (valor = `{}`) não possui o valor do percentil de um homem com altura de 185cm'.format(men_185cm_percentile))

# q9
class Q9(CodingProblem):
    _vars = ['women_height_series', 'women_150cm_percentile']
    _hints = [
        'Pesquise sobre a função `percentileofscore` do pacote SciPy',
        'Realmente use a função `percentileofscore` do pacote SciPy'
    ]

    _solution = ''

    def check(self,
            women_height_series,
            women_150cm_percentile
        ):
        assert_isinstance(float, women_150cm_percentile, name='women_150cm_percentile')
        result = percentileofscore(women_height_series, 150)
        assert women_150cm_percentile == result, ('A variável `women_150cm_percentile` (valor = `{}`) não possui o valor do percentil de um homem com altura de 185cm'.format(women_150cm_percentile))

# q10
class Q10(CodingProblem):
    _vars = ['men_height_series', 'men_top3_height', 'men_in_top3_height']
    _hints = [
        'Pesquise sobre a função `value_counts` da classe Series do Pandas',
        'Pesquise sobre a função `head` da classe Series do Pandas',
        'Pesquise sobre a função `iloc` da classe Series do Pandas',
        'Some o total das pessoas nas 3 alturas!',
    ]

    _solution = ''

    def check(self,
            men_height_series,
            men_top3_height,
            men_in_top3_height
        ):
        assert_isinstance(pd.Series, men_top3_height, name='men_top3_height')
        assert_isinstance(int, men_in_top3_height, name='men_in_top3_height')
        vc = men_height_series.value_counts()
        for i, _row in men_top3_height.iteritems():
            assert i in vc, ('O valor {} não é uma das top 3 alturas dos homens'.format(i))

     
     
# q11
class Q11(CodingProblem):
    _vars = ['women_height_series', 'women_185cm_std_distance', 'women_145cm_std_distance']
    _hints = [
        'Pesquise sobre a função `std` da classe Series do Pandas para extrair o desvio padrão',
        'Pesquise sobre a função `mean` da classe Series do Pandas para extrair a média',
    ]

    _solution = ''

    def check(self,
            women_height_series,
            women_185cm_std_distance,
            women_145cm_std_distance
        ):
        assert_isinstance(float, women_185cm_std_distance, name='women_185cm_std_distance')
        assert_isinstance(float, women_145cm_std_distance, name='women_145cm_std_distance')
        
        mean = women_height_series.mean()
        std = women_height_series.std()

        d1 = abs(185 - mean) / std
        d2 = abs(145 - mean) / std

        assert women_185cm_std_distance == d1, ('O valor {} não é o resultado correto da quantidade de desvios padrão de distância da média'.format(women_185cm_std_distance))
        assert women_145cm_std_distance == d2, ('O valor {} não é o resultado correto da quantidade de desvios padrão de distância da média'.format(women_145cm_std_distance))

# q12
class Q12(ThoughtExperiment):
    _hint = 'Tente olhar para alguma métrica para embasar sua resposta'

# q13
class Q13(ThoughtExperiment):
    _hint = 'Use algum método de teste de normalidade. O mais simples pode ser o mais elegante!'

# q14
class Q14(ThoughtExperiment):
    _hint = 'Não vale copiar e colar da documentação, hein...'

# q15
class Q15(ThoughtExperiment):
    _hint = 'Não vale copiar e colar da documentação, hein...'

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
    Q12,
    Q13,
    Q14,
    Q15,
], var_format='q{n}')

__all__ = list(qvars)
