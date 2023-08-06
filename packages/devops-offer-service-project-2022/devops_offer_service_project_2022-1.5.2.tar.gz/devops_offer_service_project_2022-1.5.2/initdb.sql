CREATE TABLE IF NOT EXISTS offers (
    id SERIAL PRIMARY KEY,
    position VARCHAR(255) NOT NULL,
    requirements VARCHAR(255) NOT NULL,
    description VARCHAR(255) NOT NULL,
    agent_application_link VARCHAR(255) NOT NULL
)
