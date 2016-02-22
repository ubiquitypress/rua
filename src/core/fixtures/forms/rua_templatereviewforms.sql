# ************************************************************
# Sequel Pro SQL dump
# Version 4499
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: 127.0.0.1 (MySQL 5.5.44-0ubuntu0.14.04.1)
# Database: rua_template
# Generation Time: 2016-02-22 12:22:50 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table review_form
# ------------------------------------------------------------
SET FOREIGN_KEY_CHECKS=0;

DROP TABLE IF EXISTS `review_form`;

CREATE TABLE `review_form` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `ref` varchar(20) NOT NULL,
  `intro_text` longtext NOT NULL,
  `completion_text` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `review_form` WRITE;
/*!40000 ALTER TABLE `review_form` DISABLE KEYS */;

INSERT INTO `review_form` (`id`, `name`, `ref`, `intro_text`, `completion_text`)
VALUES
	(1,'Peer review form','template-review-form','<p>Many thanks for agreeing to review this proposed book title, we are very grateful. Please complete each of the sections in the review form in as much detail as possible. You are also able to upload an annotated version of the manuscript, should you wish to have comments directly associated with the text. For edited books, please provide a review for each chapter. If you have any questions, then please contact us.</p>','<p>Many thanks for completing the review of this book proposal, your efforts are greatly appreciated. Should you have any questions, please get in touch.</p>'),
	(2,'Proposal review form','proposal-review-form','<p>Many thanks for agreeing to review this book proposal, we are very grateful. Please complete each of the sections detailed in the review form. If you have any questions, then please contact us.</p>','<p>Many thanks for completing the review of this book proposal, your efforts are greatly appreciated. Should you have any questions, please get in touch.</p>'),
	(3,'Additional information requested','template-additional','Thank you for providing your review feedback. There is some more information that we would like your opinion on. This has been detailed in our email to you. Please use the text box available in the review page to provide this information. Many thanks.','Many thanks for completing this task, it is much appreciated. Should the editor require further information then they will be in touch. If you have questions regarding this book then please feel free to get in touch with the editor.');

/*!40000 ALTER TABLE `review_form` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table review_form_form_fields
# ------------------------------------------------------------

DROP TABLE IF EXISTS `review_form_form_fields`;

CREATE TABLE `review_form_form_fields` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `form_id` int(11) NOT NULL,
  `formelementsrelationship_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `form_id` (`form_id`,`formelementsrelationship_id`),
  KEY `D03fdfd27b235ea18d0870a069598dad` (`formelementsrelationship_id`),
  CONSTRAINT `D03fdfd27b235ea18d0870a069598dad` FOREIGN KEY (`formelementsrelationship_id`) REFERENCES `review_formelementsrelationship` (`id`),
  CONSTRAINT `review_form_form_fiel_form_id_52b739a411d08385_fk_review_form_id` FOREIGN KEY (`form_id`) REFERENCES `review_form` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `review_form_form_fields` WRITE;
/*!40000 ALTER TABLE `review_form_form_fields` DISABLE KEYS */;

INSERT INTO `review_form_form_fields` (`id`, `form_id`, `formelementsrelationship_id`)
VALUES
	(747,1,5),
	(749,1,8),
	(750,1,9),
	(766,1,41),
	(767,1,42),
	(768,1,43),
	(769,1,44),
	(770,1,45),
	(753,2,1),
	(763,2,38),
	(764,2,39),
	(765,2,40),
	(771,3,46);

/*!40000 ALTER TABLE `review_form_form_fields` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table review_formelement
# ------------------------------------------------------------

DROP TABLE IF EXISTS `review_formelement`;

CREATE TABLE `review_formelement` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(1000) NOT NULL,
  `choices` varchar(500) DEFAULT NULL,
  `field_type` varchar(100) NOT NULL,
  `required` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `review_formelement` WRITE;
/*!40000 ALTER TABLE `review_formelement` DISABLE KEYS */;

