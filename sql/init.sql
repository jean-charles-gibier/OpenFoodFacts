SET NAMES utf8;

DROP TABLE IF EXISTS `category`;
CREATE TABLE `category` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `tag` varchar(100) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `url` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `tag` (`tag`),
  KEY `idx_name` (`name`(15))
) ENGINE=InnoDB;


DROP TABLE IF EXISTS `product`;
CREATE TABLE `product` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `ean_code` varchar(13) NOT NULL,
  `product_name` varchar(100) NOT NULL,
  `generic_name` varchar(300) DEFAULT NULL,
  `brands` varchar(100) DEFAULT NULL,
  `stores` varchar(100) DEFAULT NULL,
  `url` varchar(200) DEFAULT NULL,
  `nutrition_grade` char(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ean_code_UNIQUE` (`ean_code`),
  KEY `idx_product_generic_brand` (`product_name`(15),`generic_name`(15),`brands`(15))
) ENGINE=InnoDB;



DROP TABLE IF EXISTS `productcategory`;
CREATE TABLE `productcategory` (
  `product_id` bigint unsigned NOT NULL,
  `category_id` bigint unsigned NOT NULL,
  PRIMARY KEY (`product_id`,`category_id`),
  KEY `fk_category_id` (`category_id`),
  CONSTRAINT `fk_category_id` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`),
  CONSTRAINT `fk_product_id` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`)
) ENGINE=InnoDB;


-- Table structure for table `savedsubstitute`
--

DROP TABLE IF EXISTS `savedsubstitute`;
CREATE TABLE `savedsubstitute` (
  `original_product_id` bigint unsigned NOT NULL,
  `substitute_product_id` bigint unsigned NOT NULL,
  PRIMARY KEY (`original_product_id`,`substitute_product_id`),
  KEY `fk_substitute_product_id` (`substitute_product_id`),
  CONSTRAINT `fk_original_product_id` FOREIGN KEY (`original_product_id`) REFERENCES `product` (`id`),
  CONSTRAINT `fk_substitute_product_id` FOREIGN KEY (`substitute_product_id`) REFERENCES `product` (`id`)
) ENGINE=InnoDB;
