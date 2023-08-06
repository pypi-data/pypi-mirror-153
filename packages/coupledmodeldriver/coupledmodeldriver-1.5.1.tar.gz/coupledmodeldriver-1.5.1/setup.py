# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['coupledmodeldriver',
 'coupledmodeldriver.client',
 'coupledmodeldriver.configure',
 'coupledmodeldriver.configure.forcings',
 'coupledmodeldriver.generate',
 'coupledmodeldriver.generate.adcirc',
 'coupledmodeldriver.generate.schism']

package_data = \
{'': ['*']}

install_requires = \
['adcircpy>=1.2.1,<2.0.0',
 'file-read-backwards',
 'nemspy>=1.0.4',
 'numpy',
 'pyproj',
 'pyschism',
 'typepigeon>=1.0.3,<2.0.0']

extras_require = \
{'development': ['isort', 'oitnb'],
 'documentation': ['m2r2',
                   'sphinx',
                   'sphinx-rtd-theme',
                   'sphinxcontrib-programoutput'],
 'testing': ['pooch', 'pytest', 'pytest-cov', 'pytest-socket', 'pytest-xdist']}

entry_points = \
{'console_scripts': ['check_completion = '
                     'coupledmodeldriver.client.check_completion:main',
                     'generate_adcirc = '
                     'coupledmodeldriver.client.generate_adcirc:main',
                     'generate_schism = '
                     'coupledmodeldriver.client.generate_schism:main',
                     'initialize_adcirc = '
                     'coupledmodeldriver.client.initialize_adcirc:main',
                     'initialize_schism = '
                     'coupledmodeldriver.client.initialize_schism:main',
                     'unqueued_runs = '
                     'coupledmodeldriver.client.unqueued_runs:main']}

