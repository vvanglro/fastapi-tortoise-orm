-- upgrade --
ALTER TABLE `data` ADD `now_confirmed` BIGINT NOT NULL  COMMENT '现有确诊数量' DEFAULT 0;
ALTER TABLE `data` MODIFY COLUMN `recovered` BIGINT NOT NULL  COMMENT '累计痊愈数量' DEFAULT 0;
ALTER TABLE `data` MODIFY COLUMN `confirmed` BIGINT NOT NULL  COMMENT '累计确诊数量' DEFAULT 0;
ALTER TABLE `data` MODIFY COLUMN `deaths` BIGINT NOT NULL  COMMENT '累计死亡数量' DEFAULT 0;
ALTER TABLE `city` ADD INDEX `idx_city_updated_8f4388` (`updated_at`);
ALTER TABLE `city` ADD INDEX `idx_city_created_088683` (`created_at`);
ALTER TABLE `data` ADD INDEX `idx_data_updated_5176d3` (`updated_at`);
ALTER TABLE `data` ADD INDEX `idx_data_created_9f2fb5` (`created_at`);
ALTER TABLE `data` ADD INDEX `idx_data_date_c50110` (`date`);
-- downgrade --
ALTER TABLE `data` DROP INDEX `idx_data_date_c50110`;
ALTER TABLE `data` DROP INDEX `idx_data_created_9f2fb5`;
ALTER TABLE `data` DROP INDEX `idx_data_updated_5176d3`;
ALTER TABLE `city` DROP INDEX `idx_city_created_088683`;
ALTER TABLE `city` DROP INDEX `idx_city_updated_8f4388`;
ALTER TABLE `data` DROP COLUMN `now_confirmed`;
ALTER TABLE `data` MODIFY COLUMN `recovered` BIGINT NOT NULL  COMMENT '痊愈数量' DEFAULT 0;
ALTER TABLE `data` MODIFY COLUMN `confirmed` BIGINT NOT NULL  COMMENT '确诊数量' DEFAULT 0;
ALTER TABLE `data` MODIFY COLUMN `deaths` BIGINT NOT NULL  COMMENT '死亡数量' DEFAULT 0;
