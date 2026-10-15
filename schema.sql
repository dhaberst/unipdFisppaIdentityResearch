CREATE TABLE IF NOT EXISTS Article (
    Id INTEGER PRIMARY KEY,
    identifier TEXT NOT NULL UNIQUE,
    title TEXT,
    url TEXT,
    date TEXT,
    fullText TEXT,
    source TEXT,
    bodyPart TEXT,
    gemmaClassification INTEGER CHECK (gemmaClassification IN (0, 1, 2)),
    llamaClassification INTEGER CHECK (llamaClassification IN (0, 1, 2)),
    phiClassification INTEGER CHECK (phiClassification IN (0, 1, 2)),
    version INTEGER NOT NULL DEFAULT 1
);