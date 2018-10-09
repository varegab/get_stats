usage: app.py [-h] [--from FROM_DATE] [--to TO_DATE] [--lazy] file [file ...]

generates statistics out of log files in a given timeframe

positional arguments:
  file                  file or files contain the logs

optional arguments:
  -h, --help            show this help message and exit
  --from FROM_DATE, -f FROM_DATE
                        starting date in ISO8601 format (YYYY-MM-DDThh:mm:ss)
  --to TO_DATE, -t TO_DATE
                        ending date in ISO8601 format (YYYY-MM-DDThh:mm:ss)
  --lazy, -l            lazy mode - you can input only partial date (for
                        example: '1975-12-25'), or you can change the format
                        (for example: '25-Dec-1975 14:15:16' instead of
                        '1975-12-25T14:15:16'), pendulum is going to try to
                        parse it.
                        

  TODO: timestamp 'reverse' functionality, which converts the timestamps taken from the file(s) into ISO8601 format. 
  TODO: creating stand-alone app from the tool with PyInstaller(?) 


Example run:

./app.py ../sample-logs.txt --from 2018-07-31T00:00:00Z --to 2018-08-02T00:00:00Z

    Betweeen time 2018-07-31T00:00:00+00:00 and 2018-08-02T00:00:00+00:00:
    Response rates for "api":
        9.09% of 2xx
        0.0% of 3xx
        0.0% of 4xx
        0.0% of 5xx
    Response rates for "tools":
        84.85% of 2xx
        3.03% of 3xx
        0.0% of 4xx
        3.03% of 5xx


./app.py ../sample-logs.txt --from 2018-07-31 --to 2018-8-3 --lazy

    Betweeen time 2018-07-31T00:00:00Z and 2018-08-03T00:00:00Z:
    Response rates for "api":
        25.42% of 2xx
        0.0% of 3xx
        0.0% of 4xx
        0.42% of 5xx
    Response rates for "tools":
        62.08% of 2xx
        8.75% of 3xx
        0.42% of 4xx
        2.92% of 5xx


Build:

This tool is using pendulum (https://pendulum.eustace.io/) to parsing time intervals.

First you need to create a python3 virtual environment into the cloned directory:
  virtualenv -p python3 venv
Then activate it:
  source venv/bin/activate
Then install the required packages:
  pip install -r requirements.txt


Assumptions:

-This tool tested with python 3.7.0 under Manjaro linux. 
I do not know howto setup python environment under windows or mac, but I assume that it is possible to create the same environment.
Generally:
-This tool assuming that running environment has python3, pip3, virtualenv installed
-This tool assuming that user can install python3 packages via pip
-I assume as for now that the dict can grow as big as it needs, the python interpreter or the python memory manager take care of it (citation needed)
