select
    cast(RACEYEAR as int) as raceyear,
    trim(GRANDPRIX) as grandprix,
    trim(SESSIONTYPE) as sessiontype,
    trim(DRIVER) as driver,
    cast(LAPNUMBER as int) as lapnumber,
    cast(LAPTIME as float) as laptime,
    upper(trim(COMPOUND)) as compound,
    cast(STINT as int) as stint
from {{ source('bronze', 'f1_laps_raw') }}
where RACEYEAR is not null
  and GRANDPRIX is not null
  and SESSIONTYPE is not null
  and DRIVER is not null
  and LAPNUMBER is not null
  and LAPTIME is not null
  and COMPOUND is not null
  and STINT is not null
  and LAPTIME > 0
  and LAPNUMBER > 0
  and STINT > 0