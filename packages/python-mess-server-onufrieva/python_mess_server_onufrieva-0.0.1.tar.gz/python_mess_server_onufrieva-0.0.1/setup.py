from setuptools import setup, find_packages

setup(name="python_mess_server_onufrieva",
      version="0.0.1",
      description="Mess Server",
      author="Ivan Ivanov",
      author_email="iv.iv@yandex.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex'],
      scripts=['server/server_run']
      )
