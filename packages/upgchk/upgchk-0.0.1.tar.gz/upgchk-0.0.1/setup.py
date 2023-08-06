from setuptools import find_packages, setup

name = 'upgchk'

setup(
    name=name,
    version='0.0.1',
    author="fu.lin",
    author_email='fulin10@huawei.com',
    description="upgchk fake package",
    packages=find_packages(),
    package_data={"": ["*"]},
    include_package_data=True,
    zip_safe=False,
)
