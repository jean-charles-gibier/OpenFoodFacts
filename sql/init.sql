SET NAMES utf8;

DROP TABLE IF EXISTS ProductCategory;
DROP TABLE IF EXISTS SavedSubstitute;
DROP TABLE IF EXISTS Product;
DROP TABLE IF EXISTS Category;

CREATE TABLE Product (
	id BIGINT UNSIGNED AUTO_INCREMENT,
    ean_code VARCHAR(13),
	product_name VARCHAR(100) NOT NULL,
	generic_name VARCHAR(300),
	brands VARCHAR(100),
	stores VARCHAR(100),
	url VARCHAR(200),
	nutrition_grade CHAR(1),
/*    _category_list VARCHAR(1000), */
	PRIMARY KEY (id)
);

ALTER TABLE `openfoodfacts_schema`.`product` 
ADD INDEX `idx_product_generic_brand` (`product_name`(15) ASC, `generic_name`(15) ASC, `brands`(15) ASC);
ALTER TABLE `openfoodfacts_schema`.`product` 
ADD INDEX `idx_ean_code` (`ean_code` ASC);
ALTER TABLE `openfoodfacts_schema`.`product` 
CHANGE COLUMN `ean_code` `ean_code` VARCHAR(13) NOT NULL ,
ADD UNIQUE INDEX `ean_code_UNIQUE` (`ean_code` ASC) VISIBLE;

CREATE TABLE `category` (
  `id` BIGINT unsigned NOT NULL AUTO_INCREMENT,
  `tag` varchar(100) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `url` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `tag` (`tag`),
  KEY `idx_name` (`name`(15))
);
/*
ALTER TABLE `openfoodfacts_schema`.`category` 
ADD INDEX `idx_name` (`name`(15) ASC);
*/

CREATE TABLE ProductCategory (
	product_id BIGINT UNSIGNED,
	category_id BIGINT UNSIGNED,
	PRIMARY KEY (product_id, category_id),
	CONSTRAINT fk_product_id FOREIGN KEY (product_id) REFERENCES Product(id),
	CONSTRAINT fk_category_id FOREIGN KEY (category_id) REFERENCES Category (id)
);

CREATE TABLE SavedSubstitute (
	original_product_id BIGINT UNSIGNED,
	substitute_product_id BIGINT UNSIGNED,
	PRIMARY KEY (original_product_id, substitute_product_id),
	CONSTRAINT fk_original_product_id FOREIGN KEY (original_product_id) REFERENCES Product(id),
	CONSTRAINT fk_substitute_product_id FOREIGN KEY (substitute_product_id) REFERENCES Product(id)
);
