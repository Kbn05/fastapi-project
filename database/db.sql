CREATE DATABASE IF NOT EXISTS `fastapi`
/*!40100 DEFAULT CHARACTER SET utf8 */
;
USE `fastapi`;
CREATE TABLE IF NOT EXISTS `posts`(
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `title` VARCHAR(255) NOT NULL,
    `content` VARCHAR(255) NOT NULL,
    `published` BOOLEAN NOT NULL DEFAULT TRUE,
    `likes` INT UNSIGNED DEFAULT 0,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8;
DROP TABLE IF EXISTS `posts`;
INSERT INTO `posts` (
        `title`,
        `content`,
        `published`,
        `likes`,
        `created_at`
    )
VALUES (
        'First Post',
        'Content for the first post',
        TRUE,
        0,
        DEFAULT
    ),
    (
        'Second Post',
        'Content for the second post',
        TRUE,
        10,
        DEFAULT
    ),
    (
        'Third Post',
        'Content for the third post',
        TRUE,
        15,
        DEFAULT
    ),
    (
        'Fourth Post',
        'Content for the fourth post',
        FALSE,
        0,
        DEFAULT
    ),
    (
        'Fifth Post',
        'Content for the fifth post',
        FALSE,
        50,
        DEFAULT
    );
UPDATE `posts`
SET `content` = 'Content for the first post'
WHERE `id` = 1;