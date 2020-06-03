/*
Navicat MySQL Data Transfer

Source Server         : 127.0.0.1
Source Server Version : 50721
Source Host           : localhost:3306
Source Database       : block_game

Target Server Type    : MYSQL
Target Server Version : 50721
File Encoding         : 65001

Date: 2018-08-21 20:59:42
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `gateinfo`
-- ----------------------------
DROP TABLE IF EXISTS `gateinfo`;
CREATE TABLE `gateinfo` (
  `id` int(12) NOT NULL,
  `gid` int(12) DEFAULT NULL,
  `uid` varchar(32) DEFAULT '',
  `gatestar` tinyint(1) DEFAULT NULL,
  `state` tinyint(1) DEFAULT '0' COMMENT '未解锁：0 ， 已解锁：1 ，已通关：2',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of gateinfo
-- ----------------------------

-- ----------------------------
-- Table structure for `userinfo`
-- ----------------------------
DROP TABLE IF EXISTS `userinfo`;
CREATE TABLE `userinfo` (
  `uid` varchar(32) NOT NULL DEFAULT '',
  `nickname` varchar(256) DEFAULT '',
  `headimgurl` varchar(1024) DEFAULT '',
  `sex` tinyint(1) DEFAULT '0',
  `city` varchar(32) DEFAULT '',
  `country` varchar(32) DEFAULT '',
  `province` varchar(32) DEFAULT '',
  `unionid` varchar(32) DEFAULT '',
  `starnum` int(12) DEFAULT '0',
  `tips` int(12) DEFAULT '0',
  `allgate` varchar(1024) DEFAULT '',
  PRIMARY KEY (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of userinfo
-- ----------------------------
