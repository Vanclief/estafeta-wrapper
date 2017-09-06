from setuptools import setup

setup(
      name='estafeta_wrapper',
      version='0.0.1',
      description='A wrapper for the Estafeta API using zeep.',
      long_description='Wrapper for the Estafeta API using zeep.',
      url='https://github.com/iuPick/estafeta-wrapper',
      author='iuPick',
      author_email='devops@iupick.com',
      license='MIT',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: API',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
      ],
      keywords='estafeta api iuPick',
      install_requires=['zeep'],
      python_requires='>=3.6',
)
