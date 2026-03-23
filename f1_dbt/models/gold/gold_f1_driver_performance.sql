select
    raceyear,
    grandprix,
    driver,
    avg(avg_laptime) as avg_laptime,
    avg(laptime_stddev) as laptime_stddev
from {{ ref('silver_f1_laps_features') }}
group by
    raceyear,
    grandprix,
    driver