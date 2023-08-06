from setuptools import setup

setup(
    name='bisect_find_first_bad',
    version='0.0.1',
    description='tool like `git bisect run` but checks arbitrary options and not uses git to switch versions',
    long_description_content_type="text/markdown",
    url='https://github.com/tandav/bisect_find_first_bad',
    # packages=find_packages(),
    py_modules=['bisect_find_first_bad'],
    include_package_data=True,
)
