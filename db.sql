CREATE DATABASE loginsignup;

CREATE TABLE users (
    usrnm VARCHAR(10) PRIMARY KEY,
    email VARCHAR(25) UNIQUE,
    password VARCHAR(20)
);