SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;


CREATE TABLE `adresse` (
  `idAdresse` char(36) NOT NULL DEFAULT uuid(),
  `ville` varchar(50) DEFAULT NULL,
  `rue` varchar(50) DEFAULT NULL,
  `numeroRue` int(11) DEFAULT NULL,
  `IdPays` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `caracteristiquesordinateur` (
  `numeroSerie` varchar(50) NOT NULL,
  `DisqueDurNumeroCapacite` decimal(15,3) DEFAULT NULL,
  `UniteCapacite` varchar(50) DEFAULT NULL,
  `DisqueDurType` varchar(50) DEFAULT NULL,
  `processeur` varchar(50) DEFAULT NULL,
  `PortableOuBureauOuAutre` varchar(50) DEFAULT NULL,
  `RamNumeroCapacite` decimal(15,2) DEFAULT NULL,
  `RamUnite` varchar(50) DEFAULT NULL,
  `brandPc` varchar(50) DEFAULT NULL,
  `description` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `direction` (
  `IdDirection` char(36) NOT NULL DEFAULT uuid(),
  `nom` varchar(50) DEFAULT NULL,
  `numeroEtages` int(11) DEFAULT NULL CHECK (`numeroEtages` >= 0),
  `idAdresse` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `employe` (
  `IdUtilisateur` char(36) NOT NULL DEFAULT uuid(),
  `Prenom` varchar(50) DEFAULT NULL,
  `Nom` varchar(50) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `telephon` varchar(50) DEFAULT NULL,
  `IdSiteGeographique` varchar(50) DEFAULT NULL,
  `idAdresse` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `materiel` (
  `numeroInventaire` varchar(50) NOT NULL,
  `AnneeAcquisition` varchar(50) NOT NULL,
  `IdDirection` varchar(50) DEFAULT NULL,
  `numeroSerie` varchar(50) NOT NULL,
  `IdUtilisateur` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `observation` (
  `idOBSERVATION` char(36) NOT NULL DEFAULT uuid(),
  `descriptionOBSERVATION` varchar(50) DEFAULT NULL,
  `dateOBSERVATION` date DEFAULT NULL,
  `IdUtilisateur` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `pays` (
  `IdPays` int(11) NOT NULL,
  `nom` varchar(50) DEFAULT NULL,
  `langue` varchar(50) DEFAULT NULL,
  `surface` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `services` (
  `idServices` char(36) NOT NULL DEFAULT uuid(),
  `nom` varchar(50) DEFAULT NULL,
  `presentiel_` tinyint(1) DEFAULT NULL,
  `aDistance_` tinyint(1) DEFAULT NULL,
  `IdSiteGeographique` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `sitegeographique` (
  `IdSiteGeographique` char(36) NOT NULL DEFAULT uuid(),
  `nom` varchar(50) DEFAULT NULL,
  `numeroBureaux` varchar(50) DEFAULT NULL,
  `numeroEmploye` int(11) DEFAULT NULL CHECK (`numeroEmploye` >= 0),
  `specialite` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `situation` (
  `idSituation` char(36) NOT NULL DEFAULT uuid(),
  `PosteSensible` tinyint(1) DEFAULT NULL,
  `TraiteDemandeClient` tinyint(1) DEFAULT NULL,
  `WATERP` tinyint(1) DEFAULT NULL,
  `IdUtilisateur` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `situer` (
  `IdDirection` varchar(50) NOT NULL,
  `IdSiteGeographique` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


ALTER TABLE `adresse`
  ADD PRIMARY KEY (`idAdresse`),
  ADD UNIQUE KEY `IdPays` (`IdPays`);

ALTER TABLE `caracteristiquesordinateur`
  ADD PRIMARY KEY (`numeroSerie`);

ALTER TABLE `direction`
  ADD PRIMARY KEY (`IdDirection`),
  ADD UNIQUE KEY `idAdresse` (`idAdresse`),
  ADD KEY `idx_direction_adresse` (`idAdresse`);

ALTER TABLE `employe`
  ADD PRIMARY KEY (`IdUtilisateur`),
  ADD KEY `idx_utilisateur_site` (`IdSiteGeographique`),
  ADD KEY `employe_ibfk_2` (`idAdresse`);

ALTER TABLE `materiel`
  ADD PRIMARY KEY (`numeroInventaire`),
  ADD UNIQUE KEY `IdCaracteristiques` (`numeroSerie`),
  ADD KEY `IdUtilisateur` (`IdUtilisateur`),
  ADD KEY `idx_materiel_direction` (`IdDirection`);

ALTER TABLE `observation`
  ADD PRIMARY KEY (`idOBSERVATION`),
  ADD KEY `observation_ibfk_1` (`IdUtilisateur`);

ALTER TABLE `pays`
  ADD PRIMARY KEY (`IdPays`);

ALTER TABLE `services`
  ADD PRIMARY KEY (`idServices`),
  ADD KEY `IdSiteGeographique` (`IdSiteGeographique`);

ALTER TABLE `sitegeographique`
  ADD PRIMARY KEY (`IdSiteGeographique`);

ALTER TABLE `situation`
  ADD PRIMARY KEY (`idSituation`),
  ADD UNIQUE KEY `IdUtilisateur` (`IdUtilisateur`);

ALTER TABLE `situer`
  ADD PRIMARY KEY (`IdDirection`,`IdSiteGeographique`),
  ADD KEY `IdSiteGeographique` (`IdSiteGeographique`);


ALTER TABLE `adresse`
  MODIFY `IdPays` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `pays`
  MODIFY `IdPays` int(11) NOT NULL AUTO_INCREMENT;


ALTER TABLE `adresse`
  ADD CONSTRAINT `adresse_ibfk_1` FOREIGN KEY (`IdPays`) REFERENCES `pays` (`IdPays`);

ALTER TABLE `direction`
  ADD CONSTRAINT `direction_ibfk_1` FOREIGN KEY (`idAdresse`) REFERENCES `adresse` (`idAdresse`) ON DELETE CASCADE;

ALTER TABLE `employe`
  ADD CONSTRAINT `employe_ibfk_1` FOREIGN KEY (`IdSiteGeographique`) REFERENCES `sitegeographique` (`IdSiteGeographique`),
  ADD CONSTRAINT `employe_ibfk_2` FOREIGN KEY (`idAdresse`) REFERENCES `adresse` (`idAdresse`) ON DELETE CASCADE;

ALTER TABLE `materiel`
  ADD CONSTRAINT `materiel_ibfk_1` FOREIGN KEY (`IdDirection`) REFERENCES `direction` (`IdDirection`) ON DELETE CASCADE,
  ADD CONSTRAINT `materiel_ibfk_2` FOREIGN KEY (`numeroSerie`) REFERENCES `caracteristiquesordinateur` (`numeroSerie`),
  ADD CONSTRAINT `materiel_ibfk_3` FOREIGN KEY (`IdUtilisateur`) REFERENCES `employe` (`IdUtilisateur`);

ALTER TABLE `observation`
  ADD CONSTRAINT `observation_ibfk_1` FOREIGN KEY (`IdUtilisateur`) REFERENCES `employe` (`IdUtilisateur`) ON DELETE CASCADE;

ALTER TABLE `services`
  ADD CONSTRAINT `services_ibfk_1` FOREIGN KEY (`IdSiteGeographique`) REFERENCES `sitegeographique` (`IdSiteGeographique`);

ALTER TABLE `situation`
  ADD CONSTRAINT `situation_ibfk_1` FOREIGN KEY (`IdUtilisateur`) REFERENCES `employe` (`IdUtilisateur`) ON DELETE CASCADE;

ALTER TABLE `situer`
  ADD CONSTRAINT `situer_ibfk_1` FOREIGN KEY (`IdDirection`) REFERENCES `direction` (`IdDirection`) ON DELETE CASCADE,
  ADD CONSTRAINT `situer_ibfk_2` FOREIGN KEY (`IdSiteGeographique`) REFERENCES `sitegeographique` (`IdSiteGeographique`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
