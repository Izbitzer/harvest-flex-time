from datetime import datetime
from datetime import timedelta
import json
import os
import sys

import requests
import holidays


class HourCalculator:
    base_url = "https://api.harvestapp.com/api/v2/"
    harvest_account_id = "718423"
    hours = 0
    expected_hours = 0

    def __init__(self, start_date, end_date, user_id, token):
        self.start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        self.end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        self.user_id = user_id
        self.token = token
        self.holidays = holidays.CountryHoliday("SE", False)
        print("Start date: %s, end date: %s, user ID: %s" % (self.start_date, self.end_date, self.user_id))

    def run(self):
        self._calculate_expected_hours()
        self._process()
        self._print_result()

    def _print_result(self):
        print("Actual hours: %s. Expected hours: %s" % (self.hours, self.expected_hours))
        diff = round(self.hours - self.expected_hours, 2)
        if diff < 0:
            print("\t\033[93m%s hours below expected" % diff)
        else:
            print("\t\033[92m%s hours above expected" % diff)

    def _print_progress_dot(self, finished=False):
        sys.stdout.write(".")
        if finished:
            sys.stdout.write("\n")
        sys.stdout.flush()

    def _calculate_expected_hours(self):
        for day in date_range(self.start_date, self.end_date):
            if is_weekend(day):
                continue
            if self.holidays.get(day):
                if is_tuesday(day) and day > self.start_date and not self.holidays.get(prev_day(day)):
                    self.expected_hours -= 8
                if is_thursday(day) and day < self.end_date and not self.holidays.get(next_day(day)):
                    self.expected_hours -= 8
                continue
            self.expected_hours += 8

    def _process(self):
        url = "%stime_entries?per_page=100&from=%s&to=%s&page=1" % (self.base_url, self.start_date, self.end_date)
        if self.user_id:
            url += "&user_id=%s" % self.user_id
        while url is not None:
            response = requests.get(url, headers=self._headers()).json()
            self.hours += sum([entry["hours"] for entry in response.get("time_entries", [])])

            url = response.get("links", {}).get("next")
            self._print_progress_dot(finished=(url is None))

    def _headers(self):
        return {
            "Harvest-Account-ID": self.harvest_account_id,
            "Authorization": "Bearer %s" % self.token,
        }

# Utility functions

def date_range(start, end):
    current = start
    while current <= end:
        yield current
        current = current + timedelta(days=1)

def next_day(day):
    return day + timedelta(days=1)

def prev_day(day):
    return day - timedelta(days=1)

def is_weekend(d):
    return d.isoweekday() > 5

def is_tuesday(d):
    return d.isoweekday() == 2

def is_thursday(d):
    return d.isoweekday() == 4

if __name__ == "__main__":
    if len(sys.argv) < 4:
        start_date = os.getenv("START_DATE")
        end_date = os.getenv("END_DATE")
        token = os.getenv("TOKEN")
        user_id = os.getenv("USER_ID")
    else:
        start_date = sys.argv[1]
        end_date = sys.argv[2]
        token = sys.argv[3]
        user_id = sys.argv[4] if len(sys.argv) > 4 else None

    calculator = HourCalculator(start_date, end_date, user_id, token)
    calculator.run()
