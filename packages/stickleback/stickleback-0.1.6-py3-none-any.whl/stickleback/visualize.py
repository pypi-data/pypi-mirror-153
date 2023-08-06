from matplotlib.figure import Figure as matplotlibFigure
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.graph_objs._figure import Figure as plotlyFigure
from plotly.subplots import make_subplots
import stickleback.util as sb_util

from stickleback.types import *
from typing import Dict, Union

figure_T = Union[plotlyFigure, matplotlibFigure]

def plot_sensors_events(deployid: str, 
                        sensors: sensors_T, 
                        events: events_T, 
                        interactive=True) -> figure_T:
    """Plot sensor data and labeled events.

    Args:
        deployid (str): Deployment ID to plot.
        sensors (Dict[str, pd.DataFrame]): Sensor data.
        events (Dict[str, pd.DatetimeIndex]): Labeled events.
        interactive (bool, optional): Interaction flag. If True, produces an 
            interactive plotly figure. Else, a static matplotlib figure. 
            Defaults to True.

    Returns:
        Union[plotlyFigure, matplotlibFigure]: Figure with sensors and events.
    """
    _sensors = sensors[deployid]
    _events = _sensors.loc[events[deployid]]
    
    if interactive:
        return __plot_sensors_events_interactive(_sensors, _events)
    else:
        return __plot_sensors_events_static(_sensors, _events)

def __plot_sensors_events_interactive(sensors: pd.DataFrame, 
                                      event_sensors: pd.DataFrame) -> plotlyFigure:
    """Plot sensors and events interactively.

    Args:
        sensors (pd.DataFrame): Sensor data for one deployment.
        event_sensors (pd.DataFrame): Sensor data at event times for one 
            deployment.

    Returns:
        plotlyFigure: Interactive plotly figure.
    """
    fig = make_subplots(rows=len(sensors.columns), cols=1,
                        shared_xaxes=True,)
    for i, col in enumerate(sensors.columns):
        fig.append_trace(go.Scatter(
            x=sensors.index,
            y=sensors[col],
            mode="lines"
        ), row=i + 1, col=1)
        fig.append_trace(go.Scatter(
            x=event_sensors.index,
            y=event_sensors[col],
            mode="markers"
        ), row=i + 1, col=1)
        fig.update_yaxes(title_text=col, row=i + 1, col=1)
        
    fig.update_layout(showlegend=False)
    return fig

def __plot_sensors_events_static(sensors: pd.DataFrame, 
                                 event_sensors: pd.DataFrame) -> matplotlibFigure:
    """Plot sensors and events statically.

    Args:
        sensors (pd.DataFrame): Sensor data for one deployment.
        event_sensors (pd.DataFrame): Sensor data at event times for one 
            deployment.

    Returns:
        matplotlibFigure: Static matplotlib figure.
    """
    fig, axs = plt.subplots(len(sensors.columns), 1)
    for i, col in enumerate(sensors.columns):
        # sensor data
        axs[i].plot(sensors.index, sensors[col], "-", zorder=1)
        # events
        axs[i].scatter(event_sensors.index, 
                       event_sensors[col], 
                       facecolors="none", 
                       edgecolors="r", 
                       zorder=2)
        axs[i].set_ylabel(col)
        
    return fig

def plot_predictions(deployid: str, 
                     sensors: sensors_T, 
                     predictions: prediction_T,
                     outcomes: outcomes_T = None, 
                     interactive: bool = True) -> figure_T:
    """Plot model predictions.

    Args:
        deployid (str): Deployment ID to plot.
        sensors (Dict[str, pd.DataFrame]): Sensor data.
        predictions (Dict[str, Tuple[pd.Series, pd.DatetimeIndex]]): Model 
            predictions (as from Stickleback.predict()).
        outcomes (Dict[str, pd.Series], optional): Prediction outcomes (as from
            Stickleback.assess()). Defaults to None.
        interactive (bool, optional): Interaction flag. If True, produces an 
            interactive plotly figure. Else, a static matplotlib figure. 
            Defaults to True.

    Returns:
        Union[plotlyFigure, matplotlibFigure]: Figure with model predictions.
    """
    lcl, gbl = predictions[deployid]
    data = sensors[deployid].join(lcl)

    predicted_only = data.loc[gbl]
    actual_only = None
    if outcomes is not None:
        predicted_only = predicted_only.join(outcomes[deployid])
        is_actual = outcomes[deployid].isin(["TP", "FN"])
        actual_idx = outcomes[deployid].index[is_actual]
        actual_only = data.loc[actual_idx].join(outcomes[deployid])

    if interactive:
        return __plot_predictions_interactive(data, predicted_only, 
                                              actual_only)
    else:
        return __plot_predictions_static(data, predicted_only, actual_only)

