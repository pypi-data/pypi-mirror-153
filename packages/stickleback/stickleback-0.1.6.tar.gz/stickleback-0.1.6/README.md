# `stickleback`

> A machine learning pipeline for detecting fine-scale behavioral events in bio-logging data.

## Installation

Install with pip.

`pip install stickleback`

## Key concepts

* Behavioral events are brief behaviors that can be represented as a point in time, e.g. feeding or social interactions.
* High-resolution bio-logging data (e.g. from accelerometers and magnetometers) are multi-variate time series. Traditional classifiers struggle with time series data.
* `stickleback` takes a time series classification approach to detect behavioral events in longitudinal bio-logging data.

## Quick start

### Load sample data

The included sensor data contains the depth, pitch, roll, and speed of six blue whales at 10 Hz, and the event data contains the times of lunge-feeding behaviors.


```python
import pandas as pd
import sktime.classification.interval_based
import sktime.classification.compose
from stickleback.stickleback import Stickleback
import stickleback.data
import stickleback.util
import stickleback.visualize

# Load sample data
sensors, events = stickleback.data.load_lunges()

# Split into test and train (3 deployments each)
def split_dict(d, ks):
    dict1 = {k: v for k, v in d.items() if k in ks}
    dict2 = {k: v for k, v in d.items() if k not in ks}
    return dict1, dict2

test_deployids = list(sensors.keys())[0:2]
sensors_test, sensors_train = split_dict(sensors, test_deployids)
events_test, events_train = split_dict(events, test_deployids)
```


```python
sensors[test_deployids[0]]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>depth</th>
      <th>pitch</th>
      <th>roll</th>
      <th>speed</th>
    </tr>
    <tr>
      <th>datetime</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2018-09-05 11:55:52.400</th>
      <td>14.911083</td>
      <td>-0.059933</td>
      <td>-0.012899</td>
      <td>4.274450</td>
    </tr>
    <tr>
      <th>2018-09-05 11:55:52.500</th>
      <td>14.910864</td>
      <td>-0.067072</td>
      <td>-0.010815</td>
      <td>4.044154</td>
    </tr>
    <tr>
      <th>2018-09-05 11:55:52.600</th>
      <td>14.915853</td>
      <td>-0.075173</td>
      <td>-0.008335</td>
      <td>3.820568</td>
    </tr>
    <tr>
      <th>2018-09-05 11:55:52.700</th>
      <td>14.923190</td>
      <td>-0.085225</td>
      <td>-0.005727</td>
      <td>3.602702</td>
    </tr>
    <tr>
      <th>2018-09-05 11:55:52.800</th>
      <td>14.928955</td>
      <td>-0.096173</td>
      <td>-0.002803</td>
      <td>3.432342</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>2018-09-05 13:55:51.900</th>
      <td>22.552306</td>
      <td>-0.010861</td>
      <td>0.005441</td>
      <td>2.246061</td>
    </tr>
    <tr>
      <th>2018-09-05 13:55:52.000</th>
      <td>22.571625</td>
      <td>-0.010534</td>
      <td>0.004674</td>
      <td>2.257525</td>
    </tr>
    <tr>
      <th>2018-09-05 13:55:52.100</th>
      <td>22.588129</td>
      <td>-0.010081</td>
      <td>0.003841</td>
      <td>2.267966</td>
    </tr>
    <tr>
      <th>2018-09-05 13:55:52.200</th>
      <td>22.603341</td>
      <td>-0.009627</td>
      <td>0.003042</td>
      <td>2.272327</td>
    </tr>
    <tr>
      <th>2018-09-05 13:55:52.300</th>
      <td>22.619537</td>
      <td>-0.009355</td>
      <td>0.002164</td>
      <td>2.277328</td>
    </tr>
  </tbody>
</table>
<p>72000 rows × 4 columns</p>
</div>



### Visualize sensor and event data

`plot_sensors_events()` produces an interactive figure for exploring bio-logger data.


```python
# Choose one deployment to visualize
deployid = list(sensors.keys())[0]
stickleback.visualize.plot_sensors_events(deployid, sensors, events)
```

![Animated loop of interactively exploring data with plot_sensors_events()](https://github.com/FlukeAndFeather/stickleback/raw/main/docs/resources/plot-sensors-events.gif)

### Define model

Initialize a `Stickleback` model using Supervised Time Series Forests and a 5 s window.


```python
# Supervised Time Series Forests ensembled across the columns of `sensors`
cols = sensors[list(sensors.keys())[0]].columns
tsc = sktime.classification.interval_based.SupervisedTimeSeriesForest(n_estimators=2,
                                                                      random_state=4321)
stsf = sktime.classification.compose.ColumnEnsembleClassifier(
    estimators = [('STSF_{}'.format(col),
                   tsc,
                   [i])
                  for i, col in enumerate(cols)]
)

sb = Stickleback(
    local_clf=stsf,
    win_size=50,
    tol=pd.Timedelta("5s"),
    nth=10,
    n_folds=4,
    seed=1234
)
```

### Fit model

Fit the `Stickleback` object to the training data.


```python
sb.fit(sensors_train, events_train)
```

### Test model

Use the fitted `Stickleback` model to predict occurence of lunge-feeding events in the test dataset.


```python
predictions = sb.predict(sensors_test)
```

### Assess results

Use the temporal tolerance (in this example, 5 s) to assess model predictions. Visualize with an outcome table and an interactive visualization. In the figure, blue = true positive, hollow red = false negative, and solid red = false positive.


```python
outcomes = sb.assess(predictions, events_test)
stickleback.visualize.outcome_table(outcomes, sensors_test)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>F1</th>
      <th>TP</th>
      <th>FP</th>
      <th>FN</th>
      <th>Duration (hours)</th>
    </tr>
    <tr>
      <th>deployid</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>bw180905-49</th>
      <td>1.000000</td>
      <td>44</td>
      <td>0</td>
      <td>0</td>
      <td>1.999972</td>
    </tr>
    <tr>
      <th>bw180905-53</th>
      <td>0.943396</td>
      <td>25</td>
      <td>2</td>
      <td>1</td>
      <td>1.999972</td>
    </tr>
  </tbody>
</table>
</div>




```python
deployid = list(events_test.keys())[0]
stickleback.visualize.plot_predictions(deployid, 
                                       sensors_test, 
                                       predictions, 
                                       outcomes)
```

![Animated loop of interactively exploring predictions with plot_predictions()](https://github.com/FlukeAndFeather/stickleback/raw/main/docs/resources/plot-predictions.gif)
