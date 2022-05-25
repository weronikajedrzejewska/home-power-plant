# home-power-plant
The aim of the project is to fetch data about energy production from two sources: Tauron and SMA inverter to compare it further in Grafana dashboard.
To achieve that I used two unofficial APIs elicznik and sma_sunnyboy. Data from both sources are then stored in Postgres (Elephant SQL) as two seperate tables.
In Grafana I've prepared dahsboard presenting and comparing measurments from both. For conviniece I've prepared docker compose with Grafana and Postgres.
