import setuptools
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
name="matthew_Coef_MultiClass",
version="0.0.1",
author ="Uri Itai & Natan Katz",
include_package_data=True,
description="Calcalating Matthew Correlation Coefficient for multi class problems",
long_description=long_description,
long_description_content_type='text/markdown',
  packages=["matthew_pack"]
)