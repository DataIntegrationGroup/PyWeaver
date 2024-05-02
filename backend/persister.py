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
import csv
import os

import pandas as pd
import geopandas as gpd
from frost_sta_client import AuthHandler

from backend.record import SiteRecord


class BasePersister:
    extension = None

    def __init__(self):
        self.records = []

    def load(self, records):
        self.records.extend(records)

    def save(self, path):
        raise NotImplementedError

    def add_extension(self, path):
        if not self.extension:
            raise NotImplementedError

        if not path.endswith(self.extension):
            path = f'{path}.{self.extension}'
        return path


class CSVPersister(BasePersister):
    extension = 'csv'

    def save(self, path):
        with open(path, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(SiteRecord.keys)
            for record in self.records:
                writer.writerow(record.to_row())


class GeoJSONPersister(BasePersister):
    extension = 'geojson'

    def save(self, path):
        path = self.add_extension(path)
        df = pd.DataFrame([r.to_row() for r in self.records],
                          columns=SiteRecord.keys)

        gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude),
                               crs='EPSG:4326')
        gdf.to_file(path, driver="GeoJSON")


class ST2Persister(BasePersister):
    extension = 'st2'

    def save(self, path):
        import frost_sta_client as fsc
        service = fsc.SensorThingsService('https://st.newmexicowaterdata.org/FROST-Server/v1.0',
                                          auth_handler=AuthHandler(os.getenv('ST2_USER'),
                                                                   os.getenv('ST2_PASSWORD')))
        for record in self.records:
            for t in service.things().query().filter(name=record['id']).list():
                print(t)

# ============= EOF =============================================
