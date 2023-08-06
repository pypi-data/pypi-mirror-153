CREATE TABLE IF NOT EXISTS message (
    id SERIAL PRIMARY KEY,
    date TIMESTAMP NOT NULL,
    content TEXT NOT NULL,
	sender_id VARCHAR(255) NOT NULL,
	recipient_id VARCHAR(255) NOT NULL,
	room varchar(255) NOT NULL
);
