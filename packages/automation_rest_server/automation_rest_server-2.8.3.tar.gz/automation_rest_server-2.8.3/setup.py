from setuptools import setup, find_packages
packages = ["automation_rest_server"]
#python setup.py sdist upload  
#python setup.py bdist_wheel

setup(
    name = 'automation_rest_server',
    version = '2.8.3',
    keywords = ['runner', 'server'],
    description = 'NVMe production server',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
      ],
    license = 'MIT License',
	url = 'https://pypi.org/project/automation_rest_server',
    install_requires = ['flask',
						'flask-restful',
						'requests',
						'PyMySQL==1.0.2',
						'pyftpdlib',
						'nose',
						'nose-printlog',
                        'checksumdir',
                        'pyyaml'],
    packages = find_packages(),
    include_package_data=True, 
    author = 'yuwen123441',
    author_email = 'yuwen123441@126.com',
    platforms = 'any',
    entry_points = {
        'console_scripts': [
        'prun = automation_rest_server.run:run'
        ]}
)