## Data Drift Review
MO-02 (sprint 1)

## Data Drift
- Data drift is where sensor data slowly changes over time, like a season or from degradation of a physical sensor. With these changes, what is considered "normal" also changes. A model trained on old data does not keep up with the new data and its norms and would give incorrect feedback. E.g. trained on winter temp data, now in summer, it flags every temperature over 20 degrees, even though this is normal for summer.

## Current implementation
- After going through the data_science files I couldn't find anything that handles drift in the Models code. The model isn't saved or reused anywhere.

- detector_runner.py makes a new IsolationForestDetector every time it runs.
- In iforest_detector.py, a new detector starts with _fitted = False - line 35, so detect() trains it on whatever data it gets.
- every batch gets a brand new model and nothing carries over between runs. there is not continuity. 

## Testing
I made data_drift_testing.py to check if the results stay the same. It uses the AWS data (aws_control_merged.csv) and splits it into 2 batches that share 1000 readings. Each batch gets its own new model like how the project works now, then it compares the results for the readings that are in both.

Results:
- Readings in both batches: 1000
- Average score change: 0.0232
- Biggest score change: 0.1182
- Readings flagged differently: 70 (7%)

in testing the readings were the exact same but we still see that 7% of readungs were flagged differently in each test. this shows that whether a reading gets flagged is due to what batch it is in and. not the actual reading itself. 



## Why it's a problem
- Someone could upload the same data in a different batch and get different alerts.
- You cant compare scores between runs or over time.
- For live data, retraining on small batches means it never learns what normal actually looks like.

## Suggestions 
- Train the model once on normal past data and save it, then score new data with that instead of retraining every time.
- Retrain every so often for rolling window effect so it keeps up with slow changes.

## Files
- data_drift_testing.py 