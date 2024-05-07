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
import frost_sta_client as fsc

from backend.connectors.st2.transformer import (
    PVACDSiteTransformer,
    EBIDSiteTransformer,
    PVACDWaterLevelTransformer,
    EBIDWaterLevelTransformer,
)
from backend.source import BaseSiteSource, BaseWaterLevelsSource

URL = "https://st2.newmexicowaterdata.org/FROST-Server/v1.0"


class ST2Mixin:
    def get_service(self):
        return fsc.SensorThingsService(URL)


class ST2SiteSource(BaseSiteSource, ST2Mixin):
    agency = "ST2"

    def get_records(self, config, *args, **kw):
        service = self.get_service()

        f = f"properties/agency eq '{self.agency}'"
        if config.has_bounds():
            f = f"{f} and st_within(Location/location, geography'{config.bounding_wkt()}')"

        q = service.locations().query().filter(f)
        for location in q.list():
            yield location


class PVACDSiteSource(ST2SiteSource):
    transformer_klass = PVACDSiteTransformer
    agency = "PVACD"


class EBIDSiteSource(ST2SiteSource):
    transformer_klass = EBIDSiteTransformer
    agency = "EBID"


class ST2WaterLevelSource(BaseWaterLevelsSource, ST2Mixin):
    def _extract_most_recent(self, records):
        return records[0]["observation"].phenomenon_time

    def _extract_waterlevels(self, records):
        return [r["observation"].result for r in records]

    def get_records(self, parent_record, config, *args, **kw):
        service = self.get_service()

        things = (
            service.things()
            .query()
            .expand("Locations,Datastreams")
            .filter(f"Locations/id eq {parent_record.id}")
        )
        for t in things.list():
            if t.name == "Water Well":
                for di in t.datastreams:
                    q = di.get_observations().query()
                    if config.latest_water_level_only and not config.output_summary_waterlevel_stats:
                        q = q.orderby("phenomenonTime", "desc").top(1)

                    for obs in q.list():
                        yield {
                            "thing": t,
                            "location": parent_record,
                            "datastream": di,
                            "observation": obs,
                        }
                        if config.latest_water_level_only and not config.output_summary_waterlevel_stats:
                            break


class PVACDWaterLevelSource(ST2WaterLevelSource):
    transformer_klass = PVACDWaterLevelTransformer
    agency = "PVACD"


class EBIDWaterLevelSource(ST2WaterLevelSource):
    transformer_klass = EBIDWaterLevelTransformer
    agency = "EBID"


# ============= EOF =============================================
