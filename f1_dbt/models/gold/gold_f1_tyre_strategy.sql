select
    raceyear,
    grandprix,
    compound,
    stint,
    avg(stint_length) as stint_length,
    avg(avg_laptime) as avg_laptime,
    avg(laptime_range) as lap_time_range
from {{ ref('silver_f1_laps_features') }}
group by
    raceyear,
    grandprix,
    compound,
    stint