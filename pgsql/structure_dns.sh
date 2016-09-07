#!/bin/bash

PGSQL="/soft/PG9.4.5/bin/psql"
export PGPASSWORD=dnsadmin
PGENV="sudo -u postgres $PGSQL -h 127.0.0.1 -p5494 -Udnsadmin -ddnsadmin"

#$PGENV <<THE_VIEW
#CREATE TABLE	record_zones(
#	name		VARCHAR(200)	NOT NULL,
#	zid			BIGINT	PRIMARY KEY,
#	zgid		BIGINT 	NOT NULL,
#	description	VARCHAR(99)
#);
#THE_VIEW

$PGENV <<THE_VIEW
CREATE TABLE	ptr_zones(
	ptrid		BIGINT		PRIMARY KEY,
	name		VARCHAR(200)	NOT NULL,
	zone		varchar(200),
	description	VARCHAR(99)
);
THE_VIEW

#$PGENV <<THE_VIEW
#CREATE TABLE	ptr_zones(
#	ptrid		BIGINT		PRIMARY KEY,
#	name		VARCHAR(200)	NOT NULL,
#	zone		varchar(200),
#	description	VARCHAR(99)
#);
#THE_VIEW

#$PGENV <<THE_VIEW
#CREATE TABLE	record_groups(
#	name		VARCHAR(200)	NOT NULL,
#	rgid		BIGINT		PRIMARY KEY,
#	description	VARCHAR(99)
#);
#THE_VIEW

#$PGENV <<THE_VIEW
#CREATE TABLE	zone_groups(
#	name		VARCHAR(200)	NOT NULL,
#	zgid		BIGINT		PRIMARY KEY,
#	description	VARCHAR(99)
#);
#THE_VIEW


#$PGENV <<THE_VIEW
#CREATE TABLE	dnspod_info(
#	account_id			BIGINT			PRIMARY KEY,
#	account_name		VARCHAR(200)	NOT NULL,
#	format				VARCHAR(200)	NOT NULL,
#	ttl					VARCHAR(200)	NOT NULL,
#	line				VARCHAR(200)	NOT NULL,
#	token_id			VARCHAR(200),
#	token				VARCHAR(200),
#	description	VARCHAR(99)
#);
#THE_VIEW


#$PGENV <<THE_VIEW
#CREATE TABLE	record_list(
#	rid		BIGINT			PRIMARY KEY,
#	r_name	VARCHAR(200)	NOT NULL,
#	r_type	VARCHAR(50)		NOT NULL,
#	r_value	VARCHAR(200)	NOT NULL,
#	r_ttl	NUMERIC(39)		NOT NULL,
#	weight	NUMERIC(39),
#	mx_priority	NUMERIC(39),
#	r_line		VARCHAR(200),
#	r_status	BOOLEAN		NOT NULL,
#	zid			BIGINT			NOT NULL,
#	rgid		BIGINT		NOT NULL,
#	description	VARCHAR(200)
#);
#THE_VIEW

#$PGENV <<THE_VIEW
#CREATE	TABLE	changelog(
#	change_id	BIGINT			NOT NULL,
#	update_act	VARCHAR(200),
#	detail		VARCHAR(500),
#	option_at	TIMESTAMP
#);
#THE_VIEW

#tables='changelog record_groups record_list record_zones zone_groups dnspod_info'
#for table in $tables
#do
#	$PGENV <<THE_VIEW
#	create sequence $table_seq increment by 2 minvalue 1 no maxvalue start with 1;
#THE_VIEW
#done
