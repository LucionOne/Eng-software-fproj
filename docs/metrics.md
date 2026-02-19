# Metrics (baseline)

We track a small set of verifiable metrics weekly. Each metric has a clear definition and collection method.

1. **Lead time (flow)**  
   - **Definition:** Time from issue creation to merge (in hours).  
   - **Why:** Measures how quickly work moves through the system.  
   - **How to collect:** Use GitHub issue + PR timestamps. Report median and 90th percentile weekly.  
   - **Baseline/target:** TBD

2. **PR review time (flow)**  
   - **Definition:** Time from PR opened to first approval (in hours).  
   - **Why:** Shows review latency; long review time blocks flow.  
   - **How to collect:** PR opened/approved timestamps via GitHub UI. Report average and max weekly.  
   - **Baseline/target:** TBD

3. **Post-merge failures (quality)**  
   - **Definition:** Number of incidents where merged changes caused a regression or required a hotfix within 7 days.  
   - **Why:** Direct indicator of stability/quality.  
   - **How to collect:** Track incidents via issues labeled `regression`. Count per week.  
   - **Baseline/target:** TBD

**Reporting cadence:** generate a short metrics report weekly and keep it in `docs/metrics-logs/`  
