# Dashboard HTML Overview

This document explains how `src/assets/dashboard.html` is organized and how it works.

## Purpose

`dashboard.html` is a standalone IoT dashboard UI for SensorFlow. It renders:
- a header with live status and settings toggle
- a collapsible settings panel
- three live gauge cards for temperature, humidity, and pH
- three time-series area charts
- a footer status bar with summary metrics

The page uses inline CSS for styling and inline JavaScript for behavior, with Chart.js loaded from a CDN.

## File structure

The file is organized into these main sections:

1. `head`
   - document metadata
   - Google font imports
   - Chart.js script import
   - inline `<style>` block for all dashboard styling
2. `body`
   - main dashboard markup inside a `.dash` wrapper
   - header, settings panel, readings row, chart cards, and footer
3. `<script>`
   - dashboard logic, configuration, data generation, API calls, chart creation, rendering, and event wiring

## CSS organization

The inline styles are grouped by purpose using header comments:

- `DESIGN TOKENS`: root variables for colors, radii, shadows, fonts, and theme values
- `LAYOUT`: page wrapper and spacing
- `GLASS CARD MIXIN`: reusable glassmorphism panel styling
- `HEADER`: brand, status badge, and settings button styles
- `SETTINGS PANEL`: toggle animation, input fields, buttons, and API spec box
- `CURRENT READINGS ROW`: doughnut gauge cards and numeric stat layout
- `AREA CHART CARDS`: chart panel layout, time-range buttons, and empty-state overlay
- `FOOTER / STATUS BAR`: summary strip styling
- `SCROLLBAR`: custom scrollbar appearance
- `RESPONSIVE`: breakpoints for smaller screens

## HTML content organization

### Header

- `.header.glass`: top panel with logo, title, status indicator, and settings toggle button
- `.status-badge`: live/demo/error indicator with a small dot and text
- `#settingsBtn`: opens or closes the settings panel

### Settings panel

- `.settings-wrap` and `.settings-inner` contain the configuration UI
- Inputs:
  - `#cUrl`: API base URL
  - `#cPath`: endpoint path
  - `#cLimit`: initial data limit
  - `#cPoll`: polling interval in seconds
  - `#cMax`: max chart points stored
  - `#cDemo`: demo mode toggle
- Buttons:
  - `#applyBtn`: apply settings, restart data flow
  - `#resetBtn`: restore defaults and clear saved config
- `#specBox`: API contract reference for expected JSON shape and polling rules

### Current readings row

- three `.rcard` panels for:
  - temperature (`.tc`)
  - humidity (`.hc`)
  - pH (`.pc`)
- each card contains:
  - a doughnut chart canvas (`#dTemp`, `#dHum`, `#dPh`)
  - center value display (`#vTemp`, `#vHum`, `#vPh`)
  - min/avg/max stat values

### Area charts

- three `.chart-card` panels for temperature, humidity, and pH
- each card has:
  - chart title and subtitle
  - buttons for time ranges: `1H`, `6H`, `24H`, `ALL`
  - area chart canvas (`#aTemp`, `#aHum`, `#aPh`)
  - empty-state overlay (`#eTemp`, `#eHum`, `#ePh`)

### Footer / Status bar

- `.statusbar.glass` shows:
  - last update time (`#fTime`)
  - number of readings stored (`#fCount`)
  - latest reading ID (`#fId`)
  - current poll interval (`#fPoll`)

## JavaScript organization

The dashboard logic is separated into labeled sections:

### 1. Constants and state

- `DEFAULTS`: default configuration values
- `SENSORS`: sensor metadata for three sensors, including keys, labels, units, colors, and ranges
- `S`: runtime state object containing configuration, stored readings, last received ID, poll timer, demo clock, and chart instances

### 2. Settings persistence

- `loadCfg()`: reads saved config from `localStorage` under `sf_cfg`
- `saveCfg()`: writes current config to `localStorage`
- `pushToUI()`: populates settings inputs from `S.cfg`
- `pullFromUI()`: reads values back from inputs and validates them

### 3. Demo data generator

- `demoReadings(count)`: creates synthetic readings with sine-wave variations for temperature, humidity, and pH
- Advances the demo clock by 30 seconds per generated reading
- Used when demo mode is enabled instead of calling a real API

### 4. API layer

- `apiGet(url)`: wraps `fetch` with an 8-second timeout and error handling
- `fetchInitial()`: loads initial data on startup
  - if demo mode is enabled, generates synthetic history
  - otherwise calls the API with `?limit=` and ingests returned rows
  - updates status text and starts polling
- `fetchUpdates()`: polls for new data after the highest ID using `?after_id=` and ingests new rows

### 5. Data layer

