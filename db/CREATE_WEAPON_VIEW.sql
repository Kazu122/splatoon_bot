CREATE VIEW VIEW_WEAPON AS
SELECT TW.id AS "id", TW.name AS "weapon", TSW.name AS "sub", TSP.name AS "special", TWT.type AS "type" FROM TBL_WEAPON AS TW
    JOIN TBL_SUB_WEAPON AS TSW ON TW.subId = TSW.id
    JOIN TBL_SPECIAL_WEAPON AS TSP ON TW.specialId = TSP.id
    JOIN TBL_WEAPON_TYPE AS TWT ON TW.typeId = TWT.id;

CREATE VIEW VIEW_PLAYER_WEAPON AS 
SELECT TP.guildId AS "guildId", TR.rule AS "rule", TS.name AS "stage", TP.name AS "player", VW.weapon AS "weapon", VW.sub AS "sub", VW.special AS "special" FROM TBL_FORMATION AS TF
    JOIN TBL_RULE AS TR ON TF.ruleId = TR.id
    JOIN TBL_STAGE AS TS ON TF.stageId = TS.id
    JOIN TBL_PLAYER AS TP ON TF.playerId = TP.id
    JOIN VIEW_WEAPON AS VW ON TF.weaponId = VW.id;