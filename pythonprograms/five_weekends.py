def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Five_weekends#Python

from datetime import timedelta, date

def print(*args, **kwargs):
    pass

n = {n}

DAY     = timedelta(days=1)
START, STOP = date(1, 1, 1), date(n, 1, 1)
WEEKEND = {{6, 5, 4}}     # Sunday is day 6
FMT     = '%Y %m(%B)'
 
def fiveweekendspermonth(start=START, stop=STOP):
    'Compute months with five weekends between dates'
 
    when = start
    lastmonth = weekenddays = 0
    fiveweekends = []
    while when < stop:
        year, mon, _mday, _h, _m, _s, wday, _yday, _isdst = when.timetuple()
        if mon != lastmonth:
            if weekenddays >= 15:
                fiveweekends.append(when - DAY)
            weekenddays = 0
            lastmonth = mon
        if wday in WEEKEND:
            weekenddays += 1
        when += DAY
    return fiveweekends
 
dates = fiveweekendspermonth()
indent = '  '
print('There are %s months of which the first and last five are:' % len(dates))
print(indent +('\\n'+indent).join(d.strftime(FMT) for d in dates[:5]))
print(indent +'...')
print(indent +('\\n'+indent).join(d.strftime(FMT) for d in dates[-5:]))
 
print('\\nThere are %i years in the range that do not have months with five weekends'
      % len(set(range(START.year, STOP.year)) - {{d.year for d in dates}}))

"""
