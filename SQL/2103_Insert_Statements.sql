-- file directory is absolute, check your own device :D
-- LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/2103_Polytechnic_Data.csv' 
-- INTO TABLE polytechnic 
-- FIELDS TERMINATED BY ',' 
-- LINES TERMINATED BY '\n'
-- IGNORE 1 ROWS
-- (poly_code, poly_name,citizen_fee,pr_fee,foreigner_fee)
-- SET poly_id = NULL;

-- LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/2103_School_Data.csv' 
-- INTO TABLE school 
-- FIELDS TERMINATED BY ',' 
-- LINES TERMINATED BY '\n'
-- IGNORE 1 ROWS
-- (school_name, poly_id)
-- SET school_id = NULL;

-- LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/2103_Course_Data.csv' 
-- INTO TABLE course 
-- FIELDS TERMINATED BY ',' 
-- LINES TERMINATED BY '\n'
-- IGNORE 1 ROWS
-- (course_name, intake, school_id, course_code, lower_bound, upper_bound)
-- SET course_id = NULL;

-- LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/2103_Scholarship_Data1.csv' 
-- INTO TABLE scholarship 
-- FIELDS TERMINATED BY ',' 
-- LINES TERMINATED BY '\n'
-- IGNORE 1 ROWS
-- (scholarship_name)
-- SET scholarship_id = NULL;

-- LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/2103_Criteria_Data.csv' 
-- INTO TABLE criteria 
-- FIELDS TERMINATED BY ',' 
-- LINES TERMINATED BY '\n'
-- IGNORE 1 ROWS
-- (criteria_description)
-- SET criteria_id = NULL;

-- LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/2103_School_Scholarship_Data.csv' 
-- INTO TABLE school_scholarship 
-- FIELDS TERMINATED BY ',' 
-- LINES TERMINATED BY '\n'
-- IGNORE 1 ROWS
-- (school_id, scholarship_id)
-- SET school_scholarship_id = NULL;

-- LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/2103_Scholarship_Criteria_Data.csv' 
-- INTO TABLE scholarship_criteria 
-- FIELDS TERMINATED BY ',' 
-- LINES TERMINATED BY '\n'
-- IGNORE 1 ROWS
-- (scholarship_id,criteria_id)
-- SET scholarship_criteria_id = NULL;INSERT INTO `2103_db`.`course`

