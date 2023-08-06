CREATE TABLE IF NOT EXISTS "prod2-generico"."diagnostic-visibility"
(
	date DATE   ENCODE az64
	,"redemption-id" BIGINT   ENCODE az64
	,"reward-payment" NUMERIC(17,4)   ENCODE az64
	,"cash-payment" NUMERIC(17,4)   ENCODE az64
	,"order-created-by" VARCHAR(255)   ENCODE lzo
	,"patient-id" BIGINT   ENCODE az64
	,source VARCHAR(255)   ENCODE lzo
	,"number-of-tests" INTEGER   ENCODE az64
	,"total-sales" NUMERIC(17,4)   ENCODE az64
	,"store-id" BIGINT   ENCODE az64
	,store VARCHAR(255)   ENCODE lzo
	,abo VARCHAR(255)   ENCODE lzo
	,"store-manager" VARCHAR(255)   ENCODE lzo
	,"acq-medium" VARCHAR(255)   ENCODE lzo
	,nodo BIGINT   ENCODE az64
	,status VARCHAR(255)   ENCODE lzo
	,"booking-at" DATE   ENCODE az64
	,"call-status" VARCHAR(255)   ENCODE lzo
	,comments VARCHAR(255)   ENCODE lzo
	,"reason-name" VARCHAR(255)   ENCODE lzo
	,"reason-type" VARCHAR(255)   ENCODE lzo
	,city VARCHAR(255)   ENCODE lzo
	,line VARCHAR(255)   ENCODE lzo
	,"created-at" TIMESTAMP WITHOUT TIME ZONE   ENCODE az64
	,"created-by" VARCHAR(255)   ENCODE lzo
	,"updated-at" TIMESTAMP WITHOUT TIME ZONE   ENCODE az64
	,"updated-by" VARCHAR(255)   ENCODE lzo
)
DISTSTYLE AUTO
;
ALTER TABLE "prod2-generico"."diagnostic-visibility" owner to "admin";