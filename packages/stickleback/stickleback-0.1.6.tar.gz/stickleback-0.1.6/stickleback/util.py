import pandas as pd
import pickle
import numpy as np
import sktime.datatypes._panel._convert as convert 
from stickleback.types import *
from typing import Collection, Dict, Tuple, Union

def extract_nested(sensors: sensors_T, 
                   idx: Dict[str, pd.DatetimeIndex], 
                   win_size: int) -> nested_T:
    """Extract windows from sensor data in sktime nested DataFrame format.

    Args:
        sensors (Dict[str, pd.DataFrame]): Sensor data.
        idx (Dict[str, pd.DatetimeIndex]): Dict of indicies, keyed by 
            deployment ID. Each output window will be centered on one of these
            indices.
        win_size (int): Window size.

    Returns:
        Dict[str, pd.DataFrame]: Dict of data windows in sktime nested 
            DataFrame format.
    """
    win_size_2 = int(win_size / 2)

    def _extract(_deployid: str, _idx: pd.DatetimeIndex):
        _sensors = sensors[_deployid]
        idx = _sensors.index.get_indexer(_idx)
        data_3d = np.empty([len(idx), len(_sensors.columns), win_size], float)
        data_arr = _sensors.to_numpy().transpose()
        start_idx = idx - win_size_2
        for i, start in enumerate(start_idx):
            data_3d[i] = data_arr[:, start:(start + win_size)]
        nested = convert.from_3d_numpy_to_nested(data_3d)
        nested.columns = _sensors.columns
        nested.index = _sensors.index[idx]
        return nested

    return {d: _extract(d, i) for d, i in idx.items()}

def extract_all(sensors: sensors_T, 
                nth: int, 
                win_size: int, 
                mask: mask_T = None) -> nested_T:
    """Extract all windows from sensor data in sktime nested DataFrame format.

    Args:
        sensors (Dict[str, pd.DataFrame]): Sensor data.
        nth (int): Sliding window step size.
        win_size (int): Window size.
        mask (mask_T, optional): Window mask. Only windows in sensors[
            deployid] where mask[deployid] is True will be extracted. If None, 
            no mask applied. Defaults to None.

    Returns:
        Dict[str, pd.DataFrame]: Dict of data windows in sktime nested 
            DataFrame format.
    """
    if mask is None:
        mask = {d: np.full(len(sensors[d]), True) for d in sensors}
        
    win_size_2 = int(win_size / 2)
    idx = dict()
    for d in sensors:
        _idx = np.arange(win_size_2, len(sensors[d]) - win_size_2, nth)
        # Next line (admittedly) confusing. Look up _idx in mask[d] and keep
        # only those where mask is True
        _idx = _idx[mask[d][_idx]]
        idx[d] = sensors[d].index[_idx]
        
    return extract_nested(sensors, idx, win_size)
    
def sample_nonevents(sensors: sensors_T, 
                     events: events_T, 
                     win_size: int, 
                     mask: mask_T = None, 
                     rng: np.random.Generator = None) -> nested_T:
    """Randomly sample non-event windows from sensor data.

    Args:
        sensors (Dict[str, pd.DataFrame]): Sensor data.
        events (Dict[str, pd.DatetimeIndex]): Labeled events.
        win_size (int): Window size.
        mask (Dict[str, np.ndarray], optional): Window mask. Only windows in 
            sensors[deployid] where mask[deployid] is True will be extracted. 
            If None, no mask applied. Defaults to None.
        seed (int, optional): Random number generator seed. Defaults to None.

    Returns:
        Dict[str, pd.DataFrame]: Dict of data windows in sktime nested 
            DataFrame format.
    """
    win_size_2 = int(win_size / 2)
    if mask is None:
        mask = {d: np.full(len(sensors[d]), True) for d in sensors}

    def _diff_from(xs: np.ndarray, ys: np.ndarray) -> np.ndarray:
        return np.array([np.min(np.abs(x - ys)) for x in xs])

    def _sample(_sensors: pd.DataFrame, 
                _events: pd.DatetimeIndex, 
                _mask: np.ndarray):
        nonevent_choices = np.arange(win_size_2, 
                                     len(_sensors) - win_size_2, 
                                     win_size)
        nonevent_choices = nonevent_choices[_mask[nonevent_choices]]
        diff_from_event = _diff_from(nonevent_choices, 
                                     _sensors.index.searchsorted(_events))
        nonevent_choices = nonevent_choices[diff_from_event > win_size]
        return _sensors.index[rng.choice(nonevent_choices, 
                                         size=len(_events), 
                                         replace=True)]

    idx = {d: _sample(sensors[d], events[d], mask[d]) for d in sensors}
    return extract_nested(sensors, idx, win_size)

def align_events(events: events_T, sensors: sensors_T) -> events_T:
    """Align labeled events with sensor data indices.

    Args:
        events (Dict[str, pd.DatetimeIndex]): Labeled events
        sensors (Dict[str, pd.DataFrame]): Sensor data

    Returns:
        Dict[str, pd.DatetimeIndex]: As events, but times shifted to closest 
            index in sensors.
    """
    return {d: sensors[d].index[sensors[d].index.searchsorted(e)] 
            for d, e in events.items()}

def filter_dict(d: Dict, ks: Collection) -> Dict:
    """Filter a dict by keys.

    Args:
        d (Dict): A dictionary.
        ks (Collection): Keys to keep.

    Returns:
        Dict: d, but with only the keys in ks.
    """
    return {k: v for k, v in d.items() if k in ks}

def save_fitted(sb: "Stickleback", 
                fp: str,
                sensors: sensors_T = None, 
                events: events_T = None, 
                mask: mask_T = None) -> None:
    """Save a fitted Stickleback model.

    Args:
        sb (Stickleback): Stickleback model.
        fp (str): File path.
        sensors (Dict[str, pd.DataFrame], optional): Sensor data used to fit 
            model. Defaults to None.
        events (Dict[str, pd.DatetimeIndex], optional): Labeled events used to 
            fit model. Defaults to None.
        mask (Dict[str, np.ndarray], optional): Mask used to fit model. 
            Defaults to None.
    """
    objects = (sb, sensors, events, mask)
    with open(fp, 'wb') as f:
        pickle.dump(objects, f)
        
def load_fitted(fp: str) -> Tuple["Stickleback", 
                                  sensors_T, 
                                  events_T, 
                                  mask_T]:
    """Load a fitted Stickleback model.

    Returns:
        A tuple containing:
            The fitted Stickleback model
            The sensor data used to fit the model (possibly None).
            The labeled events used to fit the model (possibly None).
            The mask used to fit the model (possibly None).
    """
    with open(fp, 'rb') as f:
        result = pickle.load(f)
    
    return result

def f1(tps: Union[float, pd.Series],
       fps: Union[float, pd.Series],
       fns: Union[float, pd.Series]) -> Union[float, pd.Series]:
    """Calculate F1 score

    Args:
        tps (Union[float, pd.Series]): Count(s) of true positives.
        fps (Union[float, pd.Series]): Count(s) of false positives.
        fns (Union[float, pd.Series]): Count(s) of false negatives.

    Returns:
        Union[float, pd.Series]: F1 score(s).
    """
    return tps / (tps + (fps + fns) / 2)
