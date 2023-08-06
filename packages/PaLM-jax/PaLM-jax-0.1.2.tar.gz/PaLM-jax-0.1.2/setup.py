from setuptools import setup, find_packages

setup(
  name = 'PaLM-jax',
  packages = find_packages(exclude=[]),
  version = '0.1.2',
  license='MIT',
  description = 'PaLM: Scaling Language Modeling with Pathways - Jax',
  author = 'Phil Wang',
  author_email = 'lucidrains@gmail.com',
  long_description_content_type = 'text/markdown',
  url = 'https://github.com/lucidrains/PaLM-jax',
  keywords = [
    'artificial intelligence',
    'deep learning',
    'transformers',
    'attention mechanism'
  ],
  install_requires=[
    'einops==0.4',
    'equinox>=0.5',
    'jax>=0.3.4',
    'jaxlib>=0.1',
    'optax',
    'numpy'
  ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
  ],
)
