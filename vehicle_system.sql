/*
SQLyog Ultimate v12.08 (64 bit)
MySQL - 5.7.13-log : Database - vehicle_system
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`vehicle_system` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `vehicle_system`;

/*Table structure for table `alembic_version` */

DROP TABLE IF EXISTS `alembic_version`;

CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `alembic_version` */

insert  into `alembic_version`(`version_num`) values ('a65ab5a1cff8');

/*Table structure for table `bike` */

DROP TABLE IF EXISTS `bike`;

CREATE TABLE `bike` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `state` int(11) DEFAULT NULL,
  `type` int(11) DEFAULT NULL,
  `charge` int(11) DEFAULT NULL,
  `latitude` float DEFAULT NULL,
  `longitude` float DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

/*Data for the table `bike` */

insert  into `bike`(`id`,`state`,`type`,`charge`,`latitude`,`longitude`) values (2,1,1,100,55.86,-4.3),(3,1,1,100,55.87,-4.31),(4,1,1,100,55.88,-4.32),(5,1,1,100,55.85,-4.29),(6,1,1,100,55.84,-4.28);

/*Table structure for table `email_captcha` */

DROP TABLE IF EXISTS `email_captcha`;

CREATE TABLE `email_captcha` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(100) DEFAULT NULL,
  `captcha` varchar(10) DEFAULT NULL,
  `create_time` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

/*Data for the table `email_captcha` */

insert  into `email_captcha`(`id`,`email`,`captcha`,`create_time`) values (1,'zcm200605@163.com','utm4VH','2022-10-03');

/*Table structure for table `operation` */

DROP TABLE IF EXISTS `operation`;

CREATE TABLE `operation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `create_time` date DEFAULT NULL,
  `type` int(11) DEFAULT NULL,
  `is_completed` int(11) DEFAULT NULL,
  `bike_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `bike_id` (`bike_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `operation_ibfk_1` FOREIGN KEY (`bike_id`) REFERENCES `bike` (`id`),
  CONSTRAINT `operation_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `operation` */

/*Table structure for table `topup_order` */

DROP TABLE IF EXISTS `topup_order`;

CREATE TABLE `topup_order` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `create_time` date DEFAULT NULL,
  `amount` float DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `topup_order_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `topup_order` */

/*Table structure for table `user` */

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(200) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `state` int(11) DEFAULT NULL,
  `role` int(11) DEFAULT NULL,
  `balance` float DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

/*Data for the table `user` */

insert  into `user`(`id`,`username`,`password`,`email`,`state`,`role`,`balance`) values (1,'Zhang_CNN','pbkdf2:sha256:260000$iil71J9GJwSOpOia$4f04723332615de3aa6d549e4b822819076333f4b404b5e78067de9435c03510','zcm200605@163.com',1,1,10000);

/*Table structure for table `vehicle_order` */

DROP TABLE IF EXISTS `vehicle_order`;

CREATE TABLE `vehicle_order` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `create_time` date DEFAULT NULL,
  `finish_time` date DEFAULT NULL,
  `state` int(11) DEFAULT NULL,
  `amount` float DEFAULT NULL,
  `bike_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `start_latitude` float DEFAULT NULL,
  `start_longitude` float DEFAULT NULL,
  `end_latitude` float DEFAULT NULL,
  `end_longitude` float DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `bike_id` (`bike_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `vehicle_order_ibfk_1` FOREIGN KEY (`bike_id`) REFERENCES `bike` (`id`),
  CONSTRAINT `vehicle_order_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `vehicle_order` */

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
