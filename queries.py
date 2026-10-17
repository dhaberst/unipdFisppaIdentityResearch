CREATE_TABLE_SQL = """
    CREATE TABLE IF NOT EXISTS Article (
        Id INTEGER PRIMARY KEY,
        identifier TEXT NOT NULL,
        title TEXT,
        url TEXT,
        date TEXT,
        fullText TEXT,
        source TEXT,
        bodyPart TEXT,
        gemmaClassification INTEGER CHECK (gemmaClassification IN (0, 1, 2)),
        llamaClassification INTEGER CHECK (llamaClassification IN (0, 1, 2)),
        phiClassification INTEGER CHECK (phiClassification IN (0, 1, 2)),
        version INTEGER NOT NULL DEFAULT 1,
        UNIQUE (identifier, version)
    );
"""

QUERY_ALL_AGREEMENT_SQL = """
    SELECT *
    FROM Article
    WHERE gemmaClassification = 1
      AND llamaClassification = 1
      AND phiClassification = 1
      AND version = 1
"""

QUERY_ALL_OR_AMBIGUOUS_SQL = """
    SELECT *
    FROM Article
    WHERE gemmaClassification IN (1, 2)
      AND llamaClassification IN (1, 2)
      AND phiClassification IN (1, 2)
      AND version = 1
"""

QUERY_AT_MOST_TWO_AGREEMENT_SQL = """
    SELECT *
    FROM Article
    WHERE gemmaClassification IS NOT NULL
      AND llamaClassification IS NOT NULL
      AND phiClassification IS NOT NULL
      AND (
          (CASE WHEN gemmaClassification = 1 THEN 1 ELSE 0 END) +
          (CASE WHEN llamaClassification = 1 THEN 1 ELSE 0 END) +
          (CASE WHEN phiClassification = 1 THEN 1 ELSE 0 END)
      ) <= 2
      AND version = 1
"""

QUERY_AT_MOST_TWO_OR_AMBIGUOUS_SQL = """
    SELECT *
    FROM Article
    WHERE gemmaClassification IS NOT NULL
      AND llamaClassification IS NOT NULL
      AND phiClassification IS NOT NULL
      AND (
          (CASE WHEN gemmaClassification IN (1, 2) THEN 1 ELSE 0 END) +
          (CASE WHEN llamaClassification IN (1, 2) THEN 1 ELSE 0 END) +
          (CASE WHEN phiClassification IN (1, 2) THEN 1 ELSE 0 END)
      ) <= 2
      AND version = 1
"""

QUERY_AT_MOST_ONE_AGREEMENT_SQL = """
    SELECT *
    FROM Article
    WHERE gemmaClassification IS NOT NULL
      AND llamaClassification IS NOT NULL
      AND phiClassification IS NOT NULL
      AND (
          (CASE WHEN gemmaClassification = 1 THEN 1 ELSE 0 END) +
          (CASE WHEN llamaClassification = 1 THEN 1 ELSE 0 END) +
          (CASE WHEN phiClassification = 1 THEN 1 ELSE 0 END)
      ) <= 1
      AND version = 1
"""

QUERY_AT_MOST_ONE_OR_AMBIGUOUS_SQL = """
    SELECT *
    FROM Article
    WHERE gemmaClassification IS NOT NULL
      AND llamaClassification IS NOT NULL
      AND phiClassification IS NOT NULL
      AND (
          (CASE WHEN gemmaClassification IN (1, 2) THEN 1 ELSE 0 END) +
          (CASE WHEN llamaClassification IN (1, 2) THEN 1 ELSE 0 END) +
          (CASE WHEN phiClassification IN (1, 2) THEN 1 ELSE 0 END)
      ) <= 1
      AND version = 1
"""

QUERY_ALL_ZERO_SQL = """
    SELECT *
    FROM Article
    WHERE gemmaClassification = 0
      AND llamaClassification = 0
      AND phiClassification = 0
      AND version = 1
"""
