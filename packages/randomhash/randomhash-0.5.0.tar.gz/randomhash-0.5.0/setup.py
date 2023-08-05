# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['randomhash']

package_data = \
{'': ['*']}

install_requires = \
['xxhash>=3.0.0,<4.0.0']

setup_kwargs = {
    'name': 'randomhash',
    'version': '0.5.0',
    'description': 'A simple, time-tested, family of random hash functions in Python, based on CRC32 and xxHash, affine transformations, and the Mersenne Twister.',
    'long_description': '# Python `randomhash` package\n\nA simple, time-tested, family of random hash functions in Python, based on CRC32\nand xxHash, affine transformations, and the Mersenne Twister.\n\nThis is a companion library to [the identical Java version](https://github.com/jlumbroso/java-random-hash).\n\n## Installation and usage\n\nThe library is available on PyPI, and can be installed through normal means:\n\n```shell\n$ pip install randomhash\n```\n\nOnce installed, it can be called either by instantiating a family of random\nhash functions, or using the default instantiated functions:\n\n```python\nimport randomhash\n\n# Create a family of random hash functions, with 10 hash functions\n\nrfh = randomhash.RandomHashFamily(count=10)\nprint(rfh.hashes("hello"))  # will compute the ten hashes for "hello"\n\n# Use the default instantiated functions\n\nprint(randomhash.hashes("hello", count=10))\n```\n\n## Features\n\nThis introduces a family of hash functions that can be used to implement probabilistic\nalgorithms such as HyperLogLog. It is based on _affine transformations of either the\nCRC32 hash functions_, which have been empirically shown to provide good performance\n(for consistency with other versions of this library, such as the Java version), or\n[the more complex xxHash hash functions](https://cyan4973.github.io/xxHash/) that are\nmade available through [the `xxhash` Python bindings](https://github.com/ifduyue/python-xxhash).\nThe pseudo-random numbers are drawn according to\n[the standard Python implementation](https://docs.python.org/3/library/random.html)\nof the [Mersenne Twister](http://www.math.sci.hiroshima-u.ac.jp/~m-mat/MT/emt.html).\n\n<!-- NEEDS TO BE REWRITTEN FOR PYTHON VERSION\n\nTo try out the hash functions, you can compile and run the example program:\n\n```shell\njavac Example.java\njava Example\n```\n\nThis will generate a report, such as the one below, which shows how a hundred\nhash functions perform on provided data that appears pseudo-random (note that it\nis important when running these audits that the data provide as input be made\nof _unique_ elements, even if the hash functions will mainly be used in streaming\nalgorithms, to project duplicates to the same hashed value):\n\n```\njava Example\ninput: data/unique.txt\nnumber of hash functions: 100\nhashing report:\n> bucket count: 10\n> total values hashed: 1670700\n> [ 10.00% 10.03% 10.03%  9.96% 10.01% 10.00%  9.99%  9.98% 10.02%  9.98%  ]\n> chi^2 test: 0.000399\n> is uniform (with 90% confidence)? true\n```\n\nIn practice, you can use it this way, by instantiating a family and using the\n`hash(String)` method to generate a single hashed value:\n\n```java\nimport randomhash.RandomHashFamily;\n\nRandomHashFamily rhf = new RandomHashFamily(1);\n\nSystem.out.print("hello -> ");\nSystem.out.print(rhf.hash("hello"));\n```\n\nwhich will print:\n\n```\nhello -> 2852342977\n```\n\nand it can also generate several pseudo-random hash values at the same time,\nin this case 10, which it will return in an array:\n\n```java\nRandomHashFamily rhf = new RandomHashFamily(10);\nlong[] hashes = rhf.hashes(); // 10 elements\n```\n\n-->\n\n## Some history\n\nIn 1983, G. N. N. Martin and Philippe Flajolet introduced the algorithm known\nas [_Probabilistic Counting_](http://algo.inria.fr/flajolet/Publications/FlMa85.pdf),\ndesigned to provide an extremely accurate and efficient\nestimate of the number of unique words from a document that may contain repetitions.\nThis was an incredibly important algorithm, which introduced a **revolutionary idea**\nat the time:\n\n> The only assumption made is that records can be hashed in a suitably pseudo-uniform\n> manner. This does not however appear to be a severe limitation since empirical\n> studies on large industrial files [5] reveal that _careful_ implementations of\n> standard hashing techniques do achieve practically uniformity of hashed values.\n\nThe idea is that hash functions can "transform" data into pseudo-random variables.\nThen a text can be treated as a sequence of random variables drawn from a uniform\ndistribution, where a given word will always occur as the same random value (i.e.,\n`a b c a a b c` could be hashed as `.00889 .31423 .70893 .00889 .00889 .31423 .70893` with\nevery occurrence of `a` hashing to the same value). While this sounds strange,\nempirical evidence suggests it is true enough in practice, and eventually [some\ntheoretical basis](https://people.seas.harvard.edu/~salil/research/streamhash-Jun10.pdf)\nhas come to support the practice.\n\nThe original _Probabilistic Counting_ (1983) algorithm gave way to _LogLog_ (2004),\nand then eventually _HyperLogLog_ (2007), one of the most famous algorithms in the\nworld as described in [this article](https://arxiv.org/abs/1805.00612). These algorithms\nand others all used the same idea of hashing inputs to treat them as random variables,\nand proved remarkably efficient and accurate.\n\nBut as highlighted in the above passage, it is important to be _careful_.\n\n## Hash functions in practice\n\nIn practice, it is easy to use poor quality hash functions, or to use cryptographic\nfunctions which will significantly slow down the speed (and relevance) of the\nprobabilistic estimates. However, on most data, some the cyclic polynomial checksums\n(such as Adler32 or CRC32) provide good results---as do efficient, general-purpose\nnon-cryptographic hash functions such as xxHash.\n',
    'author': 'Jérémie Lumbroso',
    'author_email': 'lumbroso@cs.princeton.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jlumbroso/python-random-hash',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
