from setuptools import setup, find_packages

setup(
    name='softeam_common_utils',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'redis',
        'requests',
        'confluent-kafka',
        'Flask-APScheduler',
        'mysql-connector-python'
    ],
    include_package_data=True,  # Ensures non-Python files (like README.MD) are included
    description='A utility package for common functions in the Softeam project',
    #long_description=open('README.MD').read(),
    long_description_content_type='text/markdown',
    author='Soham Choudhury',
    author_email='soham874@gmail.com',
    url='https://github.com/soham874/Common-Utils',  # Replace with actual URL
)