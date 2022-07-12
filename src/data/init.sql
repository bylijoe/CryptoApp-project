CREATE DATABASE movimientos;
USE movimientos;

CREATE TABLE movimientos (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  date VARCHAR(45) NOT NULL,
  time VARCHAR(45) NOT NULL,
  from_currency VARCHAR(45) NOT NULL,
  from_quantity REAL NOT NULL,
  to_currency VARCHAR(45) NOT NULL,
  to_quantity REAL NOT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

insert  into 'movimientos'('id','date','time','from_currency','from_quantity','to_currency','to_quantity') values
(1,'2022-10-15','20:00','EUR',7.26, 'BTC', 1.0),
(2,'2022-10-15','20:00','EUR',7.26, 'BTC', 1.0);