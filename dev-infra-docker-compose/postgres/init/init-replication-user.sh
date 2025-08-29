#!/bin/bash

set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    ALTER USER $POSTGRES_USER WITH REPLICATION;

    DO \$\$
    BEGIN
        IF NOT EXISTS (
            SELECT 1 FROM pg_replication_slots 
            WHERE slot_name = 'eventuate_slot_' || replace(current_database(), '-', '_')
        ) THEN
            PERFORM pg_create_logical_replication_slot('eventuate_slot_' || replace(current_database(), '-', '_'), 'wal2json');
        END IF;
    END
    \$\$;
EOSQL
