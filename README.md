# Data Flow
![Screenshot from 2023-07-23 20-36-15](https://github.com/VinayPundhir/kafka-spark-prefect-pipeline/assets/51248042/b005b445-4f97-4de2-b34e-e9ac11285ad7)





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


## Approach

- Lets say there is one producer writing data to kafka topic ```clickstream```
- Here in ```broker/producer/click_data.py``` is a producer that will generate fake click stream data and write in ```clickstream topic```.
- Corresponding ```broker/consumers/save_click_data_into_db.py``` is a consumer that will write data into db by continuesly reading the stream from ```clickstream topic```.
- Prefect Flow will help controlling the number of consumers independently depending upon the size of partition.
- Consumer uses ```database``` to write data back in db. ```database``` implements different db connection and operations logic. Here we have used ```sqlite```. In production it can be replaced with any concurrent db like Mysql.
- Every db implementation uses corresponding sql given in ```sql/query_name.sql``` so that same sql can be used with different databases.
- Transformation ```transformation/aggreagate_and_index.py``` contains business logic to transform that data and push the result back to elastic index. It uses ```apis/elastic.py``` to create connection with elastic server and also implements the logic to create index and push data into the index.
- Project uses destructing from spark df to pandas df to push data row by row. As the data size increase we can use```elastic-hadoop``` connector to write in distributed fashion.
- For creating the index ```apis/elastic.py``` uses ```mapping/elastic/click_events.py``` to create new index in elastic.
- Transformation are scheduled by default when deploy the pipeline using ```pipeline/main.py```. Schedules can also be changed using prefect UI.


#### Note : 
- Replace the file ```certs/http_ca.crt``` for elastic accordingly.