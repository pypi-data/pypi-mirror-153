from setuptools import setup


def readme():
    with open('README.md') as readme_f:
        README = readme_f.read()
    return README


setup(
    name='basencode',
    version='1.0.0',
    description='Convert numbers of any base back and forth.',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/Python3-8/basencode',
    author='Pranav Pooruli',
    author_email='pranav.pooruli@gmail.com',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
    ],
    packages=['basencode'],
    include_package_data=True,
)