INSERT INTO `review_formelement` (`id`, `name`, `choices`, `field_type`, `required`)
VALUES
	(1,'Reviewer name','','text',1),
	(2,'Editorial Recommendation','Accept | Minor revisions | Major revisions | Reject','select',1),
	(5,'Full peer-review','Yes|No|Maybe','select',1),
	(6,'Are conclusions presented in an appropriate fashion and supported by the data?','','textarea',1),
	(8,'Are chapters presented in an intelligible fashion and written to a high standard of English? Please indicate if further copyediting is required.','','textarea',1),
	(9,'Do you believe that any chapters have significant errors or weaknesses that should prevent publication? If yes, please state what.','','textarea',1),
	(11,'Does the book read well as a whole? Is the structure of the book easy to follow?','','textarea',1),
	(12,'Do the Forward and Epilogue/Introduction and Conclusion introduce and summarise the content of the book and subject matter adequately?','','textarea',1),
	(14,'Competing interests','','textarea',1),
	(17,'Comments to the publisher','','textarea',0),
	(18,'General feedback to the publisher','','textarea',1),
	(19,'Feedback to the author(s)','','textarea',0),
	(20,'Full peer-review?','Yes|Maybe|No','select',1),
	(21,'Are conclusions presented in an appropriate fashion and supported by the data?','','textarea',0),
	(22,'If present, are experiments, statistics, and other analyses performed to a high standard and are described in sufficient detail?','','textarea',0),
	(23,'Are chapters presented in an intelligible fashion and written to a high standard of English? Please indicate if further copyediting is required and if specific chapters require more attention than others','','textarea',0),
	(24,'Comments to the author(s)?','','textarea',0),
	(25,'Comments to the publisher','','textarea',0),
	(26,'Additional information','','textarea',0);

/*!40000 ALTER TABLE `review_formelement` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table review_formelementsrelationship
# ------------------------------------------------------------

DROP TABLE IF EXISTS `review_formelementsrelationship`;

CREATE TABLE `review_formelementsrelationship` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `order` int(11) NOT NULL,
  `width` varchar(20) NOT NULL,
  `help_text` longtext,
  `element_id` int(11) NOT NULL,
  `form_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `review_form_element_id_619ed3ab3e00101e_fk_review_formelement_id` (`element_id`),
  KEY `review_formelementsre_form_id_22a727b56ae1c245_fk_review_form_id` (`form_id`),
  CONSTRAINT `review_formelementsre_form_id_22a727b56ae1c245_fk_review_form_id` FOREIGN KEY (`form_id`) REFERENCES `review_form` (`id`),
  CONSTRAINT `review_form_element_id_619ed3ab3e00101e_fk_review_formelement_id` FOREIGN KEY (`element_id`) REFERENCES `review_formelement` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `review_formelementsrelationship` WRITE;
/*!40000 ALTER TABLE `review_formelementsrelationship` DISABLE KEYS */;

INSERT INTO `review_formelementsrelationship` (`id`, `order`, `width`, `help_text`, `element_id`, `form_id`)
VALUES
	(1,1,'6','',1,2),
	(5,4,'col-md-12','',9,1),
	(8,5,'col-md-12','',11,1),
	(9,6,'col-md-12','',12,1),
	(38,2,'col-md-12','Please give an overview of the book proposal. Please give your opinion on 1) whether the objectives, themes and arguments of the proposed book would be a welcome addition to the subject; 2) if there are obvious additions to the content of the book that would enhance the use and understanding of the subject area; 3) if the structure of the book has been laid out in a logical manner; 4) if the target audience would benefit from such a publication; 5) if the author are qualified/informed enough to publish content in this subject.',18,2),
	(39,3,'col-md-12','If you have specific feedback suggesting ways in which the proposal could be edited to enhance the quality of the book, please add comments here.',19,2),
	(40,4,'col-md-12','If the book is accepted for full submission and peer-review, would you be interested in reviewing the book? (note: a positive indication here does not commit you to any review task in the future. You will be able to decline the invitation, should be it made in the future)',20,2),
	(41,1,'col-md-12','',21,1),
	(42,2,'col-md-12','',22,1),
	(43,3,'col-md-12','',23,1),
	(44,7,'col-md-12','',24,1),
	(45,8,'col-md-12','Please provide any additional information to the publisher, particularly if there are specific revisions that the book requires',25,1),
	(46,1,'col-md-12','Please comment on the questions asked by the press Editor as fully as possible.',26,3);

/*!40000 ALTER TABLE `review_formelementsrelationship` ENABLE KEYS */;
UNLOCK TABLES;



/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
