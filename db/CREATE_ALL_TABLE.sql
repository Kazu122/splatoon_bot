BEGIN TRANSACTION;

PRAGMA forreign_keys=true;

CREATE TABLE IF NOT EXISTS TBL_SPECIAL_WEAPON (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS TBL_SUB_WEAPON (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS TBL_WEAPON_TYPE (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS TBL_WEAPON (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    typeId INTEGER NOT NULL,
    subId INTEGER NOT NULL,
    specialId INTEGER NOT NULL,
    FOREIGN KEY (subId) REFERENCES TBL_SUB_WEAPON(id),
    FOREIGN KEY (specialId) REFERENCES TBL_SPECIAL_WEAPON(id),
    FOREIGN KEY (typeId) REFERENCES TBL_WEAPON_TYPE(id)
);

CREATE TABLE IF NOT EXISTS TBL_STAGE (
    id TEXT PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS TBL_RULE (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rule TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS TBL_GUILD (
    id TEXT PRIMARY KEY,
    name TEXT
);

CREATE TABLE IF NOT EXISTS TBL_CHANNEL_TYPE (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
); 

CREATE TABLE IF NOT EXISTS TBL_CHANNEL (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    channelId TEXT,
    guildId TEXT,
    channelType int NOT NULL,
    name TEXT,
    UNIQUE(guildId, channelType, name),
    FOREIGN KEY (guildId) REFERENCES TBL_GUILD(id) ON DELETE CASCADE
    FOREIGN KEY (channelType) REFERENCES TBL_CHANNEL_TYPE(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS TBL_PLAYER (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    guildId TEXT,
    name TEXT,
    UNIQUE(guildId, name),
    FOREIGN KEY (guildId) REFERENCES TBL_GUILD(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS TBL_FORMATION (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    playerId INTEGER,
    ruleId INTEGER,
    stageId INTEGER,
    weaponId INTEGER,
    FOREIGN KEY (playerId) REFERENCES TBL_PLAYER(id) ON DELETE CASCADE,
    FOREIGN KEY (weaponId) REFERENCES TBL_WEAPON(id) ON DELETE CASCADE
    UNIQUE(playerId, ruleId, stageId)
);

COMMIT TRANSACTION;
