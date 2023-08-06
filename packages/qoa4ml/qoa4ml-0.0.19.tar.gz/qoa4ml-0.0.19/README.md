# QoA4ML - Quality of Analytics for ML

## Source code
https://github.com/rdsea/QoA4ML

## Probes
* [QoA4ML Probes](https://github.com/rdsea/QoA4ML/tree/main/qoa4ml_lib/qoa4ml/probes.py): libraries and lightweight modules capturing metrics. They are integrated into suitable ML serving frameworks and ML code
* Probe properties:
  - Can be written in different languages (Python, GoLang)
  - Can have different communications to monitoring systems (depending on probes and its ML support)
  - Capture metrics with a clear definition/scope
    - e.g., Response time for an ML stage (training) or a service call (of ML APIs)
    - Thus output of probes must be correlated to objects to be monitored and the tenant
  - Support high or low-level metrics/attributes
    - depending on probes implementation
  - Can be instrumented into source code or standlone

## [QoA4ML Reports](https://github.com/rdsea/QoA4ML/blob/main/qoa4ml_lib/qoa4ml/reports.py)

This module defines ``QoA_Client``, an object that will gather metrics from probes and client information, create simple reports and send it to handler

## [Examples](https://github.com/rdsea/QoA4ML/tree/main/example)
https://github.com/rdsea/QoA4ML/tree/main/example



