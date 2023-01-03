SELECT TW.name AS "weapon", TSW.name AS "sub", TSP.name AS "special", TWT.type AS "type" FROM TBL_WEAPON AS TW
    JOIN TBL_SUB_WEAPON AS TSW ON TW.subId = TSW.id
    JOIN TBL_SPECIAL_WEAPON AS TSP ON TW.specialId = TSP.id
    JOIN TBL_WEAPON_TYPE AS TWT ON TW.typeId = TWT.id;