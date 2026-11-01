# Regions

Each `<country>.overpass` is an Overpass QL query for that country's administrative areas
(with their bounding boxes). `.github/workflows/regions.yml` runs them when they change and
pushes a compact `<country>.json` (id, names, admin level, bbox) to the `regions` branch.
Those boxes are copied, padded a little, into `areas.json`. Data © OpenStreetMap
contributors (ODbL).
