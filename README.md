# DoctorMoon
An analysis system for scientific publications using the principle of self-citation. 
Currently based on the S2 corpus: https://labs.semanticscholar.org/corpus/

## TLDR
Scientific papers can be classified into concept cycles by starting from a single paper, exploring all of its incoming and outgoing references, 
then processing those papers' in-out references for some N depth, and then pruning out any papers the original authors didn't use in their own later papers.

This creates a connected cycle of important papers related to the starting paper, as shown by in the original authors' citation behavior.

## Using
1. Download and extract the S2 Open Research Corpus from Semantic Scholar. 
1. Download the sqlite database I've created for that data, from here: s3://drewbuschhorn-s2-corpus/id_positions.zip (contact for access, currently). The data is in format: ```BEGIN TRANSACTION;
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
COMMIT;``` where start_position_byte and start_position_file are the file path and starting byte for the JSON entry for a given paper within the various S2 corpus extracted files. For example: ```"185"	"7e58b926bbbc122edeccb7cb4f7f68ca11480698"	"0"	"D:\corpus\s2-corpus-00"	"0"	"0"``` to look up entry ```{"entities":["Amphibians","Anura","Apache Gora","Aquatic ecosystem","Diazooxonorleucine","Habitat","Human body","Natural Selection","Natural Springs","Population","Rana esculenta","Rana temporaria"],"journalVolume":"33","journalPages":"446-451","pmid":"","year":2004,"outCitations":[],"s2Url":"https://semanticscholar.org/paper/7e58b926bbbc122edeccb7cb4f7f68ca11480698","s2PdfUrl":"","id":"7e58b926bbbc122edeccb7cb4f7f68ca11480698","authors":[{"name":"M. V. Ushakov","ids":["2506899"]}],"journalName":"Russian Journal of Ecology","paperAbstract":"The marsh frog ... ions.","inCitations":[],"pdfUrls":[],"title":"Ecomorphological Characteristics of the Marsh Frog Rana ridibunda from the Galich'ya Gora Nature Reserve","doi":"10.1023/A:1020916001559","sources":[],"doiUrl":"https://doi.org/10.1023/A:1020916001559","venue":"Russian Journal of Ecology"}```
1. Install requirements.txt using pip.
1. In publication_timeline\src run `python main.py`.
1. When prompted, give the starting paper s2 id (like 7e58b926bbbc122edeccb7cb4f7f68ca11480698) and allow the program to run. This may take some time.
1. On completion a localfile url will be provided to the example_map.html file with a GET parameter identifying a json file in the processed_data directory. Go to that url and your map should be displayed like the example below.

Screenshots:

