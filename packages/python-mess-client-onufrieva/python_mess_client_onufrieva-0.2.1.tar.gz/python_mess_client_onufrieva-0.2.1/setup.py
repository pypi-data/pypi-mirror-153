from setuptools import setup, find_packages

setup(name="python_mess_client_onufrieva",
      version="0.2.1",
      description="Mess Client",
      author="Ivan Ivanov",
      author_email="iv.iv@yandex.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )