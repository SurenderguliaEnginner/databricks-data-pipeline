# Real-Time Crypto Data Pipeline

An end-to-end data engineering pipeline built to learn and demonstrate real-time data ingestion, orchestration, and distributed processing — combining Kafka, PostgreSQL, Airflow, and Spark (via Databricks).

## Architecture

CoinGecko API (live crypto prices)
↓
Kafka Producer (fetches every 10s)
↓
Kafka Broker (crypto-prices topic)
↓
Kafka Consumer (validates, inserts)
↓
PostgreSQL (raw_prices table)
↓
┌───┴───┐
↓ ↓
Airflow CSV Export
(daily ↓
summary) Databricks
(Bronze/Silver/Gold)

## What This Project Does

- Streams live cryptocurrency prices (Bitcoin, Ethereum) from the CoinGecko API in real time using Apache Kafka
- Stores validated data in PostgreSQL
- Uses Apache Airflow to orchestrate daily summary calculations (average, high, low, volatility per coin)
- Exports data for processing in Databricks using Apache Spark, following a Bronze/Silver/Gold architecture

## Tech Stack

- **Streaming:** Apache Kafka
- **Database:** PostgreSQL
- **Orchestration:** Apache Airflow (Dockerized)
- **Distributed Processing:** Apache Spark (Databricks)
- **Language:** Python

## Key Challenges Solved

- Debugged cross-network connectivity between WSL2 (Linux) and Windows-hosted PostgreSQL — involved IP addressing, `pg_hba.conf`, `postgresql.conf`, and Windows Firewall configuration
- Handled missing/null values from unreliable API responses without crashing the pipeline
- Built idempotent, retry-safe Airflow tasks

## Setup

1. Clone this repo
2. Create a `.env` file with `DB_PASSWORD=your_postgres_password`
3. Run `docker-compose up -d` to start Airflow
4. Install dependencies: `pip install kafka-python psycopg2-binary requests`
5. Start the producer: `python3 price_producer.py`
6. Start the consumer: `python3 price_consumer_pg.py`

## Status

Actively developed — next steps include full cloud deployment (GCP) and automated JDBC connection between PostgreSQL and Databricks.
