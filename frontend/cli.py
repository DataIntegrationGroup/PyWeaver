# ===============================================================================
# Copyright 2024 Jake Ross
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============================================================================
import click

from backend.config import Config
from frontend.unifier import unify


@click.group()
def cli():
    pass

@cli.command()
@click.option(
    "--bbox",
    default="",
    help="Bounding box in the form 'minx,miny,maxx,maxy'",
)
def get_locations(bbox):
    """
    Get locations
    """
    click.echo(f"Getting locations for bounding box {bbox}")

    config = Config()
    config.bbox = bbox

    unify(config)


# ============= EOF =============================================