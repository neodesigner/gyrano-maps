# gyrano-maps

Offline map areas for [Gyrano](https://gyrano.neodesigner.com): one PMTiles file per area (zoom 0–15) — Ireland: the six Munster counties; Portugal: the Lisboa and Porto districts — cut from the daily [Protomaps](https://docs.protomaps.com/basemaps/downloads) OpenStreetMap basemap and served by GitHub Pages.

- Areas: `areas.json` — `countries: [{ id, name, areas: [{ id, name, bbox }] }]` (bbox `[west, south, east, north]`) and the max zoom. `index.json` lists `countries` and gives each area its `country`. The build stops before publishing if the site would pass GitHub Pages' 1 GB (all 20 Portuguese areas alone are about 1 GB at zoom 15).
- Region boxes: `regions/<country>.overpass` → `.github/workflows/regions.yml` → branch `regions` (OSM administrative boundaries' bounding boxes).
- Build: `.github/workflows/build.yml` runs monthly, on demand, and when `areas.json` or `build.py` change. It extracts each area with `pmtiles extract`, writes `index.json` and deploys the site. The latest run's log and index go to the `build-log` branch.
- App entry point: `index.json` on the Pages site. Files are named `<id>-<build>.pmtiles`.

## Data and licence

Map data © [OpenStreetMap contributors](https://www.openstreetmap.org/copyright), available under the [Open Database Licence (ODbL)](https://opendatacommons.org/licenses/odbl/). Tiles produced by Protomaps. The `.pmtiles` files on the Pages site are ODbL; the scripts in this repository are MIT.

GitHub Pages is used while Gyrano is a free beta. A commercial release moves the files to other storage; only the index URL in the app's `maps.json` changes.
