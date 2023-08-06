CREATE TABLE IF NOT EXISTS "prod2-generico"."goodaid-dfc"
(	"store-id" INTEGER NOT NULL  ENCODE az64
	,composition VARCHAR(3000) NOT NULL  ENCODE RAW
	,"composition-master-id" INTEGER   ENCODE RAW
	,"total-quantity" INTEGER   ENCODE RAW
	,"total-revenue" NUMERIC(10,2)  ENCODE az64
	,"goodaid-quantity" INTEGER   ENCODE RAW
	,"ethical-quantity" INTEGER   ENCODE RAW
	,"total-generic-quantity" INTEGER   ENCODE RAW
	,"goodaid-revenue-value" NUMERIC(10,2)  ENCODE az64
	,"total-quantity-15d" INTEGER   ENCODE RAW
	,"total-revenue-15d" NUMERIC(10,2)  ENCODE az64
	,"goodaid-quantity-15d" INTEGER   ENCODE RAW
	,"ethical-quantity-15d" INTEGER ENCODE RAW
	,"total-generic-quantity-15d" NUMERIC(10,2)  ENCODE az64
	,"goodaid-revenue-value-15" NUMERIC(10,2)  ENCODE az64
	,"store-opened-at" TIMESTAMP WITHOUT TIME ZONE   ENCODE az64
	,"ga-comp-first-bill" TIMESTAMP WITHOUT TIME ZONE   ENCODE az64
	,"store-age-months" INTEGER   ENCODE RAW
	,"store-type" VARCHAR(63)  ENCODE RAW
	,"drug-age-days" INTEGER   ENCODE RAW
	,"drug-type" VARCHAR(63)  ENCODE RAW
	,"ga-share-30" NUMERIC(10,2)  ENCODE az64
	,"ga-share-15" NUMERIC(10,2)  ENCODE az64
	,"dfc-val" NUMERIC(10,2)  ENCODE az64
	,"created-at" TIMESTAMP WITHOUT TIME ZONE   ENCODE az64
	,"created-by" VARCHAR(765) NOT NULL  ENCODE lzo
	,"updated-at" TIMESTAMP WITHOUT TIME ZONE   ENCODE az64
	,"updated-by" VARCHAR(765)   ENCODE lzo
)
DISTSTYLE AUTO
;