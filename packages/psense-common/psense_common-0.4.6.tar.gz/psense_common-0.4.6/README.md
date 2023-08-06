# PSENSE-COMMON
* Author brad.liang@percusense.com

[![PyPI](https://img.shields.io/pypi/v/psense-common.svg)](https://pypi.org/project/psense-common/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/psense-common.svg)
[![PyPI - License](https://img.shields.io/pypi/l/psense-common.svg)](./LICENSE)


Common Modules used by internal PercuSense python applications. This project follows semantic versioning (breaking.major.minor release).

## Getting Started

### General Instructions

Steps to try this out yourself:

1. Install the `psense-common` library:

#### From PyPi

```bash
$ pip install psense-common
```

#### Local Installation

```bash
$ git clone git@bitbucket.org:psense/psense-common.git
$ python setup.py install
```

2. Import the modules you need in your script.

```python
from psense_common import PSenseParser)
```

3. Access module methods directly.

```python
from psense_common import PSenseParser

filename = '/path/to/data/file'
parser = PSenseParser()
parser.identify_file_source(filename)

if parser.source:
    parser.load_rawfile(filename)
    print(parser.data) # this is of type pandas.DataFrame
```

### AWS

`psense_common/psense_aws_itfc.py` introduces the class `PSenseAWSInterface`, which provides an interface to the Amazon DynamoDB datastore. Currently, data is stored on a per-record basis (NoSQL) for Experiment, Sensor, and Event data ("Experiments", "SensorData", and "Calibration" -- not fully supported, will be changed to "EventData" in migration from 0.x.x to 1.x.x).

The class contains query and put operations but does not provide provisions for deleting items from the datastore.

#### Credentials

At initialization, the class will create an AWS session that is persisted. The session object allows the user to authenticate just a single time (rather than for every communication).

In generating the session, bot3 will attempt to load a profile (if not provided, will try "PShield") that contains the necessary credentials for authentication/authorization to our dynamodb instances. If the profile doesn't exist or cannot be loaded, the class reverts to the environment default AWS credentials in the 'us-east-1' region.

`config` and `credential` files for aws are stored in the user's home directory: `~/.aws/`.  In Windows, the comparable location is `C:\Users\[username]\.aws\`

#### Usage

**Get Sensor Data**

```python
from psense_common import PSenseAWSInterface
import pytz

aws = PSenseAWSInterface(debugmode=True)
aws.set_query_config(req_size=7200, query_count=2)

experiments = ['[my experiment id 1]',
               '[my experiment id 2]']

for expid in experiments:
    if not aws.verif_experiment(expid):
        print('invalid experiment id skipping {}'.format(expid))
        pass

    count, data = aws.get_sensor_data()
    data.index = data.index.tz_localize(pytz.utc).tz_convert(localtz)

    print(data)
```

**Add Experiment and real-time Sensor data**

```python
from psense_common import (PSenseAWSInterface, PSenseParser)

# user variables
filename = '[vfp600 gamry file].txt'
expid = 'experimentid'

# initialize classes + helper func
parser = PSenseParser(debugmode=True)
aws = PSenseAWSInterface(debugmode=True)
aws.set_query_config(req_size=7200, query_count=2)

def tail(fin):
    "Listen for new lines added to file."
    while True:
        where = fin.tell()            
        line = fin.readline()
        if not line:
            time.sleep(SLEEP_INTERVAL)
            fin.seek(where)
        else:
            yield line

# identify the type of file we are parsing
if not parser.identify_file_source(filename):
    print('unknown file type. exiting')
    assert False


# confirm that the experiment id is valid
if not aws.verif_experiment(expid):
    print('invalid experiment id skipping {}'.format(expid))
    assert False


# add experiment to database
add_experiment_success, if_fail_reason = aws.add_experiment()
if if_fail_reason == 'error':
    print('Aborted. Error occurred in communication with AWS.')
    assert False
elif if_fail_reason == 'exists':
    print('Experiment already exists in database. Must delete existing experiment sensor data before uploading new values.')


# "tail" the file and send each record to ddb
with open(filename, 'r') as fin:
    # skip to the end of the file before beginning tail
    fin.seek(0, os.SEEK_END)

    for line in tail(fin):
        row = parser.parse_record(line.strip())
        aws.add_sensordata(*row)
```

*Future notes: Sensor and Event data should remain as a blob-store -- we expect schema to change depending on the type of sensor (or event). For example, sensors with 3 working electrodes should contain more properties than sensors with a single signal.*

### Experiment ID Formatting

All sensor data is associated with a particular experiment ID. Experiment IDs should be unique and follow the PercuSense naming scheme.

#### Usage

Decoding an experiment:

```python
from psense_common import (psense_format)

experiment = '[my experiment id]'
validate_name = psense_format.psense_exp_title()
validate_name.decode(experiment)
```

Generating an experiment id through console IO (must provide 3-digit device id):

```python
from psense_common import (psense_format)

device_id = 'P01'
experiment = psense_format.setup_new_experiment(device_id)
```

### Data Parsing

The PSenseParser class will parse data from flat-file into Pandas DataFrame. Output object will contain columns appropriate for PercuSense analysis scripts (and PercuSense Data Viewer web application). The parser works on individual records (live streaming) as well as full files (retrospective analysis).

Supported formats:

```bash
BWII 2-channel
BWII 3-Channel ("BWII-MINI")
PSHIELD
GAMRY VFP600
GAMRY EXPLAIN
DATA VIEWER single-channel
DATA VIEWER 2-channel
DATA VIEWER 3-channel
CH Instruments (txt)
```

TODO: documentation pending

Check `demo/parser.py` for some example usage.

See above sections (General Instructions, AWS) for basic usage.

### PercuSense Data Filter

TODO: documentation pending

## Development

### Tests

```bash
$ python setup.py test
```

.. or with code coverage (`pip install --upgrade coverage`):
```bash
$ coverage run --source=psense_common/ setup.py test
$ coverage report -m
```

### Publishing

Bitbucket has been configured to run tests and publish directly to pypi after code is merged to master. See `bitbucket-pipelines.yml` for configuration details.

Manual publishing (not recommended):
```
$ rm -rf dist
$ python setup.py sdist
$ twine upload dist/*
```
