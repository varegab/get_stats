#!/usr/bin/python3

import sys
import argparse
import pendulum
import re



def readlog(args):
    # print(args, from_to_timestamp, end_to_timestamp)
    stats=[]
    if args.from_date is None:
        from_date = "1970-01-01T00:00:00"
    if args.to_date is None:
        to_date = "2070-01-01T00:00:00"
    if args.lazy is False:
        check_date = re.compile("\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}")
        if check_date.match(args.from_date) is not None:
            from_timestamp = pendulum.parse(args.from_date, strict=True).int_timestamp
            from_date = pendulum.parse(args.from_date, strict=True).to_iso8601_string
        else:
            print("Starting date must be in ISO8601 format (YYYY-MM-DDThh:mm:ss)")
            sys.exit()
        if check_date.match(args.to_date) is not None:
            to_timestamp = pendulum.parse(args.to_date, strict=True).int_timestamp
            to_date = pendulum.parse(args.to_date, strict=True).to_iso8601_string
        else:
            print("Ending date must be in ISO8601 format (YYYY-MM-DDThh:mm:ss)")
    else:
        try:
            from_timestamp = pendulum.parse(args.from_date, strict=False).int_timestamp
            from_date = pendulum.parse(args.from_date, strict=False).to_iso8601_string
            to_timestamp = pendulum.parse(args.to_date, strict=False).int_timestamp
            to_date = pendulum.parse(args.to_date, strict=False).to_iso8601_string
        except pendulum.parsing.exceptions.ParserError:
            print("Cannot parse the date, try without the 'lazy' argument")
    if from_timestamp > to_timestamp:
        print("Starting date cannot be later than ending date. Maybe you confused '--from' and '--to'")
    for logfile in args.file:
        with open(logfile.name, 'r') as f:
            for line in f:
                arr = line.split(",")
                timestamp = arr[0]
                if int(timestamp) >= int(from_timestamp) and int(timestamp) <= int(to_timestamp):
                    found={}
                    found["from_date"] = from_date
                    found["to_date"] = to_date
                    found["timestamp"] = timestamp
                    found["http_host"] = arr[1]
                    found["http_method"] = arr[2]
                    found["http_status"] = arr[3]
                    found["duration"] = arr[4]
                    found["body_size"] = arr[5]
                    found["ip_address"] = arr[6]
                    stats.append(found)
    return stats


def create_stat(stats):
    status_2xx = re.compile("2..")
    status_3xx = re.compile("3..")
    status_4xx = re.compile("4..")
    status_5xx = re.compile("5..")
    api_sum_2xx, api_sum_3xx, api_sum_4xx, api_sum_5xx = 0,0,0,0
    tools_sum_2xx, tools_sum_3xx, tools_sum_4xx, tools_sum_5xx = 0,0,0,0
    for item in stats:
        if item["http_host"] == "api":
            if status_2xx.match(item["http_status"]) is not None:
                api_sum_2xx+=1
            elif status_3xx.match(item["http_status"]) is not None:
                api_sum_3xx+=1
            elif status_4xx.match(item["http_status"]) is not None:
                api_sum_4xx+=1
            elif status_5xx.match(item["http_status"]) is not None:
                api_sum_5xx+=1
        elif item["http_host"] == "tools":
            if status_2xx.match(item["http_status"]) is not None:
                tools_sum_2xx+=1
            elif status_3xx.match(item["http_status"]) is not None:
                tools_sum_3xx+=1
            elif status_4xx.match(item["http_status"]) is not None:
                tools_sum_4xx+=1
            elif status_5xx.match(item["http_status"]) is not None:
                tools_sum_5xx+=1
    result={}
    allitem=len(stats)
    def calc_percent(divi, multi):
        percent=0
        try:
            percent = 100/divi*multi
        except ZeroDivisionError:
            return 0
        return round(percent, 2)   
    result["api"] = {}
    result["api"]["2xx"] = calc_percent(allitem, api_sum_2xx)
    result["api"]["3xx"] = calc_percent(allitem, api_sum_3xx)
    result["api"]["4xx"] = calc_percent(allitem, api_sum_4xx)
    result["api"]["5xx"] = calc_percent(allitem, api_sum_5xx)
    result["tools"] = {}
    result["tools"]["2xx"] = calc_percent(allitem, tools_sum_2xx)
    result["tools"]["3xx"] = calc_percent(allitem, tools_sum_3xx)
    result["tools"]["4xx"] = calc_percent(allitem, tools_sum_4xx)
    result["tools"]["5xx"] = calc_percent(allitem, tools_sum_5xx)
    # print(result)
    return result


def get_stat():
    parser = argparse.ArgumentParser(prog="logstat", description="generates statistics out of log files in a given timeframe")
    parser.add_argument("file", type=argparse.FileType('r'), nargs='+', help="file or files contain the logs")
    parser.add_argument("--from", dest="from_date", help="starting date in ISO8601 format (YYYY-MM-DDThh:mm:ss)")
    parser.add_argument("--to", dest="to_date", help="ending date in ISO8601 format (YYYY-MM-DDThh:mm:ss)")
    parser.add_argument("--lazy", "-l", dest="lazy", action="store_true", help="lazy mode - you can input only partial date (for example: '1975-12-25'), or you can change the format (for example: '25-Dec-1975 14:15:16' instead of '1975-12-25T14:15:16'), pendulum is going to try to parse it.")
    args = parser.parse_args()
    stats = readlog(args)
    from_date = stats[0]["from_date"]
    # print(from_date)
    to_date = stats[len(stats)-1]["to_date"]
    # print(to_date)
    result = create_stat(stats)
    # print(result)
    print("""
    Betweeen time {} and {}:
    Response rates for "api":
        {}% of 2xx
        {}% of 3xx
        {}% of 4xx
        {}% of 5xx
    Response rates for "tools":
        {}% of 2xx
        {}% of 3xx
        {}% of 4xx
        {}% of 5xx
    """.format(from_date, to_date, 
    result["api"]["2xx"],result["api"]["3xx"],result["api"]["4xx"],result["api"]["5xx"],
    result["tools"]["2xx"],result["tools"]["3xx"],result["tools"]["4xx"],result["tools"]["5xx"]))


if __name__ == "__main__":
    get_stat()
