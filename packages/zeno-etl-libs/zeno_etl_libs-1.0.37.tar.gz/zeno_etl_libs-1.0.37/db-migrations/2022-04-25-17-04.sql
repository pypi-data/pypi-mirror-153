CREATE TABLE IF NOT EXISTS "prod2-generico"."ipc-corrections-111-cases"
(
	"store-id" BIGINT   ENCODE az64
	,"drug-id" BIGINT   ENCODE az64
	,composition VARCHAR(3000) NOT NULL  ENCODE RAW
	,"avg-ptr" DOUBLE PRECISION   ENCODE RAW
	,"current-inventory" DOUBLE PRECISION   ENCODE RAW
	,"quantity-sold-0" DOUBLE PRECISION   ENCODE RAW
	,"quantity-sold-1" DOUBLE PRECISION   ENCODE RAW
	,"quantity-sold-2" DOUBLE PRECISION   ENCODE RAW
	,"original-max" BIGINT   ENCODE az64
	,"ma-3-months" DOUBLE PRECISION   ENCODE RAW
	,"corrected-max" DOUBLE PRECISION   ENCODE RAW
	,"inv-impact" DOUBLE PRECISION   ENCODE RAW
	,"max-impact" DOUBLE PRECISION   ENCODE RAW
	,"created-at" TIMESTAMP WITHOUT TIME ZONE   ENCODE az64
	,"created-by" VARCHAR(255)   ENCODE lzo
	,"updated-at" TIMESTAMP WITHOUT TIME ZONE   ENCODE az64
	,"updated-by" VARCHAR(255)   ENCODE lzo
);

ALTER TABLE "prod2-generico"."ipc-corrections-111-cases" owner to "admin";