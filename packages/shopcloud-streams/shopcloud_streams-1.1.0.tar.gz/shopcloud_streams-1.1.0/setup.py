from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name='shopcloud_streams',
    version='1.1.0',
    description='CLI Tool for Shopcloud Streams',
    long_description_content_type="text/markdown",
    long_description=README,
    license='MIT',
    packages=find_packages(),
    author='Konstantin Stoldt',
    author_email='konstantin.stoldt@talk-point.de',
    keywords=['CLI'],
    url='https://github.com/Talk-Point/shopcloud-streams-cli',
)

install_requires = [
    'requests',
    'shopcloud_secrethub'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)