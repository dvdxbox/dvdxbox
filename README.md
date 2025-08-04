# dvdxbox

This repository includes a simple avatar script that reports the current
weather and local time for a given location. It uses the free [Open-Meteo](https://open-meteo.com/) API to
fetch coordinates and weather, and Python's standard library to determine the
local time.

## Usage

```bash
python avatar.py <location>
```

Example:

```bash
python avatar.py Tokyo
```

The command outputs the temperature, wind speed, and local time for the
specified city.

> **Note**: Running the script requires internet access to contact the
> Open-Meteo API. If a network proxy blocks the request, the script will
> report an error.
