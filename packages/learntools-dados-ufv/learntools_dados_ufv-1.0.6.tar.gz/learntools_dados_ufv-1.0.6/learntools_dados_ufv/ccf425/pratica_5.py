import pandas as pd

from learntools_dados_ufv.core import *
from scipy.stats import percentileofscore

# q1
class Q1(CodingProblem):
    _vars = ['df', 'missing_invoice_no']
    _hints = [
        'Pesquise sobre a função `df.isna` do Pandas.',
        'Você pode usar a função `pd.isnull` com o seu dataframe, igual mostra o roteiro.',
        'A resposta é um número inteiro com a quantidade de registros.'
    ]

    _solution = ''

    def check(self, df, missing_invoice_no):
        assert_isinstance(pd.DataFrame, df, name='df')
        assert_isinstance(int, missing_invoice_no, name='missing_invoice_no')
        answer = len(df[df["InvoiceNo"].isna()])
        assert_equal(answer, missing_invoice_no, name='answer')

# q2
class Q2(CodingProblem):
    _vars = ['df', 'invalid_unit_price']
    _hints = [
        'Como você pode filtrar uma coluna de um dataframe?',
        'Veja os exemplos de filtros do roteiro.',
        'A resposta é um número inteiro com a quantidade de registros.'
    ]

    _solution = ''

    def check(self, df, invalid_unit_price):
        assert_isinstance(pd.DataFrame, df, name='df')
        assert_isinstance(int, invalid_unit_price, name='invalid_unit_price')
        answer = len(df[df["UnitPrice"] < 0])
        assert_equal(answer, invalid_unit_price, name='answer')

# q3
class Q3(CodingProblem):
    _vars = ['df']
    _hints = [
        'Pesquise sobre a função `df.drop` do Pandas.',
        'Execute a mesma consulta da questão anterior depois de alterar os valores para garantir que os objetos foram removidos.',
        'Restaure a versão do dataframe com `df = original_df` caso tenha alterado coisa demais.',
        'Veja os exemplos de limpeza de dados inválidos do roteiro.',
        'Você só precisa passar os índices dos valores que quer remover para a função `df.drop`.',
        'Você pode recuperar os índices de um dataframe filtrado com `df.index`.'
    ]

    _solution = ''

    def check(self, df):
        assert_isinstance(pd.DataFrame, df, name='df')
        answer = df.drop(df.index[df['UnitPrice'] < 0])
        assert_df_equals(df, answer, name='df')

# q4
class Q4(CodingProblem):
    _vars = ['df', 'top_customer_id']
    _hints = [
        'O ID do Cliente é referente ao atributo CustomerID`',
        'Revisite o roteiro e procure por uma forma fácil de visualizar a contagem de valores mais frequentes.',
        'A resposta é um inteiro com o valor do atributo CustomerID.'
    ]

    _solution = ''

    def check(self, df, top_customer_id):
        assert_isinstance(pd.DataFrame, df, name='df')
        assert_isinstance(int, top_customer_id, name='top_customer_id')
        answer = 17841
        assert_equal(top_customer_id, answer, name='top_customer_id')

# q5
class Q5(CodingProblem):
    _vars = ['df', 'most_expensive_product']
    _hints = [
        'Tente recuperar primeiro qual o maior valor da coluna de Preço Unitário.',
        'Você pode seguir o mesmo caminho da questão anterior, mas existem formas mais simples e elegante usando um simples filtro.',
        'Talvez após filtrar você precise usar a função `df.iloc` para recuperar a primeira linha do registro, e acessar a coluna desejada depois.',
        'A resposta é uma string com o valor da descrição do produto.'
    ]

    _solution = ''

    def check(self, df, most_expensive_product):
        assert_isinstance(pd.DataFrame, df, name='df')
        assert_isinstance(str, most_expensive_product, name='most_expensive_product')
        answer = 'Manual'
        assert_equal(most_expensive_product, answer, name='most_expensive_product')

# q6
class Q6(CodingProblem):
    _vars = ['df', 'germany_orders_percentage']
    _hints = [
        'Utilize os filtros como detalhado no roteiro para remover o país `United Kingdom` da seleção.',
        'Veja a função `df.value_counts` do Pandas.',
        'Você pode chamar a função `value_counts` diretamente em uma coluna (ex: `df["Coluna"].value_counts()).',
        'Você pode passar o parâmetro `normalize=True` na função `value_counts`, como mostra o roteiro.',
        'O retorno da função `value_counts` é uma Serie pandas. Basta acessá-lo passando um índice como `serie["MeuIndice"]`.',
        'A resposta é um float representando a porcentagem (lembre-se de multiplicar por 100!).'
    ]

    _solution = ''

    def check(self, df, germany_orders_percentage):
        assert_isinstance(pd.DataFrame, df, name='df')
        assert_isinstance(float, germany_orders_percentage, name='germany_orders_percentage')
        answer = df[df['Country'] != 'United Kingdom'].Country.value_counts(normalize=True)['Germany'] * 100
        assert_equal(germany_orders_percentage, answer, name='germany_orders_percentage')

# q7
class Q7(CodingProblem):
    _vars = ['df', 'most_items_order']
    _hints = [
        'Recupere primeiro qual instância tem a maior quantidade de produtos (coluna Quantity).',
        'Utilize filtros para acessar o dataframe que tem a coluna `Quantity` com o valor recuperado da dica anteiror.',
        'A resposta é um dataframe filtrado.'
    ]

    _solution = ''

    def check(self, df, most_items_order):
        assert_isinstance(pd.DataFrame, df, name='df')
        assert_isinstance(pd.DataFrame, most_items_order, name='most_items_order')
        answer = df[df['Quantity'] == df['Quantity'].max()]
        assert_df_equals(most_items_order, answer, name='most_items_order')

# q8
class Q8(CodingProblem):
    _vars = ['df', 'most_expensive_order']
    _hints = [
        'Pense numa compra que você faz em algum comércio. Como é calculado o valor final?.',
        'Veja no roteiro como criar uma coluna composta, pode ser útil.',
        'Pense que cada instância do dataframe é um registro de um produto em uma compra.',
        'O que identifica uma compra no dataframe?',
        'Tente agrupar os registros pelo identificador da compra.',
        'Com os registros agrupados, veja sobre a função `dfgroupedby.sum` do Pandas',
        'Tente somar o valor pago por todos os produtos em uma compra.',
        'Tente ordenar as instâncias da compra pelo seu valor pago e veja qual o valor da coluna InvoiceNo',
        'A resposta é um inteiro com o valor do identificador da compra (InvoiceNo).'
    ]

    _solution = ''

    def check(self, df, most_expensive_order):
        assert_isinstance(pd.DataFrame, df, name='df')
        assert_isinstance(int, most_expensive_order, name='most_expensive_order')
        answer = 581483
        assert_equal(most_expensive_order, answer, name='most_expensive_order')

qvars = bind_exercises(globals(), [
    Q1,
    Q2,
    Q3,
    Q4,
    Q5,
    Q6,
    Q7,
    Q8
], var_format='q{n}')

__all__ = list(qvars)
