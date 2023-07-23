# Project Structure

 ```
    ├── apis
    │   └── elastic.py
    |
    ├── broker
    │   ├── consumers
    │   │   └── save_click_data_into_db.py
    │   └── producers
    │       └── click_data.py
    |
    ├── certs
    │   └── http_ca.crt
    |
    ├── clickstream_data.db
    |
    ├── config.py
    |
    ├── database
    │   └── sqlite.py
    |
    ├── mappings
    │   └── elastic
    │       └── click_events.py
    |
    ├── processes
    │   ├── elastic.yml
    │   └── kafka.yml
    |
    ├── requirements.txt
    |
    ├── sql
    │   ├── create_table_clickstream_data.sql
    │   └── insert_into_clickstream_data.sql
    |
    └── transformations
        └── aggregate_and_index.py
 ```

## Usage
Before you begin, ensure you have the following installed on your system:
Docker (Docker Engine and Docker Compose)

### Create virtual env and activate

```
    python3.11 -m venv venv
    source venv/bin/activate
```

### Install Dependencies

```
    pip install -r requirements.txt
```

for elastic search connection set ELASTIC_USERNAME, ELASTIC_PASSWORD in env.
### Running kafka and elastic search instances with Docker Compose ( Optional )
- Start the Kafka service:
```
    docker-compose -f processes/kafka.yml up -d
```
This will start the Kafka service in detached mode.

- Start the Elasticsearch service:
```
    docker-compose -f processes/elastic.yml up -d
```
This will start the Elasticsearch service in detached mode.

### Setup Configuration
Open the ```config.py``` file in the root directory of the project.
Update the configuration settings according to your environment and requirements. This may include API endpoints, database connection settings, and any other necessary configurations.

### Deploy the pipeline using prefect:
```
    python pipeline/main.py
```
This will create two flows for producer and consumer respectively and one flow for transformation.

- use ``` prefect server start``` command to run prefect ui. 
- use ```prefect agent start -q 'default'``` to start a prefect agent.
- control the number of producers and consumers using UI.
- Transfomation ( aggergate_and_index ) will be scheduled for periodic runs