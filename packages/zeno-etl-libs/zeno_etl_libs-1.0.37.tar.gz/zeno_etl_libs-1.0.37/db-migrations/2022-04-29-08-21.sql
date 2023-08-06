CREATE TABLE IF NOT EXISTS "prod2-generico"."goodaid-incentive-v3"(
"attributed-store" 	INTEGER NOT NULL  ENCODE az64
,"patient-id"	INTEGER  ENCODE az64
,"group-molecule"	VARCHAR(765)   ENCODE lzo
,"group-molecule-text"	VARCHAR(765)   ENCODE lzo
,"order-source"	VARCHAR(65)   ENCODE lzo
,"date"	TIMESTAMP WITHOUT TIME ZONE   ENCODE az64
,"date-time"	TIMESTAMP  ENCODE az64
,"bill-id"	INTEGER NOT NULL  ENCODE az64
,"bill-flag"	INTEGER   ENCODE az64
,"quantity-sum"	INTEGER NOT NULL  ENCODE az64
,"sales-sum" NUMERIC(10,4)   ENCODE az64
,"incentive-ma"	 NUMERIC(10,4)   ENCODE az64
,"cum-sum"	 NUMERIC(10,4)   ENCODE az64
,"prev-cum-sum"	 NUMERIC(10,4)   ENCODE az64
,"cum-sum-old"	INTEGER   ENCODE az64
,"cum-sum-final"	INTEGER   ENCODE az64
,"incentive-flag" VARCHAR(63)   ENCODE lzo
,"store-id"	INTEGER   ENCODE az64
,"store-type" VARCHAR(63)   ENCODE lzo
,city	VARCHAR(63)   ENCODE lzo
,"store-name"	VARCHAR(256)   ENCODE lzo
,"line-manager" VARCHAR(256)   ENCODE lzo
,abo	VARCHAR(256)  ENCODE lzo
,composition	VARCHAR(765)  ENCODE lzo
,"composition-master-id"	INTEGER ENCODE az64
,"created-at" TIMESTAMP WITHOUT TIME ZONE   ENCODE az64
,"created-by" VARCHAR(765) NOT NULL  ENCODE lzo
,"updated-at" TIMESTAMP WITHOUT TIME ZONE   ENCODE az64
,"updated-by" VARCHAR(765)   ENCODE lzo
)DISTSTYLE AUTO
;

CREATE TABLE "prod2-generico"."goodaid-opportunity" (
	"store-id" INTEGER NOT NULL  ENCODE az64,
	"total-opportunity" INTEGER  ENCODE az64,
	"avg-qty" NUMERIC(10,4)   ENCODE az64,
	"total-opportunity-achieved" NUMERIC(10,4)   ENCODE az64,
	"store-type"  VARCHAR(63)   ENCODE lzo,
	city  VARCHAR(63)   ENCODE lzo,
	"store-name"  VARCHAR(256)   ENCODE lzo,
	"line-manager" VARCHAR(256)   ENCODE lzo,
	abo	VARCHAR(256)  ENCODE lzo
	,"created-at" TIMESTAMP WITHOUT TIME ZONE   ENCODE az64
	,"created-by" VARCHAR(765) NOT NULL  ENCODE lzo
	,"updated-at" TIMESTAMP WITHOUT TIME ZONE   ENCODE az64
	,"updated-by" VARCHAR(765)   ENCODE lzo
)DISTSTYLE AUTO
;

CREATE TABLE "prod2-generico"."goodaid-daily-store-opportunity" (
	"date" TIMESTAMP WITHOUT TIME ZONE   ENCODE az64,
	"store-id" INTEGER NOT NULL  ENCODE az64,
	"group-molecule"VARCHAR(256)   ENCODE lzo,
	"group-molecule-text" VARCHAR(256)   ENCODE lzo,
	"total-opportunity" INTEGER ENCODE az64,
	multiplier NUMERIC(10,4)   ENCODE az64,
	composition VARCHAR(765)  ENCODE lzo,
	"actaul-total-opp" NUMERIC(10,4)   ENCODE az64,
	"composition-master-id" NUMERIC(10,0)   ENCODE az64,
	"store-type"  VARCHAR(63)   ENCODE lzo,
	city  VARCHAR(63)   ENCODE lzo,
	"store-name"  VARCHAR(256)   ENCODE lzo,
	"line-manager" VARCHAR(256)   ENCODE lzo,
	abo	VARCHAR(256)  ENCODE lzo
	,"created-at" TIMESTAMP WITHOUT TIME ZONE   ENCODE az64
	,"created-by" VARCHAR(765) NOT NULL  ENCODE lzo
	,"updated-at" TIMESTAMP WITHOUT TIME ZONE   ENCODE az64
	,"updated-by" VARCHAR(765)   ENCODE lzo
)DISTSTYLE AUTO
;