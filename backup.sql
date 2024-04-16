-- phpMyAdmin SQL Dump
-- version 5.2.1deb2
-- https://www.phpmyadmin.net/
--
-- Hôte : localhost:3306
-- Généré le : sam. 06 avr. 2024 à 15:52
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
  `Biographie` varchar(1000) NOT NULL,
  `Date de naissance` date NOT NULL DEFAULT current_timestamp(),
  `Date de décès` date DEFAULT NULL,
  `Alias` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `Auteur`
--

INSERT INTO `Auteur` (`ID`, `Nom`, `Prénom`, `Biographie`, `Date de naissance`, `Date de décès`, `Alias`) VALUES
(1, 'Hugo', 'Victor', 'Victor Hugo, parfois surnommé l\'Homme océan ou, de manière posthume, l\'Homme siècle, est un poète, dramaturge, écrivain, romancier et dessinateur romantique français, né le 7 ventôse an X (26 février 1802) à Besançon et mort le 22 mai 1885 à Paris. Il est considéré comme l\'un des écrivains de la langue française et de la littérature mondiale les plus importants. Hugo est aussi une personnalité politique et un intellectuel engagé qui a un rôle idéologique majeur et occupe une place marquante dans l\'histoire des lettres françaises au xixe siècle.', '1802-02-26', '1885-05-22', ''),
(2, 'Rowling', 'Joanne', 'Joanne Rowling [ d͡ʒoʊˈæn ˈroʊlɪŋ]a, plus connue sous les noms de plume J. K. Rowlingb et Robert Galbraith, est une romancière et scénariste britannique née le 31 juillet 1965 dans l’agglomération de Yate (Gloucestershire du Sud). Elle doit sa notoriété mondiale à la série Harry Potter, dont les romans traduits en près de quatre-vingts langues ont été vendus à plus de 500 millions d\'exemplaires dans le monde.', '1965-07-31', NULL, 'J. K. Rowling'),
(3, 'Tolkien', 'John Ronald Reuel', 'John Ronald Reuel Tolkien, plus connu sous la forme J. R. R. Tolkien est un écrivain, poète, philologue, essayiste et professeur d’université britannique né le 3 janvier 1892 à Bloemfontein (État libre d\'Orange) et mort le 2 septembre 1973 à Bournemouth (Royaume-Uni).\r\n\r\nSes deux romans les plus connus, Le Hobbit et Le Seigneur des anneaux, prennent place dans l\'univers de fiction de la Terre du Milieu dont il développe la géographie, les peuples, l\'histoire et les langues durant la majeure partie de sa vie.', '1892-02-03', '1973-09-02', 'J. R. R. Tolkien'),
(4, 'Poquelin', 'Jean-Baptiste ', 'Jean-Baptiste Poquelin, dit Molière, baptisé le 15 janvier 1622 à l\'église Saint-Eustache de Paris et mort le soir du 17 février 1673 à son domicile de la rue de Richelieu, est le plus célèbre des comédiens et dramaturges de langue française.', '1673-01-15', '1673-01-17', 'Molière'),
(5, 'Carteron', 'Marine', 'Marine Carteron est une enseignante et une autrice pour la jeunesse.\r\n\r\nElle passe son enfance et son adolescence entre la Bretagne, la Sarthe, la Corse et les Antilles avant de faire des études d’histoire de l’Art et d’archéologie à l’Université de Tours. Enseignante de français, elle réside en Rhône-Alpes.', '1972-03-07', NULL, ''),
(6, 'Henri-Alban ', 'Fournier', 'Alain-Fournier, pseudonyme d\'Henri-Alban Fournier, né le 3 octobre 1886 à La Chapelle-d\'Angillon dans le Cher et mort au combat le 22 septembre 1914 (à 27 ans) à Saint-Remy-la-Calonne, est un écrivain français dont l\'œuvre la plus marquante, restée célèbre, est Le Grand Meaulnes.', '2024-04-01', '1914-09-22', 'Alain Fournier'),
(7, 'Riordan', 'Richard Russel', 'Richard Russell Rick Riordan Jr, né le 5 juin 1964 à San Antonio au Texas, est un écrivain américain. Il est notamment l\'auteur des séries Percy Jackson, Héros de l\'Olympe, Les Chroniques de Kane, Magnus Chase et les Dieux d\'Asgard et Les Travaux d\'Apollon. Il a également aidé à développer la série Les 39 Clés, publiée par Scholastic Corporation, série dont il a écrit le premier tome L\'Énigme des catacombes ainsi que le onzième, La Menace Vesper.', '1964-06-05', NULL, 'Rick Riordan'),
(8, 'Jean Claude', 'Mourlevat', 'Jean-Claude Mourlevat est un auteur français né à Ambert (Puy-de-Dôme) le 22 mars 1952. Il est particulièrement connu pour ses romans destinés à la jeunesse, pour lesquels il est multiprimé, notamment par le prix commémoratif Astrid-Lingren.\r\n\r\n', '1952-03-22', NULL, ''),
(9, 'Muchamor', 'Robert', 'Robert Kilgore Muchamore, né à Londres le 26 décembre 1972, est un écrivain anglais, connu pour être l\'auteur de la série best-seller CHERUB, une série de livres d\'espionnage pour adolescents.\r\n\r\nRobert Kilgore Muchamore a d\'abord été détective privé, avant de se lancer à plein temps dans la littérature pour la jeunesse.', '1972-12-26', NULL, ''),
(10, 'Antoine', 'Bello', 'Son œuvre la plus connue est une trilogie, qui narre l\'ascension d\'un jeune Islandais dans les rangs du CFR, une organisation secrète internationale qui falsifie la réalité et réécrit l\'Histoire. Le premier tome, Les Falsificateurs, est paru en 2007 ; le deuxième, Les Éclaireurs, en 2009 et le troisième, Les Producteurs, en 2015. Elle a pris une signification nouvelle avec le débat récent sur les fake news3. ', '1970-03-25', NULL, ''),
(11, 'Morpurgo', 'Michael', 'Michael Morpurgo, né le 5 octobre 1943 à St Albans, en Angleterre, est un auteur britannique, notamment connu pour ses ouvrages de littérature d\'enfance et de jeunesse souvent liés à des événements historiques.', '1943-10-05', NULL, ''),
(12, 'Chedid', 'Andrée', 'Andrée Chedid (en arabe : أندريه شديد), née Andrée Saab2 (en arabe : أندريه صعب) le 20 mars 1920 au Caire (sultanat d\'Égypte) et morte le 6 février 2011 à Paris 15e (France), est une femme de lettres et poétesse franco-syro-libanaise3.\r\n\r\nElle écrit son premier roman en 1952 et écrit des nouvelles, des poèmes, des pièces de théâtre, des romans, et de la littérature jeunesse. Elle déclare son humanisme entre autres avec son livre Le Message, écrit en 2000, en écrivant sa colère envers la guerre et la violence, à travers deux amants séparés par des guerres. Les héroïnes de ses œuvres sont décidées, prêtes à tout pour atteindre leur objectif.', '1920-03-20', '2011-02-06', ''),
(13, 'L\'Homme', 'Erik', 'Erik L\'Homme, né le 22 décembre 1967 à Grenoble, est un écrivain français qui a notamment écrit des ouvrages destinés à la jeunesse et des ouvrages de science-fiction et de fantasy.', '1967-12-22', NULL, ''),
(14, 'Bottero', 'Pierre', 'Pierre Bottero, né le 13 février 19641 à Barcelonnette, dans les Basses-Alpes, et mort le 8 novembre 2009 à Aix-en-Provence2, est un écrivain français de littérature jeunesse, dont les œuvres principales appartiennent au genre de la fantasy.', '1964-02-13', '2009-11-08', ''),
(15, 'Bordage', 'Pierre ', 'Pierre Bordage, né le 29 janvier 1955 à La Réorthe, en Vendée, est un auteur de science-fiction français. C\'est avec sa trilogie Les Guerriers du silence, publiée aux éditions de l\'Atalante et vendue à 50 000 exemplaires, qu\'il rencontre le succès. Ce space opera ainsi que le cycle de Wang sont salués par la critique littéraire comme des œuvres majeures du renouveau de la science-fiction française des années 1990, genre qui était alors dominé par les auteurs anglophones.', '1955-01-29', NULL, ''),
(16, 'Robillard', 'Anne', 'Anne Robillard, née le 9 février 1955 à Longueuil au Québec, est une écrivaine québécoise de fantasy.\r\n\r\nElle est connue notamment pour Les Chevaliers d\'Émeraude, une saga se déroulant sur le continent d\'Enkidiev, un monde magique que les Chevaliers d\'Émeraude devront protéger.\r\n\r\nEn plus de cette saga, elle a aussi écrit de nombreux livres, tels que Qui est Terra Wilder ?, sorti en 2006, et sa suite, Capitaine Wilder, les séries A.N.G.E., Les Héritiers d\'Enkidiev et Les Ailes d\'Alexanne.', '1955-02-09', NULL, ''),
(17, 'Paolini', 'Christopher', 'Christopher Paolini, né le 17 novembre 1983 à Los Angeles en Californie, est un écrivain américain de fantasy et de science-fiction. Il est connu pour sa série de fantasy à succès L\'Héritage.\r\nDès l\'âge de quinze ans, Christopher Paolini commence un premier roman de fantasy inspiré de Dragon Hatcher de Bruce Coville et du Cycle de Terremer d\' Ursula K. Le Guin. Eragon, premier tome de sa série L\'Héritage, est publié le 25 juin 2003, Christopher Paolini n\'est alors âgé que de dix-neuf ans. La seconde édition est expurgée de quelques longueurs. La traduction française paraît chez Bayard jeunesse le 21 octobre 2004. La trame de ce premier tome présente des similarités avec le scénario du Seigneur des anneaux.', '1968-11-17', NULL, ''),
(18, 'Colfer', 'Eoin', 'Eoin Colfer (/ˈoʊ.ɪn/), né le 14 mai 1965 à Wexford, en Irlande, est un écrivain irlandais.\r\nEnseignant comme l\'étaient ses parents, Eoin Colfer vit avec sa femme Jackie et son fils dans sa ville natale, où sont également installés son père, sa mère et ses quatre frères. Tout jeune, il s\'essaie à l\'écriture et compose une pièce de théâtre pour sa classe, une histoire dans laquelle, comme il l\'explique, « tout le monde mourait à la fin, sauf moi ». Grand voyageur, il a travaillé en Arabie saoudite, en Tunisie et en Italie avant de revenir en Irlande. Eoin Colfer avait déjà publié plusieurs livres pour les moins de 10 ans et il était, même avant la publication des aventures d\'Artemis Fowl le célèbre voleur, un auteur reconnu dans son pays.', '1965-05-14', NULL, ''),
(19, 'Hunter', 'Erin', 'Erin Hunter est le pseudonyme commun de trois romancières britanniques, Kate Cary, Cherith Baldry et Victoria Holmes, rejointes ensuite par l\'Américaine Tui Sutherland, l\'Israélienne Inbali Iserles et les Britanniques Gillian Philip et Rosie Best. Ces écrivaines se relaient pour écrire les livres des séries La Guerre des clans, La Quête des ours, Survivants, Bravelands, ainsi que Les Messagers du dragon. Elles ont inventé le nom Erin Hunter pour faciliter la recherche de leurs livres dans les librairies ou bibliothèques.', '1967-11-04', NULL, ''),
(20, 'Delaney', 'Joseph', 'Joseph Delaney, né le 25 juillet 1945 à Preston (Lancashire) en Angleterre et mort le 16 août 2022 à Manchester, est un auteur britannique de science-fiction et d\'heroic fantasy.\r\n\r\n', '1945-07-22', '2022-08-16', ''),
(21, 'Arouet', 'François-Marie', 'Voltaire, de son vrai nom François-Marie Arouet, né le 21 novembre 1694 à Paris où il est mort le 30 mai 1778, est un écrivain, notamment dramaturge et poète, un philosophen 1 et un encyclopédiste français, figure majeure de la philosophie des Lumières, jouissant de son vivant d\'une célébrité internationale.', '1694-11-21', '1178-05-30', 'Voltaire'),
(22, 'Damasio', 'Alain', 'Alain Damasio, né le 1er août 1969 à Lyon, est un écrivain de science-fiction et de fantasy et typoète français. Son domaine de prédilection est l\'anticipation politique. Il marie ce genre à des éléments de science-fiction ou de fantasy et décrit des dystopies politiques.\r\n\r\nIl est connu pour son ouvrage La Horde du Contrevent, qui remporte le grand prix de l\'Imaginaire en 2006. Sa nouvelle Serf-Made-Man ? ou la créativité discutable de Nolan Peskine, parue dans le recueil Au bal des actifs. Demain le travail, remporte le même prix dans la catégorie « nouvelle francophone » en 2018.', '1969-08-01', NULL, ''),
(23, 'Christie', 'Agatha', 'Agatha Christie est une femme de lettres britannique, auteur de nombreux romans policiers, née le 15 septembre 1890 à Torquay et morte le 12 janvier 1976 à Wallingford au Royaume-Uni. Son nom de plume est associé à celui de ses deux héros : Hercule Poirot, détective professionnel belge, et Miss Marple, détective amateur. On surnomme Agatha Christie « la reine du crime ». En effet, elle est l\'un des écrivains les plus importants et novateurs du genre policier. Elle a aussi écrit plusieurs romans, dont quelques histoires sentimentales, sous le pseudonyme Mary Westmacott.', '1890-09-15', '1976-01-12', ''),
(24, 'Shakespeare', 'William', 'William Shakespeare est un dramaturge, poète et acteur anglais baptisé le 26 avril 1564 à Stratford-upon-Avon et mort le 23 avril 1616 dans la même ville. Surnommé « le Barde d\'Avon », « le Barde immortel » ou simplement « le Barde », il est considéré comme l\'un des plus grands poètes et dramaturges de langue anglaise. Son œuvre, traduite dans de nombreuses langues, se compose de 39 pièces, 154 sonnets et quelques poèmes supplémentaires, dont certains ne lui sont pas attribués de manière certaine.', '1564-00-00', '1616-04-23', ''),
(25, 'Bradbury', 'Raymond Douglas', 'Raymond Douglas Bradbury dit Ray Bradbury, né le 22 août 1920 à Waukegan dans l’Illinois et mort le 5 juin 2012 (à 91 ans) à Los Angeles en Californie, est un écrivain américain, référence du genre de l’anticipation. Il est particulièrement connu pour ses Chroniques martiennes, écrites en 1950, L’Homme illustré, recueil de nouvelles publié en 1951, et surtout Fahrenheit 451, roman dystopique publié en 1953.\r\n\r\n', '2012-08-22', '2012-07-05', 'Ray Bradbury'),
(26, 'Dumas', 'Alexandre', 'Alexandre Dumas (dit aussi Alexandre Dumas père) est un écrivain français né le 24 juillet 1802 à Villers-Cotterêts (Aisne) et mort le 5 décembre 1870 au hameau de Puys, ancienne commune de Neuville-lès-Dieppe, aujourd\'hui intégrée à Dieppe (Seine-Maritime).', '1802-07-24', '1870-12-05', ''),
(27, 'Leblanc', 'Marie Émile Maurice', 'Maurice Leblanc, de son nom complet Marie Émile Maurice Leblanc, est un romancier français né le 11 décembre 18641 à Rouen et mort le 6 novembre 1941 à Perpignan.\r\n\r\nAuteur de nombreux romans policiers et d’aventures, il est le créateur du célèbre gentleman-cambrioleur Arsène Lupin. Relégué au rang de « Conan Doyle français », Maurice Leblanc est un écrivain populaire qui a souffert de ne pas avoir la reconnaissance de ses confrères mais a toujours suscité un solide noyau d\'amateurs et de quelques lupinologues2.', '1864-12-11', '1941-11-06', 'Maurice Leblanc'),
(28, 'Rémi', 'Georges', 'Georges Remia, dit Hergé, né le 22 mai 1907 en Belgique à Etterbeek (province de Brabant) et mort le 3 mars 1983 à Woluwe-Saint-Lambert (Bruxelles), est un auteur de bande dessinée belge, principalement connu pour Les Aventures de Tintin, l\'une des bandes dessinées européennes les plus populaires du xxe siècle.', '1907-05-22', '1983-03-03', 'Hergé'),
(29, 'Franquin', 'André', 'André Franquin, né le 3 janvier 1924 à Etterbeek (province de Brabant, Belgique) et mort le 5 janvier 1997 à Saint-Laurent-du-Var (Alpes-Maritimes, France), est un auteur belge francophone de bande dessinée, principalement connu pour les séries Spirou et Fantasio, Gaston, Modeste et Pompon et les Idées noires ; il est aussi le créateur du Marsupilami, animal imaginaire.', '1924-01-03', '1997-01-05', ''),
(30, 'Culliford', 'Pierre', 'Peyo, pseudonyme de Pierre Culliford, né le 25 juin 1928 à Schaerbeek (province de Brabant) et mort le 24 décembre 1992 à Bruxelles (région de Bruxelles-Capitale), est un auteur belge francophone de bande dessinée, principalement connu pour les séries Les Schtroumpfs, Johan et Pirlouit, Benoît Brisefer, Jacky et Célestin et Poussy.', '1928-06-25', '1992-12-24', 'Payo'),
(31, 'Riggs', 'Ransom', 'Ransom Riggs, né le 3 février 1979 au Maryland, est un écrivain américain de fantasy, principalement connu pour être l\'auteur du roman Miss Peregrine et les Enfants particuliers. ', '1972-02-03', NULL, '');

