# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['fastga',
 'fastga.command',
 'fastga.command.resources',
 'fastga.configurations',
 'fastga.models',
 'fastga.models.aerodynamics',
 'fastga.models.aerodynamics.components',
 'fastga.models.aerodynamics.components.resources',
 'fastga.models.aerodynamics.external',
 'fastga.models.aerodynamics.external.openvsp',
 'fastga.models.aerodynamics.external.openvsp.openvsp3201',
 'fastga.models.aerodynamics.external.openvsp.resources',
 'fastga.models.aerodynamics.external.vlm',
 'fastga.models.aerodynamics.external.xfoil',
 'fastga.models.aerodynamics.external.xfoil.resources',
 'fastga.models.aerodynamics.external.xfoil.xfoil699',
 'fastga.models.aerodynamics.resources',
 'fastga.models.geometry',
 'fastga.models.geometry.geom_components',
 'fastga.models.geometry.geom_components.fuselage',
 'fastga.models.geometry.geom_components.fuselage.components',
 'fastga.models.geometry.geom_components.ht',
 'fastga.models.geometry.geom_components.ht.components',
 'fastga.models.geometry.geom_components.landing_gears',
 'fastga.models.geometry.geom_components.nacelle',
 'fastga.models.geometry.geom_components.propeller',
 'fastga.models.geometry.geom_components.propeller.components',
 'fastga.models.geometry.geom_components.vt',
 'fastga.models.geometry.geom_components.vt.components',
 'fastga.models.geometry.geom_components.wing',
 'fastga.models.geometry.geom_components.wing.components',
 'fastga.models.geometry.geom_components.wing_tank',
 'fastga.models.geometry.profiles',
 'fastga.models.handling_qualities',
 'fastga.models.handling_qualities.tail_sizing',
 'fastga.models.load_analysis',
 'fastga.models.load_analysis.wing',
 'fastga.models.loops',
 'fastga.models.loops.wing_area_component',
 'fastga.models.performances',
 'fastga.models.performances.mission',
 'fastga.models.performances.mission.mission_components',
 'fastga.models.performances.mission.resources',
 'fastga.models.performances.mission_vector',
 'fastga.models.performances.mission_vector.initialization',
 'fastga.models.performances.mission_vector.mission',
 'fastga.models.performances.payload_range',
 'fastga.models.propulsion',
 'fastga.models.propulsion.fuel_propulsion',
 'fastga.models.propulsion.fuel_propulsion.basicIC_engine',
 'fastga.models.propulsion.fuel_propulsion.basicIC_engine.resources',
 'fastga.models.propulsion.fuel_propulsion.basicTurbo_prop',
 'fastga.models.propulsion.fuel_propulsion.basicTurbo_prop.resources',
 'fastga.models.propulsion.fuel_propulsion.basicTurbo_prop_map',
 'fastga.models.weight',
 'fastga.models.weight.cg',
 'fastga.models.weight.cg.cg_components',
 'fastga.models.weight.cg.cg_components.a_airframe',
 'fastga.models.weight.cg.cg_components.b_propulsion',
 'fastga.models.weight.cg.cg_components.c_systems',
 'fastga.models.weight.cg.cg_components.d_furniture',
 'fastga.models.weight.mass_breakdown',
 'fastga.models.weight.mass_breakdown.a_airframe',
 'fastga.models.weight.mass_breakdown.a_airframe.fuselage_components',
 'fastga.models.weight.mass_breakdown.a_airframe.wing_components',
 'fastga.models.weight.mass_breakdown.b_propulsion',
 'fastga.models.weight.mass_breakdown.c_systems',
 'fastga.models.weight.mass_breakdown.d_furniture',
 'fastga.notebooks',
 'fastga.notebooks.pre_processing',
 'fastga.notebooks.pre_processing.data',
 'fastga.notebooks.pre_processing.img',
 'fastga.notebooks.tutorial',
 'fastga.notebooks.tutorial.data',
 'fastga.notebooks.tutorial.img',
 'fastga.utils',
 'fastga.utils.postprocessing',
 'fastga.utils.postprocessing.load_analysis']

package_data = \
{'': ['*']}

install_requires = \
['fast-oad-core>=1.3.3,<1.4.0', 'openmdao<3.18.0', 'stdatm==0.2.0']

entry_points = \
{'fastoad.plugins': ['cs23 = fastga']}

setup_kwargs = {
    'name': 'fast-oad-cs23',
    'version': '1.0.2',
    'description': 'FAST-OAD-CS23 is a framework for performing rapid Overall Aircraft Design for General Aircraft',
    'long_description': "![Tests](https://github.com/supaero-aircraft-design/FAST-GA/workflows/Tests/badge.svg)\n[![Documentation Status](https://readthedocs.org/projects/fast-ga/badge/?version=latest)](https://fast-ga.readthedocs.io/en/latest/?badge=latest)\n\n[![Codacy Badge](https://app.codacy.com/project/badge/Grade/ee153dd5e82d41e7b2f3a964ef5756f5)](https://www.codacy.com/gh/supaero-aircraft-design/FAST-GA/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=supaero-aircraft-design/FAST-GA&amp;utm_campaign=Badge_Grade)\n[![codecov](https://codecov.io/gh/supaero-aircraft-design/FAST-GA/branch/main/graph/badge.svg?token=VZEDUOFE8V)](https://codecov.io/gh/supaero-aircraft-design/FAST-GA)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)\n\n[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/supaero-aircraft-design/FAST-GA/HEAD?urlpath=lab%2Ftree%2Fsrc%2Ffastga%2Fnotebooks)\n\nFAST-(OAD)-GA: Future Aircraft Sizing Tool - Overall Aircraft Design (General Aviation extension)\n===============================================================================================\n\nFAST-(OAD)-GA is derived from FAST-OAD framework performing rapid Overall Aircraft Design.\n\nIt proposes multi-disciplinary analysis and optimisation by relying on\nthe [OpenMDAO framework](https://openmdao.org/).\n\nFAST-(OAD)-GA allows easy switching between models for a same discipline, and\nalso adding/removing disciplines to match the need of your study.\n\nCurrently, FAST-(OAD)-GA is bundled with models for general aviation and conventional\npropulsion (ICE propeller based). Other models will come soon, and you may create\nyour own models and use them instead of bundled ones.\n\nMore details can be found in the [official\ndocumentation](https://fast-ga.readthedocs.io/).\n\nWant to try quickly ?\n-------\n\nYou can run FAST-OAD-GA notebooks number 1, 2 and 3 using our [Binder-hosted Jupyter notebooks](https://mybinder.org/v2/gh/supaero-aircraft-design/FAST-GA/HEAD). Just go to src/fastga/notebooks/tutorial after you click the link.\n\nAs these Binder-hosted notebooks are not setup to work in a Windows environment, external applications such as OpenVSP and Xfoil can't be run. Therefore, notebook number 4 will not fully work.\n\nInstall\n-------\n\n**Prerequisite**:FAST-(OAD)-GA needs at least **Python 3.7.0**.\n\nIt is recommended (but not required) to install FAST-(OAD)-GA in a virtual\nenvironment ([conda](https://docs.conda.io/en/latest/),\n[venv](https://docs.python.org/3.7/library/venv.html), ...).\n\nThe FAST-(OAD)-GA is not registered for a direct pip install.\nYet an installation using pip command is possible. To do so, use command:\n**pip install fast-oad-cs23==xxx**, where xxx is the version number (ex: 1.0.0).\n",
    'author': 'Florent LUTZ',
    'author_email': 'Florent.LUTZ2@isae-supaero.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/supaero-aircraft-design/FAST-GA',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
