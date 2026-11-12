CREATE DATABASE IF NOT EXISTS db_products 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE db_products;

CREATE TABLE IF NOT EXISTS tb_items (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(30) NOT NULL,
    description VARCHAR(60) NULL,
    family VARCHAR(20) NOT NULL,
    value FLOAT NOT NULL,
    quantity INT NOT NULL DEFAULT 0,
    PRIMARY KEY (id),
    INDEX ix_tb_items_id (id)
);