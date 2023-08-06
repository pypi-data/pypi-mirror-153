# Change log for Bamboo API Client
All notable changes to this project will be documented in this file.

## 1.13.1 - 2022-06-03
- Add method `get_energy_market`
- Add `portfolios_api`

## 1.13.0 - 2022-05-25
- Update to bamboo backend v1.13.0

## 1.12.1 - 2022-05-24
- Add support to python 3.8 and higher.

## 1.12.0 - 2022-05-19
- Update to bamboo backend v1.12.0
- Create `ContractsApi` and remove `TariffsApi`
- Make `insert_device_measurements` of `SitesApi` return `None`
- Add fields `frequency` and `interpolation_threshold` to `BaselineModel`
- Add device type `CurtailableLoad`
- Add field `type` to `ShiftableLoad`
- Add fields `virtual_device` and `associated_meter` to `ThermalLoad`
- Update types of multiple device fields (`max_power`, `min_power`, `charge_max_power` and `discharge_max_power` become floats; `min_soc` and `max_soc` become ints)

## 1.10.0 - 2022-04-25
- Update to bamboo backend 1.10.0
- Unify arguments `start_date`, `start`, `period_start`, etc. to `start_time`.
- Unify arguments `end_date`, `stop`, `period_end`, etc. to `end_time`.

## 1.9.1 - 2022-04-08
- Add tox and poetry.
- Update to bamboo backend v1.9.1
- The type of arguments `start_date` and `end_date` is now `datetime`.
- Removed PeriodRange optional parameters. `start_date` and `end_date` are
no longer optional parameters.
- Update method names to match with bamboo backend names.

## 1.8.3 - 2022-03-09
- Update to bamboo backend v1.8.3

## 1.8.1 - 2022-03-03
- Add bambooapi_client.markets_api. GET/PUT market prices endpoints. 

## 1.7.2 - 2022-02-04
- Update microgrid devices models accordingly to Bamboo Backend v1.7.2. 
- Update `controllable` type to `str`in MeterFactory, LoadFactory, 
ShiftableLoadFactory, PVSystemFactory, EVCHargerFactory, BatteryFactory,
ThermalLoadFactory, ThermalComfortDeviceFactory, ThermalZoneFactory and 
ThermalZoneFactory.

## 1.7.1 - 2022-01-27
- Rename `temperature` to `temp`.

## 1.7.0 - 2022-01-25
- Add `frequency` argument (optional) to methods that return time series data.

## 1.6.4 -  2021-12-23
- Fix endpoints return `datetime` objects and `Enum`s instead of `str` instances.

## 1.6.3 -  2021-12-21
- Fix endpoints return DataFrames with DateTimeIndex

## 1.6.2 - 2021-12-20
- Make SOCs a float between 0 and 100
- Add `loads` as a new type of device

## 1.6.0 - 2021-10-11
- Added `KernelBaselineModelFactory`, `KNNBaselineModelFactory`, `BaselineModelFactory`
- Drop int support in `BaselineModel.training_set`

## 1.5.2 - 2021-09-27
- Refactored `bambooapi_client.testing.factory.sites_api.forecast_factory_from_datapoints` to `bambooapi_client.testing.factory.timeseries.timeseries_factory_from_datapoints`
- Refactored `bambooapi_client.testing.factory.sites_api.forecast_factory_from_dataframe` to `bambooapi_client.testing.factory.timeseries.timeseries_factory_from_dataframe`

## 1.5.1 - 2021-09-17
- Added `ThermalZoneSetpointsFactory`.
- Added read&update thermal zone setpoints endpoints in `SitesApi`.

## 1.5.0 - 2021-09-17
- Renamed `SitesApi.list_zones` to `SitesApi.list_thermal_zones`
- Renamed `SitesApi.get_zone` to `SitesApi.get_thermal_zone`
- Renamed `SitesApi.read_measurements` to `SitesApi.read_device_measurements`
- Renamed `SitesApi.update_measurements` to `SitesApi.update_device_measurements`
- Renamed `SitesApi.read_forecasts` to `SitesApi.read_device_baseline_forecasts`
- Renamed `SitesApi.update_forecasts` to `SitesApi.update_device_baseline_forecasts`
- Renamed `SitesApi.read_activations` to `SitesApi.read_device_activations`
- Renamed `SitesApi.read_baseline_model` to `SitesApi.read_device_baseline_model`
- Renamed `SitesApi.update_baseline_model` to `SitesApi.update_device_baseline_model`
- Renamed `SitesApi.read_flexibility_model` to `SitesApi.read_thermal_flexibility_model`
- Renamed `SitesApi.update_flexibility_model` to `SitesApi.update_thermal_flexibility_model`
- Updated `SitesApi.update_device_flexibility_forecast` to accept a DataFrame
- Added read&update flexibility forecast endpoints in `SitesApi` for devices and thermal zones

## 1.4.1 - 2021-09-08
- Added `Tariffs` CRUD endpoints
- Added endpoints to store & retrieve flexibility model parameters
- Split `DataPoint` model into `SitesDataPoint` and `WeatherDataPoint` models
- Added missing fields to `WeatherDataPoint` schema: `dewpoint`, `humidity`, `pressure` and `wind_speed`

## 1.3.0 - 2021-08-11
- Added `elevation` to Site & Weather Station schemas
- Added type hinting to all public methods

## 1.2.1 - 2021-08-05
- Added Mock API client for testing with factories

## 1.2.0 - 2021-07-27
- News fields in Sites schema: `country_code`, `timezone`, `latitude` & `longitude`
- Modified `list_sites` to return a simpler schema
- Renamed all `asset_name` arguments to `device_name`
- Added input data validation rules for all data models
- Added all variables in [mapping format](https://bambooenergy.atlassian.net/wiki/spaces/BMD/pages/175472655/Mapping+Format) to DataPoint schema
- Updated battery schema, removing the redundant `max_power` and `min_power` variables
- **BUGFIX**: Decreased min length for device names to 2 characters

## 1.1.5 - 2021-06-22
- Modify setup and requirements to make package compatible with Python 3.5 and up
- Update requirements in README and add dynamic version badges

## 1.1.3 - 2021-06-11
- Restrict exception catching to "NotFoundException" (HTTP 404) in get methods

## 1.1.2 - 2021-06-11
- Updated client based con v1.1.2 of openapi definition for Bamboo API

## 1.1.1 - 2021-06-04
- Updated README with usage instructions

## 1.1.0 - 2021-06-03
- Updated client based con latest openapi definition for Bamboo API
- Renamed `find` method to `get`: `find_site` becomes `get_site`, etc...
- In GET methods, catch `NotFound` API errors (HTTP 404) and return None instead of raising an error
- Added `get_site_id_by_name` method to obtain site ID given a site name
- Added `get_station_id_by_name` method to obtain weather station ID given a station name
- Renamed `read_load_model` to `read_baseline_model` and `update_load_model` to `update_baseline_model`
- Added missing `horizon` parameter in `update_forecasts` method

## 1.0.0 - 2021-05-27
- Initial release
