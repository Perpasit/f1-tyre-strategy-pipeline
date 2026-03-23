select
    raceyear,
    grandprix,
    compound,
    avg(avg_laptime) as avg_laptime
from {{ ref('silver_f1_laps_features') }}
group by
    raceyear,
    grandprix,
    compound