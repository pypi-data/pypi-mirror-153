import setuptools
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()



setuptools.setup(
    name="pctk",
    version="0.1.8",
    author="Miguel Ponce de Leon",
    author_email="miguel.ponce@bsc.es",
    description="PhysiCell ToolKit: a tool for handling MultiCellDS output from PhysiCell and PhysiBoSS simulations.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PhysiBoSS/pctk",
    packages=setuptools.find_packages(where="src"   ),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    # install_requires=["numpy>=1.22.4", "scipy>=1.5.1", "matplotlib>=3.5.2",  "pandas>=1.4.2",  "seaborn>=0.11.2"],
    setup_requires=['numpy', 'scipy', 'matplotlib',  'pandas',  'seaborn'],
    install_requires=['numpy', 'scipy', 'matplotlib',  'pandas',  'seaborn'],
    entry_points={
        'console_scripts': ['plot-time-course=pctk.cmds.plot_time_course:main',
                            'write-pov-files=pctk.cmds.write_pov_files:main',
                            ]
        
    }
)
