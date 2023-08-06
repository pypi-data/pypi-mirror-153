# FruitSpec Cloud Utils
## A shareable library with common code for FruitSpec developers

[![https://github.com/FruitSpec/cloud-utils.git](https://github.com/FruitSpec/cloud-utils.git)](https://github.com/FruitSpec/cloud-utils.git)

fscloudutils is as python package that enables FruitSpec developers to share code between various cloud services, without having to repetativley copy entire blocks of code.


## Features

- **Chatbot** - Both SES client and Slack chatbot instances could be initiated using this module. 
- **Data Validation** - I/O validation.
- **DB client** - Initiate a connection with any RDS, interact with some basic queries.
- **Processors** - Abstract class that define minimum requirements for a cloud service.
- **Utils** - A general module that holds various useful tools, e.g. nmea parser etc.

## Installation

fscloudutils requires [Python>=3.6](https://python.org/) and [pip](https://pip.pypa.io/en/stable/installation/) to run.

``` pip install fscloudutils```

Dependencies included in the package:

```sh
pillow
skimage
requests
boto3
mysql
mysql-connector-python-rf
pandas
```


## License

MIT



