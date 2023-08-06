CREATE TABLE IF NOT EXISTS "prod2-generico"."distributor-ranking-preference"
(
	"dc-id" BIGINT   ENCODE az64
	,"franchisee-id" BIGINT   ENCODE az64
	,"store-id" BIGINT   ENCODE az64
	,"distributor-id" BIGINT NOT NULL  ENCODE az64
	,"distributor-preference" BIGINT NOT NULL  ENCODE az64
	,"drug-id" BIGINT NOT NULL  ENCODE az64
	,"start-date" DATE NOT NULL  ENCODE az64
	,"end-date" DATE NOT NULL  ENCODE az64
	,"is-active" BIGINT NOT NULL  ENCODE az64
	,"created-at" TIMESTAMP WITHOUT TIME ZONE   ENCODE az64
	,"created-by" VARCHAR(255)   ENCODE lzo
	,"updated-at" TIMESTAMP WITHOUT TIME ZONE   ENCODE az64
	,"updated-by" VARCHAR(255)   ENCODE lzo
);

ALTER TABLE "prod2-generico"."distributor-ranking-preference" owner to "admin";