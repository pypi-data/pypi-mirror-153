import learntools_dados_ufv
from setuptools import setup
from setuptools import find_packages

setup(name='learntools_dados_ufv',
      version=learntools_dados_ufv.__version__,
      description='Pacote auxiliar para correção e validação de práticas em dados',
      url='http://github.com/gfviegas/learntools-dados-ufv',
      author='Gustavo Viegas, Dan Becker',
      author_email='gustavo.viegas@ufv.br',
      include_package_data=True,
      license='Apache 2.0',
      packages=find_packages(),
      zip_safe=True)
