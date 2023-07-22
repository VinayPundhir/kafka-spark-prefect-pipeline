CREATE TABLE IF NOT EXISTS clickstream_data (
            row_key INTEGER PRIMARY KEY,
            user_id TEXT,
            timestamp TEXT,
            url TEXT,
            country TEXT,
            city TEXT,
            browser TEXT,
            os TEXT,
            device TEXT
        )