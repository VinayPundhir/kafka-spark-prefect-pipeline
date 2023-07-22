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

# Project Setup Guide
This guide will help you set up the project and run the processes using Docker Compose. The project contains various modules and components that interact with APIs, databases, and messaging systems to handle clickstream data.

### Usage
Before you begin, ensure you have the following installed on your system:
Docker (Docker Engine and Docker Compose)

### Step 1: Clone the Repository

```
    git clone https://github.com/your-username/your-project.git
    cd your-project
```

### Step 2: Install Dependencies

```
    pip install -r requirements.txt
```

### Step 3: Setup Configuration
Open the **config.py** file in the root directory of the project.
Update the configuration settings according to your environment and requirements. This may include API endpoints, database connection settings, and any other necessary configurations.

### Step 4: Running the Processes with Docker Compose ( Optional )
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


### step 5: Run the producer that creates clickstream data:
```
    python broker/producers/click_data.py
```

### step 6: Run the consumer that consumes data from Kafka and saves it into the SQLite database:

```
    python broker/consumers/save_click_data_into_db.py
```

### step 7: Run the script for transformations that will aggregate the clickstream data and index the results in Elasticsearch:
```
    python transformations/aggregate_and_index.py
```