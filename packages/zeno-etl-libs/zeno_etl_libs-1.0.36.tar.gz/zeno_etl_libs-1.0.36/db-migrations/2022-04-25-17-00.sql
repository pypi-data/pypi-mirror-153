CREATE TABLE IF NOT EXISTS "prod2-generico"."distributor-features-dc"
(
	"dc-id" DOUBLE PRECISION   ENCODE RAW
	,"dc-name" VARCHAR(256)   ENCODE lzo
	,"distributor-id" BIGINT   ENCODE az64
	,"distributor-name" VARCHAR(256)   ENCODE lzo
	,"distributor-type" VARCHAR(256)   ENCODE lzo
	,"is-small" INTEGER   ENCODE az64
	,"drug-id" BIGINT   ENCODE az64
	,"drug-name" VARCHAR(256)   ENCODE lzo
	,"drug-type" VARCHAR(256)   ENCODE lzo
	,"lead-time" DOUBLE PRECISION   ENCODE RAW
	,margin DOUBLE PRECISION   ENCODE RAW
	,"total-lost" INTEGER   ENCODE az64
	,"total-requests" BIGINT   ENCODE az64
	,"bounce-rate" DOUBLE PRECISION   ENCODE RAW
	,ff DOUBLE PRECISION   ENCODE RAW
	,"lost-recency" DOUBLE PRECISION   ENCODE RAW
	,"success-recency" DOUBLE PRECISION   ENCODE RAW
	,performance DOUBLE PRECISION   ENCODE RAW
	,rank INTEGER   ENCODE az64
	,"final-dist-1" DOUBLE PRECISION   ENCODE RAW
	,"final-dist-2" DOUBLE PRECISION   ENCODE RAW
	,"final-dist-3" DOUBLE PRECISION   ENCODE RAW
	,"dc-drug-type-level-dist-1" DOUBLE PRECISION   ENCODE RAW
	,"dc-drug-type-level-dist-2" DOUBLE PRECISION   ENCODE RAW
	,"dc-drug-type-level-dist-3" DOUBLE PRECISION   ENCODE RAW
	,"enterprise-drug-type-level-dist-1" DOUBLE PRECISION   ENCODE RAW
	,"enterprise-drug-type-level-dist-2" DOUBLE PRECISION   ENCODE RAW
	,"enterprise-drug-type-level-dist-3" DOUBLE PRECISION   ENCODE RAW
	,"volume-fraction" VARCHAR(256)   ENCODE lzo
	,"request-type" VARCHAR(256)   ENCODE lzo
	,"reset-date" DATE NOT NULL  ENCODE az64
	,"created-at" TIMESTAMP WITHOUT TIME ZONE   ENCODE az64
	,"created-by" VARCHAR(256)   ENCODE lzo
);

ALTER TABLE "prod2-generico"."distributor-features-dc" owner to "admin";

