-- MySQL dump 10.13  Distrib 8.0.40, for Linux (x86_64)
--
-- Host: localhost    Database: SpinStand
-- ------------------------------------------------------
-- Server version	8.0.40-0ubuntu0.24.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Fruit`
--

DROP TABLE IF EXISTS `Fruit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Fruit` (
  `ProductID` int NOT NULL,
  `SpecialCare` varchar(255) DEFAULT NULL,
  `Variety` varchar(255) DEFAULT NULL,
  `UnitPrice` decimal(10,2) DEFAULT NULL,
  `HarvestDate` date DEFAULT NULL,
  `YearPrice` int DEFAULT NULL,
  PRIMARY KEY (`ProductID`),
  CONSTRAINT `Fruit_ibfk_1` FOREIGN KEY (`ProductID`) REFERENCES `Product` (`ProductID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fruit`
--

LOCK TABLES `Fruit` WRITE;
/*!40000 ALTER TABLE `Fruit` DISABLE KEYS */;
INSERT INTO `Fruit` VALUES (1,'PickedandPacked','Tart',10.00,NULL,2024),(2,'U-Pick','Marquette',4.00,NULL,2024),(3,'Freeze','BlushingStar',8.00,NULL,2023),(4,'PickedandPacked','Arctic Glo',8.00,NULL,2023),(5,'U-Pick','Jupiter',5.00,NULL,2023),(6,'U-Pick','Rainier',10.00,NULL,2024),(7,'U-Pick','Montmorrency',10.00,NULL,2024),(8,'U-Pick','Skeena',10.00,NULL,2024),(9,'U-Pick','Sweetheart',10.00,NULL,2024),(10,'PickedandPacked','ColumbiaStar',8.00,NULL,2024),(11,'PickedandPacked','RedGeorge',8.00,NULL,2024),(12,'PickedandPacked','Gold',8.00,NULL,2024),(13,'PickedandPacked','Champagne',10.00,NULL,2024),(14,'PickedandPacked','Honeycrisp',6.00,NULL,2024),(15,'PickedandPacked','AuroraBorealis',12.00,NULL,2024);
/*!40000 ALTER TABLE `Fruit` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `OrderProduct`
--

DROP TABLE IF EXISTS `OrderProduct`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `OrderProduct` (
  `OrderID` int NOT NULL,
  `ProductID` int NOT NULL,
  `Quantity` int NOT NULL,
  PRIMARY KEY (`OrderID`,`ProductID`),
  KEY `ProductID` (`ProductID`),
  CONSTRAINT `OrderProduct_ibfk_1` FOREIGN KEY (`OrderID`) REFERENCES `SalesOrder` (`OrderID`) ON DELETE CASCADE,
  CONSTRAINT `OrderProduct_ibfk_2` FOREIGN KEY (`ProductID`) REFERENCES `Product` (`ProductID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `OrderProduct`
--

