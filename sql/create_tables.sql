CREATE TABLE `LUsers` (
	`user_id`	INT AUTO_INCREMENT	NOT NULL,
	`name`	VARCHAR(255)	NULL,
	`birthday`	DATE	NULL,
	`call`	VARCHAR(255)	NULL,
	`address`	VARCHAR(255)	NULL,
	`created_at`	DATETIME(3)	NOT NULL	DEFAULT CURRENT_TIMESTAMP(3),
    PRIMARY KEY (`user_id`)
);

CREATE TABLE `LChapter` (
	`chapter_id`	INT AUTO_INCREMENT	NOT NULL,
	`title`	VARCHAR(255)	NOT NULL,
	PRIMARY KEY (`chapter_id`)
);
)

CREATE TABLE `LQuestions` (
	`question_id`	INT AUTO_INCREMENT	NOT NULL,
	`is_fixed`	BOOL	NOT NULL	DEFAULT FALSE,
	`user_id`	INT	NOT NULL	DEFAULT -1,
	`parents_id`	INT	NOT NULL,
	`content`	TEXT	NOT NULL,
	`created_at`	DATETIME(3)	NOT NULL	DEFAULT CURRENT_TIMESTAMP(3),
    PRIMARY KEY (`question_id`),
    FOREIGN KEY (`user_id`) REFERENCES `LUsers`(`user_id`),
	FOREIGN kEY (`chapter_id`) REFERENCES `LChapter`(`chapter_id`
);

CREATE TABLE `LAnswers` (
	`answer_id`	INT AUTO_INCREMENT	NOT NULL,
	`question_id`	INT	NOT NULL,
	`user_id`	INT	NOT NULL,
	`content`	TEXT	NOT NULL,
	`created_at`	DATETIME(3)	NOT NULL	DEFAULT CURRENT_TIMESTAMP(3),
    PRIMARY KEY (`answer_id`),
    FOREIGN KEY (`question_id`) REFERENCES `LQuestions`(`question_id`),
    FOREIGN KEY (`user_id`) REFERENCES `LUsers`(`user_id`)
);

CREATE TABLE `LSound` (
	`sound_id`	INT AUTO_INCREMENT	NOT NULL,
	`question_id`	INT	NOT NULL,
	`sound_url`	VARCHAR(255)	NOT NULL,
    PRIMARY KEY (`sound_id`),
    FOREIGN KEY (`question_id`) REFERENCES `LQuestions`(`question_id`)
);

CREATE TABLE `LImages` (
	`image_id`	INT AUTO_INCREMENT	NOT NULL,
	`answer_id`	INT	NOT NULL,
	`image_url`	VARCHAR(255)	NOT NULL,
    PRIMARY KEY (`image_id`),
    FOREIGN KEY (`answer_id`) REFERENCES `LAnswers`(`answer_id`)
);
