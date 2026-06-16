# Report Generator

Builds Markdown reports from the mock agent pipeline output.

## Files
- `field_packet_report.py` — `build_report()` → per-packet review report at
  `data/outputs/reports/<packet_id>_report.md`.
- `mvp_summary_report.py` — `build_mvp_summary()` → one-page build/status summary.

## A Field Packet report includes
Field Packet ID · contributor code · place label · observation date · data
included · photo quality summary · voice observation summary · AI summary ·
indicators · AI limitations · recommended next action · human review status ·
**sensitivity note**.

## Run
```bash
python3 services/report-generator/field_packet_report.py
python3 services/report-generator/mvp_summary_report.py
```
Reports never contain raw coordinates or contributor identities.
