from preprocessor import load_and_prepare
from detectors.iforest_detector import IsolationForestDetector

# load nab data
df, _ = load_and_prepare("../datasets/nab_realtraffic/aws_control_merged.csv")

# split into two batches - includes overlap
batch_a = df.iloc[:2000]
batch_b = df.iloc[1000:3000]

# run iso Forest on each batch separately
out_a = IsolationForestDetector().detect(batch_a)

out_b = IsolationForestDetector().detect(batch_b)

# only look at readings that are in both batches
overlap = out_a["score"].index.intersection(out_b["score"].index)

# compare the scores and flags for those same readings
score_change = (out_a["score"][overlap] - out_b["score"][overlap]).abs()

flag_change = (out_a["anomaly_flag"][overlap] != out_b["anomaly_flag"][overlap]).sum()

print("readings in both of the batches:", len(overlap))

print("Average score change:", round(score_change.mean(), 4))

print("Biggest score change:", round(score_change.max(), 4))

print("readings flagged differntly:", int(flag_change))