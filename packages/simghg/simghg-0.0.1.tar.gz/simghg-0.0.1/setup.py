import setuptools
with open('README.md', 'r', encoding='utf-8') as fh:
  long_description = fh.read()
  setuptools.setup(
    name='simghg',
    version='0.0.1',
    author='ryusei doi',
    author_email='s2022048@stu.musashino-u.ac.jp',
    description='Package for N2O changing trends in each country in Annex.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/RyuseiDoi/ds_ad', # (accessed on 30 May 2022)
    project_urls={
      'Bug Tracker': 'https://github.com/RyuseiDoi/ds_ad',
    },
    classifiers=[
      'Programming Language :: Python :: 3',
      'License :: OSI Approved :: MIT License',
      'Operating System :: OS Independent',
    ],
    package_dir={'': 'src'},
    py_modules=['simghg'],
    packages=setuptools.find_packages(where='src'),
    python_requires='>=3.7',
    entry_points = {
      'console_scripts': [
        'simghg = simghg:main'
      ]
    },
  )
