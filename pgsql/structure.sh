#!/bin/bash

PGSQL="/soft/PG9.4.5/bin/psql"
export PGPASSWORD=dev_storage
PGENV="sudo -u postgres $PGSQL -h 127.0.0.1 -p5494 -Udev_storage -ddevice_storage"

$PGENV <<THE_VIEW
CREATE TABLE	device_group(
	id		SERIAL		PRIMARY KEY,
	name		VARCHAR(200)	NOT NULL,
	description	VARCHAR(99)
);
THE_VIEW


$PGENV <<THE_VIEW
CREATE TABLE	device_info(
	id		SERIAL		PRIMARY KEY,
	device_name	VARCHAR(200)	NOT NULL,
	model		VARCHAR(99),
	group_id	NUMERIC,
	status		VARCHAR(39),
	created_at	TIMESTAMP,
	updated_at	TIMESTAMP,
	deleted_at	TIMESTAMP,
	description	VARCHAR(200)
);
THE_VIEW

$PGENV <<THE_VIEW
CREATE	TABLE	update_info(
	device_id	NUMERIC		NOT NULL,
	update_act	VARCHAR(200),
	detail		VARCHAR(200),
	updated_at	TIMESTAMP
);
THE_VIEW
