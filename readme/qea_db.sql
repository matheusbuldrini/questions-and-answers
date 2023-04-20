-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Tempo de geração: 20-Abr-2023 às 12:06
-- Versão do servidor: 8.0.31
-- versão do PHP: 8.0.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `qea`
--

-- --------------------------------------------------------

--
-- Estrutura da tabela `answer`
--

DROP TABLE IF EXISTS `answer`;
CREATE TABLE IF NOT EXISTS `answer` (
  `idanswer` int NOT NULL AUTO_INCREMENT,
  `idquestion` int NOT NULL,
  `iduser` int NOT NULL,
  `description` text,
  `data` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`idanswer`),
  KEY `idquestion` (`idquestion`),
  KEY `iduser` (`iduser`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Extraindo dados da tabela `answer`
--

INSERT INTO `answer` (`idanswer`, `idquestion`, `iduser`, `description`, `data`) VALUES
(1, 1, 1, 'Eu Também nao sei :(', '2023-04-20 09:04:12');

-- --------------------------------------------------------

--
-- Estrutura da tabela `question`
--

DROP TABLE IF EXISTS `question`;
CREATE TABLE IF NOT EXISTS `question` (
  `idquestion` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `iduser` int NOT NULL,
  `tags` varchar(255) DEFAULT NULL,
  `data` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`idquestion`),
  KEY `iduser` (`iduser`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Extraindo dados da tabela `question`
--

INSERT INTO `question` (`idquestion`, `title`, `description`, `iduser`, `tags`, `data`) VALUES
(1, 'Como usar esse site?', 'Nao sei usar me ajuda', 1, '{\"Tags\": {\"tag 0\": \"ajuda\"}}', '2023-04-20 09:02:05');

-- --------------------------------------------------------

--
-- Estrutura da tabela `user`
--

DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
  `iduser` int NOT NULL AUTO_INCREMENT,
  `fullname` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `description` text,
  PRIMARY KEY (`iduser`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Extraindo dados da tabela `user`
--

INSERT INTO `user` (`iduser`, `fullname`, `email`, `password`, `description`) VALUES
(1, 'Matheus', 'matheus@matheus.com', '45339359513f09155110f63f7ca91c3e', NULL);

-- --------------------------------------------------------

--
-- Estrutura da tabela `voteanswer`
--

DROP TABLE IF EXISTS `voteanswer`;
CREATE TABLE IF NOT EXISTS `voteanswer` (
  `idanswer` int DEFAULT NULL,
  `iduser` int DEFAULT NULL,
  `vote` int DEFAULT NULL,
  KEY `idanswer` (`idanswer`),
  KEY `iduser` (`iduser`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Extraindo dados da tabela `voteanswer`
--

INSERT INTO `voteanswer` (`idanswer`, `iduser`, `vote`) VALUES
(1, 1, -1);

-- --------------------------------------------------------

--
-- Estrutura da tabela `votequestion`
--

DROP TABLE IF EXISTS `votequestion`;
CREATE TABLE IF NOT EXISTS `votequestion` (
  `id` int NOT NULL,
  `idquestion` int NOT NULL,
  `iduser` int NOT NULL,
  `vote` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idquestion` (`idquestion`),
  KEY `iduser` (`iduser`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Extraindo dados da tabela `votequestion`
--

INSERT INTO `votequestion` (`id`, `idquestion`, `iduser`, `vote`) VALUES
(0, 1, 1, 1);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
