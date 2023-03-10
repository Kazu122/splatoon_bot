CREATE TABLE TBL_WEAPON (
    id INT AUTO_INCREMENT,
    name VARCHAR(16) NOT NULL,
    subId INT NOT NULL,
    specialId INT NOT NULL,
    typeId INT NOT NULL,
    INDEX(id),
    FOREIGN KEY FK_SUBID(subId) REFERENCES TBL_SUB_WEAPON(id),
    FOREIGN KEY FK_SPECIALID(specialId) REFERENCES TBL_SPECIAL_WEAPON(id),
    FOREIGN KEY FK_TYPEID(typeId) REFERENCES TBL_WEAPON_TYPE(id)
);