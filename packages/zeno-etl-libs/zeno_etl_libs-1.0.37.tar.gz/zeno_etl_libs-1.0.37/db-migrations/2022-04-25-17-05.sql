CREATE TABLE IF NOT EXISTS "prod2-generico"."ipc-corrections-probability-matrix"
(
	"historical-bucket" VARCHAR(256)   ENCODE lzo
	,"selling-probability" DOUBLE PRECISION   ENCODE RAW
	,"cumm-prob" DOUBLE PRECISION   ENCODE RAW
	,"historical-flag-ma-less-than-2" BIGINT   ENCODE az64
	,"created-at" TIMESTAMP WITHOUT TIME ZONE   ENCODE az64
	,"created-by" VARCHAR(255)   ENCODE lzo
	,"updated-at" TIMESTAMP WITHOUT TIME ZONE   ENCODE az64
	,"updated-by" VARCHAR(255)   ENCODE lzo
);

ALTER TABLE "prod2-generico"."ipc-corrections-probability-matrix" owner to "admin";