/*
Navicat MySQL Data Transfer

Source Server         : localhost_3306
Source Server Version : 50726
Source Host           : localhost:3306
Source Database       : block_game

Target Server Type    : MYSQL
Target Server Version : 50726
File Encoding         : 65001

Date: 2020-06-23 20:41:29
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for gateinfo
-- ----------------------------
DROP TABLE IF EXISTS `gateinfo`;
CREATE TABLE `gateinfo` (
  `id` int(12) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `gid` int(12) DEFAULT '0' COMMENT '关卡id',
  `uid` varchar(32) DEFAULT '' COMMENT '用户id',
  `gatestar` tinyint(1) DEFAULT '0',
  `state` tinyint(1) DEFAULT '0' COMMENT '未解锁：0 ， 已解锁：1 ，已通关：2',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of gateinfo
-- ----------------------------

-- ----------------------------
-- Table structure for operated
-- ----------------------------
DROP TABLE IF EXISTS `operated`;
CREATE TABLE `operated` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `uid` varchar(255) DEFAULT NULL COMMENT '用户id',
  `type` int(11) unsigned zerofill DEFAULT '00000000000' COMMENT '操作类型',
  `time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '操作时间',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of operated
-- ----------------------------

-- ----------------------------
-- Table structure for userinfo
-- ----------------------------
DROP TABLE IF EXISTS `userinfo`;
CREATE TABLE `userinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(256) DEFAULT '',
  `nickname` varchar(256) DEFAULT '',
  `headimgurl` varchar(1024) DEFAULT '',
  `sex` tinyint(1) DEFAULT '0',
  `city` varchar(32) DEFAULT '',
  `country` varchar(32) DEFAULT '',
  `province` varchar(32) DEFAULT '',
  `unionid` varchar(32) DEFAULT '',
  `tips` int(12) DEFAULT '0' COMMENT '获得的提示机会次数',
  `gates` varchar(4096) DEFAULT '' COMMENT '对应的解锁关卡信息',
  `dtips` int(11) DEFAULT '0' COMMENT '临时辅助，游戏内用',
  `ranklevel` int(11) DEFAULT '0' COMMENT '用户排位等级',
  `gold` int(11) DEFAULT '0' COMMENT '游戏币',
  `money` int(11) DEFAULT '0' COMMENT '钻石（人民币）',
  `goods` varchar(4096) DEFAULT '' COMMENT '个人物品, id:count;id:count',
  `tipstime` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '获取提示的时间',
  `ads` int(11) unsigned zerofill DEFAULT '00000000000' COMMENT '看视频广告的次数',
  `adtime` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '看视频广告的时间',
  `shares` int(11) unsigned zerofill DEFAULT '00000000000' COMMENT '分享的次数',
  `sharetime` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '分享的时间',
  `popadds` int(11) unsigned zerofill DEFAULT '00000000000' COMMENT '弹出式广告',
  `popaddtime` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '弹出式广告时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of userinfo
-- ----------------------------