setup_kwargs = {
    'name': 'coupledmodeldriver',
    'version': '1.5.1',
    'description': 'coupled model configuration generation',
    'long_description': '# CoupledModelDriver\n\n[![tests](https://github.com/noaa-ocs-modeling/CoupledModelDriver/workflows/tests/badge.svg)](https://github.com/noaa-ocs-modeling/CoupledModelDriver/actions?query=workflow%3Atests)\n[![codecov](https://codecov.io/gh/noaa-ocs-modeling/coupledmodeldriver/branch/main/graph/badge.svg?token=4DwZePHp18)](https://codecov.io/gh/noaa-ocs-modeling/coupledmodeldriver)\n[![build](https://github.com/noaa-ocs-modeling/CoupledModelDriver/workflows/build/badge.svg)](https://github.com/noaa-ocs-modeling/CoupledModelDriver/actions?query=workflow%3Abuild)\n[![version](https://img.shields.io/pypi/v/CoupledModelDriver)](https://pypi.org/project/CoupledModelDriver)\n[![license](https://img.shields.io/github/license/noaa-ocs-modeling/CoupledModelDriver)](https://creativecommons.org/share-your-work/public-domain/cc0)\n[![style](https://sourceforge.net/p/oitnb/code/ci/default/tree/_doc/_static/oitnb.svg?format=raw)](https://sourceforge.net/p/oitnb/code)\n[![documentation](https://readthedocs.org/projects/coupledmodeldriver/badge/?version=latest)](https://coupledmodeldriver.readthedocs.io/en/latest/?badge=latest)\n\nCoupledModelDriver generates an overlying job submission framework and configuration directories for NEMS-coupled coastal ocean\nmodel ensembles.\n\n```shell\npip install coupledmodeldriver\n```\n\nIt utilizes [NEMSpy](https://nemspy.readthedocs.io) to generate NEMS configuration files, shares common configurations between\nruns, and organizes spinup and mesh partition into separate jobs for dependant submission.\n\nDocumentation can be found at https://coupledmodeldriver.readthedocs.io\n\n## supported models and platforms\n\n- **models**\n    - circulation models\n        - ADCIRC (uses [ADCIRCpy](https://pypi.org/project/adcircpy))\n        - SCHISM (uses [PySCHISM](https://github.com/schism-dev/pyschism))\n    - forcings\n        - ATMESH\n        - WW3DATA\n        - HURDAT best track\n        - OWI\n- **platforms**\n    - local\n    - Slurm\n        - Hera\n        - Stampede2\n        - Orion\n\n## organization / responsibility\n\nCoupledModelDriver is developed for the COASTAL Act project by the [Coastal Marine Modeling Branch (CMMB)](https://coastaloceanmodels.noaa.gov) of the Office of Coast Survey (OCS), a part of the [National Oceanic and Atmospheric Administration (NOAA)](https://www.noaa.gov), an agency of the United States federal government.\n\n- Zachary Burnett (**lead**) - zachary.burnett@noaa.gov\n- William Pringle - wpringle@anl.gov\n- Saeed Moghimi - saeed.moghimi@noaa.gov\n\n## usage example\n\n### 1. generate JSON configuration files\n\n`initialize_adcirc` creates JSON configuration files according to the given parameters. ADCIRC run options that are not exposed\nby this command, such as `runs` or `gwce_solution_scheme`, can be specified by directly modifying the JSON files. The following\ncreates JSON files for coupling `(ATMESH + WW3DATA) -> ADCIRC` over a small Shinnecock Inlet mesh:\n\n```shell\ninitialize_adcirc \\\n    --platform HERA \\\n    --mesh-directory /scratch2/COASTAL/coastal/save/shared/models/meshes/shinnecock/v1.0 \\\n    --output-directory hera_shinnecock_ike_spinup_tidal_atmesh_ww3data \\\n    --modeled-start-time 20080823 \\\n    --modeled-duration 14:06:00:00 \\\n    --modeled-timestep 00:00:02 \\\n    --nems-interval 01:00:00 \\\n    --adcirc-executable /scratch2/COASTAL/coastal/save/shared/repositories/CoastalApp/ALLBIN_INSTALL/NEMS-adcirc-atmesh-ww3data.x \\\n    --adcirc-processors 40\n    --adcprep-executable /scratch2/COASTAL/coastal/save/shared/repositories/CoastalApp/ALLBIN_INSTALL/adcprep \\\n    --modulefile /scratch2/COASTAL/coastal/save/shared/repositories/CoastalApp/modulefiles/envmodules_intel.hera \\\n    --forcings tidal,atmesh,ww3data \\\n    --tidal-source TPXO \\\n    --tidal-path /scratch2/COASTAL/coastal/save/shared/models/forcings/tides/h_tpxo9.v1.nc \\\n    --tidal-spinup-duration 12:06:00:00 \\\n    --atmesh-path /scratch2/COASTAL/coastal/save/shared/models/forcings/shinnecock/ike/wind_atm_fin_ch_time_vec.nc \\\n    --ww3data-path /scratch2/COASTAL/coastal/save/shared/models/forcings/shinnecock/ike/ww3.Constant.20151214_sxy_ike_date.nc\n```\n\nThis will create the directory `hera_shinnecock_ike_spinup_tidal_atmesh_ww3data/` with the following JSON configuration files:\n\n```\n📂 hera_shinnecock_ike_spinup_tidal_atmesh_ww3data/\n┣ 📜 configure_adcirc.json\n┣ 📜 configure_atmesh.json\n┣ 📜 configure_modeldriver.json\n┣ 📜 configure_nems.json\n┣ 📜 configure_slurm.json\n┣ 📜 configure_tidal_forcing.json\n┗ 📜 configure_ww3data.json\n```\n\nThese files contain relevant configuration values for an ADCIRC run. You will likely wish to change these values to alter the\nresulting run, before generating the actual model configuration. For instance, NEMS connections and the run sequence need to be\nmanually specified in `configure_nems.json`.\n\n### 2. generate model configuration files\n\n`generate_adcirc` generates an ADCIRC run configuration (`fort.14`, `fort.15`, etc.) using options read from the JSON\nconfiguration files (generated in the previous step).\n\n```shell\ncd hera_shinnecock_ike_spinup_tidal_atmesh_ww3data\ngenerate_adcirc\n```\n\nThe resulting configuration will look like this:\n\n```\n📂 hera_shinnecock_ike_spinup_tidal_atmesh_ww3data/\n┣ 📜 configure_adcirc.json\n┣ 📜 configure_atmesh.json\n┣ 📜 configure_modeldriver.json\n┣ 📜 configure_nems.json\n┣ 📜 configure_slurm.json\n┣ 📜 configure_tidal_forcing.json\n┣ 📜 configure_ww3data.json\n┣ 📂 spinup/\n┃  ┣ 📜 fort.13\n┃  ┣ 🔗 fort.14 -> ../fort.14\n┃  ┣ 📜 fort.15\n┃  ┣ 📜 nems.configure\n┃  ┣ 📜 model_configure\n┃  ┣ 🔗 atm_namelist.rc -> ./model_configure\n┃  ┣ 📜 config.rc\n┃  ┣ 📜 setup.job\n┃  ┗ 📜 adcirc.job\n┣ 📂 runs/\n┃  ┗ 📂 unperturbed/\n┃    ┣ 📜 fort.13\n┃    ┣ 🔗 fort.14 -> ../../fort.14\n┃    ┣ 📜 fort.15\n┃    ┣ 🔗 fort.67.nc -> ../../spinup/fort.67.nc\n┃    ┣ 🔗 fort.68.nc -> ../../spinup/fort.68.nc\n┃    ┣ 📜 nems.configure\n┃    ┣ 📜 model_configure\n┃    ┣ 🔗 atm_namelist.rc -> ./model_configure\n┃    ┣ 📜 config.rc\n┃    ┣ 📜 setup.job\n┃    ┗ 📜 adcirc.job\n┣ 📜 fort.14\n┣ 📜 cleanup.sh\n┗ 📜 run_hera.sh\n```\n\n### 3. run the model\n\nThe previous step will also have generated a script called `./run_hera.sh`. You can run it to submit the model run to the Slurm\njob queue:\n\n```shell\n./run_hera.sh\n``` \n\nThe queue will have the following jobs added:\n\n```\n   JOBID CPU NODE DEPENDENCY       NODELIST(REA NAME\n20967647 1   1    (null)           (None)       ADCIRC_SETUP_SPINUP\n20967648 40  1    afterok:20967647 (Dependency) ADCIRC_COLDSTART_SPINUP\n20967649 1   1    (null)           (None)       ADCIRC_SETUP_unperturbed\n20967650 42  2    afterok:20967649 (Dependency) ADCIRC_HOTSTART_unperturbed\n```\n\n### 4. track model progress\n\n`check_completion` checks the completion status of a running model directory.\n\n```shell\ncd hera_shinnecock_ike_spinup_tidal_atmesh_ww3data\ncheck_completion\n```\n\n```json\n{\n    "hera_shinnecock_ike_spinup_tidal_atmesh_ww3data": {\n        "spinup": "running - 15%",\n        "runs": "not_started - 0%"\n    }\n}\n```\n\nyou can also pass a specific directory (or several directories):\n\n```shell\ncheck_completion spinup\n```\n\n```json\n{\n    "spinup": "running - 27%"\n}\n```\n\n```shell\ncd run_20211027_florence_besttrack_250msubset_quadrature\ncheck_completion runs/*_13\n```\n\n```json\n{\n    "vortex_4_variable_perturbation_13": "completed - 100.0%",\n    "vortex_4_variable_quadrature_13": "not_started - 0%"\n}\n```\n\nif a run has an error, you can pass `--verbose` to see detailed logs:\n\n```shell\ncheck_completion spinup\n```\n\n```json\n{\n    "spinup": "error - 0%"\n}\n```\n\n```shell\ncheck_completion spinup --verbose\n```\n\n```json\n{\n    "spinup": {\n        "status": "error",\n        "progress": "0%",\n        "error": {\n            "ADCIRC_SETUP_SPINUP.err.log": [\n                "forrtl: severe (24): end-of-file during read, unit -4, file /proc/92195/fd/0\\n",\n                "Image              PC                Routine            Line        Source             \\n",\n                "adcprep            000000000069A72E  Unknown               Unknown  Unknown\\n",\n                "adcprep            00000000006CBAAF  Unknown               Unknown  Unknown\\n",\n                "adcprep            000000000050A5CB  openprepfiles_           6996  prep.F\\n",\n                "adcprep            0000000000507F22  prep13_                   753  prep.F\\n",\n                "adcprep            000000000042E2E9  prepinput_                717  adcprep.F\\n",\n                "adcprep            000000000042BCDB  MAIN__                    239  adcprep.F\\n",\n                "adcprep            000000000040B65E  Unknown               Unknown  Unknown\\n",\n                "libc-2.17.so       00002AAEC02EB555  __libc_start_main     Unknown  Unknown\\n",\n                "adcprep            000000000040B569  Unknown               Unknown  Unknown\\n",\n                "srun: error: h24c51: task 0: Exited with exit code 24\\n",\n                "srun: launch/slurm: _step_signal: Terminating StepId=25366266.1\\n"\n            ]\n        }\n    }\n}\n```\n\n```shell\ncheck_completion runs\n```\n\n```json\n{\n    "spinup": "failed - 0%"\n}\n```\n\n```shell\ncheck_completion runs --verbose\n```\n\n```json\n{\n    "runs": {\n        "status": "failed",\n        "progress": "0%",\n        "failed": {\n            "fort.16": "ADCIRC output file `fort.16` not found"\n        },\n        "error": {\n            "ADCIRC_SETUP_unperturbed.err.log": [\n                "slurmstepd: error: execve(): /scratch2/COASTAL/coastal/save/shared/repositories/CoastalApp/ADCIRC/ALLBIN_INSTALL/adcprep: No such file or directory\\n",\n                "srun: error: h18c49: task 0: Exited with exit code 2\\n",\n                "srun: launch/slurm: _step_signal: Terminating StepId=25366268.0\\n"\n            ]\n        }\n    }\n}\n```\n',
    'author': 'Zach Burnett',
    'author_email': 'zachary.r.burnett@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/noaa-ocs-modeling/CoupledModelDriver.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
