# Real-Time Fraud Detection Streaming Pipeline

This project simulates a real-time fraud detection system using Apache Kafka.

Fake transactions are generated and streamed through Kafka. A fraud detection
service processes the events and flags suspicious transactions. Fraud alerts
are then written to PostgreSQL.

The entire pipeline is containerized using Docker Compose.

## Architecture

Producer → Kafka (transactions topic) → Fraud Detection Service
→ Kafka (fraud_alerts topic) → Database Writer → PostgreSQL

## Tech Stack

- Python
- Apache Kafka
- PostgreSQL
- Docker
- Docker Compose

## Features

- Real-time transaction streaming
- Fraud detection rule engine
- Kafka-based microservice architecture
- PostgreSQL storage
- Fully containerized pipeline
