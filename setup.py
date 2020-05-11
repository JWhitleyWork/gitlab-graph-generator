from distutils.core import setup

setup(
    name='GitlabGraphGenerator',
    version='0.1',
    packages=['gitlabgraphgenerator'],
    package_data={'gitlabgraphgenerator': ['data/*']},
    requires=['gitlab'],
    license='MIT License',
    long_description=open('README.md').read(),
)
