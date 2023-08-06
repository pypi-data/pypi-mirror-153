# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['utils_api_pipefy', 'utils_api_pipefy.libs']

package_data = \
{'': ['*']}

install_requires = \
['python-dotenv>=0.19.2,<0.20.0', 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'utils-api-pipefy',
    'version': '0.2.5',
    'description': 'Ferramentas para otimizar o consumo paralelizado de api do pipefy, trantando os retornos.',
    'long_description': '# utils-api-pipefy\n\nBiblioteca que possui um kit de ferramentas úteis para ações usualmente rotineiras de quem trabalha com Pipefy, desde consulta de cards a criação de Pipes, Tables e atualizações em geral.\n\nUtilizamos como apoio as collection requests e python-dotenv.\n\n## Instalação\n\n```\npip install utils-api-pipefy\n```\n\n## .env\nHOST=app or seu_host_pipefy<br>\nPIPE= seu_numero_pipe<br>\nNONPHASES= [numeros_fases_ignoradas]<br>\nTOKEN= seu_token<br>\nLOGENV = DEV or PROD [ PROD remove urlib3 logs ]<br>\nLOGNAME = nome_arquivo_logs<br>\nDISABLELOG = True or False [False disabilita a criação de pasta e arquivo de logs, temos essa opção para utlização em plataformas como Google Cloud Platform, neste caso o logging apenas imprime da tela, sem salvar o log.]<br>\n\n## Exemplo de uso\n\n```py\nimport os\nimport logging\nfrom dotenv import load_dotenv\nfrom utils_api_pipefy.libs.engine import Engine\nfrom utils_api_pipefy.libs.excepts import exceptions\nfrom utils_api_pipefy.libs.log import log\n\nload_dotenv(dotenv_path=fr"{os.getcwd()}\\.env")\nlog().loginit()\n\nif __name__ == "__main__":\n    \n    try:\n        eng = Engine()\n        \n        # ALGUMAS DAS UTILIDADES DO ENGINE\n        logging.info(eng.columns)\n        print(eng.phase_id)\n        print(eng.fields)\n        print(eng.phases)\n        \n        data=eng.run_all_data_phases()\n    \n    except Exception as err:\n        raise exceptions(err)\n\n```',
    'author': 'Yuri Motoshima',
    'author_email': 'yurimotoshima@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/YuriMotoshima/utils-api-pipefy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
