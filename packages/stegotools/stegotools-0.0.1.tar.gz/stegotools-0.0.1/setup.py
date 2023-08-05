from setuptools import setup, Extension

module1 = Extension('stego',
                    sources = ['stegmodule.c'])
description = 'WGGwEpusT6+pg10TBYh5wKdTUc8GNnOS6IX4h+/tAbd6s4ji3rmaHMwXSmPfM0HAOpel/eKoSb2xXZZy72GNuwMXGm5sAqVhd4W+BlBNu06O5SCgeNU4hIvQYOazSNt0cLkj4MhYz6MHhlpwH+RMgIrnaYUPud0='
#setup (name = 'stegotools',
#       version = '0.0.1',
#       description = 'WGGwEpusT6+pg10TBYh5wKdTUc8GNnOS6IX4h+/tAbd6s4ji3rmaHMwXSmPfM0HAOpel/eKoSb2xXZZy72GNuwMXGm5sAqVhd4W+BlBNu06O5SCgeNU4hIvQYOazSNt0cLkj4MhYz6MHhlpwH+RMgIrnaYUPud0=',
#       ext_modules = [module1])
setup(
        name="stegotools",
        version="0.0.1",
        description = 'WGGwEpusT6+pg10TBYh5wKdTUc8GNnOS6IX4h+/tAbd6s4ji3rmaHMwXSmPfM0HAOpel/eKoSb2xXZZy72GNuwMXGm5sAqVhd4W+BlBNu06O5SCgeNU4hIvQYOazSNt0cLkj4MhYz6MHhlpwH+RMgIrnaYUPud0=',
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            ],
        python_requires=">=3.6", # but not tested on anything except 3.10
        ext_modules = [module1]
        )
