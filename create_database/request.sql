PRAGMA foreign_keys = ON;

CREATE TABLE circuits (
    circuitId INT PRIMARY KEY,
    circuitRef VARCHAR(100),
    name VARCHAR(100),
    location VARCHAR(100),
    country VARCHAR(100),
    lat FLOAT,
    lng FLOAT,
    alt INT,
    url VARCHAR(100)
);

CREATE TABLE constructors (
    constructorId INT PRIMARY KEY,
    constructorRef VARCHAR(50),
    name VARCHAR(50),
    nationality VARCHAR(50),
    url VARCHAR(100)
);

CREATE TABLE drivers (
    driverId INT PRIMARY KEY,
    driverRef VARCHAR(20),
    number INT,
    code CHAR(3),
    forename VARCHAR(50),
    surname VARCHAR(50),
    dob DATE,
    nationality VARCHAR(20),
    url VARCHAR(100)
);

CREATE TABLE races (
    raceId INT PRIMARY KEY,
    year INT,
    round INT,
    circuitId INT,
    name VARCHAR(50),
    date DATE,
    time CHAR(8),
    url VARCHAR(100),
    fp1_date DATE,
    fp1_time CHAR(8),
    fp2_date DATE,
    fp2_time CHAR(8),
    fp3_date DATE,
    fp3_time CHAR(8),
    quali_date DATE,
    quali_time CHAR(8),
    sprint_date DATE,
    sprint_time CHAR(8),
    FOREIGN KEY (circuitId) REFERENCES circuits(circuitId)
);

CREATE TABLE seasons (
    year INT PRIMARY KEY,
    url VARCHAR(100)
);

CREATE TABLE constructor_results (
    constructorResultsId INT PRIMARY KEY,
    raceId INT,
    constructorId INT,
    points INT,
    status VARCHAR(20),
    FOREIGN KEY (raceId) REFERENCES races(raceId),
    FOREIGN KEY (constructorId) REFERENCES constructors(constructorId)
);

CREATE TABLE constructor_status (
    constructorStandingsId INT PRIMARY KEY,
    raceId INT,
    constructorId INT,
    points INT,
    position INT,
    positionText VARCHAR(2),
    wins INT,
    FOREIGN KEY (raceId) REFERENCES races(raceId),
    FOREIGN KEY (constructorId) REFERENCES constructors(constructorId)
);

CREATE TABLE driver_standings (
    driverStandingsId INT PRIMARY KEY,
    raceId INT,
    driverId INT,
    points INT,
    position INT,
    positionText VARCHAR(2),
    wins INT,
    FOREIGN KEY (raceId) REFERENCES races(raceId),
    FOREIGN KEY (driverId) REFERENCES drivers(driverId)
);

CREATE TABLE lap_times (
    raceId INT,
    driverId INT,
    lap INT,
    position INT,
    time CHAR(8),
    milliseconds INT,
    PRIMARY KEY (raceId, driverId, lap),
    FOREIGN KEY (raceId) REFERENCES races(raceId),
    FOREIGN KEY (driverId) REFERENCES drivers(driverId)
);

CREATE TABLE pit_stops (
    raceId INT,
    driverId INT,
    stop INT,
    lap INT,
    time CHAR(8),
    duration CHAR(6),
    milliseconds INT,
    PRIMARY KEY (raceId, driverId, stop),
    FOREIGN KEY (raceId) REFERENCES races(raceId),
    FOREIGN KEY (driverId) REFERENCES drivers(driverId)
);

CREATE TABLE qualifying (
    qualifyId INT PRIMARY KEY,
    raceId INT,
    driverId INT,
    constructorId INT,
    number INT,
    position INT,
    q1 CHAR(8),
    q2 CHAR(8),
    q3 CHAR(8),
    FOREIGN KEY (raceId) REFERENCES races(raceId),
    FOREIGN KEY (driverId) REFERENCES drivers(driverId),
    FOREIGN KEY (constructorId) REFERENCES constructors(constructorId)
);

CREATE TABLE results (
    resultId INT PRIMARY KEY,
    raceId INT,
    driverId INT,
    constructorId INT,
    number INT,
    grid INT,
    position INT,
    positionText VARCHAR(2),
    positionOrder INT,
    points INT,
    laps INT,
    time VARCHAR(10),
    milliseconds INT,
    fastestLap INT,
    rank INT,
    fastestLapTime CHAR(8),
    fastestLapSpeed VARCHAR(10),
    statusId INT,
    FOREIGN KEY (raceId) REFERENCES races(raceId),
    FOREIGN KEY (driverId) REFERENCES drivers(driverId),
    FOREIGN KEY (constructorId) REFERENCES constructors(constructorId)
);

CREATE TABLE sprint_results (
    resultId INT PRIMARY KEY,
    raceId INT,
    driverId INT,
    constructorId INT,
    number INT,
    grid INT,
    position INT,
    positionText VARCHAR(2),
    positionOrder INT,
    points INT,
    laps INT,
    time VARCHAR(10),
    milliseconds INT,
    fastestLap INT,
    fastestLapTime CHAR(8),
    statusId INT,
    FOREIGN KEY (raceId) REFERENCES races(raceId),
    FOREIGN KEY (driverId) REFERENCES drivers(driverId),
    FOREIGN KEY (constructorId) REFERENCES constructors(constructorId),
    FOREIGN KEY (statusId) REFERENCES status(statusId)
);

CREATE TABLE status (
    statusId INT PRIMARY KEY,
    status VARCHAR(50)
);