LOCK TABLES `OrderProduct` WRITE;
/*!40000 ALTER TABLE `OrderProduct` DISABLE KEYS */;
INSERT INTO `OrderProduct` VALUES (1,1,80),(2,2,250);
/*!40000 ALTER TABLE `OrderProduct` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Person`
--

DROP TABLE IF EXISTS `Person`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Person` (
  `PersonID` int NOT NULL AUTO_INCREMENT,
  `FirstName` varchar(100) NOT NULL,
  `LastName` varchar(100) NOT NULL,
  `PhoneNumber` varchar(15) DEFAULT NULL,
  `Email` varchar(255) DEFAULT NULL,
  `Company` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`PersonID`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Person`
--

LOCK TABLES `Person` WRITE;
/*!40000 ALTER TABLE `Person` DISABLE KEYS */;
INSERT INTO `Person` VALUES (1,'Sylvie','Von Doersten','801-888-1111','sylvievond@gmail.com','Spindrift Organics'),(2,'Felix','Bacon','801-888-2222','felix@gmail.com','Spindrift Organics'),(3,'Melissa','Kagaya','801-888-3333','keytothemountain@gmail.com','Key to the Mountain'),(4,'Martha','Pundsack','3479090972','martha@bentfrenchman.com','Arcadian Winery'),(5,'Andy','Sponseller','406-218-8095','tenspoonwinery@gmail.com','Ten Spoon Winery'),(6,'Laura','Miller','406-253-9357','gatewayorchard@gmail.com','Gateway Orchard'),(8,'Howie','Long','917-658-7878','firebrand@earthlink.net','Firebrand Orchard'),(9,'Alexis','Von Doersten','406-360-2112','ARVenterprises@gmail.com','ARV, Enterprises'),(10,'Kelly','Moriarty','566-676-6687','kelly90803@yahoo.com','Brady Inc.'),(12,'Bill','McLaughlin','406-541-3772','butteinsuranceprof@gmail.com',''),(13,'Keila','Cross','406-360-1359','artastherapy@gmail.com','crossarttherapy@gmail.com'),(24,'Frank','Brickowski','503-779-3296','highliner@earthlink.net','Portland Trailblazers'),(25,'Paul','Beighle','406-274-7012','paulbeighle@gmail.com','Brothers Orchard');
/*!40000 ALTER TABLE `Person` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Product`
--

DROP TABLE IF EXISTS `Product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Product` (
  `ProductID` int NOT NULL AUTO_INCREMENT,
  `ProductName` varchar(255) NOT NULL,
  `ProductType` enum('produce','event','other') NOT NULL,
  PRIMARY KEY (`ProductID`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Product`
--

LOCK TABLES `Product` WRITE;
/*!40000 ALTER TABLE `Product` DISABLE KEYS */;
INSERT INTO `Product` VALUES (1,'Cherry','produce'),(2,'WineGrape','produce'),(3,'Peach','produce'),(4,'Nectarine','produce'),(5,'TableGrape','produce'),(6,'RainierCherry','produce'),(7,'MontmorrencyCherry','produce'),(8,'SkeenaCherry','produce'),(9,'SweetheartCherry','produce'),(10,'Blackberry','produce'),(11,'Gooseberry','produce'),(12,'Raspberry','produce'),(13,'Current','produce'),(14,'Apple','produce'),(15,'Honeyberry','produce');
/*!40000 ALTER TABLE `Product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ProductSeasonAvailability`
--

DROP TABLE IF EXISTS `ProductSeasonAvailability`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ProductSeasonAvailability` (
  `ProductID` int NOT NULL,
  `SeasonAvailability` varchar(100) NOT NULL,
  PRIMARY KEY (`ProductID`,`SeasonAvailability`),
  CONSTRAINT `ProductSeasonAvailability_ibfk_1` FOREIGN KEY (`ProductID`) REFERENCES `Product` (`ProductID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ProductSeasonAvailability`
--

LOCK TABLES `ProductSeasonAvailability` WRITE;
/*!40000 ALTER TABLE `ProductSeasonAvailability` DISABLE KEYS */;
INSERT INTO `ProductSeasonAvailability` VALUES (1,'Spring'),(1,'Summer'),(2,'Fall'),(3,'Summer'),(4,'Summer'),(5,'Fall'),(6,'Summer'),(7,'Summer'),(8,'Summer'),(9,'Summer'),(10,'Fall'),(10,'Summer'),(11,'Summer'),(13,'Fall'),(14,'Fall'),(15,'Spring');
/*!40000 ALTER TABLE `ProductSeasonAvailability` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `SalesOrder`
--

DROP TABLE IF EXISTS `SalesOrder`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `SalesOrder` (
  `OrderID` int NOT NULL AUTO_INCREMENT,
  `OrderDate` datetime NOT NULL,
  `TotalCost` decimal(10,2) NOT NULL,
  `PersonID` int DEFAULT NULL,
  PRIMARY KEY (`OrderID`),
  KEY `PersonID` (`PersonID`),
  CONSTRAINT `SalesOrder_ibfk_1` FOREIGN KEY (`PersonID`) REFERENCES `Person` (`PersonID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SalesOrder`
--

LOCK TABLES `SalesOrder` WRITE;
/*!40000 ALTER TABLE `SalesOrder` DISABLE KEYS */;
INSERT INTO `SalesOrder` VALUES (1,'2024-07-22 09:30:00',800.00,3),(2,'2024-10-22 10:45:00',1000.00,4);
/*!40000 ALTER TABLE `SalesOrder` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `TimeSheet`
--

DROP TABLE IF EXISTS `TimeSheet`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `TimeSheet` (
  `TimeSheetID` int NOT NULL AUTO_INCREMENT,
  `Rate` decimal(10,2) NOT NULL,
  `Description` varchar(255) DEFAULT NULL,
  `PersonID` int DEFAULT NULL,
  PRIMARY KEY (`TimeSheetID`),
  KEY `PersonID` (`PersonID`),
  CONSTRAINT `TimeSheet_ibfk_1` FOREIGN KEY (`PersonID`) REFERENCES `Person` (`PersonID`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `TimeSheet`
--

LOCK TABLES `TimeSheet` WRITE;
/*!40000 ALTER TABLE `TimeSheet` DISABLE KEYS */;
INSERT INTO `TimeSheet` VALUES (1,20.00,'Harvest',1),(2,16.00,'Maintenance',2);
/*!40000 ALTER TABLE `TimeSheet` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-11-16 18:31:39
