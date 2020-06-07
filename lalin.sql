-- phpMyAdmin SQL Dump
-- version 4.9.0.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 07, 2020 at 10:50 AM
-- Server version: 10.4.6-MariaDB
-- PHP Version: 7.3.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `lalin`
--

-- --------------------------------------------------------

--
-- Table structure for table `calendar`
--

CREATE TABLE `calendar` (
  `id` int(11) NOT NULL,
  `Topic_ID` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `Term` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `Start_Date` date NOT NULL,
  `Finish_Date` date NOT NULL,
  `Year` varchar(200) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `calendar`
--

INSERT INTO `calendar` (`id`, `Topic_ID`, `Term`, `Start_Date`, `Finish_Date`, `Year`) VALUES
(2, '5', '1', '2020-07-08', '2020-07-12', '2563'),
(3, '1', '1', '2020-06-29', '0000-00-00', '2563'),
(4, '2', '1', '2020-08-08', '2020-08-15', '2563');

-- --------------------------------------------------------

--
-- Table structure for table `gpa`
--

CREATE TABLE `gpa` (
  `Rows_id` int(11) NOT NULL,
  `Subject_ID` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `Name_TH` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `Unit` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `gpa`
--

INSERT INTO `gpa` (`Rows_id`, `Subject_ID`, `Name_TH`, `Unit`) VALUES
(1, '225111', 'การเขียนโปรแกรมเชิงโครงสร้าง', 3),
(2, '225434', 'สถาปัตยกรรมคอมพิวเตอร์', 4),
(3, '225101', 'ตรรกะพื้นฐานและการแก้ปัญหา', 5),
(4, '241334', 'คณิตศาสตร์เต็มหน่วย', 2);

-- --------------------------------------------------------

--
-- Table structure for table `topic`
--

CREATE TABLE `topic` (
  `Topic_ID` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `Topic` char(255) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `topic`
--

INSERT INTO `topic` (`Topic_ID`, `Topic`) VALUES
('1', 'เปิดเทอม'),
('2', 'สอบกลางภาค'),
('3', 'สอบปลายภาค'),
('4', 'ปิดเทอม'),
('5', 'ชำระค่าลงทะเบียนทุกชั้นปี');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `calendar`
--
ALTER TABLE `calendar`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id` (`Topic_ID`);

--
-- Indexes for table `gpa`
--
ALTER TABLE `gpa`
  ADD PRIMARY KEY (`Rows_id`);

--
-- Indexes for table `topic`
--
ALTER TABLE `topic`
  ADD PRIMARY KEY (`Topic_ID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `calendar`
--
ALTER TABLE `calendar`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `gpa`
--
ALTER TABLE `gpa`
  MODIFY `Rows_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `calendar`
--
ALTER TABLE `calendar`
  ADD CONSTRAINT `calendar_ibfk_1` FOREIGN KEY (`Topic_ID`) REFERENCES `topic` (`Topic_ID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
