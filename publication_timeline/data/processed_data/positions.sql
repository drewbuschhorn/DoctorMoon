BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS `positions` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`uuid`	TEXT NOT NULL UNIQUE,
	`start_position_byte`	INTEGER NOT NULL,
	`start_position_file`	TEXT NOT NULL,
	`in_citation_count`	INTEGER,
	`out_citation_count`	INTEGER
);
CREATE UNIQUE INDEX IF NOT EXISTS `uuid` ON `positions` (
	`uuid`
);
CREATE UNIQUE INDEX IF NOT EXISTS `position` ON `positions` (
	`start_position_byte`,
	`start_position_file`
);
CREATE INDEX IF NOT EXISTS `outcitation` ON `positions` (
	`out_citation_count`
);
CREATE INDEX IF NOT EXISTS `incitation` ON `positions` (
	`in_citation_count`
);
COMMIT;
