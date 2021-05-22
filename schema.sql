CREATE TABLE IF NOT EXISTS StreamingService(
    StreamingServiceID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS Genre(
    GenreID INT PRIMARY KEY AUTO_INCREMENT,
    Type VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS Movie(
    MovieID INT PRIMARY KEY AUTO_INCREMENT,
    Title VARCHAR(50),
    Year SMALLINT,
    GenreID INT,
    ContentRating VARCHAR(6),
    Director VARCHAR(50),
    RunningTime VARCHAR(50),
    Actor1 VARCHAR(50),
    Actor2 VARCHAR(50),
    Actor3 VARCHAR(50),
    Actor4 VARCHAR(50),
    StreamingServiceID INT,
    isDeleted BIT NOT NULL DEFAULT 0,
    FOREIGN KEY (GenreID) REFERENCES Genre(GenreID),
    FOREIGN KEY (StreamingServiceID) REFERENCES StreamingService(StreamingServiceID)
);

CREATE TABLE IF NOT EXISTS User(
    UserID INT PRIMARY KEY AUTO_INCREMENT,
    FirstName VARCHAR(25),
    LastName VARCHAR(25),
    Email VARCHAR(50),
    isDeleted BIT NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS UserWatched(
    UserID INT,
    MovieID INT,
    Watched BIT(1) DEFAULT 1,
    UserRating FLOAT,
    isDeleted BIT NOT NULL DEFAULT 0,
    FOREIGN KEY (UserID) REFERENCES User(UserID),
    FOREIGN KEY (MovieID) REFERENCES Movie(MovieID),
    PRIMARY KEY (UserID, MovieID)
);

CREATE TABLE IF NOT EXISTS UserPlanned(
    UserID INT,
    MovieID Int,
    Planned BIT(1) DEFAULT 1,
    isDeleted BIT NOT NULL DEFAULT 0,
    FOREIGN KEY (UserID) REFERENCES User(UserID),
    FOREIGN KEY (MovieID) REFERENCES Movie(MovieID),
    PRIMARY KEY (UserID, MovieID)
);


# indexes
CREATE INDEX Movie_index
 on Movie(MovieID);

CREATE INDEX User_index
 on User(UserID);


DROP PROCEDURE SearchTitle;
DROP PROCEDURE SearchYear;
DROP PROCEDURE SearchGenre;
DROP PROCEDURE SearchContentRating;
DROP PROCEDURE SearchDirector;
DROP PROCEDURE SearchActor;
DROP PROCEDURE SearchAverageRating;
DROP PROCEDURE SearchStreamingService;
DROP PROCEDURE AllTimeMovie;


# stored procedures
CREATE PROCEDURE SearchTitle(IN mTitle VARCHAR(50))
BEGIN
    SELECT M.MovieID, Title, Year, G.Type, ContentRating, Director, Actor1, Actor2, IFNULL(AR.Rating, 0), SS.Name
    FROM Movie M
    JOIN Genre G on M.GenreID = G.GenreID
    JOIN AverageRating AR on M.MovieID = AR.MovieID
    JOIN StreamingService SS on M.StreamingServiceID = SS.StreamingServiceID
    WHERE Title LIKE CONCAT('%', mTitle, '%');
END;

CREATE PROCEDURE SearchYear(IN mYear SMALLINT(6))
BEGIN
    SELECT M.MovieID, Title, Year, G.Type, ContentRating, Director, Actor1, Actor2, IFNULL(AR.Rating, 0), SS.Name
    FROM Movie M
    JOIN Genre G on M.GenreID = G.GenreID
    JOIN AverageRating AR on M.MovieID = AR.MovieID
    JOIN StreamingService SS on M.StreamingServiceID = SS.StreamingServiceID
    WHERE Year LIKE mYear;
END;

CREATE PROCEDURE SearchGenre(IN mGenre VARCHAR(32))
BEGIN
    SELECT M.MovieID, Title, Year, G.Type, ContentRating, Director, Actor1, Actor2, IFNULL(AR.Rating, 0), SS.Name
    FROM Movie M
    JOIN Genre G on M.GenreID = G.GenreID
    JOIN AverageRating AR on M.MovieID = AR.MovieID
    JOIN StreamingService SS on M.StreamingServiceID = SS.StreamingServiceID
    WHERE G.Type LIKE CONCAT(mGenre, '%');
END;

CREATE PROCEDURE SearchContentRating(IN mCR VARCHAR(32))
BEGIN
    SELECT M.MovieID, Title, Year, G.Type, ContentRating, Director, Actor1, Actor2, IFNULL(AR.Rating, 0), SS.Name
    FROM Movie M
    JOIN Genre G on M.GenreID = G.GenreID
    JOIN AverageRating AR on M.MovieID = AR.MovieID
    JOIN StreamingService SS on M.StreamingServiceID = SS.StreamingServiceID
    WHERE ContentRating LIKE CONCAT(mCR, '%');
END;

CREATE PROCEDURE SearchDirector(IN mDir VARCHAR(32))
BEGIN
    SELECT M.MovieID, Title, Year, G.Type, ContentRating, Director, Actor1, Actor2, IFNULL(AR.Rating, 0), SS.Name
    FROM Movie M
    JOIN Genre G on M.GenreID = G.GenreID
    JOIN AverageRating AR on M.MovieID = AR.MovieID
    JOIN StreamingService SS on M.StreamingServiceID = SS.StreamingServiceID
    WHERE Director LIKE CONCAT(mDir, '%');
END;

CREATE PROCEDURE SearchActor(IN mAct VARCHAR(32))
BEGIN
    SELECT M.MovieID, Title, Year, G.Type, ContentRating, Director, Actor1, Actor2, IFNULL(AR.Rating, 0), SS.Name
    FROM Movie M
    JOIN Genre G on M.GenreID = G.GenreID
    JOIN AverageRating AR on M.MovieID = AR.MovieID
    JOIN StreamingService SS on M.StreamingServiceID = SS.StreamingServiceID
    WHERE (Actor1 LIKE CONCAT('%', mAct, '%')
           OR Actor2 LIKE CONCAT('%', mAct, '%')
           OR Actor3 LIKE CONCAT('%', mAct, '%'));
END;

CREATE PROCEDURE SearchAverageRating(IN mAR VARCHAR(32))
BEGIN
    SELECT M.MovieID, Title, Year, G.Type, ContentRating, Director, Actor1, Actor2, IFNULL(AR.Rating, 0), SS.Name
    FROM Movie M
    JOIN Genre G on M.GenreID = G.GenreID
    JOIN AverageRating AR on M.MovieID = AR.MovieID
    JOIN StreamingService SS on M.StreamingServiceID = SS.StreamingServiceID
    WHERE AR.Rating LIKE mAR;
END;

CREATE PROCEDURE SearchStreamingService(IN mStream VARCHAR(32))
BEGIN
    SELECT M.MovieID, Title, Year, G.Type, ContentRating, Director, Actor1, Actor2, IFNULL(AR.Rating, 0), SS.Name
    FROM Movie M
    JOIN Genre G on M.GenreID = G.GenreID
    JOIN AverageRating AR on M.MovieID = AR.MovieID
    JOIN StreamingService SS on M.StreamingServiceID = SS.StreamingServiceID
    WHERE SS.Name LIKE CONCAT(mStream, '%');
END;

CREATE PROCEDURE Planned(IN user INT)
BEGIN
   SELECT M.MovieID, Title, G.Type, Director, Actor1, SS.Name
   FROM Movie M, UserPlanned UP, Genre G, StreamingService SS
   WHERE M.MovieID = UP.MovieID
     AND M.GenreID = G.GenreID
     AND M.StreamingServiceID = SS.StreamingServiceID
     AND UP.UserID = user
     AND UP.isDeleted = 0
     AND Planned = 1;
END;

CREATE PROCEDURE Watched(IN user INT)
BEGIN
   SELECT M.MovieID, Title, G.Type, Director, Actor1, SS.Name
   FROM Movie M, UserWatched UW, Genre G, StreamingService SS
   WHERE M.MovieID = UW.MovieID
     AND M.GenreID = G.GenreID
     AND M.StreamingServiceID = SS.StreamingServiceID
     AND UW.UserID = user
     AND UW.isDeleted = 0
     AND Watched = 1;
END;

CREATE PROCEDURE AllTimeMovie(IN uID INT)
BEGIN
   SELECT Title, MAX(UW.UserRating)
    FROM Movie M, UserWatched UW
    WHERE M.MovieID = UW.MovieID
    AND UserID = uID
    AND Watched = 1
    GROUP BY M.MovieID
    LIMIT 1;
END;

CREATE PROCEDURE AddMovie(IN mtitle VARCHAR(50), IN myear SMALLINT(6), IN mgenreID INT(11), IN mcontentrating VARCHAR(6), IN mdirector VARCHAR(50), IN mrunningtime VARCHAR(50), IN mactor1 VARCHAR(50), IN mactor2 VARCHAR(50), IN mactor3 VARCHAR(50), IN mactor4 VARCHAR(50), IN mstreamingserviceID INT(11))
BEGIN
    INSERT INTO Movie(Title, Year, GenreID, ContentRating, Director, RunningTime, Actor1, Actor2, Actor3, Actor4, StreamingServiceID)
    VALUES (mtitle, myear, mgenreID, mcontentrating, mdirector, mrunningtime, mactor1, mactor2, mactor3, mactor4, mstreamingserviceID);
END;

CREATE PROCEDURE AddUser(IN first VARCHAR(25), IN last VARCHAR(25), IN uemail VARCHAR(50))
BEGIN
    INSERT INTO User(FirstName, LastName, Email)
    VALUES (first, last, uemail);
END;

CREATE PROCEDURE AddUserPlanned(IN uID INT, IN mID INT)
BEGIN
    INSERT INTO UserPlanned(UserID, MovieID)
    VALUES (uID, mID);
END;

CREATE PROCEDURE AddUserWatched(IN uID INT, IN mID INT, IN rating FLOAT)
BEGIN
    INSERT INTO UserWatched(UserID, MovieID, UserRating)
    VALUES (uID, mID, rating);
END;

CREATE PROCEDURE DeleteMovie(IN mID INT)
BEGIN
    UPDATE Movie SET isDeleted = 1
    WHERE MovieID = mID AND EXISTS (SELECT MovieID FROM AverageRating WHERE MovieID = mID);
END;


# views
CREATE VIEW Movies AS
    SELECT M.MovieID, Title, Year, G.Type, ContentRating, Director, Actor1, Actor2, AR.Rating, SS.Name
    FROM Movie M
    JOIN Genre G on M.GenreID = G.GenreID
    JOIN AverageRating AR on M.MovieID = AR.MovieID
    JOIN StreamingService SS on M.StreamingServiceID = SS.StreamingServiceID
    WHERE M.isDeleted = 0;

CREATE VIEW Users AS
    SELECT DISTINCT U.UserID, FirstName, LastName, M.MovieID, M.Title, M.Year, G.Type, UP.Planned, UW.Watched, U.isDeleted
    FROM User U
    JOIN UserPlanned UP on U.UserID = UP.UserID
    JOIN UserWatched UW on U.UserID = UW.UserID
    JOIN Movie M on M.MovieID = UP.MovieID
    JOIN Genre G on M.GenreID = G.GenreID
    WHERE U.isDeleted = 0;

CREATE VIEW AverageRating AS
    SELECT M.MovieID, IFNULL((ROUND(AVG(UserRating), 1)), 0) as Rating, M.isDeleted
    FROM Movie M
    LEFT JOIN UserWatched UW on M.MovieID = UW.MovieID
    GROUP BY M.MovieID;