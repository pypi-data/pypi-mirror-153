fml40 python reference implementation
==============================

Reference implementation for building a Digital Twin based on the Forest Modeling Language 4.0 (fml40), as specified in [this white paper](https://www.kwh40.de/wp-content/uploads/2020/03/KWH40-Standpunkt-fml40-Version-1.0.pdf) (in German). 

# Installation
To use the fml40 reference implementation package in your own project, install it from Pypi

```
python -m pip install fml40-reference-implementation
```

or from our self hosted [wheel](https://git.rwth-aachen.de/kwh40/fml40-reference-implementation/-/jobs/artifacts/master/raw/public/fml40_reference_implementation-0.2.4.4-py3-none-any.whl?job=wheel)

``` 
pip install https://git.rwth-aachen.de/kwh40/fml40-reference-implementation/-/jobs/artifacts/master/raw/public/fml40_reference_implementation-0.2.4.4-py3-none-any.whl?job=wheel
``` 

Documentation
--------
We provide a documentation to get start with the fml40 python reference implementation package. It can be found [here](https://git.rwth-aachen.de/kwh40/fml40-reference-implementation/-/jobs/artifacts/master/file/public/html/index.html?job=pages).

Features
--------
This package provides two different modes to launch your Digital Twins: 

-   Launching Digital Twin quickly in persistent mode via `fml40s.py`. You need to register a thing identity for your Digital Twin via [S³I Config REST API](https://config.s3i.vswf.dev/apidoc) and prepare a respective config file that describes a fml40-compliant DT in JSON. For more details, refer to the example `MyDigitalTwin.json` in the section `Config files`. 
-   Extending the capabilities with user defined Digital Twins, which means you can additionally define and insert a function according to ForestML 4.0 into the Digital Twin. We provide an exemplary Digital Twin built in [Jupyter Notebook](https://mybinder.org/v2/gh/kwh40/notebooks/master), refer to notebooks `08a`, `08b`, `08d` and `08e`. 

Usage
-----
### Using fml40s.py

A Digital Twin can be launched in persistent mode by executing

``` 
python fml40s.py launch <CONFIG_FILE>
```
Config files for Digital Twin must be located in the folder `configs`. 
For more options call just run 

```
python fml40s.py -h
```

### Develop your Digital Twin using this package
Here, we introduce briefly how to develop a user-specified Digital Twin. For more details, refer to the cloud/edge Digital Twin built in [Jupyter Notebook](https://mybinder.org/v2/gh/kwh40/notebooks/master). 
The following steps can only be carried out after you have created the thing identity of your Digital Twin via S³I Config REST API and made a respective config file. Here, we use the config file `MyDigitalTwin.json` from section `Config files`. Now we continue the following steps:

- Optionally, set a logger using the function `setup_logger`. The generated log file will then be located in the folder `logs`.
```
ml.setup_logger("MyDigitalTwin")
```
- Set the path of the config file and import it in JSON format. 
```
config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "configs"))

dt_model = ml.load_config(config_filepath=os.path.join(config_path, "MyDigitalTwin.json"))

```
- Create the thing instance. 
```
client_secret = "" #To be filled
thing = ml.create_thing(
    model=dt_model, grant_type="client_credentials", secret=client_secret,
    is_broker_rest=False, is_broker=True, is_repo=True
)
```
- As specified in the config file, the Digital Twin has a feature named fml40::ProvidesProductionData. In the next step, we extend/implement this class with our own logic. 
```
class ProvidesProductionDataImpl(ProvidesProductionData):
    def __init__(self, name="", identifier=""):
        super(ProvidesProductionData, self).__init__(
            name=name,
            identifier=identifier)
        self.production_data_list = thing.features["ml40::ProductionData"].subFeatures["ml40::Composite"].targets

    def getProductionData(self, name):
        for key in self.production_data_list.keys():
            if key == name:
                return self.production_data_list[key].to_subthing_json()
        return {"error": "NOT FOUND"}

```
- Insert the class into the respective feature of your Digital Twin
```
ml.add_function_impl_obj(thing, ProvidesProductionDataImpl, "fml40::ProvidesProductionData")
```
- Launch your Digital Twin
```
thing.run_forever()
```
So far, your Digital Twin has been created. In the meantime, you can establish a connection with it using S³I-B messages. 

Config files
------------

A valid configuration consists of exactly one JSON object. Mandatory fields of the JSON object are

-   thingId
-   policyId and
-   attributes 

The configuration file must be created in accordance with ForestML 4.0, refer to Cap. 7.1 of the [KWH4.0 ForestML 4.0 white paper](https://www.kwh40.de/wp-content/uploads/2020/03/KWH40-Standpunkt-fml40-Version-1.0.pdf). Additionally, we provide an exemplary JSON config file, see below.

MyDigitalTwin.json:
``` 
{
  "thingId": "s3i:id",
  "policyId": "s3i:id",
  "attributes": {
        "class": "ml40::Thing",
        "name": "my digital twin",
        "roles": [
                {
                    "class": "fml40::Harvester"
                }
            ],
        "features": [
                {
                    "class": "fml40::ProvidesProductionData"
                },
                {
                    "class": "ml40::ProductionData",
                    "subFeatures": [
                        {
                            "class": "ml40::Composite",
                            "targets": [
                                {
                                    "class": "ml40::Thing",
                                    "name": "Stammsegment 4711",
                                    "roles": [
                                        {
                                            "class": "fml40::StemSegment",
                                        }
                                    ],
                                    "features": [
                                        {
                                            "class": "ml40::Location",
                                            "latitude": 50.1231,
                                            "longitude": 6.1231
                                        },
                                        {
                                            "class": "fml40::StemSegmentProperties",
                                            "diameter": 0.4,
                                            "length": 2,
                                            "woodType": "Spruce"
                                        }
                                    ]
                                },
                                {
                                    "class": "ml40::Thing",
                                    "name": "Stammsegment 4712",
                                    "roles": [
                                        {
                                            "class": "fml40::StemSegment",
                                        }
                                    ],
                                    "features": [
                                        {
                                            "class": "ml40::Location",
                                            "latitude": 50.1231,
                                            "longitude": 6.1231
                                        },
                                        {
                                            "class": "fml40::StemSegmentProperties",
                                            "diameter": 0.6,
                                            "length": 3,
                                            "woodType": "Spruce"
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    "class": "ml40::Location",
                    "longitude": 5.03424,
                    "latitude": 52.52345
                }
            ]

    }
}
```


Structure
---------

### Configs

This folder contains configuration files in JSON format for Digital Twins.

### ml

This directory includes the implementations of the fml40 python reference implementation as described in the KWH ForestML 4.0 white paper.


### demo

Example for creating and launching an HMI, which is used to communicate with the permanent Digital Twin using S³I-B protocol.

### logs

This folder contains the log files of the created and launched Digital Twins.

### tests

This folder contains all test scripts (currently in development).
