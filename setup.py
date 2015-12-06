from setuptools import setup

setup(
    name='twitter-race',
    version='0.0.4',
    description='',
    license='GPLv2',
    py_modules=['track'],
    author='patillacode',
    author_email='patillacode@gmail.com',
    url='https://github.com/patillacode/twitter-race',
    install_requires=['tweepy>=3.5.0', 'bumpversion>=0.5.3'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: GNU General Public License v2',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7']
)
