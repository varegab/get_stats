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
                        

  TODO: testing, testing, and testing to eliminate remining BUGS !!!
  TODO: timestamp 'reverse' functionality, which converts the timestamps taken from the file(s) into ISO8601 format. 
  TODO: creating stand-alone app from the tool with PyInstaller(?) 


Example runs:

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


./app.py ../sample-logs.txt

    Betweeen time 1970-01-01T00:00:00Z and 2070-01-01T00:00:00Z:
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


Assumptions:

-This tool tested with python 3.7.0 under Manjaro linux. 
I do not know howto setup python environment under windows or mac, but I assume that it is possible to create the same environment.
Generally:
-This tool assuming that running environment has python3, pip3, virtualenv installed
-This tool assuming that user can install python3 packages via pip


========================================================
TESTING PERFORMANCE CASE 2:
(Refactored the code to not using dictionary, just incerasing counters while iterating through the file.)
configuration: intel i7 with 16G ram

18M file with 385000 lines:
-------------
time ./app.py ../test-log2.txt

    Betweeen time 1970-01-01T00:00:00Z and 2070-01-01T00:00:00Z:
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
    

real	0m0,527s
user	0m0,517s
sys	0m0,010s


179M file with 3850000 lines:
--------------
time ./app.py ../test-log3.txt
real	0m4,701s


1.8G file with 38500000 lines:
--------------
time ./app.py ../test-log4.txt
real	0m55,240s



TESTING PERFORMANCE CASE 1:
configuration: intel i7 with 16G ram

created a 18M log with 385000 lines from the sample:
-------------
for i in {1..1000}; do cat sample-logs.txt >> test-log2.txt; done
ls -lh test-log2.txt 
-rw-r--r-- 1 roka roka 18M okt    9 14.44 test-log2.txt <-- 18MB

wc -l test-log2.txt 
385000 test-log2.txt <-- 385000 lines

measuring the execution time:
time ./app.py ../test-log2.txt <-- feed all 385000 lines into the app

    Betweeen time 1970-01-01T00:00:00Z and 2070-01-01T00:00:00Z:
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
    

real	0m0,826s <-- approximately 1 second
user	0m0,756s
sys	0m0,070s


179M file with 3850000 lines:
--------------
ls -lh test-log3.txt 
-rw-r--r-- 1 roka roka 179M okt    9 14.50 test-log3.txt
wc -l test-log3.txt 
3850000 test-log3.txt
time ./app.py ../test-log3.txt 
real	0m7,663s


1.8G file with 38500000 lines:
I had to interrupt it, it kept running even after 78 minutes, and it rendererd my computer unusable
Read 1.8G into a dict is not a good approach by any means.
TODO: Refactor the code to incerase performance.
-------------
ls -lh test-log4.txt 
-rw-r--r-- 1 roka roka 1,8G okt    9 15.00 test-log4.txt
wc -l test-log4.txt 
38500000 test-log4.txt
time ./app.py ../test-log4.txt
^C^C^C^C^C^C^C^C^C^C^C^C^C

^C^C^C^C^C^C^C^C^C^C^CTraceback (most recent call last):
  File "./app.py", line 143, in <module>
    get_stat()
  File "./app.py", line 123, in get_stat
    result = create_stat(alldata["stats"])
  File "./app.py", line 72, in create_stat
    if item["http_host"] == "api":
KeyboardInterrupt

^C

real	78m34,679s
user	2m42,194s
sys	3m7,862s






