from setuptools import setup, find_packages

setup(
    name='gitlab-kanban',
    version='0.0.1',
    url="https://github.com/rofrano/gitlab-kanban",
    author="John Rofrano",
    author_email='rofrano@gmail.com',
    description="GitLab Kanban Board Command Line Interface",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    keywords="gitlab kanban",
    license="Apache",
    python_requires=">=3.9.0",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    install_requires=[
        'click==8.1.3',
        'requests==2.27.1',
        'tqdm==4.64.0'
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
    ],
    extras_require = {
        "dev": [
            "nose==1.3.7",
            "pinocchio==0.4.3",
            "coverage==6.3.2",
            "pylint==2.13",
            "flake8==4.0.1",
            "black==22.3.0"
        ],
    },
    entry_points={
        'console_scripts': [
            'kanban = kanban.cli:cli'
        ],
    },
)
