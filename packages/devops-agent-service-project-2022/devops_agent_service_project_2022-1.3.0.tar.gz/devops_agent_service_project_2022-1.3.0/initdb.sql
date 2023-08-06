CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
	password VARCHAR(255) NOT NULL,
	email VARCHAR(255) NOT NULL,
    first_name VARCHAR(255) NOT NULL,
	last_name VARCHAR(255) NOT NULL,
	role VARCHAR(255) NOT NULL
);

insert into users (id, username, password, email, first_name, last_name, role) values (1, 'a1', '$2b$12$GUi.8kgtMV.ksqVjf9vnweSag/V/Q.hMtTsL2gcp8IyWXws7Ue89.', 'a1', 'a1', 'a1', 'admin') ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS company (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
	description VARCHAR(255) NOT NULL,
	job_positions VARCHAR(255),
	address VARCHAR(255) NOT NULL,
    city VARCHAR(255) NOT NULL,
	owner_id VARCHAR(255) NOT NULL,
	active BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS review (
    id SERIAL PRIMARY KEY,
    text_comment VARCHAR(255) NOT NULL,
	payment_review VARCHAR(255) NOT NULL,
	interview_review VARCHAR(255) NOT NULL,
	company_id VARCHAR(255) NOT NULL,
	author_id VARCHAR(255) NOT NULL
);
