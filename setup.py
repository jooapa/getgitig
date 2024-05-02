from setuptools import setup, find_packages

setup(
    name='getgitig',
    version='0.1',
    packages=find_packages(),
    author='Jooapa',
    author_email='your@email.com',
    description='get .gitignore fast for your project',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/jooapa/getgitig',
    license='Unlicense',
    install_requires=[
        'inquirer',
        'requests',
    ],
    classifiers=[
        # Classifiers (optional)
    ],
)
