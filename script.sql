-- DROP TABLE Graduate
-- DROP TABLE Activity_Relation
-- DROP TABLE EPAREG_Activity_Relation
-- DROP TABLE EPAREG_Employment_Status
-- DROP TABLE Residence_Place
-- DROP TABLE Gender
-- DROP TABLE Degree
-- DROP TABLE University
-- DROP TABLE Teaching_Field
-- DROP TABLE Academic_Level

CREATE TABLE University (
    University_ID INT PRIMARY KEY,
    University_Name VARCHAR(255) NOT NULL,
	Description VARCHAR(255)
);

CREATE TABLE Teaching_Field (
    Teaching_Field_ID INT PRIMARY KEY,
    Teaching_Field_Name VARCHAR(255) NOT NULL,
	Description VARCHAR(255)
);

CREATE TABLE Academic_Level (
    Academic_Level_ID INT PRIMARY KEY,
    Academic_Level_Name VARCHAR(255) NOT NULL,
	Description VARCHAR(255)
);

CREATE TABLE Gender (
    Gender_ID INT PRIMARY KEY,
    Gender_Name VARCHAR(50) NOT NULL,
	Description VARCHAR(255)
);

CREATE TABLE Residence_Place (
    Residence_Place_ID INT PRIMARY KEY,
    Residence_Place_Name VARCHAR(255) NOT NULL,
	Description VARCHAR(255)
);

CREATE TABLE EPAREG_Activity_Relation (
    EPAREG_Activity_Relation_ID INT PRIMARY KEY,
    Activity_Relation_Description VARCHAR(255) NOT NULL,
	Description VARCHAR(255)
);

CREATE TABLE EPAREG_Employment_Status (
    EPAREG_Employment_Status_ID INT PRIMARY KEY,
    Employment_Status_Description VARCHAR(255) NOT NULL,
	Description VARCHAR(255)
);

CREATE TABLE Activity_Relation (
    Activity_Relation_ID INT PRIMARY KEY,
    Activity_Relation_Description VARCHAR(255) NOT NULL,
	Description VARCHAR(255)
);


CREATE TABLE Degree (
    Degree_ID INT PRIMARY KEY,
    Degree_Name VARCHAR(255) NOT NULL,
	Description VARCHAR(255)
);

CREATE TABLE Graduate (
    Graduate_ID INT PRIMARY KEY,
    Degree_ID INT,
    Teaching_Field_ID INT,
    Academic_Level_ID INT,
    University_ID INT,
    End_Term INT,
    Graduation_Term INT,
    Gender_ID INT,
    Residence_Place_ID INT,
    EPAREG_Activity_Relation_ID INT,
    EPAREG_Employment_Status_ID INT,
    Activity_Relation_ID INT,
    Additional_Enrollment_ULL1 VARCHAR(max),
    Additional_Enrollment_ULL2 VARCHAR(max),
    Additional_Enrollment_ULL3 VARCHAR(max),
    Additional_Enrollment_ULPGC1 VARCHAR(max),
    Additional_Enrollment_ULPGC2 VARCHAR(max),
    Additional_Enrollment_ULPGC3 VARCHAR(max),
    FOREIGN KEY (Degree_ID) REFERENCES Degree(Degree_ID),
	FOREIGN KEY (Teaching_Field_ID) REFERENCES Teaching_Field(Teaching_Field_ID),
	FOREIGN KEY (Academic_Level_ID) REFERENCES Academic_Level(Academic_Level_ID),
	FOREIGN KEY (University_ID) REFERENCES University(University_ID),
    FOREIGN KEY (Gender_ID) REFERENCES Gender(Gender_ID),
    FOREIGN KEY (Residence_Place_ID) REFERENCES Residence_Place(Residence_Place_ID),
    FOREIGN KEY (EPAREG_Activity_Relation_ID) REFERENCES EPAREG_Activity_Relation(EPAREG_Activity_Relation_ID),
    FOREIGN KEY (EPAREG_Employment_Status_ID) REFERENCES EPAREG_Employment_Status(EPAREG_Employment_Status_ID),
    FOREIGN KEY (Activity_Relation_ID) REFERENCES Activity_Relation(Activity_Relation_ID)
);
