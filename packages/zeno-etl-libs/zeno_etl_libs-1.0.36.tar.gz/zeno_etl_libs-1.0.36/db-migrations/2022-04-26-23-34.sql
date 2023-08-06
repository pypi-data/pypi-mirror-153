CREATE TABLE IF NOT EXISTS "prod2-generico"."goodaid-incentive-rate-day"
("drug-id" INTEGER NOT NULL  ENCODE az64
,incentive INTEGER ENCODE az64
, "rate-date" TIMESTAMP WITHOUT TIME ZONE   ENCODE az64
,"created-at" TIMESTAMP WITHOUT TIME ZONE   ENCODE az64
,"created-by" VARCHAR(765) NOT NULL  ENCODE lzo
,"updated-at" TIMESTAMP WITHOUT TIME ZONE   ENCODE az64
,"updated-by" VARCHAR(765)   ENCODE lzo
)
DISTSTYLE AUTO
;