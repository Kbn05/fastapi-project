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
CREATE TABLE IF NOT EXISTS `users`(
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `username` VARCHAR(255) NOT NULL,
    `email` VARCHAR(255) NOT NULL,
    `password` VARCHAR(255) NOT NULL,
    `is_active` BOOLEAN NOT NULL DEFAULT TRUE,
    `is_superuser` BOOLEAN NOT NULL DEFAULT FALSE,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8;
ALTER TABLE `posts`
ADD COLUMN `author_id` INT UNSIGNED NOT NULL;
ALTER TABLE `posts`
ADD FOREIGN KEY (`author_id`) REFERENCES `users`(`id`) ON DELETE CASCADE;
INSERT INTO `posts` (
        `title`,
        `content`,
        `published`,
        `likes`,
        `created_at`,
        `author_id`
    )
VALUES (
        'First Post',
        'Content for the first post',
        TRUE,
        0,
        DEFAULT,
        1
    ),
    (
        'Second Post',
        'Content for the second post',
        TRUE,
        10,
        DEFAULT,
        7
    ),
    (
        'Third Post',
        'Content for the third post',
        TRUE,
        15,
        DEFAULT,
        7
    ),
    (
        'Fourth Post',
        'Content for the fourth post',
        FALSE,
        0,
        DEFAULT,
        6
    ),
    (
        'Fifth Post',
        'Content for the fifth post',
        FALSE,
        50,
        DEFAULT,
        7
    );
CREATE TABLE IF NOT EXISTS `locations`(
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `latitude` DECIMAL(9, 6) NOT NULL,
    `longitude` DECIMAL(9, 6) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8;
ALTER TABLE `locations`
ADD FOREIGN KEY (`id`) REFERENCES `posts`(`id`) ON DELETE CASCADE;
INSERT INTO `locations` (
        `id`,
        `latitude`,
        `longitude`
    )
VALUES (
        53,
        7.035262,
        -73.067737
    ),
    (
        54,
        7.048775,
        -73.078787
    ),
    (
        55,
        7.145176,
        -73.709435
    ),
    (
        58,
        7.490777,
        -75.247947
    ),
    (
        59,
        7.064514,
        -73.089676
    );
INSERT INTO `locations` (
        `id`,
        `latitude`,
        `longitude`
    )
VALUES (
        56,
        7.146174,
        -73.126335
    );
CREATE TABLE IF NOT EXISTS `likes`(
    `post_id` INT NOT NULL,
    `user_id` INT NOT NULL,
    PRIMARY KEY (`post_id`, `user_id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8;
ALTER TABLE `likes`
ADD FOREIGN KEY (`post_id`) REFERENCES `posts`(`id`) ON DELETE CASCADE;
ALTER TABLE `likes`
ADD FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE;
use fastapi;
CREATE TABLE IF NOT EXISTS `likes`(
    `post_id` INT UNSIGNED NOT NULL,
    `user_id` INT UNSIGNED NOT NULL,
    PRIMARY KEY (`post_id`, `user_id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8;
ALTER TABLE `likes`
ADD FOREIGN KEY (`post_id`) REFERENCES `posts`(`id`) ON DELETE CASCADE;
ALTER TABLE `likes`
ADD FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE;
CREATE TABLE IF NOT EXISTS `likes` (
    `post_id` INT UNSIGNED NOT NULL,
    `user_id` INT UNSIGNED NOT NULL,
    PRIMARY KEY (`post_id`, `user_id`),
    FOREIGN KEY (`post_id`) REFERENCES `posts`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE
) ENGINE = InnoDB DEFAULT CHARSET = utf8;
INSERT INTO `likes` (`post_id`, `user_id`)
VALUES (55, 7),
    (56, 7),
    (58, 6),
    (59, 7),
    (55, 6);
DELIMITER // CREATE TRIGGER insert_like_trigger
AFTER
INSERT ON likes FOR EACH ROW BEGIN
UPDATE posts
SET likes = likes + 1
WHERE id = NEW.post_id;
END;
// DELIMITER // CREATE TRIGGER delete_like_trigger
AFTER DELETE ON likes FOR EACH ROW BEGIN
UPDATE posts
SET likes = likes - 1
WHERE id = OLD.post_id;
END;
// DELIMITER;
ALTER TABLE `posts`
ADD COLUMN `image` VARCHAR(255) NOT NULL;
ALTER TABLE `posts`
ADD COLUMN `datetime` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE `posts`
ADD COLUMN `type` VARCHAR(255) NOT NULL;
ALTER TABLE `posts`
ADD COLUMN `location` VARCHAR(255) NOT NULL;
ALTER TABLE `posts`
ADD COLUMN `tags` VARCHAR(255) NOT NULL;
ALTER TABLE `users`
ADD COLUMN `career` VARCHAR(255) NOT NULL;
ALTER TABLE `users`
ADD COLUMN `age` INT NOT NULL;
CREATE TABLE IF NOT EXISTS `comments`(
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `content` VARCHAR(255) NOT NULL,
    `post_id` INT UNSIGNED NOT NULL,
    `user_id` INT UNSIGNED NOT NULL,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8;
ALTER TABLE `comments`
ADD FOREIGN KEY (`post_id`) REFERENCES `posts`(`id`) ON DELETE CASCADE;
ALTER TABLE `comments`
ADD FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE;
ALTER TABLE `users`
ADD COLUMN `image` VARCHAR(255) NOT NULL;