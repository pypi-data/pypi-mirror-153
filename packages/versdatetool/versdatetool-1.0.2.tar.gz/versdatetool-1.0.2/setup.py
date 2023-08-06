from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
with open('requirements.txt') as f:
    requirements = f.readlines()

# long_description = 'Description: Package making for simple CLI AUTOMATION TOOL FOR QUICK pr GENERATION'

setup(
    name='versdatetool',
    version='1.0.2',
    author='V Surya kumar',
    author_email='kumarsurya.2001@gmail.com',
    url='https://github.com/dyte-submissions/dyte-vit-2022-surya-x',
    description='Package making for simple CLI AUTOMATION TOOL FOR QUICK pr GENERATION.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    packages=find_packages(),
    package_data={'': ['config.py']},
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'versdatetool = app.main:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords='Dyte SDK Tooling CLI Tool',
    install_requires=requirements,
    zip_safe=False
)
