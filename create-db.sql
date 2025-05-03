-- CREATE SCHEMA wearable_devices_dataset;
use wearable_devices_dataset;

-- table for participant.csv
CREATE TABLE user_info (
	user_id varchar(12) primary key,
    wearable varchar(20),
    age int -- specific age
);

-- table for dailyRegister.csv
CREATE TABLE measured_physical_data (
	timestamp varchar(20) primary key,
    user_id varchar(12),
    height double,
    weight double,
    steps double,
    calories double, -- calories spent
    light_sleep double,
    deep_sleep double,
    rem_sleep double,
    foreign key (user_id) references user_info(user_id)
);

-- table for daily stress
CREATE TABLE measured_stress_data (
	timestamp varchar(20) primary key,
    user_id varchar(12),
    stress_level varchar(12),
    foreign key (user_id) references user_info(user_id)
);

-- table for processed physical data
CREATE TABLE user_input_data (
	user_id varchar(12),
    height double,
    weight double,
    steps double,
    calories double,
    light_sleep double,
    deep_sleep double,
    rem_sleep double,
	foreign key (user_id) references user_info(user_id)
);



