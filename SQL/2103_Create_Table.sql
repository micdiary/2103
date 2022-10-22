
-- find the secure file directory to store excel data to be imported into db
-- SHOW VARIABLES LIKE "secure_file_priv";
CREATE DATABASE 2103_db;
USE 2103_db;
-- DROP TABLE polytechnic;
CREATE TABLE IF NOT EXISTS Polytechnic (
	poly_id int NOT NULL AUTO_INCREMENT,
    poly_code varchar(2),
    poly_name varchar(5),
    citizen_fee decimal(13,2),
    pr_fee decimal(13,2),
    foreigner_fee decimal(13,2),
	PRIMARY KEY (poly_id)
);
-- DROP TABLE school;
CREATE TABLE IF NOT EXISTS School (
	school_id int NOT NULL AUTO_INCREMENT,
    school_name varchar(255),
    poly_id int,
	PRIMARY KEY (school_id),
    FOREIGN KEY (poly_id) REFERENCES polytechnic(poly_id)
);
-- DROP TABLE Course;
CREATE TABLE IF NOT EXISTS Course (
	course_id int NOT NULL AUTO_INCREMENT,
    course_name varchar(255),
    intake int,
    school_id int,
    course_code varchar(255),
    lower_bound int,
	upper_bound int,
	PRIMARY KEY (course_id),
    FOREIGN KEY (school_id) REFERENCES school(school_id)
);

-- DROP TABLE Scholarship;
CREATE TABLE IF NOT EXISTS Scholarship (
	scholarship_id int NOT NULL AUTO_INCREMENT,
    scholarship_name varchar(255),
	PRIMARY KEY (scholarship_id)
);


CREATE TABLE IF NOT EXISTS Criteria (
	criteria_id int NOT NULL AUTO_INCREMENT,
    criteria_description varchar(255),
	PRIMARY KEY (criteria_id)
);

CREATE TABLE IF NOT EXISTS School_Scholarship (
	school_scholarship_id int NOT NULL AUTO_INCREMENT,
    school_id int NOT NULL,
	scholarship_id int NOT NULL,
	PRIMARY KEY (school_scholarship_id),
	FOREIGN KEY (school_id) REFERENCES school(school_id),
	FOREIGN KEY (scholarship_id) REFERENCES scholarship(scholarship_id)
);

CREATE TABLE IF NOT EXISTS Scholarship_Criteria (
	scholarship_criteria_id int NOT NULL AUTO_INCREMENT,
	scholarship_id int NOT NULL,
    criteria_id int NOT NULL,
	PRIMARY KEY (scholarship_criteria_id),
	FOREIGN KEY (scholarship_id) REFERENCES scholarship(scholarship_id),
    FOREIGN KEY (criteria_id) REFERENCES criteria(criteria_id)
);

CREATE TABLE IF NOT EXISTS Users (
	user_id int NOT NULL AUTO_INCREMENT,
	username varchar(255) NOT NULL,
    password varchar(255) NOT NULL,
	PRIMARY KEY (user_id)
);

CREATE TABLE IF NOT EXISTS Comments (
	comment_id int NOT NULL AUTO_INCREMENT,
	description varchar(255),
    course_id int NOT NULL,
    user_id int NOT NULL,
	PRIMARY KEY (comment_id),
	FOREIGN KEY (course_id) REFERENCES Course(course_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE IF NOT EXISTS Vote (
	vote_id int NOT NULL AUTO_INCREMENT,
	user_id int NOT NULL,
    comment_id int NOT NULL,
    vote_value int NOT NULL,
	PRIMARY KEY (vote_id),
	FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (comment_id) REFERENCES criteria(criteria_id)
);