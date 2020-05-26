
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
) ENGINE=InnoDB AUTO_INCREMENT=836985 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