-- --------------------------------------------------------

--
-- Structure de la table `Editeur`
--

CREATE TABLE `Editeur` (
  `Nom` varchar(20) NOT NULL,
  `Adresse` varchar(120) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `Editeur`
--

INSERT INTO `Editeur` (`Nom`, `Adresse`) VALUES
('Bayard Jeunesse', 'Bayard\r\n18, rue Barbès\r\n92128 Montrouge Cedex'),
('Casterman', 'Éditions Casterman\r\n56 rue Saint-Lazare\r\n75009 Paris\r\nFrance'),
('Dupuis', 'Dupuis Édition et Audiovisuel,\r\n57, rue Gaston Tessier CS50061\r\n75166 Paris CEDEX 19'),
('Édition du Rouergue', 'Éditions du Rouergue\r\n47, rue du Docteur Fanton\r\nBP 90038\r\n13633 Arles cedex'),
('Flammarion', 'Éditions Flammarion\r\n82, rue Saint-Lazare CS 10124\r\n75009 Paris.'),
('Gallimard', 'Éditions Gallimard\r\n5 rue Gaston-Gallimard\r\n75328 Paris cedex 07 FRANC'),
('Hachette', '58, Rue Jean Bleuzen\r\nCS 70007\r\n92 178 Vanves CEDEX\r\nFrance'),
('HarperCollins', 'HarperCollins France Service Ressources Humaines 83-85 boulevard Vincent Auriol 75646 PARIS CEDEX 13'),
('Nathan', 'Relation Enseignants Nathan\r\nBP 20073\r\n13321 MARSEILLE cedex 16'),
('Pocket Jeunesse', '92 avenue de France, 75013 Paris, France'),
('Rageot', 'Rageot Éditeur\r\n8 rue d’Assas\r\n75006 PARIS\r\n\r\n'),
('Wellan Inc', 'Wellan Inc.\r\n257 Boul. Sir Wilfrid-Laurier\r\nCP 85059 - PJC\r\nMont-Saint-Hilaire, QC\r\nJ3H 5W1');

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
  `Titre` varchar(100) NOT NULL,
  `Auteur` int(11) NOT NULL,
  `Description` varchar(1000) NOT NULL,
  `Note` float NOT NULL,
  `Date de parution` date NOT NULL,
  `Statut` enum('emprunté','disponible','hors stock','') NOT NULL DEFAULT 'emprunté',
  `Genre` enum('Historique','Romantique','Policier','Science-fiction','Fantastique','Aventure','Biographique','Autobiographique','Épistolaire','Thriller','Tragédie','Drame','Absurde','Philosophique','Politique','Légendes & Mythes','Lettres personnelles','Voyages','Journal intime','Bandes dessinées','Documentaires','Religieux') NOT NULL,
  `Format` enum('Poche','Grand Format','E-book & numérique','Manga','Bande Dessinée','Magazine','CD','DVD & Blu-ray') NOT NULL,
  `Prix` float NOT NULL,
  `Point de vente` varchar(100) NOT NULL,
  `Editeur` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `Livre`
--

INSERT INTO `Livre` (`ISBN`, `Titre`, `Auteur`, `Description`, `Note`, `Date de parution`, `Statut`, `Genre`, `Format`, `Prix`, `Point de vente`, `Editeur`) VALUES
('2700238974', 'La Quête d\'Ewilan - Tome 3 : L\'île du destin ', 14, 'Après avoir libéré les Sentinelles, Ewilan et Salim rejoignent la Citadelle des Frontaliers avec leurs compagnons. Là, Ewilan découvre la retraite de Merwyn, le plus grand des dessinateurs. Il leur conseille de regagner l’autre monde et de convaincre Mathieu, le frère d’Ewilan, de les suivre en Gwendalavir. À leur retour, ils embarquent pour les îles Alines afin de délivrer les parents d’Ewilan, retenus par Eléa, la sentinelle traîtresse…', 10, '2004-00-00', 'disponible', 'Fantastique', 'Grand Format', 8.4, '31 rue Madier de Montjau\r\n26000 Valence', 'Rageot'),
('1041834365', 'Notre-Dame de Paris ', 1, 'En 1831, Victor Hugo réinvente le Moyen Âge et élève un monument littéraire aussi durable que l\'œuvre de pierre qui l\'a inspiré. Sous la silhouette noire et colossale de la cathédrale fourmille le Paris en haillons des truands de la Cour des Miracles. Image de grâce et de pureté surgie de ce cauchemar, la bohémienne Esméralda danse pour le capitaine Phoebus et ensorcelle le tendre et difforme Quasimodo, sonneur de cloches de son état. Pour elle, consumé d\'amour, l\'archidiacre magicien Claude Frollo court à la damnation.... ', 5.5, '1881-00-00', 'disponible', 'Historique', 'Poche', 4.4, 'Place Charles de Gaulle à Chabeuil (Drôme)', 'Pocket Jeunesse'),
('2010056426', 'ABC contre Poirot', 23, 'Un lieu, une date : l\'assassin annonce ses crimes et lance un défi à Hercule Poirot. L\'assassin est-il un maniaque des annuaires téléphoniques et des indicateurs de chemins de fer ? Celui qui signe A.B.C. tue par ordre alphabétique. Le lecteur croit en savoir plus que le détective lui-même, mais l\'auteur est diabolique. Bien malin celui qui aura le dernier mot !', 5.8, '1936-01-06', 'disponible', 'Policier', 'Poche', 7.99, '31 rue Madier de Montjau\r\n26000 Valence', 'Gallimard'),
('2017010090', 'Miss Peregrine et les enfants particuliers - Hollow City Tome 2', 31, 'Miss Peregrine, changée en oiseau, est prisonnière de son état, suite à l’attaque des Estres. Les enfants particuliers n’ont plus qu’un espoir  : trouver une Ombrune susceptible de rendre à la directrice de l’orphelinat sa forme humaine. Après avoir essuyé une tempête, le petit groupe d’enfants échoue sur une rive de Grande-Bretagne, alors que la Seconde Guerre fait rage. Aussitôt pris en chasse par des Estres, ils se réfugient, in extremis, dans une boucle temporelle. Là, vit une ménagerie d’animaux singuliers. Parmi eux,... ', 8.4, '2017-02-01', 'hors stock', 'Fantastique', 'Grand Format', 10.99, '17, avenue Victor-Hugo Centre commercial Victor-Hugo - 26000  Valence\r\n\r\n', 'Bayard Jeunesse'),
('2070415732', 'Fahrenheit 451', 25, '451 degrés Fahrenheit représentent la température à laquelle un livre s\'enflamme et se consume.Dans cette société future où la lecture, source de questionnement et de réflexion, est considérée comme un acte antisocial, un corps spécial de pompiers est chargé de brûler tous les livres, dont la détention est interdite pour le bien collectif.Montag, le pompier pyromane, se met pourtant à rêver d\'un monde différent, qui ne bannirait pas la littérature et l\'imaginaire au profit d\'un bonheur immédiatement consommable. Il devient...', 7.2, '1953-00-00', 'emprunté', 'Science-fiction', 'Grand Format', 7.9, 'ZC le Plateau des Couleures\r\n26000 VALENCE\r\n07.57.59.94.95', 'Gallimard'),
('2070450333', 'L\'aiguille creuse', 27, 'Avec L\'Aiguille creuse, Maurice Leblanc offre enfin à Arsène Lupin un adversaire à sa mesure. Et pourtant, avec son visage rose de jeune fille et ses cheveux en brosse, Isidore Beautrelet n\'est qu\'un lycéen, prêt à passer le baccalauréat. Saura-t-il expliquer l\'étrange crime commis au château d\'Ambrumésy ? Comprendre les liens qui unissent le gentleman cambrioleur à la belle Mlle de Saint-Véran ? Déchiffrer le secret de l\'Aiguille creuse, dont seuls les rois de France possédaient la clé ? Publié en 1909, L\'Aiguille creuse...', 5, '1909-00-00', 'disponible', 'Policier', 'Poche', 3, '12, place des clercs 26000 Valence', 'Gallimard'),
('2070541290', 'Harry Potter - Tome 2 : Harry potter et la chambre des secrets', 2, 'Cette deuxième aventure d\'Harry Potter mêle avec génie humour, mystère et frisson. L\'intrigue savamment ficelée et pleine de rebondissements inattendus envoûte littéralement le lecteur de la première à la dernière page. Un régal !', 10, '1999-11-00', 'hors stock', 'Fantastique', 'Grand Format', 22.5, '12, place des clercs 26000 Valence', 'Gallimard'),
('2070543587', 'Harry Potter - Tome 4 : Harry potter et la coupe de feu', 2, 'Après un horrible été chez les Dursley, Harry Potter entre en quatrième année au collège de Poudlard. À quatorze ans, il voudrait simplement être un jeune sorcier comme les autres, retrouver ses amis Ron et Hermione, assister avec eux à la Coupe du Monde de Quidditch, apprendre de nouveaux sortilèges et essayer des potions inconnues. Une grande nouvelle l\'attend à son arrivée : la tenue à Poudlard d\'un tournoi de magie entre les plus célèbres écoles de sorcellerie. Déjà les spectaculaires délégations étrangères font leur entrée... Harry se réjouit. Trop vite. Il va se trouver plongé au coeur des événements les plus dramatiques qu\'il ait jamais eu à affronter.\r\nEnvoûtant, drôle, bouleversant, ce quatrième tome est le pilier central des aventures de Harry Potter.', 10, '2000-11-00', 'disponible', 'Fantastique', 'Grand Format', 14.5, 'Place Charles de Gaulle à Chabeuil (Drôme)', 'Gallimard'),
('2070556859', 'Harry Potter - Tome 5 : Harry potter et l\'ordre du phenix ', 2, 'À quinze ans, Harry entre en cinquième année à Poudlard, mais il n\'a jamais été si anxieux. L\'adolescence, la perspective des examens et ces étranges cauchemars... Car Celui-Dont-On-Ne-Doit-Pas-Prononcer-Le-Nom est de retour. Le ministère de la Magie semble ne pas prendre cette menace au sérieux, contrairement à Dumbledore. La résistance s\'organise alors autour de Harry qui va devoir compter sur le courage et la fidélité de ses amis de toujours... ', 10, '2003-12-00', 'disponible', 'Fantastique', 'Grand Format', 12.99, 'Place Charles de Gaulle à Chabeuil (Drôme)', 'Gallimard'),
('2070572676', 'Harry Potter - Tome 6 : Harry potter et le prince de sang-mele ', 2, 'Harry, Ron et Hermione entrent en sixième année à Poudlard où ils vont vivre leur dernière année avant la majorité qui est fixée, chez les sorciers, à l\'âge de dix-sept ans. Des événements particulièrement marquants vont contribuer à faire passer Harry du statut d\'adolescent à celui d\'homme. Ce tome, sur fond de guerre contre un Voldemort plus puissant que jamais, se révèle plus sombre que les précédents. Secrets, alliances et trahisons conduisent aux événements les plus dramatiques qu\'Harry ait eu à affronter. Mais, en... ', 10, '2005-10-00', 'disponible', 'Fantastique', 'Grand Format', 10.99, '31 rue Madier de Montjau\r\n26000 Valence', 'Gallimard'),
('2070615367', 'Harry Potter - Tome 7 : Harry potter et les reliques de la mort', 2, '«Envers et contre tout» est une caractéristique-clé chez J.K. Rowling. Paradoxalement, c\'est lorsqu\'elle a continué à écrire avec une énergie, une passion, un engagement inentamés, en particulier à partir du tome 4 - alors qu\'elle était devenue l\'une des femmes les plus célèbres et riches au monde, et que chaque suite était attendue par des dizaines de millions de lecteurs du monde entier - , qu\'elle force le plus l\'admiration. Elle accomplit la mission qu\'elle s\'est donnée sans faillir, sans jamais décevoir.\r\nL\'ambition de... ', 10, '2007-10-27', 'emprunté', 'Fantastique', 'Grand Format', 15.99, '17, avenue Victor-Hugo Centre commercial Victor-Hugo - 26000  Valence\r\n\r\n', 'Gallimard'),
('2070624544', 'Harry Potter - : Harry Potter et le prisonnier d\'Azkaban', 2, 'Harry Potter a treize ans. Après des vacances insupportables chez les horribles Dursley, il retrouve ses fidèles amis, Ron et Hermione, pour prendre le train qui les ramène au collège Poudlard. Le monde des gens ordinaires, les Moldus, comme celui des sorciers, est en émoi : aux dernières nouvelles, Sirius Black, un dangereux criminel proche de Voldemort, s\'est échappé de la prison d\'Azkaban. Les redoutables gardiens de la prison assureront la sécurité du collège Poudlard, car le prisonnier évadé recherche Harry Potter, responsable de l\'élimination de son maître. C\'est donc sous bonne garde que l\'apprenti sorcier fait sa troisième rentrée. Au programme : des cours de divination, la fabrication d\'une potion de ratatinage, le dressage des hippogriffes... Mais Harry est-il vraiment à l\'abri du danger qui le menace ?', 10, '1999-10-19', 'emprunté', 'Fantastique', 'Grand Format', 9.99, '17, avenue Victor-Hugo Centre commercial Victor-Hugo - 26000  Valence\r\n\r\n', 'Gallimard'),
('2072847923', 'Les furtifs', 22, 'Ils sont là, parmi nous, jamais où tu regardes, à circuler dans les angles morts de la vision humaine. On les appelle les furtifs. Des fantômes ? Plutôt l\'exact inverse : des êtres de chair et de sons, à la vitalité hors norme, qui métabolisent dans leur trajet pierres, déchets, animaux ou plantes pour alimenter leurs métamorphoses incessantes. Lorca Varèse, sociologue pour communes autogérées, et sa femme, Sahar, proferrante dans la rue pour les enfants que l\'Education nationale, en faillite, a abandonnés, ont vu leur...', 7.6, '2021-02-04', 'hors stock', 'Science-fiction', 'Grand Format', 12.4, 'Place Charles de Gaulle à Chabeuil (Drôme)', 'Gallimard'),
('2253093289', 'Les Trois Mousquetaires - Intégral', 26, 'Dumas séduit, fascine, intéresse, amuse, enseigne.\r\nVictor Hugo.\r\n\r\nTout le monde connaît la verve prodigieuse de M. Dumas, son entrain facile, son bonheur de mise en scène, son dialogue spirituel et toujours en mouvement, ce récit léger qui court sans cesse et qui sait enlever l’obstacle et l’espace sans jamais faiblir. Il couvre d’immenses toiles sans jamais fatiguer ni son pinceau, ni son lecteur.\r\nSainte-Beuve.\r\n\r\nLes Trois Mousquetaires… notre seule épopée depuis le Moyen Âge.\r\nRoger Nimier.\r\n\r\nLes Trois Mousquetaires...', 3.5, '1844-00-00', 'disponible', 'Historique', 'Grand Format', 6.9, 'ZC le Plateau des Couleures\r\n26000 VALENCE\r\n07.57.59.94.95', 'Hachette'),
('2266282395', 'Le Seigneur Des Anneaux - Tome 1', 3, 'Aux temps reculés de ce récit, la Terre est peuplée d\'innombrables créatures : les Hobbits, apparentés à l\'Homme, les Elfes et les Nains vivent en paix. Une paix menacée depuis que l\'Anneau de Pouvoir, forgé par Sauron de Mordor, a été dérobé. Or cet anneau est doté d\'un pouvoir maléfique qui confère à son détenteur une autorité sans limite et fait de lui le Maître du monde. Sauron s\'est donc juré de le reconquérir...', 6.1, '1954-00-00', 'disponible', 'Fantastique', 'Poche', 8.74, '17, avenue Victor-Hugo Centre commercial Victor-Hugo - 26000  Valence\r\n\r\n', 'Gallimard'),
('2700238931', 'La Quête d\'Ewilan - Tome 1 : D\'un monde à l\'autre ', 14, 'La vie de Camille, adolescente surdouée, bascule quand elle pénètre accidentellement dans l’univers de Gwendalavir avec son ami Salim. Là des créatures, les Ts’liches, la reconnaissent sous le nom d’Ewilan et tentent de la tuer. Originaire de ce monde, elle est l’unique héritière d’un don prodigieux, le Dessin, qui peut s’avérer une arme fatale dans la lutte de son peuple pour reconquérir pouvoir, liberté et dignité. Épaulée par le maître d’armes de l’empereur et un vieil... ', 10, '2003-00-00', 'disponible', 'Fantastique', 'Grand Format', 8.4, 'ZC le Plateau des Couleures\r\n26000 VALENCE\r\n07.57.59.94.95', 'Rageot'),
('2700238958', 'La Quête d\'Ewilan - Tome 2 : Les frontières de glace ', 14, 'Revenus dans l’Empire de Gwendalavir, Ewilan et Salim partent avec leurs compagnons aux abords des Frontières de Glace pour libérer les Sentinelles. Ils repoussent en chemin les attaques de guerriers cochons, d’ogres et de mercenaires du Chaos, alliés des Ts’liches, mais se découvrent un peuple allié : les Faëls. Salim se lie d’amitié avec une marchombre, Ellana, dont les pouvoirs le fascinent ; tandis que, face au maître d’armes, Ewilan assoit son autorité et affermit... ', 10, '2003-06-17', 'disponible', 'Fantastique', 'Grand Format', 8.4, '17, avenue Victor-Hugo Centre commercial Victor-Hugo - 26000  Valence\r\n\r\n', 'Rageot'),
('2700256506', 'Le pacte des Marchombres - Tome 1 : Ellana', 14, 'Ellana, jeune fille d\'un autre monde, va faire ses premiers pas d\'apprentie sur la route des Marchombres. Elle rencontre Jilano Alhuïn qui l\'initie aux secrets de la guilde. Grand prix Roman jeunesse Lire-SNCF 2007. ', 10, '2006-10-25', 'hors stock', 'Fantastique', 'Grand Format', 15.99, 'Place Charles de Gaulle à Chabeuil (Drôme)', 'Gallimard'),
('2747037916', 'Miss Peregrine et les enfants particuliers - Tome 1', 31, 'Jacob Portman, 16 ans, écoute depuis son enfance les récits fabuleux de son grand-père. Ce dernier, un juif polonais, a passé une partie de sa vie sur une minuscule île du pays de Galles, où ses parents l\'avaient envoyé pour le protéger de la menace nazie. Le jeune Abe Portman y a été recueilli par Miss Peregrine Faucon, la directrice d\'un orphelinat pour enfants « particuliers ». Selon ses dires, Abe y côtoyait une ribambelle d\'enfants doués de capacités surnaturelles, censées les protéger des « Monstres ».Un soir, Jacob... ', 9, '2012-05-31', 'disponible', 'Fantastique', 'Grand Format', 27, '31 rue Madier de Montjau\r\n26000 Valence', 'Bayard Jeunesse'),
('2812608935', 'Les autodafeurs - Tome 3 : Nous sommes tous des propagateurs', 5, ' Réfugiés sur l\'île de Redonda à l\'abri des Autodafeurs avec les autres enfants de la Confrérie, Césarine, Auguste et Néné assistent de loin à la mise en oeuvre du plan de leur ennemi. La résistance s\'organise en réponse à la destruction des livres et à la prise de pouvoir par les Autodafeurs.', 9.2, '2015-05-06', 'emprunté', 'Aventure', 'Grand Format', 16.5, '17, avenue Victor-Hugo Centre commercial Victor-Hugo - 26000  Valence\r\n\r\n', 'Rageot'),
('2812619090', 'Les autodafeurs', 5, 'Je m\'appelle Auguste Mars, j\'ai 14 ans et je suis un dangereux délinquant.\r\nEnfin, ça, c\'est ce qu\'ont l\'air de penser la police, le juge pour mineur et la quasi-totalité des habitants de la ville.\r\nÉvidement, je suis totalement innocent des charges de \"violences aggravées, vol, effraction et incendie criminel\" qui pèsent contre moi mais pour le prouver, il faudrait que je révèle au monde l\'existence de la Confrérie et du complot mené par les Autodafeurs et j\'ai juré sur ma vie de garder le secret.\r\nDu coup, soit je trahis ma parole et je dévoile un secret vieux de vingt-cinq siècles (pas cool), soit je me tais et je passe pour un dangereux délinquant (pas cool non plus).\r\n', 9.1, '2014-05-02', 'emprunté', 'Aventure', 'Grand Format', 22.74, '17, avenue Victor-Hugo Centre commercial Victor-Hugo - 26000  Valence\r\n\r\n', 'Pocket Jeunesse'),
('2812623985', 'Les autodafeurs - Ma soeur est une artiste de guerre Tome 2', 5, 'Le Grand Jeu ne fait que commencer mais il a déjà coûté cher à la famille Mars. Après avoir perdu son père, ce sont les grand- parents d\'Auguste qui sont morts en affrontant les Autodafeurs et leur mère est toujours dans le coma suite à sa blessure à la tête. Auguste et Césarine n\'ont jamais été aussi seuls mais avec l\'aide de DeVergy et des membres de la Confrérie, ils vont devoir se préparer et se battre car les Autodafeurs n\'ont jamais été aussi près de parvenir à leur fin... Trilogie culte vendue à plus de 110 000... ', 9.4, '2016-00-00', 'hors stock', 'Aventure', 'Grand Format', 16.5, '31 rue Madier de Montjau\r\n26000 Valence', 'Rageot'),
('2890746623', 'Les Chevaliers d\'Emeraude - Tome 1 : Le feu dans le ciel ', 16, 'Se déroulant dans un monde oublié et dans des temps lointains, cette épopée tumultueuse raconte l\'histoire de Kira, l\'enfant mauve conçue lors du viol de la Reine Fan de Shola par Amecareth, l\'Empereur Noir. Les Chevaliers d\'Emeraude devront mener de durs combats pour protéger cette petite fille, afin que s\'accomplisse la prophétie qui verra la destruction d\'Amecareth. Apprenant que l\'Empereur Noir s\'apprête à envahir le continent de nouveau, le Roi d\'Emeraude, soucieux de protéger tous les peuples d\'Enkidiev, ressuscite un... ', 7.9, '2003-03-00', 'disponible', 'Fantastique', 'Poche', 10.99, 'Place Charles de Gaulle à Chabeuil (Drôme)', 'Wellan Inc'),
('9782070518425', 'Harry Potter, tome 1 : Harry Potter à l\'école des sorciers\r\n', 2, 'Pour et Mrs Dursley, qui habitaient au 4, Privet Drive, avaient toujours affirmé avec la plus grande fierté qu\'ils étaient parfaitement nor­maux, merci pour eux. Jamais quiconque n\'aurait imaginé qu\'ils puissent se trouver impliqués dans quoi que ce soit d\'étrange ou de mystérieux. Ils n\'avaient pas de temps à perdre avec des sornettes.', 10, '1998-00-00', 'emprunté', 'Fantastique', 'Poche', 10.99, '12, place des clercs 26000 Valence', 'Gallimard');

-- --------------------------------------------------------

--
-- Structure de la table `Note`
--

CREATE TABLE `Note` (
  `ID` int(11) NOT NULL,
  `Note` int(10) NOT NULL,
  `Utilisateur` varchar(50) NOT NULL,
  `Livre` varchar(13) NOT NULL
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

--
-- Déchargement des données de la table `Point de vente`
--

INSERT INTO `Point de vente` (`Adresse`, `Nom`, `Site web`, `Tel`) VALUES
('12, place des clercs 26000 Valence', 'La Licorne', 'https://fr-fr.facebook.com/librairie.lalicorne/', '0475829117'),
('17, avenue Victor-Hugo Centre commercial Victor-Hugo - 26000  Valence\r\n\r\n', 'Fnac', 'https://www.fnac.com/Valence/Fnac-Valence/cl51/w-4', '0825020020'),
('31 rue Madier de Montjau\r\n26000 Valence', 'L\'Étincelle', 'https://librairieletincelle.wordpress.com/', '0973137597'),
('Place Charles de Gaulle à Chabeuil (Drôme)', ' Librairie Ecriture', 'https://www.librairie-ecriture.fr/', '0475592948'),
('ZC le Plateau des Couleures\r\n26000 VALENCE\r\n07.57.59.94.95', 'Cultura', 'https://www.cultura.com', '0986860293');

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
-- Déchargement des données de la table `Utilisateur`
--

INSERT INTO `Utilisateur` (`email`, `mdp`, `Grade`, `Nom`, `Prénom`, `Adresse`, `Tel`) VALUES
('admin@admin.com', 'admin', 'admin', 'admin', 'admin', 'Chez M.Admin 26100 Valence', 'telAdmin'),
('camille@ewilan.com', 'camille', 'user', 'Duciel', 'Camille', '10 rue des dessins, Al-Jeit, Gwendalavir', '0541635218'),
('gaston@dupuis.com', 'gaston', 'user', 'Gaston', 'Lagaffe', 'Chez M. Gaston Lagaffe et Mademoiselle Jeanne.', '0623564891'),
('harrypotter@magic.com', 'harrypotter', 'user', 'Harry ', 'Potter ', 'Maison 9 3/4, Londres', '0650595152'),
('james@cherub.com', 'james', 'user', 'Adams', 'James', 'Inconnue, Angleterre', 'inconnue');

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
-- Index pour la table `Note`
--
ALTER TABLE `Note`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `Utilisateur` (`Utilisateur`),
  ADD KEY `Livre` (`Livre`);

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
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- AUTO_INCREMENT pour la table `Emprunt`
--
ALTER TABLE `Emprunt`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT pour la table `Note`
--
ALTER TABLE `Note`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;

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

--
-- Contraintes pour la table `Note`
--
ALTER TABLE `Note`
  ADD CONSTRAINT `Note_ibfk_1` FOREIGN KEY (`Utilisateur`) REFERENCES `Utilisateur` (`email`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `Note_ibfk_2` FOREIGN KEY (`Livre`) REFERENCES `Livre` (`ISBN`) ON DELETE NO ACTION ON UPDATE NO ACTION;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
