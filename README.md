# Sydney Weather CLI

A command-line Python app that fetches real-time hourly weather 
forecasts for Sydney and displays the next 6 hours in a clean format.

## How It Works

Connects to the Open-Meteo API and requests hourly temperature 
and weather data for Sydney using its coordinates. Converts 
timestamps to the Australia/Sydney timezone, filters to the 
next 6 hours from now, and prints the forecast cleanly in the terminal.

## Example Output

```
--- Sydney Weather — Next 6 Hours ---
  02:00 PM  →  21.4°C
  03:00 PM  →  21.1°C
  04:00 PM  →  20.7°C
  05:00 PM  →  20.1°C
  06:00 PM  →  19.8°C
  07:00 PM  →  19.3°C
```

## How to Run

```bash
pip install openmeteo-requests pandas requests-cache retry-requests
python3 main.py
```

## Tech Used

- Python
- Open-Meteo API
- Pandas
- requests-cache
