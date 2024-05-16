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
import pprint

from backend.record import SiteRecord, AnalyteSummaryRecord
from backend.transformer import BaseTransformer, SiteTransformer


class WQPSiteTransformer(SiteTransformer):
    def transform(self, record, config):
        # pprint.pprint(record)
        provider = record["ProviderName"]
        rec = {
            "source": f"WQP/{provider}",
            "id": record["MonitoringLocationIdentifier"],
            "name": record["MonitoringLocationName"],
            "latitude": record["LatitudeMeasure"],
            "longitude": record["LongitudeMeasure"],
            "elevation": record["VerticalMeasure/MeasureValue"],
            "elevation_units": record["VerticalMeasure/MeasureUnitCode"],
            "horizontal_datum": record["HorizontalCoordinateReferenceSystemDatumName"],
            "vertical_datum": record["VerticalCoordinateReferenceSystemDatumName"],
            "aquifer": record["AquiferName"],
            "well_depth": record["WellDepthMeasure/MeasureValue"],
            "well_depth_units": record["WellDepthMeasure/MeasureUnitCode"],
        }
        return rec


class WQPAnalyteTransformer(BaseTransformer):
    def _get_record_klass(self, config):
        return AnalyteSummaryRecord

    def transform(self, record, config, parent_record):
        rec = {
            "source": "WQP",
            "id": parent_record.id,
            "location": parent_record.name,
            "usgs_site_id": parent_record.id,
            "latitude": parent_record.latitude,
            "longitude": parent_record.longitude,
            "elevation": parent_record.elevation,
            "elevation_units": parent_record.elevation_units,
            "well_depth": parent_record.well_depth,
            "well_depth_units": parent_record.well_depth_units,
            "parameter": config.analyte,
            # "date": record["datetime"],
            # "value": record["lev_va"],
            # "units": "ft",
            # "qualifiers": record["lev_status_cd"],
        }
        rec.update(record)
        return rec
# ============= EOF =============================================
