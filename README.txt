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



Example run:

./app.py ../sample-logs.* --from '25-Dec-1975 14:15:16' --to 2200 --lazy

    Betweeen time 1975-12-25T14:15:16Z and 2200-01-01T00:00:00Z:
    Response rates for "api":
        25.97% of 2xx
        0.0% of 3xx
        0.0% of 4xx
        0.26% of 5xx
    Response rates for "tools":
        60.26% of 2xx
        8.57% of 3xx
        0.52% of 4xx
        4.42% of 5xx



Build:

This tool is using pendulum (https://pendulum.eustace.io/) to parsing time intervals.

First you need to create a python3 virtual environment into the cloned directory:
  virtualenv -p python3 venv
Then activate it:
  source venv/bin/activate
Then install the required packages:
  pip install -r requirements.txt
