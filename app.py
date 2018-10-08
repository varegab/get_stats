#!/usr/bin/python3

import sys
import argparse
import pendulum
import re



def readlog(args, timestamp_from, timestamp_to):
    # print(args, from_to_timestamp, end_to_timestamp)
    stat=[]
    for logfile in args.file:
        with open(logfile.name, 'r') as f:
            for line in f:
                arr = line.split(",")
                timestamp = arr[0]
                if int(timestamp) >= timestamp_from and int(timestamp) <= timestamp_to:
                    found={}
                    found["timestamp"] = timestamp
                    found["http_host"] = arr[1]
                    found["http_method"] = arr[2]
                    found["http_status"] = arr[3]
                    found["duration"] = arr[4]
                    found["body_size"] = arr[5]
                    found["ip_address"] = arr[6]
                    stat.append(found)
    return stat


def create_stat(stat):
    status_2xx = re.compile("2..")
    status_3xx = re.compile("3..")
    status_4xx = re.compile("4..")
    status_5xx = re.compile("5..")
    api_sum_2xx, api_sum_3xx, api_sum_4xx, api_sum_5xx = 0,0,0,0
    tools_sum_2xx, tools_sum_3xx, tools_sum_4xx, tools_sum_5xx = 0,0,0,0
    for item in stat:
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
    allitem=len(stat)
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
    parser.add_argument("--lazy", "-l", dest="lazy", action="store_true", help="lazy mode - you can omit everything except year")
    args = parser.parse_args()
    if args.from_date is None:
        args.from_date = "1970-01-01T00:00:00" # If we just want to test without giving from-to
    if args.to_date is None:
        args.to_date = "2070-01-01T00:00:00" # If we just want to test without giving from-to
    if args.lazy is False:
        check_date = re.compile("\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}")
        if check_date.match(args.from_date) is not None:
            from_to_timestamp = pendulum.parse(args.from_date, strict=True).int_timestamp
        else:
            print("Starting date must be in ISO8601 format (YYYY-MM-DDThh:mm:ss)")
            sys.exit()
        if check_date.match(args.to_date) is not None:
            end_to_timestamp = pendulum.parse(args.to_date, strict=True).int_timestamp
        else:
            print("Ending date must be in ISO8601 format (YYYY-MM-DDThh:mm:ss)")
    else:
        try:
            from_to_timestamp = pendulum.parse(args.from_date, strict=False).int_timestamp
            end_to_timestamp = pendulum.parse(args.to_date, strict=False).int_timestamp
        except pendulum.parsing.exceptions.ParserError:
            print("Cannot parse the date, try without the 'lazy' argument")
    if from_to_timestamp > end_to_timestamp:
        print("Starting date cannot be later than ending date. Maybe you confused '--from' and '--to'")
    stat = readlog(args, from_to_timestamp, end_to_timestamp)
    # print(stat)
    result = create_stat(stat)
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
    """.format(args.from_date, args.to_date, 
    result["api"]["2xx"],result["api"]["3xx"],result["api"]["4xx"],result["api"]["5xx"],
    result["tools"]["2xx"],result["tools"]["3xx"],result["tools"]["4xx"],result["tools"]["5xx"]))


if __name__ == "__main__":
    get_stat()
