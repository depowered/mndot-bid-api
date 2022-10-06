import enum


class UnitAbbreviation(str, enum.Enum):
    ACRE = "ACRE"
    ASMY = "ASMY"
    CY = "CY"
    DAY = "DAY"
    DOL = "DOL"
    EACH = "EACH"
    GAL = "GAL"
    HOUR = "HOUR"
    LF = "LF"
    LB = "LB"
    LS = "LS"
    MBM = "MBM"
    MGAL = "MGAL"
    PLT = "PLT"
    RDST = "RDST"
    SF = "SF"
    SY = "SY"
    SHRB = "SHRB"
    SIGS = "SIGS"
    STR = "STR"
    SYS = "SYS"
    TON = "TON"
    TREE = "TREE"
    UDAY = "UDAY"
    VINE = "VINE"


class Unit(str, enum.Enum):
    ACRE = "ACRE"
    ASSEMBLY = "ASSEMBLY"
    CU_YD = "CU YD"
    DAY = "DAY"
    DOLLAR = "DOLLAR"
    EACH = "EACH"
    GALLON = "GALLON"
    HOUR = "HOUR"
    LIN_FT = "LIN FT"
    POUND = "POUND"
    LUMP_SUM = "LUMP SUM"
    MBM = "MBM"
    M_GALLON = "M GALLON"
    PLANT = "PLANT"
    ROAD_STA = "ROAD STA"
    SQ_FT = "SQ FT"
    SQ_YD = "SQ YD"
    SHRUB = "SHRUB"
    SIGNAL_SYSTEM = "SIGNAL SYSTEM"
    STRUCTURE = "STRUCTURE"
    SYSTEM = "SYSTEM"
    TON = "TON"
    TREE = "TREE"
    UNIT_DAY = "UNIT DAY"
    VINE = "VINE"


class District(str, enum.Enum):
    BAXTER: "Baxter"
    BEMIDJI: "Bemidji"
    DETROIT_LAKES: "Detroit Lakes"
    DULUTH: "Duluth"
    MANKATO: "Mankato"
    METRO: "Metro"
    ROCHESTER: "Rochester"
    WILLMAR: "Willmar"


class County(str, enum.Enum):
    AITKIN: "Aitkin"
    ANOKA: "Anoka"
    BECKER: "Becker"
    BELTRAMI: "Beltrami"
    BENTON: "Benton"
    BIG_STONE: "Big Stone"
    BLUE_EARTH: "Blue Earth"
    BROWN: "Brown"
    CARLTON: "Carlton"
    CARVER: "Carver"
    CASS: "Cass"
    CHIPPEWA: "Chippewa"
    CHISAGO: "Chisago"
    CLAY: "Clay"
    CLEARWATER: "Clearwater"
    COOK: "Cook"
    COTTONWOOD: "Cottonwood"
    CROW_WING: "Crow Wing"
    DAKOTA: "Dakota"
    DODGE: "Dodge"
    DOUGLAS: "Douglas"
    FARIBAULT: "Faribault"
    FILLMORE: "Fillmore"
    FREEBORN: "Freeborn"
    GOODHUE: "Goodhue"
    GRANT: "Grant"
    HENNEPIN: "Hennepin"
    HOUSTON: "Houston"
    HUBBARD: "Hubbard"
    ISANTI: "Isanti"
    ITASCA: "Itasca"
    JACKSON: "Jackson"
    KANABEC: "Kanabec"
    KANDIYOHI: "Kandiyohi"
    KITTSON: "Kittson"
    KOOCHICHING: "Koochiching"
    LAC_QUI_PARLE: "Lac qui Parle"
    LAKE: "Lake"
    LAKE_OF_THE_WOODS: "Lake of the Woods"
    LE_SUEUR: "Le Sueur"
    LINCOLN: "Lincoln"
    LYON: "Lyon"
    MAHNOMEN: "Mahnomen"
    MARSHALL: "Marshall"
    MARTIN: "Martin"
    MCLEOD: "McLeod"
    MEEKER: "Meeker"
    MILLE_LACS: "Mille Lacs"
    MORRISON: "Morrison"
    MOWER: "Mower"
    MURRAY: "Murray"
    NICOLLET: "Nicollet"
    NOBLES: "Nobles"
    NORMAN: "Norman"
    OLMSTED: "Olmsted"
    OTTER_TAIL: "Otter Tail"
    PENNINGTON: "Pennington"
    PINE: "Pine"
    PIPESTONE: "Pipestone"
    POLK: "Polk"
    POPE: "Pope"
    RAMSEY: "Ramsey"
    RED_LAKE: "Red Lake"
    REDWOOD: "Redwood"
    RENVILLE: "Renville"
    RICE: "Rice"
    ROCK: "Rock"
    ROSEAU: "Roseau"
    SAINT_LOUIS: "Saint Louis"
    SCOTT: "Scott"
    SHERBURNE: "Sherburne"
    SIBLEY: "Sibley"
    STEARNS: "Stearns"
    STEELE: "Steele"
    STEVENS: "Stevens"
    SWIFT: "Swift"
    TODD: "Todd"
    TRAVERSE: "Traverse"
    WABASHA: "Wabasha"
    WADENA: "Wadena"
    WASECA: "Waseca"
    WASHINGTON: "Washington"
    WATONWAN: "Watonwan"
    WILKIN: "Wilkin"
    WINONA: "Winona"
    WRIGHT: "Wright"
    YELLOW_MEDICINE: "Yellow Medicine"
