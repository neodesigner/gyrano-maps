# gyrano-maps

Offline map areas for [Gyrano](https://gyrano.neodesigner.com): one PMTiles file per Munster county (zoom 0–15), cut from the daily [Protomaps](https://docs.protomaps.com/basemaps/downloads) OpenStreetMap basemap and served by GitHub Pages.

- Areas: `areas.json` (id, name, bbox `[west, south, east, north]`, max zoom).
- Build: `.github/workflows/build.yml` runs monthly, on demand, and when `areas.json` or `build.py` change. It extracts each area with `pmtiles extract`, writes `index.json` and deploys the site. The latest run's log and index go to the `build-log` branch.
- App entry point: `index.json` on the Pages site. Files are named `<id>-<build>.pmtiles`.

## Data and licence

Map data © [OpenStreetMap contributors](https://www.openstreetmap.org/copyright), available under the [Open Database Licence (ODbL)](https://opendatacommons.org/licenses/odbl/). Tiles produced by Protomaps. The `.pmtiles` files on the Pages site are ODbL; the scripts in this repository are MIT.

GitHub Pages is used while Gyrano is a free beta. A commercial release moves the files to other storage; only the index URL in the app's `maps.json` changes.
