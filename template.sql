-- phpMyAdmin SQL Dump
-- version 5.2.1deb2
-- https://www.phpmyadmin.net/
--
-- Hôte : localhost:3306
-- Généré le : sam. 30 mars 2024 à 15:59
-- Version du serveur : 10.11.6-MariaDB-2
-- Version de PHP : 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `BookWorm`
--

-- --------------------------------------------------------

--
-- Structure de la table `Auteur`
--

CREATE TABLE `Auteur` (
  `ID` int(11) NOT NULL,
  `Nom` varchar(20) NOT NULL,
  `Prénom` varchar(20) NOT NULL,
  `Alias` varchar(20) DEFAULT NULL,
  `Biographie` varchar(1000) NOT NULL,
  `Date de naissance` date NOT NULL DEFAULT current_timestamp(),
  `Date de décès` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `Editeur`
--

CREATE TABLE `Editeur` (
  `Nom` varchar(20) NOT NULL,
  `Adresse` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `Emprunt`
--

CREATE TABLE `Emprunt` (
  `ID` int(11) NOT NULL,
  `Livre` varchar(13) NOT NULL,
  `Date` date NOT NULL DEFAULT current_timestamp(),
  `Utilisateur` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `Livre`
--

CREATE TABLE `Livre` (
  `ISBN` varchar(13) NOT NULL,
  `Titre` varchar(50) NOT NULL,
  `Auteur` int(11) NOT NULL,
  `Description` varchar(1000) NOT NULL,
  `Note` float(10) NOT NULL,
  `Date de parution` date NOT NULL,
  `Statut` enum('emprunté','disponible','hors stock','') NOT NULL DEFAULT 'emprunté',
  `Genre` enum('Historique','Romantique','Policier','Science-fiction','Fantastique','Aventure','Biographique','Autobiographique','Épistolaire','Thriller','Tragédie','Drame','Absurde','Philosophique','Politique','Légendes & Mythes','Lettres personnelles','Voyages','Journal intime','Bandes dessinées','Documentaires','Religieux') NOT NULL,
  `Format` enum('Poche','Grand Format','E-book & numérique','Manga','Bande Dessinée','Magazine','CD','DVD & Blu-ray') NOT NULL,
  `Prix` float NOT NULL,
  `Point de vente` varchar(100) NOT NULL,
  `Editeur` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `Point de vente`
--

CREATE TABLE `Point de vente` (
  `Adresse` varchar(100) NOT NULL,
  `Nom` varchar(20) NOT NULL,
  `Site web` varchar(50) NOT NULL,
  `Tel` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `Utilisateur`
--

CREATE TABLE `Utilisateur` (
  `email` varchar(50) NOT NULL,
  `mdp` varchar(200) NOT NULL,
  `Grade` enum('admin','user') NOT NULL DEFAULT 'user',
  `Nom` varchar(20) NOT NULL,
  `Prénom` varchar(20) NOT NULL,
  `Adresse` varchar(100) NOT NULL,
  `Tel` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `Auteur`
--
ALTER TABLE `Auteur`
  ADD PRIMARY KEY (`ID`);

--
-- Index pour la table `Editeur`
--
ALTER TABLE `Editeur`
  ADD PRIMARY KEY (`Nom`);

--
-- Index pour la table `Emprunt`
--
ALTER TABLE `Emprunt`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `Emprunt_ibfk_1` (`Livre`),
  ADD KEY `Emprunt_ibfk_2` (`Utilisateur`);

--
-- Index pour la table `Livre`
--
ALTER TABLE `Livre`
  ADD PRIMARY KEY (`ISBN`),
  ADD KEY `Auteur` (`Auteur`),
  ADD KEY `Point de vente` (`Point de vente`),
  ADD KEY `Editeur` (`Editeur`);

--
-- Index pour la table `Point de vente`
--
ALTER TABLE `Point de vente`
  ADD PRIMARY KEY (`Adresse`);

--
-- Index pour la table `Utilisateur`
--
ALTER TABLE `Utilisateur`
  ADD PRIMARY KEY (`email`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `Auteur`
--
ALTER TABLE `Auteur`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `Emprunt`
--
ALTER TABLE `Emprunt`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `Emprunt`
--
ALTER TABLE `Emprunt`
  ADD CONSTRAINT `Emprunt_ibfk_1` FOREIGN KEY (`Livre`) REFERENCES `Livre` (`ISBN`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `Emprunt_ibfk_2` FOREIGN KEY (`Utilisateur`) REFERENCES `Utilisateur` (`email`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Contraintes pour la table `Livre`
--
ALTER TABLE `Livre`
  ADD CONSTRAINT `Livre_ibfk_1` FOREIGN KEY (`Auteur`) REFERENCES `Auteur` (`ID`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `Livre_ibfk_2` FOREIGN KEY (`Point de vente`) REFERENCES `Point de vente` (`Adresse`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `Livre_ibfk_3` FOREIGN KEY (`Editeur`) REFERENCES `Editeur` (`Nom`) ON DELETE NO ACTION ON UPDATE NO ACTION;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

