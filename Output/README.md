# FlowDroid Output Results

## Overview
This repository contains the results of FlowDroid taint analysis performed on 10 Android APKs using three different timeout configurations (60 seconds, 300 seconds, and 1200 seconds). For each APK and timeout configuration, there are two files:
- A **TXT file**: Captures the FlowDroid console output.
- An **XML file**: Contains the detailed taint analysis results including sources, sinks, and data flow paths.

The analysis was conducted on a MinisForum Venus EM780 MiniPC running Windows 11, leveraging 16 CPU threads and 32GB of RAM. Each timeout configuration allocated specific proportions of time for callback collection (-ct), main data flow analysis (-dt), and result collection (-rt).

### Timeout Configuration Details:
- **60-Second Timeout**:
  - Callback Collection (-ct): 15 seconds
  - Main Data Flow Analysis (-dt): 35 seconds
  - Result Collection (-rt): 10 seconds
- **300-Second Timeout**:
  - Callback Collection (-ct): 60 seconds
  - Main Data Flow Analysis (-dt): 210 seconds
  - Result Collection (-rt): 30 seconds
- **1200-Second Timeout**:
  - Callback Collection (-ct): 240 seconds
  - Main Data Flow Analysis (-dt): 840 seconds
  - Result Collection (-rt): 120 seconds

---

## Analyzed APKs
The following APKs were analyzed:

1. **com.delhi.metro.dtc.apk**
2. **com.hawaiianairlines.app.apk**
3. **com.imo.android.imoim.apk**
4. **com.tado.apk**
5. **com.walkme.azores.new.apk**
6. **com.wooxhome.smart.apk**
7. **com.yourdelivery.pyszne.apk**
8. **linko.home.apk**
9. **mynt.app.apk**
10. **nz.co.stuff.android.news.apk**

---

## Output Folder Structure
The `Output` folder contains the results for each APK and timeout configuration. Each set includes:

### File Naming Convention:
```
[APK_NAME]_timeout[TIMEOUT].txt
[APK_NAME]_timeout[TIMEOUT].xml
```
- `APK_NAME`: Name of the APK file (e.g., com.tado).
- `TIMEOUT`: Timeout duration in seconds (60, 300, or 1200).

### Example Files:
For `com.delhi.metro.dtc.apk`:
- `com.delhi.metro.dtc_timeout60.txt` and `com.delhi.metro.dtc_timeout60.xml`
- `com.delhi.metro.dtc_timeout300.txt` and `com.delhi.metro.dtc_timeout300.xml`
- `com.delhi.metro.dtc_timeout1200.txt` and `com.delhi.metro.dtc_timeout1200.xml`

---

## Results Summary

### General Observations:
- **Timeout Impact**: Longer timeouts generally yielded more comprehensive results, identifying additional taint paths and leaks. However, there were some anomalies where shorter timeouts found more results, likely due to differences in processing order or resource constraints.
- **No Failures**: All analyses completed successfully without crashing on the MiniPC setup.
- **Leak Variability**: Certain APKs like `com.hawaiianairlines.app.apk` revealed additional leaks with longer timeouts, whereas `com.wooxhome.smart.apk` showed no leaks across all timeouts.

### Notable Findings:
1. **com.tado.apk**:
   - Identified high-risk data flows involving sensitive user credentials (e.g., passwords written to output streams).
   - Anomalous result: The 1200s timeout found fewer leaks than the 60s or 300s timeouts.

2. **com.hawaiianairlines.app.apk**:
   - More leaks were discovered with increasing timeout durations.
   - High-risk data flows included serialization and data encoding for potential exfiltration.

3. **com.imo.android.imoim.apk**:
   - Found the highest number of leaks among all analyzed APKs.
   - Additional leaks were only identified with the 1200s timeout.

4. **linko.home.apk**:
   - Showed unusual behavior where the 300s timeout found fewer leaks than the 60s or 1200s timeouts.

5. **com.wooxhome.smart.apk**:
   - No leaks identified across all timeout configurations, suggesting minimal or no taint propagation within the app.

---

## Performance Metrics
- **Resource Utilization**: The analysis maximized CPU and memory usage, especially during the main data flow analysis (-dt) phase.
- **Runtime**: Total runtime for all analyses was approximately 5 hours and 5 minutes.

---

## Challenges
- Anomalies in timeout results for certain APKs require further investigation.
- No significant issues were encountered with hardware on the MiniPC setup. However, when running the analysis on a Virtual Machine, memory limitations necessitated configuration changes (e.g., removing the `-r` flag).

---

## Notes
- The XML files contain detailed taint paths, sources, and sinks for each identified leak.
- TXT files provide a high-level summary of the FlowDroid process and any notable console output.

For further details on the analysis configuration, refer to the [FlowDroid GitHub repository](https://github.com/secure-software-engineering/FlowDroid).

---

If you have questions or need assistance interpreting the results, feel free to reach out!
