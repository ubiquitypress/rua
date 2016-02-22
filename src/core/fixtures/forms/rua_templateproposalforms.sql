# ************************************************************
# Sequel Pro SQL dump
# Version 4499
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: 127.0.0.1 (MySQL 5.5.44-0ubuntu0.14.04.1)
# Database: rua_template
# Generation Time: 2016-02-22 12:22:31 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table core_proposalform
# ------------------------------------------------------------
SET FOREIGN_KEY_CHECKS=0;

DROP TABLE IF EXISTS `core_proposalform`;

CREATE TABLE `core_proposalform` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `ref` varchar(20) NOT NULL,
  `intro_text` longtext NOT NULL,
  `completion_text` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `core_proposalform` WRITE;
/*!40000 ALTER TABLE `core_proposalform` DISABLE KEYS */;

INSERT INTO `core_proposalform` (`id`, `name`, `ref`, `intro_text`, `completion_text`)
VALUES
	(2,'Proposal form','template-proposal','<p>To submit a book proposal, please complete the below form.</p>','<p>Many thanks for completing the book proposal form, one of our book editors will contact you once we have examined the information provided.</p> <p>Kind regards</p>');

/*!40000 ALTER TABLE `core_proposalform` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table core_proposalform_proposal_fields
# ------------------------------------------------------------

DROP TABLE IF EXISTS `core_proposalform_proposal_fields`;

CREATE TABLE `core_proposalform_proposal_fields` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `proposalform_id` int(11) NOT NULL,
  `proposalformelementsrelationship_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `proposalform_id` (`proposalform_id`,`proposalformelementsrelationship_id`),
  KEY `d7f303aac1fa0a4c8c3d84c21b0d3b44` (`proposalformelementsrelationship_id`),
  CONSTRAINT `core_pr_proposalform_id_2851f2ae3729470c_fk_core_proposalform_id` FOREIGN KEY (`proposalform_id`) REFERENCES `core_proposalform` (`id`),
  CONSTRAINT `d7f303aac1fa0a4c8c3d84c21b0d3b44` FOREIGN KEY (`proposalformelementsrelationship_id`) REFERENCES `core_proposalformelementsrelationship` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `core_proposalform_proposal_fields` WRITE;
/*!40000 ALTER TABLE `core_proposalform_proposal_fields` DISABLE KEYS */;

INSERT INTO `core_proposalform_proposal_fields` (`id`, `proposalform_id`, `proposalformelementsrelationship_id`)
VALUES
	(1,2,2),
	(2,2,3),
	(3,2,4),
	(4,2,5),
	(5,2,6),
	(6,2,7),
	(7,2,8),
	(8,2,9),
	(9,2,10),
	(10,2,11),
	(11,2,12),
	(12,2,13),
	(16,2,17);

/*!40000 ALTER TABLE `core_proposalform_proposal_fields` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table core_proposalformelement
# ------------------------------------------------------------

DROP TABLE IF EXISTS `core_proposalformelement`;

CREATE TABLE `core_proposalformelement` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(1000) NOT NULL,
  `choices` varchar(500) DEFAULT NULL,
  `field_type` varchar(100) NOT NULL,
  `required` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `core_proposalformelement` WRITE;
/*!40000 ALTER TABLE `core_proposalformelement` DISABLE KEYS */;

INSERT INTO `core_proposalformelement` (`id`, `name`, `choices`, `field_type`, `required`)
VALUES
	(1,'Element #1','','text',1),
	(2,'Email','','email',1),
	(3,'ORCID','','text',1),
	(4,'Institution','','text',1),
	(5,'Series','','text',0),
	(6,'Brief description','','textarea',1),
	(7,'Outline','','textarea',1),
	(8,'Author and editor details','','textarea',1),
	(9,'Audience & Similar books','','textarea',1),
	(10,'Illustrations and tables','','text',1),
	(11,'Estimated word count','','text',1),
	(12,'Estimated submission date','','date',1),
	(13,'Supporting file','','upload',0),
	(15,'Additional Information','','textarea',0);

/*!40000 ALTER TABLE `core_proposalformelement` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table core_proposalformelementsrelationship
# ------------------------------------------------------------

DROP TABLE IF EXISTS `core_proposalformelementsrelationship`;

CREATE TABLE `core_proposalformelementsrelationship` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `order` int(11) NOT NULL,
  `help_text` longtext,
  `element_id` int(11) NOT NULL,
  `form_id` int(11) NOT NULL,
  `width` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core__element_id_5c439ddd560876d5_fk_core_proposalformelement_id` (`element_id`),
  KEY `core_proposalfo_form_id_7b7d1d3929c2b9fc_fk_core_proposalform_id` (`form_id`),
  CONSTRAINT `core_proposalfo_form_id_7b7d1d3929c2b9fc_fk_core_proposalform_id` FOREIGN KEY (`form_id`) REFERENCES `core_proposalform` (`id`),
  CONSTRAINT `core__element_id_5c439ddd560876d5_fk_core_proposalformelement_id` FOREIGN KEY (`element_id`) REFERENCES `core_proposalformelement` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `core_proposalformelementsrelationship` WRITE;
/*!40000 ALTER TABLE `core_proposalformelementsrelationship` DISABLE KEYS */;

INSERT INTO `core_proposalformelementsrelationship` (`id`, `order`, `help_text`, `element_id`, `form_id`, `width`)
VALUES
	(2,1,'',2,2,'col-md-6'),
	(3,2,'',3,2,'col-md-6'),
	(4,3,'',4,2,'col-md-6'),
	(5,4,'',5,2,'col-md-6'),
	(6,5,'Please describe the proposed book in a few paragraphs. Set out the objectives, themes and arguments of the proposed book. Which academic discipline/s would you suggest it falls within, and why is this book necessary? If the book is to be part of a series, please provide the name of the series and give a brief description of each of the volumes you have in mind or have already published.',6,2,'col-md-12'),
	(7,6,'Please list the proposed table of contents for the book, with a 100-200 word description of each chapter. If you plan to approach others to contribute chapters to the book please provide the names and affiliations of those contributing authors.',7,2,'col-md-12'),
	(8,7,'Please provide a brief biography for each of the author(s), including academic/professional experience, past publications and relevant research. ',8,2,'col-md-12'),
	(9,8,'Please provide information about the intended readership of the proposed book (scientific disciplines, industries, level of education achieved, for books which can be used in university courses names of typical courses, etc.). Please also list other books which are most similar to your proposed book in terms of coverage and/or readership and describe how your book would differentiate to existing similar books. Against this background, please explain why there is a need for the proposed book? If it is a series, give a brief summary of where you see the series in three years’ time, e.g. how many volumes do you envisage there to be.',9,2,'col-md-12'),
	(10,9,'Approximately how many illustrations and tables will be included within the book?',10,2,'col-md-6'),
	(11,10,'Please provide an estimate of the total number of words to be included in the book.',11,2,'col-md-6'),
	(12,11,'Date the complete manuscript will be finalised and submitted for review.',12,2,'col-md-6'),
	(13,12,'If you have any draft chapters or chapters that have been published elsewhere, please upload them.',13,2,'col-md-6'),
	(17,13,'Any additional information you think may support your proposal that is not covered by any of the other questions.',15,2,'col-md-12');

/*!40000 ALTER TABLE `core_proposalformelementsrelationship` ENABLE KEYS */;
UNLOCK TABLES;



/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
