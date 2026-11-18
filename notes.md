# Bus Arrival Prediction — Progress Notes

## Done
- Project set up with `uv` (polars, sqlalchemy, psycopg, pandas, python-dotenv, gtfs-realtime-bindings)
- Static GTFS feed downloaded into `path/` (gitignored, since `stop_times.txt` is 155 MB)
- Postgres 17 runs in Docker via `docker-compose.yml`
  - Credentials live in `.env`
  - Data persists in the `pgdata` volume
  - `sql/` runs automatically on first startup (only when the volume is empty)
- Schema designed in `sql/schema.sql`: `routes`, `stops`, `trips`, `stop_times`
- Loader script: `scripts/load_static_GTFS_feed.py`
  - Loads only the routes in `interested_routes.txt`: 007, 054, 108, 113
  - Load order: routes → stops → trips → stop_times (foreign keys)

## Next
- Add an `observations` table for realtime data
- Write `scripts/poll_realtime.py` to poll GTFS-Realtime TripUpdates every ~30 s
- Join observations against `stop_times` to get scheduled vs. actual times (the training data)

## Gotchas
- Read GTFS with `infer_schema=False` (IDs look numeric but aren't)
- GTFS times can exceed 24:00, so they're stored as `INTERVAL`
- The schema uses `stop_long`, but GTFS uses `stop_lon` (aliased in the loader)
- Re-running the loader gives duplicate-key errors, so reset with `docker compose down -v`

## Commands
- `docker compose up -d` / `docker compose stop` — start / stop the DB
- `docker compose down -v` — wipe the DB and re-run the schema on next start
- `docker exec -it transit-db psql -U bus -d transit` — open a SQL shell
- `uv run scripts/load_static_GTFS_feed.py` — load static data
