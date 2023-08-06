CREATE TABLE IF NOT EXISTS "prod2-generico"."migration-testing"
(
	"patient-id" BIGINT NOT NULL  ENCODE az64
	,"store-id" INTEGER NOT NULL  ENCODE az64
	,"year-bill" INTEGER NOT NULL  ENCODE az64
	,"month-bill" INTEGER NOT NULL  ENCODE az64
	,"bill-date" DATE NOT NULL  ENCODE az64
	,"bill-id" BIGINT NOT NULL  ENCODE az64
	,composition VARCHAR(1000)   ENCODE lzo
	,"drug-id" INTEGER   ENCODE az64
	,"drug-name" VARCHAR(255)   ENCODE lzo
	,"drug-type" VARCHAR(255)   ENCODE lzo
	,"drug-category" VARCHAR(255)   ENCODE lzo
	,"repeatability-index" INTEGER   ENCODE az64
	,"is-repeatable" INTEGER   ENCODE az64
	,"is-generic" INTEGER   ENCODE az64
	,quantity INTEGER   ENCODE az64
	,"interval-per-strip" NUMERIC(17,4)   ENCODE az64
	,"expected-next-interval-drug" NUMERIC(17,4)   ENCODE az64
	,"mean-interval-hist" NUMERIC(17,4)   ENCODE az64
	,"expected-next-interval" NUMERIC(17,4)   ENCODE az64
	,"refill-date" DATE   ENCODE az64
	,"year-refill" INTEGER   ENCODE az64
	,"month-refill" INTEGER   ENCODE az64
	,"refill-relevancy-flag" INTEGER   ENCODE az64
	,"created-at" TIMESTAMP WITHOUT TIME ZONE   ENCODE az64
	,"created-by" VARCHAR(255)   ENCODE lzo
	,"updated-at" TIMESTAMP WITHOUT TIME ZONE   ENCODE az64
	,"updated-by" VARCHAR(255)   ENCODE lzo
)
DISTSTYLE AUTO
;
ALTER TABLE "prod2-generico"."migration-testing" owner to "admin";