
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
