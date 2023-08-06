from setuptools import setup

setup(
    name = 'qhsmodule',
    version = '1.0.0',
    description = 'My first module',
    author = 'qinhaisheng',
    author_email = '1849039507@qq.com',
    # 需要打包的目录(包含__init__.py文件夹)
    packages=['qhsmodule'],
    #如果不是所有文件打包,可以指定打包文件
    py_modules = ['qhsmodule.module1','qhsmodule.module2']
)