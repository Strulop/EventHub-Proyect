-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: bd_eventos
-- ------------------------------------------------------
-- Server version	8.0.41

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `categoria`
--

DROP TABLE IF EXISTS `categoria`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categoria` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categoria`
--

LOCK TABLES `categoria` WRITE;
/*!40000 ALTER TABLE `categoria` DISABLE KEYS */;
INSERT INTO `categoria` VALUES (1,'Conciertos'),(2,'Conferencias'),(3,'Deportes'),(4,'Teatro'),(5,'Gastronomía'),(6,'Ciencias');
/*!40000 ALTER TABLE `categoria` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `eventos`
--

DROP TABLE IF EXISTS `eventos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `eventos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(150) NOT NULL,
  `descripcion` text,
  `duracion` int NOT NULL,
  `hora_inicio` time NOT NULL,
  `precio` int NOT NULL,
  `fecha` date NOT NULL,
  `capacidad` int NOT NULL,
  `tickets_disponibles` int NOT NULL,
  `url_imagen` varchar(255) NOT NULL,
  `id_organizador` int NOT NULL,
  `id_categoria` int NOT NULL,
  `id_ubicacion` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id_organizador` (`id_organizador`),
  KEY `id_categoria` (`id_categoria`),
  KEY `id_ubicacion` (`id_ubicacion`),
  CONSTRAINT `eventos_ibfk_1` FOREIGN KEY (`id_organizador`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE,
  CONSTRAINT `eventos_ibfk_2` FOREIGN KEY (`id_categoria`) REFERENCES `categoria` (`id`) ON DELETE CASCADE,
  CONSTRAINT `eventos_ibfk_3` FOREIGN KEY (`id_ubicacion`) REFERENCES `ubicacion` (`id`) ON DELETE CASCADE,
  CONSTRAINT `eventos_chk_1` CHECK ((`duracion` > 0)),
  CONSTRAINT `eventos_chk_2` CHECK ((`precio` > 0)),
  CONSTRAINT `eventos_chk_3` CHECK ((`capacidad` > 0)),
  CONSTRAINT `eventos_chk_4` CHECK ((`tickets_disponibles` > 0))
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `eventos`
--

LOCK TABLES `eventos` WRITE;
/*!40000 ALTER TABLE `eventos` DISABLE KEYS */;
INSERT INTO `eventos` VALUES (1,'Charla Tech 2031','Una charla sobre las tendencias tecnológicas del año 2030, inteligencia artificial, IoT y más.',120,'18:00:00',20,'2025-06-15',200,200,'https://ik.imagekit.io/otcvghwe9/Imagenes_Eventos/evento_conferencia_1.png?updatedAt=1740678888383',2,2,2),(2,'Concierto Nocturno de Estrellas','Un espectáculo musical con artistas emergentes bajo un cielo estrellado.',180,'21:30:00',50,'2025-07-10',500,500,'https://ik.imagekit.io/otcvghwe9/Imagenes_Eventos/concierto.png?updatedAt=1740682617533',2,1,3),(3,'Maratón 15 Km','Carrera de 15 kilómetros.',120,'08:00:00',15,'2025-06-25',1000,1000,'https://ik.imagekit.io/otcvghwe9/Imagenes_Eventos/maraton.png?updatedAt=1740682617299',2,3,4),(4,'Obra de Teatro: Sombras del Pasado','Una obra de teatro que explora la memoria y los secretos ocultos de una familia.',150,'20:00:00',30,'2025-08-05',300,300,'https://ik.imagekit.io/otcvghwe9/Imagenes_Eventos/obra%20teatro.png?updatedAt=1740682617303',2,4,5),(5,'Feria del Sabor Loco','Un evento gastronómico con degustaciones de comida internacional y chefs invitados.',240,'12:00:00',25,'2025-02-10',600,600,'https://ik.imagekit.io/otcvghwe9/Imagenes_Eventos/gastro.png?updatedAt=1740682617439',2,5,4),(6,'Cumbre de Innovación Empresarial','Líderes de la industria se reúnen para discutir el futuro de los negocios.',180,'09:00:00',100,'2025-10-20',150,150,'https://ik.imagekit.io/otcvghwe9/Imagenes_Eventos/cumbre.png?updatedAt=1740682617499',2,2,2),(7,'Conferencia sobre situación aranceles','Se expondra las posibles consecuencias y soluciones para la actual crisis y malestar, frente a la problematica de los aranceles.',180,'10:50:00',100,'2025-09-20',150,150,'https://ik.imagekit.io/otcvghwe9/Imagenes_Eventos/aranceles.png?updatedAt=1740684406926',2,1,2),(13,'Festival Internacional de Arte y Cultura','Este evento reúne a artistas y creadores de todo el mundo para presentar sus obras más innovadoras. El festival incluye exhibiciones de pintura, escultura, danza y música, además de talleres y charlas magistrales. Se celebra en un espacio al aire libre, rodeado de un ambiente festivo donde se fomenta la colaboración y el intercambio cultural.',340,'12:30:00',25,'2025-06-15',250,250,'https://ik.imagekit.io/otcvghwe9/Imagenes_Eventos/Festival%20Internacional%20de%20Arte%20y%20M%C3%BAsica.png?updatedAt=1741378319740',2,5,5);
/*!40000 ALTER TABLE `eventos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tickets`
--

DROP TABLE IF EXISTS `tickets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tickets` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuario_id` int NOT NULL,
  `evento_id` int NOT NULL,
  `codigo` varchar(50) NOT NULL,
  `fecha_compra` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `codigo` (`codigo`),
  KEY `usuario_id` (`usuario_id`),
  KEY `evento_id` (`evento_id`),
  CONSTRAINT `tickets_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE,
  CONSTRAINT `tickets_ibfk_2` FOREIGN KEY (`evento_id`) REFERENCES `eventos` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tickets`
--

LOCK TABLES `tickets` WRITE;
/*!40000 ALTER TABLE `tickets` DISABLE KEYS */;
/*!40000 ALTER TABLE `tickets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ubicacion`
--

DROP TABLE IF EXISTS `ubicacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ubicacion` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ubicacion`
--

LOCK TABLES `ubicacion` WRITE;
/*!40000 ALTER TABLE `ubicacion` DISABLE KEYS */;
INSERT INTO `ubicacion` VALUES (1,'Ceuta'),(2,'Barcelona'),(3,'Valencia'),(4,'Sevilla'),(5,'Toledo'),(7,'Bilbao'),(8,'Madrid');
/*!40000 ALTER TABLE `ubicacion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `contra` varchar(500) NOT NULL,
  `rol` enum('organizador','asistente') NOT NULL,
  `fecha_registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (1,'Tomas','tomas@gmail.com','scrypt:32768:8:1$cV7Ufg79QIuRabcc$d8e4699f0f23f98f01d3e632161032af73471628d3af935a5c261f449547642adbdde7c31b6c73e7ee2be94a306a80a1f0926498786de53ba134949767546c5a','organizador','2025-02-26 23:00:00'),(2,'Manuel','manuel@gmail.com','scrypt:32768:8:1$DQFwEvyvPcxHfuq0$ea529b94a6f8759ddceaea14ea4a808d18253789fb09fcadcb6d06b5c756d36a0d83561b61ef30009c8fd3f12bd3378e216d3e4dd77947c47e3863e78703ea4e','organizador','2025-02-26 23:00:00'),(4,'ricardo','ricardo@gmail.com','scrypt:32768:8:1$X12JQ0W6NSSgT3zZ$0d989a92ec0a0fa0a4102925a917aa11083f598dc44e49ae9b041a552055c194c2e3ec700447ab307606c98b6e56a768bfd893cff4731ca9fd0bff89cf4b2066','asistente','2025-02-26 23:00:00'),(5,'juanjo','juanjo@gmail.com','scrypt:32768:8:1$im7yeZh0vZjtLhQ2$c5804179e72796b609744ea3bdba582a156a4bafffecdb10c72f3afcfcef2ac55dc7bfadd40e13f945569d49159b209f3f09759941acf0a3df91a9fb3415a66f','asistente','2025-02-26 23:00:00'),(7,'sergio','sergiotru88@gmail.com','scrypt:32768:8:1$aHLJYscVtt887XFM$f7765b0e0159fb3008da927b1e9bcc4bb4bb5902db525a42748bdaa4ba4907dfd06f9d7070c582fe2ecd16f5870df943e7013516199a56b447e3fc32f6a1b88a','asistente','2025-03-06 23:00:00'),(9,'tomas heduan','tomasheduan@gmail.com','scrypt:32768:8:1$cgV7cPcMWAmwVyLF$bb3fbf6cfb4a26e5e968bcea922b7b25c194c46d3372211bc28e6d1f6f1ac27e461e7cc0994fb78f9c92e07d19c857e5d4b23cf0ab28730247eb4463e407904d','asistente','2025-03-17 23:00:00');
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-20 18:48:13
