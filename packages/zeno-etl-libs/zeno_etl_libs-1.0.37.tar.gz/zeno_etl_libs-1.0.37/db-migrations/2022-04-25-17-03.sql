CREATE TABLE IF NOT EXISTS "prod2-generico"."ipc-corrections-rest-cases"
(
	"store-id" BIGINT   ENCODE az64
	,"drug-id" BIGINT   ENCODE az64
	,composition VARCHAR(3000) NOT NULL  ENCODE RAW
	,"original-max" BIGINT   ENCODE az64
	,"avg-ptr" DOUBLE PRECISION   ENCODE RAW
	,"current-inventory" DOUBLE PRECISION   ENCODE RAW
	,"current-ma-3-months" DOUBLE PRECISION   ENCODE RAW
	,"bucket-flag-is-repeatable" BIGINT   ENCODE az64
	,"bucket-flag-total-months-comp-sold" BIGINT   ENCODE az64
	,"quantity-sold-2" DOUBLE PRECISION   ENCODE RAW
	,"quantity-sold-1" DOUBLE PRECISION   ENCODE RAW
	,"quantity-sold-0" DOUBLE PRECISION   ENCODE RAW
	,"current-bucket" VARCHAR(256)   ENCODE lzo
	,"current-flag-ma-less-than-2" BIGINT   ENCODE az64
	,"selling-probability" DOUBLE PRECISION   ENCODE RAW
	,"cumm-prob" DOUBLE PRECISION   ENCODE RAW
	,"corrected-max" DOUBLE PRECISION   ENCODE RAW
	,"inv-impact" DOUBLE PRECISION   ENCODE RAW
	,"max-impact" DOUBLE PRECISION   ENCODE RAW
	,"created-at" TIMESTAMP WITHOUT TIME ZONE   ENCODE az64
	,"created-by" VARCHAR(255)   ENCODE lzo
	,"updated-at" TIMESTAMP WITHOUT TIME ZONE   ENCODE az64
	,"updated-by" VARCHAR(255)   ENCODE lzo
);

ALTER TABLE "prod2-generico"."ipc-corrections-rest-cases" owner to "admin";