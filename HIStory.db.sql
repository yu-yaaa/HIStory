BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "chapter" (
	"chapter_id"	VARCHAR NOT NULL,
	"title"	VARCHAR NOT NULL,
	"description"	VARCHAR,
	"chapter_order"	INTEGER NOT NULL,
	PRIMARY KEY("chapter_id")
);
CREATE TABLE IF NOT EXISTS "chapter_bg" (
	"chapter_bg_id"	VARCHAR NOT NULL,
	"chapter_id"	VARCHAR NOT NULL,
	"bg_path"	TEXT NOT NULL,
	PRIMARY KEY("chapter_bg_id"),
	FOREIGN KEY("chapter_id") REFERENCES "chapter"("chapter_id")
);
CREATE TABLE IF NOT EXISTS "character" (
	"character_id"	VARCHAR NOT NULL,
	"name"	TEXT NOT NULL,
	"role"	TEXT NOT NULL,
	"character_pic"	VARCHAR NOT NULL,
	PRIMARY KEY("character_id")
);
CREATE TABLE IF NOT EXISTS "classroom" (
	"classroom_id"	VARCHAR NOT NULL,
	"user_id"	VARCHAR NOT NULL,
	"class_name"	VARCHAR NOT NULL,
	"class_code"	TEXT NOT NULL,
	"created_at"	DATETIME NOT NULL,
	PRIMARY KEY("classroom_id"),
	FOREIGN KEY("user_id") REFERENCES "user"("user_id")
);
CREATE TABLE IF NOT EXISTS "comment" (
	"comment_id"	VARCHAR NOT NULL,
	"user_id"	VARCHAR NOT NULL,
	"progress_id"	VARCHAR NOT NULL,
	"comment_text"	VARCHAR NOT NULL,
	"sent_at"	DATE NOT NULL,
	PRIMARY KEY("comment_id"),
	FOREIGN KEY("progress_id") REFERENCES "progress"("progress_id"),
	FOREIGN KEY("user_id") REFERENCES "user"("user_id")
);
CREATE TABLE IF NOT EXISTS "dialogue" (
	"dialogue_id"	VARCHAR NOT NULL,
	"chapter_id"	VARCHAR NOT NULL,
	"character_id"	VARCHAR NOT NULL,
	"dialogue_text"	VARCHAR NOT NULL,
	"sequence_order"	INTEGER NOT NULL,
	"event_type"	TEXT,
	"chapter_bg_id"	VARCHAR NOT NULL,
	PRIMARY KEY("dialogue_id"),
	FOREIGN KEY("chapter_bg_id") REFERENCES "chapter_bg"("chapter_bg_id"),
	FOREIGN KEY("chapter_id") REFERENCES "chapter"("chapter_id"),
	FOREIGN KEY("character_id") REFERENCES "character"("character_id")
);
CREATE TABLE IF NOT EXISTS "minigame" (
	"minigame_id"	VARCHAR NOT NULL,
	"name"	TEXT NOT NULL,
	"description"	VARCHAR NOT NULL,
	"difficulty_level"	TEXT,
	PRIMARY KEY("minigame_id")
);
CREATE TABLE IF NOT EXISTS "minigame_result" (
	"minigame_result_id"	VARCHAR NOT NULL,
	"user_id"	VARCHAR NOT NULL,
	"minigame_id"	VARCHAR NOT NULL,
	"score"	INTEGER NOT NULL,
	"status"	TEXT NOT NULL,
	"played_at"	DATE NOT NULL,
	PRIMARY KEY("minigame_result_id"),
	FOREIGN KEY("minigame_id") REFERENCES "minigame"("minigame_id"),
	FOREIGN KEY("user_id") REFERENCES "user"("user_id")
);
CREATE TABLE IF NOT EXISTS "player_ans" (
	"player_ans_id"	VARCHAR NOT NULL,
	"user_id"	VARCHAR NOT NULL,
	"question_id"	VARCHAR NOT NULL,
	"selected_ans"	TEXT NOT NULL,
	"is_correct"	INTEGER NOT NULL,
	"answered_at"	DATE NOT NULL,
	PRIMARY KEY("player_ans_id"),
	FOREIGN KEY("question_id") REFERENCES "question"("question_id"),
	FOREIGN KEY("user_id") REFERENCES "user"("user_id")
);
CREATE TABLE IF NOT EXISTS "player_reward" (
	"player_reward_id"	VARCHAR NOT NULL,
	"user_id"	VARCHAR NOT NULL,
	"reward_id"	VARCHAR NOT NULL,
	"quantity"	INTEGER NOT NULL,
	PRIMARY KEY("player_reward_id"),
	FOREIGN KEY("reward_id") REFERENCES "reward"("reward_id"),
	FOREIGN KEY("user_id") REFERENCES "user"("user_id")
);
CREATE TABLE IF NOT EXISTS "progress" (
	"progress_id"	VARCHAR NOT NULL,
	"user_id"	VARCHAR NOT NULL,
	"chapter_id"	VARCHAR NOT NULL,
	"status"	TEXT NOT NULL,
	"last_accessed"	DATETIME NOT NULL,
	"attempts_count"	INTEGER NOT NULL,
	"score"	INTEGER NOT NULL,
	PRIMARY KEY("progress_id"),
	FOREIGN KEY("chapter_id") REFERENCES "chapter"("chapter_id"),
	FOREIGN KEY("user_id") REFERENCES "user"("user_id")
);
CREATE TABLE IF NOT EXISTS "question" (
	"question_id"	VARCHAR NOT NULL,
	"quiz_id"	VARCHAR NOT NULL,
	"question_text"	VARCHAR NOT NULL,
	"option_a"	VARCHAR NOT NULL,
	"option_b"	VARCHAR NOT NULL,
	"option_c"	VARCHAR NOT NULL,
	"option_d"	VARCHAR,
	"correct_answer"	TEXT NOT NULL,
	"explanation"	VARCHAR NOT NULL,
	PRIMARY KEY("question_id"),
	FOREIGN KEY("quiz_id") REFERENCES "quiz"("quiz_id")
);
CREATE TABLE IF NOT EXISTS "quiz" (
	"quiz_id"	VARCHAR NOT NULL,
	"chapter_id"	VARCHAR NOT NULL,
	"title"	VARCHAR NOT NULL,
	"type"	TEXT NOT NULL,
	PRIMARY KEY("quiz_id"),
	FOREIGN KEY("chapter_id") REFERENCES "chapter"("chapter_id")
);
CREATE TABLE IF NOT EXISTS "reward" (
	"reward_id"	VARCHAR NOT NULL,
	"reward_name"	VARCHAR NOT NULL,
	"description"	VARCHAR NOT NULL,
	"reward_type"	TEXT,
	"reward_pic"	VARCHAR,
	PRIMARY KEY("reward_id")
);
CREATE TABLE IF NOT EXISTS "user" (
	"user_id"	VARCHAR NOT NULL,
	"username"	VARCHAR NOT NULL,
	"email"	VARCHAR NOT NULL,
	"password"	VARCHAR NOT NULL,
	"user_role"	TEXT NOT NULL,
	"profile_picture"	VARCHAR NOT NULL,
	"classroom_id"	VARCHAR,
	"otp_code"	INTEGER,
	"otp_created_at"	INTEGER,
	PRIMARY KEY("user_id"),
	FOREIGN KEY("classroom_id") REFERENCES "user"("classroom_id"),
	FOREIGN KEY("profile_picture") REFERENCES ""
);
INSERT INTO "chapter" ("chapter_id","title","description","chapter_order") VALUES ('CH001','Self-Government','Focuses on Tunku Abdul Rahman becoming the leader of UMNO and forming the Alliance Party to win the first General Election.',1);
INSERT INTO "chapter" ("chapter_id","title","description","chapter_order") VALUES ('CH002','Independence Negotiations','Follows the delegation to London to negotiate independence with the British government through diplomatic debate.',2);
INSERT INTO "chapter" ("chapter_id","title","description","chapter_order") VALUES ('CH003','Independence Day','The historic moment at Dataran Merdeka where the Union Jack is lowered and the Malayan flag is raised for the first time.',3);
INSERT INTO "chapter_bg" ("chapter_bg_id","chapter_id","bg_path") VALUES ('BG001','CH001','Assets/BG001.png');
INSERT INTO "chapter_bg" ("chapter_bg_id","chapter_id","bg_path") VALUES ('BG002','CH001','Assets/BG002.png');
INSERT INTO "chapter_bg" ("chapter_bg_id","chapter_id","bg_path") VALUES ('BG003','CH002','Assets/BG003.png');
INSERT INTO "chapter_bg" ("chapter_bg_id","chapter_id","bg_path") VALUES ('BG004','CH002','Assets/BG004.png');
INSERT INTO "chapter_bg" ("chapter_bg_id","chapter_id","bg_path") VALUES ('BG005','CH003','Assets/BG005.png');
INSERT INTO "chapter_bg" ("chapter_bg_id","chapter_id","bg_path") VALUES ('BG006','CH003','Assets/BG006.png');
INSERT INTO "character" ("character_id","name","role","character_pic") VALUES ('CR001','Tunku Abdul Rahman','Leader of UMNO and Chief Minister of Malaya','Assets/CR001.png');
INSERT INTO "character" ("character_id","name","role","character_pic") VALUES ('CR002','Tan Cheng Lock','Leader of the MCA','Assets/CR002.png');
INSERT INTO "character" ("character_id","name","role","character_pic") VALUES ('CR003','Tun VT Sambathan','Leader of the MIC','Assets/CR003.png');
INSERT INTO "character" ("character_id","name","role","character_pic") VALUES ('CR004','British Officer','United Kingdom Government Representative','Assets/CR004.png');
INSERT INTO "character" ("character_id","name","role","character_pic") VALUES ('CR005','The Crowd','The citizens at Dataran Merdeka','Assets/CR005.png');
INSERT INTO "classroom" ("classroom_id","user_id","class_name","class_code","created_at") VALUES ('C001','USR001','History A','XeKtP','2026-04-01');
INSERT INTO "classroom" ("classroom_id","user_id","class_name","class_code","created_at") VALUES ('C002','USR001','History B','MfLwQ','2026-04-02');
INSERT INTO "classroom" ("classroom_id","user_id","class_name","class_code","created_at") VALUES ('C003','USR002','Apple  Sejarah','AsZwD','2026-04-01');
INSERT INTO "classroom" ("classroom_id","user_id","class_name","class_code","created_at") VALUES ('C004','USR002','Banana  Sejarah','BxYaF','2026-04-03');
INSERT INTO "classroom" ("classroom_id","user_id","class_name","class_code","created_at") VALUES ('C005','USR002','Cranberry Sejarah','CqXfH','2026-04-05');
INSERT INTO "comment" ("comment_id","user_id","progress_id","comment_text","sent_at") VALUES ('CM001','USR001','P001','Great job on completing this! Your understanding is very solid.','2026-04-20');
INSERT INTO "comment" ("comment_id","user_id","progress_id","comment_text","sent_at") VALUES ('CM002','USR002','P002','Well done. You have a good grasp, but review the tricky questions.','2026-04-21');
INSERT INTO "comment" ("comment_id","user_id","progress_id","comment_text","sent_at") VALUES ('CM003','USR001','P004','Excellent performance! You have mastered this chapter.','2026-04-20');
INSERT INTO "comment" ("comment_id","user_id","progress_id","comment_text","sent_at") VALUES ('CM004','USR002','P006','I appreciate your persistence. Let''s discuss the parts you find difficult.','2026-04-20');
INSERT INTO "comment" ("comment_id","user_id","progress_id","comment_text","sent_at") VALUES ('CM005','USR001','P008','Well done. You have a good grasp, but review the tricky questions.','2026-04-21');
INSERT INTO "comment" ("comment_id","user_id","progress_id","comment_text","sent_at") VALUES ('CM006','USR002','P010','Excellent performance! You have mastered this chapter.','2026-04-20');
INSERT INTO "comment" ("comment_id","user_id","progress_id","comment_text","sent_at") VALUES ('CM007','USR001','P012','Excellent performance! You have mastered this chapter.','2026-04-22');
INSERT INTO "comment" ("comment_id","user_id","progress_id","comment_text","sent_at") VALUES ('CM008','USR002','P013','I see you are working through this chapter. Keep it up!','2026-04-23');
INSERT INTO "comment" ("comment_id","user_id","progress_id","comment_text","sent_at") VALUES ('CM009','USR001','P014','Good effort, but I recommend reviewing the key concepts once more.','2026-04-20');
INSERT INTO "comment" ("comment_id","user_id","progress_id","comment_text","sent_at") VALUES ('CM010','USR002','P021','Good effort, but I recommend reviewing the key concepts once more.','2026-04-20');
INSERT INTO "comment" ("comment_id","user_id","progress_id","comment_text","sent_at") VALUES ('CM011','USR001','P024','Great job on completing this! Your understanding is very solid.','2026-04-21');
INSERT INTO "comment" ("comment_id","user_id","progress_id","comment_text","sent_at") VALUES ('CM012','USR002','P027','I see you are working through this chapter. Keep it up!','2026-04-24');
INSERT INTO "comment" ("comment_id","user_id","progress_id","comment_text","sent_at") VALUES ('CM013','USR001','P028','Excellent performance! You have mastered this chapter.','2026-04-20');
INSERT INTO "comment" ("comment_id","user_id","progress_id","comment_text","sent_at") VALUES ('CM014','USR002','P031','I appreciate your persistence. Let''s discuss the parts you find difficult.','2026-04-21');
INSERT INTO "comment" ("comment_id","user_id","progress_id","comment_text","sent_at") VALUES ('CM015','USR001','P034','Great job on completing this! Your understanding is very solid.','2026-04-20');
INSERT INTO "dialogue" ("dialogue_id","chapter_id","character_id","dialogue_text","sequence_order","event_type","chapter_bg_id") VALUES ('D001','CH001','CR005','Malaysia was once known as The Federation of Malaya under British Rule.',1,'narrator','BG001');
INSERT INTO "dialogue" ("dialogue_id","chapter_id","character_id","dialogue_text","sequence_order","event_type","chapter_bg_id") VALUES ('D002','CH001','CR005','Tunku Abdul Rahman is known as the Father of Independence due to his contributions.',2,'narrator','BG001');
INSERT INTO "dialogue" ("dialogue_id","chapter_id","character_id","dialogue_text","sequence_order","event_type","chapter_bg_id") VALUES ('D003','CH001','CR005','This is how we got our independence. This is HIStory.',3,'narrator','BG001');
INSERT INTO "dialogue" ("dialogue_id","chapter_id","character_id","dialogue_text","sequence_order","event_type","chapter_bg_id") VALUES ('D004','CH001','CR001','I am now leader of UMNO. I hope to live up to my predecessor, Dato Onn Jaafar.',4,'dialogue','BG001');
INSERT INTO "dialogue" ("dialogue_id","chapter_id","character_id","dialogue_text","sequence_order","event_type","chapter_bg_id") VALUES ('D005','CH001','CR001','My most important goal is this country’s independence from the British.',5,'dialogue','BG001');
INSERT INTO "dialogue" ("dialogue_id","chapter_id","character_id","dialogue_text","sequence_order","event_type","chapter_bg_id") VALUES ('D006','CH001','CR005','(Tunku Abdul Rahman meets with Tan Cheng Lock and Tun VT Sambathan)',6,'narrator','BG001');
INSERT INTO "dialogue" ("dialogue_id","chapter_id","character_id","dialogue_text","sequence_order","event_type","chapter_bg_id") VALUES ('D007','CH001','CR001','Good day gentlemen. I have a proposal for the two of you as leaders of MCA and MIC.',7,'dialogue','BG001');
INSERT INTO "dialogue" ("dialogue_id","chapter_id","character_id","dialogue_text","sequence_order","event_type","chapter_bg_id") VALUES ('D008','CH001','CR003','Sure Tuan. What is your proposal?',8,'dialogue','BG001');
INSERT INTO "dialogue" ("dialogue_id","chapter_id","character_id","dialogue_text","sequence_order","event_type","chapter_bg_id") VALUES ('D009','CH001','CR001','In order to make independence a success, I need the support of the Chinese and Indians.',9,'dialogue','BG001');
INSERT INTO "dialogue" ("dialogue_id","chapter_id","character_id","dialogue_text","sequence_order","event_type","chapter_bg_id") VALUES ('D010','CH001','CR001','Maybe we should combine our associations for the upcoming General Election.',10,'dialogue','BG001');
INSERT INTO "dialogue" ("dialogue_id","chapter_id","character_id","dialogue_text","sequence_order","event_type","chapter_bg_id") VALUES ('D011','CH001','CR001','Together we can be known as the Alliance party.',11,'dialogue','BG001');
INSERT INTO "dialogue" ("dialogue_id","chapter_id","character_id","dialogue_text","sequence_order","event_type","chapter_bg_id") VALUES ('D012','CH001','CR002','Hmm... I agree. With our unity, we can encourage the people to be united for our common goal.',12,'dialogue','BG001');
INSERT INTO "dialogue" ("dialogue_id","chapter_id","character_id","dialogue_text","sequence_order","event_type","chapter_bg_id") VALUES ('D013','CH001','CR003','I agree as well. Let us work together for Malaya.',13,'dialogue','BG001');
INSERT INTO "dialogue" ("dialogue_id","chapter_id","character_id","dialogue_text","sequence_order","event_type","chapter_bg_id") VALUES ('D014','CH001','CR005','27 July 1955: The first General Election is held to choose representatives.',14,'narrator','BG002');
INSERT INTO "dialogue" ("dialogue_id","chapter_id","character_id","dialogue_text","sequence_order","event_type","chapter_bg_id") VALUES ('D015','CH001','CR003','Tuan! We have the results of the election!',15,'dialogue','BG002');
INSERT INTO "dialogue" ("dialogue_id","chapter_id","character_id","dialogue_text","sequence_order","event_type","chapter_bg_id") VALUES ('D016','CH001','CR002','The Alliance party won 51 out of the 52 seats contested!',16,'dialogue','BG002');
INSERT INTO "dialogue" ("dialogue_id","chapter_id","character_id","dialogue_text","sequence_order","event_type","chapter_bg_id") VALUES ('D017','CH001','CR001','This is a great victory! This shows that the people are with us.',17,'dialogue','BG002');
INSERT INTO "dialogue" ("dialogue_id","chapter_id","character_id","dialogue_text","sequence_order","event_type","chapter_bg_id") VALUES ('D018','CH001','CR001','Now as Chief Minister, I will lead a delegation to London to negotiate for our independence.',18,'dialogue','BG002');
INSERT INTO "dialogue" ("dialogue_id","chapter_id","character_id","dialogue_text","sequence_order","event_type","chapter_bg_id") VALUES ('D019','CH001','CR005','Tunku Abdul Rahman leads a mission to London consisting of 4 Alliance leaders and 4 Malay Kings.',19,'narrator','BG002');
INSERT INTO "dialogue" ("dialogue_id","chapter_id","character_id","dialogue_text","sequence_order","event_type","chapter_bg_id") VALUES ('D020','CH002','CR005','The delegation arrives in London to meet the British officers.',1,'narrator','BG003');
INSERT INTO "dialogue" ("dialogue_id","chapter_id","character_id","dialogue_text","sequence_order","event_type","chapter_bg_id") VALUES ('D021','CH002','CR001','We are here to negotiate for the independence of the Federation of Malaya.',2,'dialogue','BG003');
INSERT INTO "dialogue" ("dialogue_id","chapter_id","character_id","dialogue_text","sequence_order","event_type","chapter_bg_id") VALUES ('D022','CH002','CR004','Independence is a serious matter. Is Malaya truly ready to govern itself?',3,'dialogue','BG003');
INSERT INTO "dialogue" ("dialogue_id","chapter_id","character_id","dialogue_text","sequence_order","event_type","chapter_bg_id") VALUES ('D023','CH002','CR001','Our people have shown unity and our leaders are ready. We seek a peaceful transition.',4,'dialogue','BG003');
INSERT INTO "dialogue" ("dialogue_id","chapter_id","character_id","dialogue_text","sequence_order","event_type","chapter_bg_id") VALUES ('D024','CH002','CR005','Negotiations begin. There are 5 rounds of debate.',5,'narrator','BG004');
INSERT INTO "dialogue" ("dialogue_id","chapter_id","character_id","dialogue_text","sequence_order","event_type","chapter_bg_id") VALUES ('D025','CH002','CR001','Through diplomatic debate, we must convince them of our sovereignty.',6,'dialogue','BG004');
INSERT INTO "dialogue" ("dialogue_id","chapter_id","character_id","dialogue_text","sequence_order","event_type","chapter_bg_id") VALUES ('D026','CH002','CR005','After intense negotiation, the British government agrees to the date.',7,'narrator','BG004');
INSERT INTO "dialogue" ("dialogue_id","chapter_id","character_id","dialogue_text","sequence_order","event_type","chapter_bg_id") VALUES ('D027','CH002','CR004','Very well. We agree. The Federation of Malaya will be independent on 31 August 1957.',8,'dialogue','BG004');
INSERT INTO "dialogue" ("dialogue_id","chapter_id","character_id","dialogue_text","sequence_order","event_type","chapter_bg_id") VALUES ('D028','CH003','CR005','30 August 1957: Night time at Dataran Merdeka. The crowd gathers.',1,'narrator','BG005');
INSERT INTO "dialogue" ("dialogue_id","chapter_id","character_id","dialogue_text","sequence_order","event_type","chapter_bg_id") VALUES ('D029','CH003','CR005','The Union Jack is lowered for the last time as the clock strikes midnight.',2,'narrator','BG005');
INSERT INTO "dialogue" ("dialogue_id","chapter_id","character_id","dialogue_text","sequence_order","event_type","chapter_bg_id") VALUES ('D030','CH003','CR005','31 August 1957: The Malayan flag is raised.',3,'narrator','BG006');
INSERT INTO "dialogue" ("dialogue_id","chapter_id","character_id","dialogue_text","sequence_order","event_type","chapter_bg_id") VALUES ('D031','CH003','CR001','At this historic moment, we proclaim the independence of our nation!',4,'dialogue','BG006');
INSERT INTO "dialogue" ("dialogue_id","chapter_id","character_id","dialogue_text","sequence_order","event_type","chapter_bg_id") VALUES ('D032','CH003','CR001','MERDEKA!',5,'dialogue','BG006');
INSERT INTO "dialogue" ("dialogue_id","chapter_id","character_id","dialogue_text","sequence_order","event_type","chapter_bg_id") VALUES ('D033','CH003','CR005','MERDEKA!',6,'dialogue','BG006');
INSERT INTO "dialogue" ("dialogue_id","chapter_id","character_id","dialogue_text","sequence_order","event_type","chapter_bg_id") VALUES ('D034','CH003','CR001','MERDEKA!',7,'dialogue','BG006');
INSERT INTO "dialogue" ("dialogue_id","chapter_id","character_id","dialogue_text","sequence_order","event_type","chapter_bg_id") VALUES ('D035','CH003','CR005','MERDEKA!',8,'dialogue','BG006');
INSERT INTO "dialogue" ("dialogue_id","chapter_id","character_id","dialogue_text","sequence_order","event_type","chapter_bg_id") VALUES ('D036','CH003','CR001','MERDEKA!',9,'dialogue','BG006');
INSERT INTO "dialogue" ("dialogue_id","chapter_id","character_id","dialogue_text","sequence_order","event_type","chapter_bg_id") VALUES ('D037','CH003','CR005','MERDEKA!',10,'dialogue','BG006');
INSERT INTO "dialogue" ("dialogue_id","chapter_id","character_id","dialogue_text","sequence_order","event_type","chapter_bg_id") VALUES ('D038','CH003','CR001','MERDEKA!',11,'dialogue','BG006');
INSERT INTO "dialogue" ("dialogue_id","chapter_id","character_id","dialogue_text","sequence_order","event_type","chapter_bg_id") VALUES ('D039','CH003','CR005','MERDEKA!',12,'dialogue','BG006');
INSERT INTO "dialogue" ("dialogue_id","chapter_id","character_id","dialogue_text","sequence_order","event_type","chapter_bg_id") VALUES ('D040','CH003','CR001','MERDEKA!',13,'dialogue','BG006');
INSERT INTO "dialogue" ("dialogue_id","chapter_id","character_id","dialogue_text","sequence_order","event_type","chapter_bg_id") VALUES ('D041','CH003','CR005','MERDEKA!',14,'dialogue','BG006');
INSERT INTO "dialogue" ("dialogue_id","chapter_id","character_id","dialogue_text","sequence_order","event_type","chapter_bg_id") VALUES ('D042','CH003','CR001','MERDEKA!',15,'dialogue','BG006');
INSERT INTO "dialogue" ("dialogue_id","chapter_id","character_id","dialogue_text","sequence_order","event_type","chapter_bg_id") VALUES ('D043','CH003','CR005','MERDEKA!',16,'dialogue','BG006');
INSERT INTO "dialogue" ("dialogue_id","chapter_id","character_id","dialogue_text","sequence_order","event_type","chapter_bg_id") VALUES ('D044','CH003','CR001','MERDEKA!',17,'dialogue','BG006');
INSERT INTO "dialogue" ("dialogue_id","chapter_id","character_id","dialogue_text","sequence_order","event_type","chapter_bg_id") VALUES ('D045','CH003','CR005','MERDEKA!',18,'dialogue','BG006');
INSERT INTO "dialogue" ("dialogue_id","chapter_id","character_id","dialogue_text","sequence_order","event_type","chapter_bg_id") VALUES ('D046','CH003','CR005','101 cannon shots are fired to celebrate the birth of a new nation.',19,'narrator','BG006');
INSERT INTO "minigame" ("minigame_id","name","description","difficulty_level") VALUES ('MG001','Whack a Mole','Hit the mole that appears on the screen','Easy');
INSERT INTO "minigame" ("minigame_id","name","description","difficulty_level") VALUES ('MG002',' ⁠AimLab','Click on the circle that appears on the screen','Easy');
INSERT INTO "minigame_result" ("minigame_result_id","user_id","minigame_id","score","status","played_at") VALUES ('MGR001','USR023','MG001',5,'Pass','2026-04-26');
INSERT INTO "minigame_result" ("minigame_result_id","user_id","minigame_id","score","status","played_at") VALUES ('MGR002','USR006','MG001',4,'Fail','2026-04-21');
INSERT INTO "minigame_result" ("minigame_result_id","user_id","minigame_id","score","status","played_at") VALUES ('MGR003','USR003','MG001',4,'Fail','2026-04-20');
INSERT INTO "minigame_result" ("minigame_result_id","user_id","minigame_id","score","status","played_at") VALUES ('MGR004','USR011','MG001',5,'Pass','2026-04-26');
INSERT INTO "minigame_result" ("minigame_result_id","user_id","minigame_id","score","status","played_at") VALUES ('MGR005','USR010','MG001',5,'Pass','2026-04-24');
INSERT INTO "minigame_result" ("minigame_result_id","user_id","minigame_id","score","status","played_at") VALUES ('MGR006','USR019','MG001',5,'Fail','2026-04-26');
INSERT INTO "minigame_result" ("minigame_result_id","user_id","minigame_id","score","status","played_at") VALUES ('MGR007','USR005','MG002',5,'Pass','2026-04-22');
INSERT INTO "minigame_result" ("minigame_result_id","user_id","minigame_id","score","status","played_at") VALUES ('MGR008','USR014','MG001',5,'Pass','2026-04-21');
INSERT INTO "minigame_result" ("minigame_result_id","user_id","minigame_id","score","status","played_at") VALUES ('MGR009','USR004','MG001',5,'Pass','2026-04-21');
INSERT INTO "minigame_result" ("minigame_result_id","user_id","minigame_id","score","status","played_at") VALUES ('MGR010','USR013','MG002',5,'Pass','2026-04-24');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA001','USR003','QT001','C',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA002','USR003','QT002','C',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA003','USR003','QT003','A',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA004','USR003','QT004','B',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA005','USR003','QT005','D',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA006','USR003','QT006','C',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA007','USR003','QT007','A',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA008','USR003','QT008','C',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA009','USR003','QT009','B',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA010','USR003','QT010','A',0,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA011','USR003','QT011','C',1,'2026-04-21');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA012','USR003','QT012','A',1,'2026-04-21');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA013','USR003','QT013','D',1,'2026-04-21');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA014','USR003','QT014','B',1,'2026-04-21');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA015','USR003','QT015','B',0,'2026-04-21');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA016','USR004','QT001','C',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA017','USR004','QT002','C',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA018','USR004','QT003','A',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA019','USR004','QT004','B',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA020','USR004','QT005','D',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA021','USR004','QT006','C',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA022','USR004','QT007','A',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA023','USR004','QT008','C',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA024','USR004','QT009','B',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA025','USR004','QT010','C',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA026','USR005','QT001','C',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA027','USR005','QT002','C',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA028','USR005','QT003','A',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA029','USR005','QT004','B',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA030','USR005','QT005','D',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA031','USR005','QT006','C',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA032','USR005','QT007','B',0,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA033','USR005','QT008','A',0,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA034','USR005','QT009','A',0,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA035','USR005','QT010','A',0,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA036','USR006','QT001','C',1,'2026-04-21');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA037','USR006','QT002','C',1,'2026-04-21');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA038','USR006','QT003','A',1,'2026-04-21');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA039','USR006','QT004','B',1,'2026-04-21');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA040','USR006','QT005','D',1,'2026-04-21');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA041','USR006','QT006','C',1,'2026-04-21');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA042','USR006','QT007','A',1,'2026-04-21');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA043','USR006','QT008','C',1,'2026-04-21');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA044','USR006','QT009','A',0,'2026-04-21');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA045','USR006','QT010','A',0,'2026-04-21');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA046','USR007','QT001','C',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA047','USR007','QT002','C',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA048','USR007','QT003','A',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA049','USR007','QT004','B',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA050','USR007','QT005','D',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA051','USR007','QT006','C',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA052','USR007','QT007','A',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA053','USR007','QT008','C',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA054','USR007','QT009','B',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA055','USR007','QT010','C',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA056','USR007','QT011','C',1,'2026-04-21');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA057','USR007','QT012','A',1,'2026-04-21');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA058','USR007','QT013','D',1,'2026-04-21');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA059','USR007','QT014','B',1,'2026-04-21');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA060','USR007','QT015','B',0,'2026-04-21');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA061','USR007','QT016','C',1,'2026-04-22');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA062','USR007','QT017','B',1,'2026-04-22');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA063','USR007','QT018','C',1,'2026-04-22');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA064','USR007','QT019','C',1,'2026-04-22');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA065','USR007','QT020','B',1,'2026-04-22');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA066','USR007','QT021','C',1,'2026-04-22');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA067','USR007','QT022','C',1,'2026-04-22');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA068','USR007','QT023','C',1,'2026-04-22');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA069','USR007','QT024','B',1,'2026-04-22');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA070','USR007','QT025','A',1,'2026-04-22');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA071','USR009','QT001','C',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA072','USR009','QT002','C',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA073','USR009','QT003','A',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA074','USR009','QT004','B',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA075','USR009','QT005','D',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA076','USR009','QT006','C',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA077','USR009','QT007','A',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA078','USR009','QT008','A',0,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA079','USR009','QT009','A',0,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA080','USR009','QT010','A',0,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA081','USR010','QT001','C',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA082','USR010','QT002','C',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA083','USR010','QT003','A',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA084','USR010','QT004','B',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA085','USR010','QT005','D',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA086','USR010','QT006','C',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA087','USR010','QT007','A',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA088','USR010','QT008','C',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA089','USR010','QT009','A',0,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA090','USR010','QT010','A',0,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA091','USR012','QT001','C',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA092','USR012','QT002','C',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA093','USR012','QT003','A',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA094','USR012','QT004','B',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA095','USR012','QT005','D',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA096','USR012','QT006','C',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA097','USR012','QT007','A',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA098','USR012','QT008','C',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA099','USR012','QT009','B',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA100','USR012','QT010','A',0,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA101','USR013','QT001','C',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA102','USR013','QT002','C',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA103','USR013','QT003','A',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA104','USR013','QT004','B',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA105','USR013','QT005','D',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA106','USR013','QT006','C',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA107','USR013','QT007','A',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA108','USR013','QT008','A',0,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA109','USR013','QT009','A',0,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA110','USR013','QT010','A',0,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA111','USR015','QT001','C',1,'2026-04-21');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA112','USR015','QT002','C',1,'2026-04-21');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA113','USR015','QT003','A',1,'2026-04-21');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA114','USR015','QT004','B',1,'2026-04-21');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA115','USR015','QT005','D',1,'2026-04-21');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA116','USR015','QT006','C',1,'2026-04-21');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA117','USR015','QT007','A',1,'2026-04-21');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA118','USR015','QT008','C',1,'2026-04-21');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA119','USR015','QT009','B',1,'2026-04-21');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA120','USR015','QT010','A',0,'2026-04-21');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA121','USR015','QT011','C',1,'2026-04-22');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA122','USR015','QT012','A',1,'2026-04-22');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA123','USR015','QT013','D',1,'2026-04-22');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA124','USR015','QT014','B',1,'2026-04-22');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA125','USR015','QT015','B',0,'2026-04-22');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA126','USR017','QT001','C',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA127','USR017','QT002','C',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA128','USR017','QT003','A',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA129','USR017','QT004','B',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA130','USR017','QT005','D',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA131','USR017','QT006','C',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA132','USR017','QT007','A',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA133','USR017','QT008','C',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA134','USR017','QT009','B',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA135','USR017','QT010','C',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA136','USR019','QT001','C',1,'2026-04-21');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA137','USR019','QT002','C',1,'2026-04-21');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA138','USR019','QT003','A',1,'2026-04-21');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA139','USR019','QT004','B',1,'2026-04-21');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA140','USR019','QT005','D',1,'2026-04-21');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA141','USR019','QT006','C',1,'2026-04-21');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA142','USR019','QT007','B',0,'2026-04-21');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA143','USR019','QT008','A',0,'2026-04-21');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA144','USR019','QT009','A',0,'2026-04-21');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA145','USR019','QT010','A',0,'2026-04-21');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA146','USR021','QT001','C',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA147','USR021','QT002','C',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA148','USR021','QT003','A',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA149','USR021','QT004','B',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA150','USR021','QT005','D',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA151','USR021','QT006','C',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA152','USR021','QT007','A',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA153','USR021','QT008','C',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA154','USR021','QT009','B',1,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA155','USR021','QT010','A',0,'2026-04-20');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA156','USR022','QT001','C',1,'2026-04-22');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA157','USR022','QT002','C',1,'2026-04-22');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA158','USR022','QT003','A',1,'2026-04-22');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA159','USR022','QT004','B',1,'2026-04-22');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA160','USR022','QT005','D',1,'2026-04-22');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA161','USR022','QT006','C',1,'2026-04-22');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA162','USR022','QT007','A',1,'2026-04-22');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA163','USR022','QT008','C',1,'2026-04-22');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA164','USR022','QT009','A',0,'2026-04-22');
INSERT INTO "player_ans" ("player_ans_id","user_id","question_id","selected_ans","is_correct","answered_at") VALUES ('PA165','USR022','QT010','A',0,'2026-04-22');
INSERT INTO "player_reward" ("player_reward_id","user_id","reward_id","quantity") VALUES ('PR001','USR003','R001',2);
INSERT INTO "player_reward" ("player_reward_id","user_id","reward_id","quantity") VALUES ('PR002','USR003','R004',1);
INSERT INTO "player_reward" ("player_reward_id","user_id","reward_id","quantity") VALUES ('PR003','USR004','R002',1);
INSERT INTO "player_reward" ("player_reward_id","user_id","reward_id","quantity") VALUES ('PR004','USR004','R005',2);
INSERT INTO "player_reward" ("player_reward_id","user_id","reward_id","quantity") VALUES ('PR005','USR005','R003',1);
INSERT INTO "player_reward" ("player_reward_id","user_id","reward_id","quantity") VALUES ('PR006','USR006','R004',2);
INSERT INTO "player_reward" ("player_reward_id","user_id","reward_id","quantity") VALUES ('PR007','USR006','R006',1);
INSERT INTO "player_reward" ("player_reward_id","user_id","reward_id","quantity") VALUES ('PR008','USR007','R001',1);
INSERT INTO "player_reward" ("player_reward_id","user_id","reward_id","quantity") VALUES ('PR009','USR007','R002',1);
INSERT INTO "player_reward" ("player_reward_id","user_id","reward_id","quantity") VALUES ('PR010','USR008','R005',1);
INSERT INTO "player_reward" ("player_reward_id","user_id","reward_id","quantity") VALUES ('PR011','USR009','R004',3);
INSERT INTO "player_reward" ("player_reward_id","user_id","reward_id","quantity") VALUES ('PR012','USR010','R006',2);
INSERT INTO "progress" ("progress_id","user_id","chapter_id","status","last_accessed","attempts_count","score") VALUES ('P001','USR003','CH001','Completed','2026-04-20 11:00:00',1,90);
INSERT INTO "progress" ("progress_id","user_id","chapter_id","status","last_accessed","attempts_count","score") VALUES ('P002','USR003','CH002','Completed','2026-04-21 14:20:00',2,75);
INSERT INTO "progress" ("progress_id","user_id","chapter_id","status","last_accessed","attempts_count","score") VALUES ('P003','USR003','CH003','In Progress','2026-04-22 09:30:00',1,0);
INSERT INTO "progress" ("progress_id","user_id","chapter_id","status","last_accessed","attempts_count","score") VALUES ('P004','USR004','CH001','Completed','2026-04-20 10:45:00',1,100);
INSERT INTO "progress" ("progress_id","user_id","chapter_id","status","last_accessed","attempts_count","score") VALUES ('P005','USR004','CH002','Unlocked','2026-04-20 10:46:00',0,0);
INSERT INTO "progress" ("progress_id","user_id","chapter_id","status","last_accessed","attempts_count","score") VALUES ('P006','USR005','CH001','Completed','2026-04-20 15:10:00',3,60);
INSERT INTO "progress" ("progress_id","user_id","chapter_id","status","last_accessed","attempts_count","score") VALUES ('P007','USR005','CH002','Unlocked','2026-04-20 15:11:00',0,0);
INSERT INTO "progress" ("progress_id","user_id","chapter_id","status","last_accessed","attempts_count","score") VALUES ('P008','USR006','CH001','Completed','2026-04-21 11:00:00',1,80);
INSERT INTO "progress" ("progress_id","user_id","chapter_id","status","last_accessed","attempts_count","score") VALUES ('P009','USR006','CH002','In Progress','2026-04-22 16:45:00',1,0);
INSERT INTO "progress" ("progress_id","user_id","chapter_id","status","last_accessed","attempts_count","score") VALUES ('P010','USR007','CH001','Completed','2026-04-20 10:15:00',1,95);
INSERT INTO "progress" ("progress_id","user_id","chapter_id","status","last_accessed","attempts_count","score") VALUES ('P011','USR007','CH002','Completed','2026-04-21 12:30:00',1,85);
INSERT INTO "progress" ("progress_id","user_id","chapter_id","status","last_accessed","attempts_count","score") VALUES ('P012','USR007','CH003','Completed','2026-04-22 14:00:00',1,100);
INSERT INTO "progress" ("progress_id","user_id","chapter_id","status","last_accessed","attempts_count","score") VALUES ('P013','USR008','CH001','In Progress','2026-04-23 08:20:00',1,0);
INSERT INTO "progress" ("progress_id","user_id","chapter_id","status","last_accessed","attempts_count","score") VALUES ('P014','USR009','CH001','Completed','2026-04-20 09:00:00',2,70);
INSERT INTO "progress" ("progress_id","user_id","chapter_id","status","last_accessed","attempts_count","score") VALUES ('P015','USR009','CH002','Unlocked','2026-04-20 09:01:00',0,0);
INSERT INTO "progress" ("progress_id","user_id","chapter_id","status","last_accessed","attempts_count","score") VALUES ('P016','USR010','CH001','Completed','2026-04-20 13:40:00',1,85);
INSERT INTO "progress" ("progress_id","user_id","chapter_id","status","last_accessed","attempts_count","score") VALUES ('P017','USR010','CH002','Unlocked','2026-04-20 13:41:00',0,0);
INSERT INTO "progress" ("progress_id","user_id","chapter_id","status","last_accessed","attempts_count","score") VALUES ('P018','USR011','CH001','Unlocked','2026-04-24 09:15:00',0,0);
INSERT INTO "progress" ("progress_id","user_id","chapter_id","status","last_accessed","attempts_count","score") VALUES ('P019','USR012','CH001','Completed','2026-04-20 11:30:00',1,88);
INSERT INTO "progress" ("progress_id","user_id","chapter_id","status","last_accessed","attempts_count","score") VALUES ('P020','USR012','CH002','In Progress','2026-04-21 15:45:00',1,0);
INSERT INTO "progress" ("progress_id","user_id","chapter_id","status","last_accessed","attempts_count","score") VALUES ('P021','USR013','CH001','Completed','2026-04-20 14:00:00',2,72);
INSERT INTO "progress" ("progress_id","user_id","chapter_id","status","last_accessed","attempts_count","score") VALUES ('P022','USR013','CH002','Unlocked','2026-04-20 14:01:00',0,0);
INSERT INTO "progress" ("progress_id","user_id","chapter_id","status","last_accessed","attempts_count","score") VALUES ('P023','USR014','CH001','Unlocked','2026-04-25 10:00:00',0,0);
INSERT INTO "progress" ("progress_id","user_id","chapter_id","status","last_accessed","attempts_count","score") VALUES ('P024','USR015','CH001','Completed','2026-04-21 09:20:00',1,94);
INSERT INTO "progress" ("progress_id","user_id","chapter_id","status","last_accessed","attempts_count","score") VALUES ('P025','USR015','CH002','Completed','2026-04-22 11:10:00',1,82);
INSERT INTO "progress" ("progress_id","user_id","chapter_id","status","last_accessed","attempts_count","score") VALUES ('P026','USR015','CH003','In Progress','2026-04-23 16:30:00',1,0);
INSERT INTO "progress" ("progress_id","user_id","chapter_id","status","last_accessed","attempts_count","score") VALUES ('P027','USR016','CH001','In Progress','2026-04-24 13:45:00',1,0);
INSERT INTO "progress" ("progress_id","user_id","chapter_id","status","last_accessed","attempts_count","score") VALUES ('P028','USR017','CH001','Completed','2026-04-20 16:15:00',1,100);
INSERT INTO "progress" ("progress_id","user_id","chapter_id","status","last_accessed","attempts_count","score") VALUES ('P029','USR017','CH002','Unlocked','2026-04-20 16:16:00',0,0);
INSERT INTO "progress" ("progress_id","user_id","chapter_id","status","last_accessed","attempts_count","score") VALUES ('P030','USR018','CH001','Unlocked','2026-04-26 11:30:00',0,0);
INSERT INTO "progress" ("progress_id","user_id","chapter_id","status","last_accessed","attempts_count","score") VALUES ('P031','USR019','CH001','Completed','2026-04-21 10:45:00',3,64);
INSERT INTO "progress" ("progress_id","user_id","chapter_id","status","last_accessed","attempts_count","score") VALUES ('P032','USR019','CH002','Unlocked','2026-04-21 10:46:00',0,0);
INSERT INTO "progress" ("progress_id","user_id","chapter_id","status","last_accessed","attempts_count","score") VALUES ('P033','USR020','CH001','In Progress','2026-04-25 14:20:00',1,0);
INSERT INTO "progress" ("progress_id","user_id","chapter_id","status","last_accessed","attempts_count","score") VALUES ('P034','USR021','CH001','Completed','2026-04-20 08:50:00',1,90);
INSERT INTO "progress" ("progress_id","user_id","chapter_id","status","last_accessed","attempts_count","score") VALUES ('P035','USR021','CH002','Unlocked','2026-04-21 09:00:00',0,0);
INSERT INTO "progress" ("progress_id","user_id","chapter_id","status","last_accessed","attempts_count","score") VALUES ('P036','USR022','CH001','Completed','2026-04-22 13:10:00',1,78);
INSERT INTO "progress" ("progress_id","user_id","chapter_id","status","last_accessed","attempts_count","score") VALUES ('P037','USR022','CH002','Unlocked','2026-04-22 13:11:00',0,0);
INSERT INTO "progress" ("progress_id","user_id","chapter_id","status","last_accessed","attempts_count","score") VALUES ('P038','USR023','CH001','Unlocked','2026-04-27 15:00:00',0,0);
INSERT INTO "question" ("question_id","quiz_id","question_text","option_a","option_b","option_c","option_d","correct_answer","explanation") VALUES ('QT001','QZ001','On what date did Tunku Abdul Rahman become the leader of UMNO in this scene?','27 July 1955','16 September 1963','26 August 1951','31 August 1957','C','This was the day Tunku Abdul Rahman officially took over the leadership of UMNO.');
INSERT INTO "question" ("question_id","quiz_id","question_text","option_a","option_b","option_c","option_d","correct_answer","explanation") VALUES ('QT002','QZ001','Who was the predecessor of Tunku Abdul Rahman as leader of UMNO?','Tan Cheng Lock','British Governor','Dato Onn Jaafar','Tun VT Sambathan','C','Dato Onn Jaafar led UMNO before Tunku Abdul Rahman was chosen. ');
INSERT INTO "question" ("question_id","quiz_id","question_text","option_a","option_b","option_c","option_d","correct_answer","explanation") VALUES ('QT003','QZ001','Which two leaders did Tunku Abdul Rahman meet?','Tan Cheng Lock and Tun VT Sambathan','Tun Dr. Mahathir and Lee Kuan Yew','British officers','Dato Onn Jaafar and Sultan of Johor','A','He met with the leaders of the Chinese and Indian associations to form an alliance. ');
INSERT INTO "question" ("question_id","quiz_id","question_text","option_a","option_b","option_c","option_d","correct_answer","explanation") VALUES ('QT004','QZ001','Tan Cheng Lock was the leader of which organization?','MIC','MCA','PAS','UMNO','B','Tan Cheng Lock was the leader of the Malaysian Chinese Association. ');
INSERT INTO "question" ("question_id","quiz_id","question_text","option_a","option_b","option_c","option_d","correct_answer","explanation") VALUES ('QT005','QZ001','Tun VT Sambathan represented which group?','Malays','British','Chinese','Indians','D','Tun VT Sambathan was the leader representing the Malaysian Indian Congress. ');
INSERT INTO "question" ("question_id","quiz_id","question_text","option_a","option_b","option_c","option_d","correct_answer","explanation") VALUES ('QT006','QZ001','What was the purpose of the first general election?','To form a military','To declare independence','To choose representatives for the Federal Legislative Council','To elect a king','C','The election was held so the people could choose their own government leaders');
INSERT INTO "question" ("question_id","quiz_id","question_text","option_a","option_b","option_c","option_d","correct_answer","explanation") VALUES ('QT007','QZ001','Why did Tunku Abdul Rahman want to work with MCA and MIC?','To unite different communities for independence','To gain financial support','To defeat other countries','To start a business','A','Working together showed that all races in Malaya wanted independence');
INSERT INTO "question" ("question_id","quiz_id","question_text","option_a","option_b","option_c","option_d","correct_answer","explanation") VALUES ('QT008','QZ001','What was the significance of forming the Alliance Party?','It ended elections','It removed leaders','It promoted unity among races','It divided the people','C','It was the first time different racial groups joined together as one party');
INSERT INTO "question" ("question_id","quiz_id","question_text","option_a","option_b","option_c","option_d","correct_answer","explanation") VALUES ('QT009','QZ001','How many seats did the Alliance Party win?','49 out of 52','51 out of 52','50 out of 52','52 out of 52','B','Winning 51 out of 52 seats was a massive victory for the Alliance');
INSERT INTO "question" ("question_id","quiz_id","question_text","option_a","option_b","option_c","option_d","correct_answer","explanation") VALUES ('QT010','QZ001','Why was unity between UMNO, MCA, and MIC important?','It stopped elections','It benefited only one group','It showed cooperation among different races','It weakened the country','C','It proved that different communities could live and work together peacefully');
INSERT INTO "question" ("question_id","quiz_id","question_text","option_a","option_b","option_c","option_d","correct_answer","explanation") VALUES ('QT011','QZ002','Why should we grant your country independence from us?','We want our independence because you only use our resources.','It would be better if we governed because you make bad laws.','We are now capable of governing as we have capable leaders.','Because we want to. Isn''t that enough?','C','A kind and professional answer shows we are ready to lead our own nation');
INSERT INTO "question" ("question_id","quiz_id","question_text","option_a","option_b","option_c","option_d","correct_answer","explanation") VALUES ('QT012','QZ002','What assurance can you give us that these communities will remain united?','We have already proven our ability to work together.','That is no longer your concern.','You should have promoted harmony during your own rule.','We are all Malayans at the end of the day.','A','The Alliance Party is proof that our different communities can cooperate');
INSERT INTO "question" ("question_id","quiz_id","question_text","option_a","option_b","option_c","option_d","correct_answer","explanation") VALUES ('QT013','QZ002','How do you intend to sustain the economy without our presence?','We will manage fine; we do not need Britain''s help.','The resources were ours and should benefit our people.','We will simply find other trading partners.','We intend to maintain strong and fair economic ties with Britain.','D','Keeping good business ties with other countries helps our economy grow');
INSERT INTO "question" ("question_id","quiz_id","question_text","option_a","option_b","option_c","option_d","correct_answer","explanation") VALUES ('QT014','QZ002','How will your government manage the communist insurgency (The Emergency)?','Our own forces can handle it easily.','We propose a formal defence agreement with Britain.','We will handle troublemakers firmly.','Our people have always defended this land.','B','A partnership for safety helps protect the country while we are still growing');
INSERT INTO "question" ("question_id","quiz_id","question_text","option_a","option_b","option_c","option_d","correct_answer","explanation") VALUES ('QT015','QZ002','What reason do we have to trust that Malaya will remain a friendly nation?','We propose that Malaya remain a member of the Commonwealth.','You have our word as leaders and gentlemen.','Malaya will always act in its own best interest.','Because we have no reason not to be friendly.','A','Staying in the Commonwealth shows we value long-lasting partnerships');
INSERT INTO "question" ("question_id","quiz_id","question_text","option_a","option_b","option_c","option_d","correct_answer","explanation") VALUES ('QT016','QZ003','What historic event is taking place?','Formation of Malaysia','End of World War II','Independence of the Federation of Malaya','Signing of a trade agreement','C','This was the moment Malaya finally became its own free country');
INSERT INTO "question" ("question_id","quiz_id","question_text","option_a","option_b","option_c","option_d","correct_answer","explanation") VALUES ('QT017','QZ003','On what date did this event occur?','16 September 1963','31 August 1957','1 January 1957','31 August 1965','B','August 31st, 1957 is the official birthday of our independence');
INSERT INTO "question" ("question_id","quiz_id","question_text","option_a","option_b","option_c","option_d","correct_answer","explanation") VALUES ('QT018','QZ003','Which flag was lowered during the ceremony?','Malayan Flag','ASEAN Flag','Union Jack','State Flag','C','The British Union Jack was lowered to show their rule had ended');
INSERT INTO "question" ("question_id","quiz_id","question_text","option_a","option_b","option_c","option_d","correct_answer","explanation") VALUES ('QT019','QZ003','How many times was "Merdeka" shouted?','5','6','7','10','C','Tunku Abdul Rahman shouted "Merdeka" 7 times with the crowd');
INSERT INTO "question" ("question_id","quiz_id","question_text","option_a","option_b","option_c","option_d","correct_answer","explanation") VALUES ('QT020','QZ003','What does "Merdeka" mean?','Peace','Independence','Unity','Strength','B','Merdeka is the special word for our freedom and independence');
INSERT INTO "question" ("question_id","quiz_id","question_text","option_a","option_b","option_c","option_d","correct_answer","explanation") VALUES ('QT021','QZ003','What does the raising of the Malayan flag represent?','Economic growth','Cultural unity','Independence and sovereignty','Military strength','C','A new flag in the sky shows that our nation is now free');
INSERT INTO "question" ("question_id","quiz_id","question_text","option_a","option_b","option_c","option_d","correct_answer","explanation") VALUES ('QT022','QZ003','What do the 101 cannon shots represent?','A warning signal','Celebration of a festival','Official independence of the country','Military training','C','The loud cannon shots announced to the world that we were free');
INSERT INTO "question" ("question_id","quiz_id","question_text","option_a","option_b","option_c","option_d","correct_answer","explanation") VALUES ('QT023','QZ003','What emotions were likely felt by the people?','Anger and fear','Sadness and regret','Joy and pride','Boredom','C','The people were very happy and proud to see their country become independent');
INSERT INTO "question" ("question_id","quiz_id","question_text","option_a","option_b","option_c","option_d","correct_answer","explanation") VALUES ('QT024','QZ003','What does this event represent historically?','Beginning of colonization','End of colonial rule','A trade agreement','A war victory','B','It marks the end of the time when other countries ruled over us');
INSERT INTO "question" ("question_id","quiz_id","question_text","option_a","option_b","option_c","option_d","correct_answer","explanation") VALUES ('QT025','QZ003','Why is this moment important today?','It marks independence and national identity','It changed the language','It started a war','It ended celebrations','A','It reminds us who we are as a united and free nation');
INSERT INTO "quiz" ("quiz_id","chapter_id","title","type") VALUES ('QZ001','CH001','The Road to Unity Quiz','quiz');
INSERT INTO "quiz" ("quiz_id","chapter_id","title","type") VALUES ('QZ002','CH002','The London Independence Debate','debate');
INSERT INTO "quiz" ("quiz_id","chapter_id","title","type") VALUES ('QZ003','CH003','The Merdeka Proclamation Quiz','quiz');
INSERT INTO "reward" ("reward_id","reward_name","description","reward_type","reward_pic") VALUES ('R001','Regenerate Health','Restores 15% of health during the debate.','debate','Assets/R001.png');
INSERT INTO "reward" ("reward_id","reward_name","description","reward_type","reward_pic") VALUES ('R002','Shield','Blocks all incoming damage for one round in the debate.','debate','Assets/R002.png');
INSERT INTO "reward" ("reward_id","reward_name","description","reward_type","reward_pic") VALUES ('R003','Damage Reduction','Reduces incoming damage for the next few rounds.','debate','Assets/R003.png');
INSERT INTO "reward" ("reward_id","reward_name","description","reward_type","reward_pic") VALUES ('R004','Hint','Provides a hint to help answer the question correctly.','both','Assets/R004.png');
INSERT INTO "reward" ("reward_id","reward_name","description","reward_type","reward_pic") VALUES ('R005','Second Chance','Allows the player to retry a question after an incorrect attempt.','quiz','Assets/R005.png');
INSERT INTO "reward" ("reward_id","reward_name","description","reward_type","reward_pic") VALUES ('R006','Extra Time','Adds additional time to answer quiz questions.','quiz','Assets/R006.png');
INSERT INTO "user" ("user_id","username","email","password","user_role","profile_picture","classroom_id","otp_code","otp_created_at") VALUES ('USR001','MrLim','lim@school.com','pass123','teacher','Assets/USR001.png',NULL,NULL,NULL);
INSERT INTO "user" ("user_id","username","email","password","user_role","profile_picture","classroom_id","otp_code","otp_created_at") VALUES ('USR002','MsAisha','aisha@school.com','pass123','teacher','Assets/USR002.png',NULL,NULL,NULL);
INSERT INTO "user" ("user_id","username","email","password","user_role","profile_picture","classroom_id","otp_code","otp_created_at") VALUES ('USR003','JamalC','jamal@gmail.com','pass123','student','Assets/USR003.png','C001',NULL,NULL);
INSERT INTO "user" ("user_id","username","email","password","user_role","profile_picture","classroom_id","otp_code","otp_created_at") VALUES ('USR004','SitiN','siti@gmail.com','pass123','student','Assets/USR004.png','C001',483921,'2026-04-20 10:00:00');
INSERT INTO "user" ("user_id","username","email","password","user_role","profile_picture","classroom_id","otp_code","otp_created_at") VALUES ('USR005','ArjunK','arjun@gmail.com','pass123','student','Assets/USR005.png','C001',NULL,NULL);
INSERT INTO "user" ("user_id","username","email","password","user_role","profile_picture","classroom_id","otp_code","otp_created_at") VALUES ('USR006','MeiLing','meiling@gmail.com','pass123','student','Assets/USR006.png','C001',NULL,NULL);
INSERT INTO "user" ("user_id","username","email","password","user_role","profile_picture","classroom_id","otp_code","otp_created_at") VALUES ('USR007','DanielT','daniel@gmail.com','pass123','student','Assets/USR007.png','C001',739201,'2026-04-20 10:08:20');
INSERT INTO "user" ("user_id","username","email","password","user_role","profile_picture","classroom_id","otp_code","otp_created_at") VALUES ('USR008','HafizN','hafiz@gmail.com','pass123','student','Assets/USR008.png','C001',NULL,NULL);
INSERT INTO "user" ("user_id","username","email","password","user_role","profile_picture","classroom_id","otp_code","otp_created_at") VALUES ('USR009','AliciaW','alicia@gmail.com','pass123','student','Assets/USR009.png','C001',NULL,NULL);
INSERT INTO "user" ("user_id","username","email","password","user_role","profile_picture","classroom_id","otp_code","otp_created_at") VALUES ('USR010','FarhanZ','farhan@gmail.com','pass123','student','Assets/USR010.png','C001',652198,0);
INSERT INTO "user" ("user_id","username","email","password","user_role","profile_picture","classroom_id","otp_code","otp_created_at") VALUES ('USR011','NishaR','nisha@gmail.com','pass123','student','Assets/USR011.png','C001',NULL,NULL);
INSERT INTO "user" ("user_id","username","email","password","user_role","profile_picture","classroom_id","otp_code","otp_created_at") VALUES ('USR012','JasonL','jason@gmail.com','pass123','student','Assets/USR012.png','C001',NULL,NULL);
INSERT INTO "user" ("user_id","username","email","password","user_role","profile_picture","classroom_id","otp_code","otp_created_at") VALUES ('USR013','HaziqM','haziq@gmail.com','pass123','student','Assets/USR013.png','C002',NULL,NULL);
INSERT INTO "user" ("user_id","username","email","password","user_role","profile_picture","classroom_id","otp_code","otp_created_at") VALUES ('USR014','ChloeT','chloe@gmail.com','pass123','student','Assets/USR014.png','C002',NULL,NULL);
INSERT INTO "user" ("user_id","username","email","password","user_role","profile_picture","classroom_id","otp_code","otp_created_at") VALUES ('USR015','RyanK','ryan@gmail.com','pass123','student','Assets/USR015.png','C002',918273,'2026-04-20 10:33:20');
INSERT INTO "user" ("user_id","username","email","password","user_role","profile_picture","classroom_id","otp_code","otp_created_at") VALUES ('USR016','SaraL','sara@gmail.com','pass123','student','Assets/USR016.png','C002',NULL,NULL);
INSERT INTO "user" ("user_id","username","email","password","user_role","profile_picture","classroom_id","otp_code","otp_created_at") VALUES ('USR017','AmirH','amir@gmail.com','pass123','student','Assets/USR017.png','C003',NULL,NULL);
INSERT INTO "user" ("user_id","username","email","password","user_role","profile_picture","classroom_id","otp_code","otp_created_at") VALUES ('USR018','YukiTan','yuki@gmail.com','pass123','student','Assets/USR018.png','C003',564738,'2026-04-20 10:50:00');
INSERT INTO "user" ("user_id","username","email","password","user_role","profile_picture","classroom_id","otp_code","otp_created_at") VALUES ('USR019','DeepaS','deepa@gmail.com','pass123','student','Assets/USR019.png','C003',NULL,NULL);
INSERT INTO "user" ("user_id","username","email","password","user_role","profile_picture","classroom_id","otp_code","otp_created_at") VALUES ('USR020','ZulF','zul@gmail.com','pass123','student','Assets/USR020.png','C004',NULL,NULL);
INSERT INTO "user" ("user_id","username","email","password","user_role","profile_picture","classroom_id","otp_code","otp_created_at") VALUES ('USR021','BenW','ben@gmail.com','pass123','student','Assets/USR021.png','C004',NULL,NULL);
INSERT INTO "user" ("user_id","username","email","password","user_role","profile_picture","classroom_id","otp_code","otp_created_at") VALUES ('USR022','LinaG','lina@gmail.com','pass123','student','Assets/USR022.png','C005',NULL,NULL);
INSERT INTO "user" ("user_id","username","email","password","user_role","profile_picture","classroom_id","otp_code","otp_created_at") VALUES ('USR023','OmarK','omar@gmail.com','pass123','student','Assets/USR023.png','C005',837261,'2026-04-20 11:00:00');
COMMIT;
