# Date Uts
##### _Better way to handle dates_
#
### Installation

```sh
pip install dateUts
```

### Usage
#
#### sqlToDate
```py
from dateUts import sqlToDate
result = sqlToDate('1991-12-23')
print(result)
```
```py
datetime.datetime(1991, 12, 23, 0, 0)
```
#### dateToSql
```py
from dateUts import dateToSql
from datetime import datetime

today = datetime.now()
result = dateToSql(today)
print(result)
```
```py
'2022-05-25'
```
#### now
```py
from dateUts import now

now1 = now()
now2 = now(fmt='%Y-%d-%m')
now3 = now(fmt='sql')
print(now1)
print(now2)
print(now3)
```
```py
datetime.datetime(2022, 5, 25, 18, 57, 5, 710329)
'2022-05-25'
'2022-25-05'
```
#### today
```py
from dateUts import today

today1 = today()
today2 = today(fmt='%Y-%d-%m')
today3 = today(fmt='sql')
today4 = today(fmt='sql',addDays=1)
today5 = today(fmt='sql',addDays=-1)
print(today1)
print(today2)
print(today3)
print(today4)
print(today5)
```
```py
datetime.datetime(2022, 5, 25, 18, 57, 5, 710329)
'2022-05-25'
'2022-25-05'
'2022-25-06'
'2022-25-04'
```

#### yesterday
```py
from dateUts import yesterday

ystd1 = yesterday()
ystd2 = yesterday(fmt='%Y-%d-%m')
ystd3 = yesterday(fmt='sql')
print(ystd1)
print(ystd2)
print(ystd3)
```
```py
datetime.datetime(2022, 5, 24, 18, 57, 5, 710329)
'2022-24-05'
'2022-05-24'
```
#### dateRange
```py
from dateUts import sqlToDate,dateRange

start = sqlToDate('2022-05-01')
end   = sqlToDate('2022-05-03')

range1 = dateRange(start,end)
range2 = dateRange(start,end,fmt='sql')
print(range1)
print(range2)
```
```py
[datetime.datetime(2022, 5, 1, 0, 0), datetime.datetime(2022, 5, 2, 0, 0), datetime.datetime(2022, 5, 3, 0, 0)]
['2022-05-01', '2022-05-02', '2022-05-03']
```

#### dateAdd
```py
from dateUts import sqlToDate,dateToSql,dateAdd

mydate           = sqlToDate('2022-05-02')
mydate_plus1_day = dateAdd(mydate,1,'day')
mydate_less1_day = dateAdd(mydate,-1,'day')
mydate_plus1_yer = dateAdd(mydate,1,'year')

print(dateToSql(mydate))
print(dateToSql(mydate_plus1_day))
print(dateToSql(mydate_less1_day))
print(dateToSql(mydate_plus1_yer))
```
```py
'2022-05-02'
'2022-05-03'
'2022-05-01'
'2023-05-02'
```

#### lastWorkingDate
```py
from dateUts import lastWorkingDate

#Assuming today as '2022-05-25'
dt = lastWorkingDate(fmt='sql')
print(dt)

#Assuming today as '2022-05-23'
dt = lastWorkingDate(fmt='sql')
print(dt)
```
```py
'2022-05-24'
'2022-05-20'
```