-- migrate:up
CREATE TABLE feature_flags(
    name VARCHAR(256) NOT NULL PRIMARY KEY,
    enabled BOOLEAN DEFAULT FALSE
);
-- migrate:down
DROP TABLE feature_flags;
