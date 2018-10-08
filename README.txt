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


Assumptions: (version 1)

-This tool tested with python 3.7.0 under Manjaro linux. 
I do not know howto setup python environment under windows or mac, but I assume that it is possible to create the same environment.
Generally:
-This tool assuming that running environment has python3, pip3, virtualenv installed
-This tool assuming that user can install python3 packages via pip
-This tool assuming that the computer has at least few GB of free memory, because it is possible
to feed multiple log files into the app, and each file can hold several GB of content. (Especially if the user omits the '--from' and '--to' arguments, because 
the entire content of the files will be read into the 'stat' dictionary by line after line.
TODO: measure the size of the 'stat' with a few million entries...? (The problem is with
sys.getsizeof(object[, default]) is: "only the memory consumption directly attributed to the object is accounted for, not the memory consumption of objects it refers to")

I assume as for now that the dict can grow as big as it needs, the python interpreter or the python memory manager take care of it (citation needs)


