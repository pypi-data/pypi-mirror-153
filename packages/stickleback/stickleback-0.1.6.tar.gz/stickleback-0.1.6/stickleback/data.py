import pandas as pd
import pkg_resources
from typing import Dict, Tuple

def load_lunges() -> Tuple[Dict[str, pd.DataFrame], 
                           Dict[str, pd.DatetimeIndex]]:
    """Load sample data.

    Loads a small dataset containing six blue whale deployments and labeled 
    lunge-feeding behaviors.

    Returns:
        Tuple[Dict[str, pd.DataFrame], Dict[str, pd.DatetimeIndex]]: Sensors 
            and events, in Stickleback format.
    """
    sensors_file = (pkg_resources
                    .resource_filename('stickleback', 'data/sensors.csv'))
    sensors_csv = pd.read_csv(sensors_file)
    
    events_file = (pkg_resources
                   .resource_filename('stickleback', 'data/events.csv'))
    events_csv = pd.read_csv(events_file)
    
    sensors, events = dict(), dict()
    
    for k in sensors_csv["deployid"].unique():
        sensors[k] = (sensors_csv[sensors_csv["deployid"] == k]
                      .drop("deployid", axis=1)
                      .set_index("datetime"))
        sensors[k].index = pd.DatetimeIndex(sensors[k].index)
        
    for k in events_csv["deployid"].unique():
        events[k] = pd.DatetimeIndex(
            events_csv[events_csv["deployid"] == k]["datetime"]
        )
    
    return sensors, events
