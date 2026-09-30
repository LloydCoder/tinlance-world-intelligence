# Phase 6 — Geospatial Intelligence
Spatial state uses PostGIS geometry with SRID 4326 at the canonical API boundary and GiST indexes.
Containment/intersection uses index-aware predicates; proximity uses ST_DWithin rather than
ST_Distance for filtering. Temporal validity is stored alongside geometry so spatial-temporal
queries can constrain both dimensions. OGC API Features and Moving Features inform external
interoperability. citeturn0search1turn0search8 PostGIS documents GiST and index-aware
ST_DWithin/ST_Intersects predicates. citeturn2search0turn2search1
