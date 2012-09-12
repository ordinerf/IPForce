-- phpMyAdmin SQL Dump
-- version 3.4.11.1deb1
-- http://www.phpmyadmin.net
--
-- Client: localhost
-- Gérée: Mer 12 Septembre 2012 à4:36
-- Version du serveur: 5.5.24
-- Version de PHP: 5.4.4-4

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Base de donné: `iptables`
--

-- --------------------------------------------------------

--
-- Structure de la table `banned`
--

CREATE TABLE IF NOT EXISTS `banned` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `IP` varchar(36) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=11 ;

--
-- Contenu de la table `banned`
--

INSERT INTO `banned` (`id`, `IP`) VALUES
(1, '95.35.94.0/24'),
(2, '94.231.83.147'),
(3, '182.140.145.17'),
(4, '85.25.100.44'),
(5, '188.138.91.50'),
(6, '188.138.0.0/16'),
(7, '64.31.58.66'),
(8, '37.8.53.65'),
(9, '64.22.82.236'),
(10, '198.143.130.194');

-- --------------------------------------------------------

--
-- Structure de la table `rules`
--

CREATE TABLE IF NOT EXISTS `rules` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `DESC` text NOT NULL,
  `interface` varchar(8) NOT NULL DEFAULT 'eth0',
  `protocole` varchar(3) NOT NULL,
  `sourceIP` varchar(40) DEFAULT NULL,
  `destinationIP` varchar(40) DEFAULT NULL,
  `destinationPORT` varchar(16) DEFAULT NULL,
  `policy` varchar(64) NOT NULL DEFAULT 'DROP',
  `direction` varchar(3) NOT NULL DEFAULT 'IN',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=26 ;

--
-- Contenu de la table `rules`
--

INSERT INTO `rules` (`id`, `DESC`, `interface`, `protocole`, `sourceIP`, `destinationIP`, `destinationPORT`, `policy`, `direction`) VALUES
(1, 'SSH 31141', 'eth0', 'TCP', NULL, NULL, '31141', 'ACCEPT', 'IN'),
(2, 'Web80', 'eth0', 'TCP', NULL, NULL, '80', 'ACCEPT', 'IN'),
(3, 'SSL443', 'eth0', 'TCP', NULL, NULL, '443', 'ACCEPT', 'IN'),
(4, 'POP110', 'eth0', 'TCP', NULL, NULL, '110', 'ACCEPT', 'IN'),
(5, 'SMTP995', 'eth0', 'TCP', NULL, NULL, '995', 'ACCEPT', 'IN'),
(6, 'IMAP143', 'eth0', 'TCP', NULL, NULL, '143', 'ACCEPT', 'IN'),
(7, 'IMAP993', 'eth0', 'TCP', NULL, NULL, '993', 'ACCEPT', 'IN'),
(8, 'SIP5060', 'eth0', 'TCP', NULL, NULL, '5060', 'ACCEPT', 'IN'),
(9, 'SIP5080', 'eth0', 'TCP', NULL, NULL, '5080', 'ACCEPT', 'IN'),
(10, 'SIP5880', 'eth0', 'TCP', NULL, NULL, '5880', 'ACCEPT', 'IN'),
(11, 'Mumble30000', 'eth0', 'TCP', NULL, NULL, '30000', 'ACCEPT', 'IN'),
(12, 'ProxyWeb3122', 'eth0', 'TCP', NULL, NULL, '3122', 'ACCEPT', 'IN'),
(13, 'NodeJS6789', 'eth0', 'TCP', NULL, NULL, '6789', 'ACCEPT', 'IN'),
(14, '137 Netbios', 'eth0', 'UDP', NULL, NULL, '137', 'DROP', 'IN'),
(15, 'Netbios137', 'eth0', 'UDP', NULL, NULL, '137', 'DROP', 'IN'),
(16, 'Netbios138', 'eth0', 'UDP', NULL, NULL, '138', 'DROP', 'IN'),
(17, 'Netbios113', 'eth0', 'UDP', NULL, NULL, '113', 'REJECT', 'IN'),
(18, 'NTP 123', 'eth0', 'UDP', NULL, NULL, '123', 'ACCEPT', 'IN'),
(19, 'DNS53', 'eth0', 'UDP', NULL, NULL, '137', 'ACCEPT', 'IN'),
(20, 'SIP5060', 'eth0', 'UDP', NULL, NULL, '5060', 'ACCEPT', 'IN'),
(21, 'SIP5080', 'eth0', 'UDP', NULL, NULL, '5080', 'ACCEPT', 'IN'),
(22, 'SIP5080', 'eth0', 'UDP', NULL, NULL, '5880', 'ACCEPT', 'IN'),
(23, 'MUMBLE 30000', 'eth0', 'UDP', NULL, NULL, '30000', 'ACCEPT', 'IN'),
(24, '3122', 'eth0', 'UDP', NULL, NULL, '3122', 'ACCEPT', 'IN'),
(25, '16384:32768', 'eth0', 'UDP', NULL, NULL, '16384:32768', 'ACCEPT', 'IN');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