- `ingest(newRows)`: appends new readings, updates `S.lastId`, trims stored readings to `MAX_POINTS`, renders charts, and updates footer
- `rangeFilter(rows, range)`: filters history for the selected chart range (`1h`, `6h`, `24h`, or `all`)
- `triStats(arr)`: computes min, average, and max values

### 6. Chart builders

- `buildDonut(canvasId, sensor)`: initializes a Chart.js doughnut gauge with a 270° arc
- `buildArea(canvasId, sensor)`: initializes a Chart.js line chart for time-series data with custom tooltip formatting

### 7. Render

- `renderAll()`: updates:
  - area chart labels and datasets for each sensor
  - doughnut gauge values for the latest reading
  - numeric readouts and pulse animation
  - min/avg/max values across stored data
  - empty state overlays when insufficient data is available

### 8. Status and footer

- `setStatus(type, text)`: updates the header status badge state and text
- `updateFooter()`: refreshes footer values for time, reading count, and latest ID

### 9. Utilities

- `cap(s)`: capitalizes sensor keys
- `fmtFull(iso)`: formats timestamps for tooltips
- `fmtTick(iso)`: formats x-axis labels on charts

### 10. Initialization

- Runs on `DOMContentLoaded`
- Loads saved config and initializes UI
- Builds all Chart.js instances for donut and area charts
- Calls `fetchInitial()` to populate data
- Wires event handlers for:
  - opening/closing the settings panel
  - keyboard shortcut `S`
  - applying settings and restarting
  - resetting defaults
  - switching chart time ranges

## How the file works at runtime

1. User opens `dashboard.html` in a browser.
2. The script loads saved settings from `localStorage` or falls back to defaults.
3. Chart.js instances are created for three donuts and three area charts.
4. The dashboard fetches data:
   - from the demo generator when demo mode is enabled
   - or from a configured API endpoint when demo mode is disabled
5. New readings are ingested, stored in `S.readings`, and trimmed to the maximum chart length.
6. The UI updates charts, gauge values, min/avg/max stats, and footer metadata.
7. The dashboard polls every `POLL_INTERVAL` seconds for incremental updates.

## Notes

- The file is intentionally self-contained with no external JavaScript aside from Chart.js.
- The API expectations are documented in the settings panel and assume ascending `id` order.
- The settings panel is collapsible and persisted across page reloads.
- `Apply & Restart` clears current readings and reloads the data flow from the beginning.

## Useful IDs and classes

- `#settingsBtn`, `#settingsWrap`, `#applyBtn`, `#resetBtn`
- `#cUrl`, `#cPath`, `#cLimit`, `#cPoll`, `#cMax`, `#cDemo`
- `#dTemp`, `#dHum`, `#dPh` for donuts
- `#aTemp`, `#aHum`, `#aPh` for area charts
- `#vTemp`, `#vHum`, `#vPh` for current values
- `#nTemp`, `#aTemp`, `#xTemp` etc. for stats
- `#eTemp`, `#eHum`, `#ePh` for no-data placeholders
- `#fTime`, `#fCount`, `#fId`, `#fPoll`

## API GET format and endpoints

The dashboard expects two GET requests when demo mode is disabled:

1. Initial data load
   - URL: `{API_BASE_URL}{API_PATH}?limit={INITIAL_LIMIT}`
   - Purpose: fetch the first batch of readings on startup

2. Polling updates
   - URL: `{API_BASE_URL}{API_PATH}?after_id={last known id}`
   - Purpose: fetch only new readings after the latest received ID

### Expected JSON response shape

The API response must be a JSON object with this structure:

```json
{
  "status": "ok",
  "data": {
    "readings": [
      {
        "id": 1,
        "timestamp": "2024-06-14T10:00:00.000Z",
        "temperature": 23.5,
        "humidity": 65.2,
        "ph": 7.1
      }
    ],
    "latest_id": 100,
    "count": 100
  }
}
```

### GET functions in the dashboard logic

- `apiGet(url)`
  - performs the `fetch` call with an 8-second timeout
  - throws an error for non-OK HTTP status codes

- `fetchInitial()`
  - called once on page load or when `Apply & Restart` is pressed
  - if demo mode is disabled, it requests initial historical data using `?limit=` and ingests the returned readings
  - if demo mode is enabled, it generates synthetic history locally

- `fetchUpdates()`
  - called repeatedly every `POLL_INTERVAL` seconds
  - if demo mode is disabled, it requests new readings using `?after_id=` and ingests any returned rows
  - if demo mode is enabled, it generates one synthetic reading per poll cycle

This addition clarifies the exact API contract and the dashboard functions responsible for GET operations.

This overview should help you understand the dashboard's layout, styling, and runtime behavior.