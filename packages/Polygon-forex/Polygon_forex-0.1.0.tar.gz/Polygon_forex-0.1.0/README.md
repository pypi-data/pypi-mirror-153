# polygon
Data engineering HW1

### Install
pip install Polygon

## Get started
```Python
from Polygon_forex import AUDUSD_return
#Instantiate a object
#avg price = 1
A = AUDUSD_return(tick_time="2022-06-04 10:39:06",avg_price=1)
A.last_price = 10
A.hist_return = 100
A.run_sum = 100.0
A.num = 10
#pop price = 2
#Get avg return
print("The average return of AUDUSD is:")
print(A.get_avg(pop_value=2.0))
'''