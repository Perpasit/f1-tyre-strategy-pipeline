with base as (

    select *
    from {{ ref('silver_f1_laps_clean') }}

),

stint_stats as (

    select
        raceyear,
        grandprix,
        sessiontype,
        driver,
        compound,
        stint,
        count(*) as stint_length,
        avg(laptime) as avg_laptime,
        min(laptime) as best_laptime,
        max(laptime) as worst_laptime,
        stddev(laptime) as laptime_stddev,
        max(laptime) - min(laptime) as laptime_range
    from base
    group by
        raceyear,
        grandprix,
        sessiontype,
        driver,
        compound,
        stint

)

select *
from stint_stats