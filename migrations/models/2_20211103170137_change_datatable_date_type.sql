-- upgrade --
ALTER TABLE `data` MODIFY COLUMN `date` DATETIME(6) NOT NULL  COMMENT '数据日期';
-- downgrade --
ALTER TABLE `data` MODIFY COLUMN `date` DATE NOT NULL  COMMENT '数据日期';
