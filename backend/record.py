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


class BaseRecord:
    def to_csv(self):
        raise NotImplementedError

    def __init__(self, payload):
        self._payload = payload

    def to_row(self):

        def get(attr):
            v = self._payload.get(attr)
            if attr == "elevation" and v is not None:
                v = round(v, 2)

            if v is None:
                v = self.defaults.get(attr)
            return v

        return [get(k) for k in self.keys]

    def update(self, **kw):
        self._payload.update(kw)

    def __getattr__(self, k):
        return self._payload.get(k)


class WaterLevelRecord(BaseRecord):
    keys = (
        "source",
        "id",
        "surface_elevation_ft",
        "well_depth_ft_below_ground_surface",
        "depth_to_water_ft_below_ground_surface",
        "date_measured",
        "time_measured",
    )
    defaults = {}


class AnalyteRecord(BaseRecord):
    keys = (
        "source",
        "id",
        "date_measured",
        "time_measured",
        "analyte",
        "result",
        "units",
    )


class SiteRecord(BaseRecord):
    keys = (
        "source",
        "id",
        "name",
        "latitude",
        "longitude",
        "elevation",
        "elevation_units",
        "horizontal_datum",
        "vertical_datum",
        "usgs_site_id",
        "alternate_site_id",
        "formation",
        "aquifer",
        "well_depth",
    )

    defaults = {
        "source": None,
        "id": None,
        "name": "",
        "latitude": None,
        "longitude": None,
        "elevation": None,
        "elevation_units": "feet",
        "horizontal_datum": "",
        "vertical_datum": "",
        "usgs_site_id": "",
        "alternate_site_id": "",
        "formation": "",
        "aquifer": "",
        "well_depth": None,
    }


# ============= EOF =============================================