def __plot_predictions_interactive(data: pd.DataFrame, 
                                   predicted: pd.DataFrame, 
                                   actual: pd.DataFrame = None) -> plotlyFigure:
    """Plot model predictions interactively.

    Args:
        data (pd.DataFrame): Sensor data for one deployment.
        predicted (pd.DataFrame): Sensor data at predicted event times.
        actual (pd.DataFrame, optional): Sensor data at actual event times.
            Defaults to None.

    Returns:
        plotlyFigure: Interactive plotly figure.
    """
    fig = make_subplots(rows=len(data.columns), cols=1,
                        shared_xaxes=True,)

    pred_color = "purple"
    if "outcome" in predicted.columns:
        pred_color = ["blue" if o == "TP" else "red" 
                      for o in predicted["outcome"]]
    if actual is not None:
        actual_color = ["blue" if o == "TP" else "red" 
                        for o in actual["outcome"]]

    for i, col in enumerate(data):
        # Line plot
        fig.append_trace(go.Scatter(
            x=data.index,
            y=data[col],
            mode="lines"
        ), row=i + 1, col=1)
        # Predicted events
        fig.append_trace(go.Scatter(
            x=predicted.index,
            y=predicted[col],
            marker_color=pred_color,
            mode="markers"
        ), row=i + 1, col=1)
        # Actual events
        if actual is not None:
            fig.append_trace(go.Scatter(
                x=actual.index,
                y=actual[col],
                mode="markers",
                marker_symbol="circle-open",
                marker_size=10,
                marker_color=actual_color,
            ), row=i + 1, col=1)
        fig.update_yaxes(title_text=col, row=i + 1, col=1)
        
    fig.update_layout(showlegend=False)
    return fig

def __plot_predictions_static(data: pd.DataFrame, 
                              predicted: pd.DataFrame, 
                              actual: pd.DataFrame = None) -> matplotlibFigure:
    """Plot model predictions statically.

    Args:
        data (pd.DataFrame): Sensor data for one deployment.
        predicted (pd.DataFrame): Sensor data at predicted event times.
        actual (pd.DataFrame, optional): Sensor data at actual event times. 
            Defaults to None.

    Returns:
        matplotlibFigure: Static matplotlib figure.
    """
    fig, axs = plt.subplots(len(data.columns), 1)
    for i, col in enumerate(data):
        # sensor data
        axs[i].plot(data.index, data[col], "-", zorder=1)
        axs[i].set_ylabel(col)
        # predicted events
        axs[i].scatter(predicted.index, 
                        predicted[col], 
                        c=["blue" if o == "TP" else "red" 
                           for o in predicted["outcome"]], zorder=2)
        # actual events
        axs[i].scatter(actual.index, 
                        actual[col], 
                        edgecolors=["blue" if o == "TP" else "red" 
                                    for o in actual["outcome"]],
                        facecolors="none",
                        zorder=3)
        
    return fig

def outcome_table(outcomes: outcomes_T,
                  sensors: sensors_T) -> pd.DataFrame:
    """Create a table of model prediction outcomes.

    Args:
        outcomes (Dict[str, pd.Series]): Model prediction outcomes (as from 
            Stickleback.assess()).
        sensors (Dict[str, pd.DataFrame]): Sensor data.

    Returns:
        pd.DataFrame: A table of prediction outcomes. Each row is a deployment.
            Columns are F1 score (F1); number of true positives (TP), false 
            positives (FP), and false negatives (FN); and deployment duration 
            in hours (Duration (hours)).
    """
    def add_deployid(d, o):
        result = pd.DataFrame(o)
        result.insert(0, "deployid", np.full(len(o), [d]))
        return result
    
    counts = pd.concat([add_deployid(d, o) for d, o in outcomes.items()])
    result = (counts
              .groupby(["deployid", "outcome"])
              .size()
              .unstack(fill_value=0))
    
    for o in ["TP", "FP", "FN"]:
        if o not in result:
            result[o] = 0
    
    result["F1"] = sb_util.f1(result["TP"], result["FP"], result["FN"])
    
    dur_dict = {k: (v.index[-1] - v.index[0]) / pd.Timedelta(hours=1) 
                for k, v in sensors.items()}
    durations = pd.DataFrame.from_dict(dur_dict, "index")
    durations.columns = ["Duration (hours)"]
    result = result.join(durations)
    
    result = result[["F1", 
                     "TP", 
                     "FP", 
                     "FN", 
                     "Duration (hours)"]]
    return result
