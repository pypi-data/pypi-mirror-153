import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='faster_dj_dev',
    version='0.1.6',
    author='Selmi Abderrahim',
    author_email='contact@selmi.tech',
    description='A tool that makes your Django development faster.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/SelmiAbderrahim/faster-dj-dev',
    project_urls = {
        "Bug Tracker": "https://github.com/SelmiAbderrahim/faster-dj-dev/issues"
    },
    entry_points={
        'console_scripts': [
            'faster_dj_dev=faster_dj_dev.faster_dj:main',
        ],
    },

    include_package_data=True,
    package_data={
        "faster_dj_dev.data": ["*.json"],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    keywords='django productivity automation fast development',
    license='MIT',
    packages=['faster_dj_dev','faster_dj_dev.codebase','faster_dj_dev.starter', 'faster_dj_dev.core', 'faster_dj_dev.data', 'faster_dj_dev.utils', 'faster_dj_dev.venvs', 'faster_dj_dev.commands'],
    install_requires=['yapf==0.32.0', 'click==8.1.0', 'colorama==0.4.4', 'termcolor==1.1.0'],
)
