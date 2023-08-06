CREATE TABLE "prod2-generico"."calling-history-metadata" (
	"calling-history-id" int4 NOT NULL,
	"call-duration" numeric(17, 4) NOT NULL DEFAULT 0.0000
);

CREATE table "prod2-generico"."dnd-list" (
	phone varchar(255) NULL,
	"sms-dnd" int4 NOT NULL DEFAULT 1,
	"call-dnd" int4 NOT NULL DEFAULT 1,
	reason varchar(255) NULL,
	"patient-id" int8 NULL,
	"created-at" timestamp NOT NULL DEFAULT 'now'::text::timestamp with time zone
);
