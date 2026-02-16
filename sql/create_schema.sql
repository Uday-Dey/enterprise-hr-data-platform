-- ============================
-- RAW HISTORY TABLE (Append Only)
-- ============================

CREATE TABLE IF NOT EXISTS employee_raw_history (
    employee_id              VARCHAR,
    first_name               VARCHAR,
    last_name                VARCHAR,
    gender                   VARCHAR,
    department               VARCHAR,
    salary                   DOUBLE,
    location                 VARCHAR,
    performance_score        INTEGER,
    hire_date                DATE,
    employee_status          VARCHAR,

    source_updated_timestamp TIMESTAMP,
    ingestion_timestamp      TIMESTAMP,
    file_id                  VARCHAR,
    lineage_id               VARCHAR
);

-- ============================
-- CURRENT CURATED TABLE
-- ============================

CREATE TABLE IF NOT EXISTS employee_current (
    employee_id              VARCHAR PRIMARY KEY,
    first_name               VARCHAR,
    last_name                VARCHAR,
    gender                   VARCHAR,
    department               VARCHAR,
    salary                   DOUBLE,
    location                 VARCHAR,
    performance_score        INTEGER,
    hire_date                DATE,
    employee_status          VARCHAR,

    created_timestamp        TIMESTAMP,
    last_updated_timestamp   TIMESTAMP,
    file_id                  VARCHAR,
    lineage_id               VARCHAR
);

-- ============================
-- METADATA TRACKER TABLE
-- ============================

CREATE TABLE IF NOT EXISTS metadata_pipeline_tracker (
    pipeline_name                VARCHAR,
    last_processed_timestamp     TIMESTAMP,
    last_run_timestamp           TIMESTAMP,
    records_loaded               INTEGER,
    lineage_id                   VARCHAR
);
