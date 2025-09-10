CREATE TABLE demographics (
participant_id FLOAT PRIMARY KEY,
gender FLOAT,
age_year FLOAT,
race FLOAT,
education_level FLOAT,
marital_status FLOAT,
family_income_poverty FLOAT
);

SELECT * from demographics;

CREATE TABLE anthropometry (
participant_id FLOAT primary KEY,
weight_kg FLOAT,
weight_comment FLOAT,
recumbent_length_cm FLOAT,
standing_height FLOAT,
standing_height_comment FLOAT,
bmi FLOAT,
bmi_category_child FLOAT,
upper_leg_cm FLOAT,
upper_arm_cm FLOAT,
arm_circumference_cm FLOAT,
waist_circ_cm FLOAT,
hip_circ_cm FLOAT
);

SELECT * FROM anthropometry;

CREATE TABLE blood_labs (
b_lab_id SERIAL PRIMARY KEY,
participant_id FLOAT NOT NULL,
test_name VARCHAR(100),
test_value FLOAT
);

select * from blood_labs limit 5;

CREATE TABLE urine_labs (
u_lab_id SERIAL PRIMARY KEY,
participant_id FLOAT NOT NULL,
test_name VARCHAR(100),
test_value FLOAT
);

select * from urine_labs limit 5;

CREATE TABLE hepatitis_labs (
hep_lab_id SERIAL PRIMARY KEY,
participant_id FLOAT NOT NULL,
test_name VARCHAR(100),
test_value FLOAT
);

select * from demographics limit 10;

select * from blood_labs limit 10;

select count(*) from demographics;

DELETE FROM blood_labs
WHERE participant_id NOT IN (
    SELECT participant_id
    FROM demographics
);

ALTER TABLE blood_labs
ADD CONSTRAINT fk_demographics
FOREIGN KEY(participant_id)
REFERENCES demographics(participant_id)
ON DELETE CASCADE;

DELETE FROM urine_labs
WHERE participant_id NOT IN (
    SELECT participant_id
    FROM demographics
);

ALTER TABLE urine_labs
ADD CONSTRAINT fk_demographics
FOREIGN KEY(participant_id)
REFERENCES demographics(participant_id)
ON DELETE CASCADE;

DELETE FROM hepatitis_labs
WHERE participant_id NOT IN (
    SELECT participant_id
    FROM demographics
);

ALTER TABLE hepatitis_labs
ADD CONSTRAINT fk_demographics
FOREIGN KEY(participant_id)
REFERENCES demographics(participant_id)
ON DELETE CASCADE;

DELETE FROM anthropometry
WHERE participant_id NOT IN (
    SELECT participant_id
    FROM demographics
);

ALTER TABLE anthropometry
ADD CONSTRAINT fk_demographics
FOREIGN KEY(participant_id)
REFERENCES demographics(participant_id)
ON DELETE CASCADE;

