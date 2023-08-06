"""
Copyright 2021 Kelvin Inc.

Licensed under the Kelvin Inc. Developer SDK License Agreement (the "License"); you may not use
this file except in compliance with the License.  You may obtain a copy of the
License at

http://www.kelvininc.com/developer-sdk-license

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OF ANY KIND, either express or implied.  See the License for the
specific language governing permissions and limitations under the License.

"""

from typing import Any

import click


class Dependency:
    name: str
    version: str

    def __init__(self, dependency: str) -> None:
        self.name, self.version = dependency.split(" ")

    @property
    def is_ksos_core_component(self) -> bool:
        return self.name in ["kelvin-sdk"]

    @property
    def pretty_name(self) -> str:
        return f"{self.name}  {self.version}"


def display_ksos_libraries(*args) -> Any:
    try:
        import pkg_resources
        all_dependencies = [Dependency(str(d)) for d in pkg_resources.working_set]
        ksos_version = ""
        kelvin_dists = []
        for dependency in all_dependencies:
            if dependency.is_ksos_core_component:
                kelvin_dists.append(dependency.pretty_name)
            elif dependency.name.startswith("ksos"):
                ksos_version = dependency.version
        kelvin_dists_str = "\n\t\t".join(kelvin_dists)
        click.echo(f"""
            KSOS version: {ksos_version}
            
            Component versions:
    
            \t{kelvin_dists_str}
        
        """)
        return True
    except Exception:
        click.echo("Error retrieving versions.")
    return False


@click.command()
@click.option(
    "--version",
    is_flag=True,
    help="Display the KSOS components versions",
    callback=display_ksos_libraries,
    expose_value=False,
    is_eager=True,
)
def ksos() -> bool:
    """

    KSOS (Kelvin Intelligent Control System)

    """
