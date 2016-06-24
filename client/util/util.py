import datetime

def parseDate(date_str):
    if date_str == "next":
        d = datetime.date.today()
        d += datetime.timedelta(1)
        while d.weekday() != 2 and d.weekday() != 6 :
            d += datetime.timedelta(1)
            print(str(d))
        return d
    else:
        day, month = map(int, date_str.split('-'))
        my_date = datetime.date(datetime.datetime.now().year, month, day)
        return my_date
