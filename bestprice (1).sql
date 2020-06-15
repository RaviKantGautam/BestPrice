-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 10, 2020 at 02:03 PM
-- Server version: 10.1.36-MariaDB
-- PHP Version: 7.2.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `bestprice`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `email` varchar(500) NOT NULL,
  `password` varchar(500) NOT NULL,
  `type` varchar(500) NOT NULL,
  `mobile` varchar(100) NOT NULL,
  `username` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`email`, `password`, `type`, `mobile`, `username`) VALUES
('admin@gmail.com', '123', 'admin', '6280406195', 'harpreet');

-- --------------------------------------------------------

--
-- Table structure for table `bill`
--

CREATE TABLE `bill` (
  `billid` int(11) NOT NULL,
  `dateofbill` date NOT NULL,
  `modeofbill` varchar(500) NOT NULL,
  `totalbill` float NOT NULL,
  `memberid` int(11) NOT NULL,
  `storeid` int(11) NOT NULL,
  `modeofpayment` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `bill`
--

INSERT INTO `bill` (`billid`, `dateofbill`, `modeofbill`, `totalbill`, `memberid`, `storeid`, `modeofpayment`) VALUES
(8, '2020-05-13', 'ONLINE', 19000, 4, 8, 'online'),
(9, '2020-05-13', 'ONLINE', 21800, 4, 9, 'online');

-- --------------------------------------------------------

--
-- Table structure for table `billdetail`
--

CREATE TABLE `billdetail` (
  `bdid` int(11) NOT NULL,
  `productid` int(11) NOT NULL,
  `price` float NOT NULL,
  `qty` int(11) NOT NULL,
  `billid` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `billdetail`
--

INSERT INTO `billdetail` (`bdid`, `productid`, `price`, `qty`, `billid`) VALUES
(13, 11, 19000, 1, 8),
(14, 13, 10900, 2, 9);

-- --------------------------------------------------------

--
-- Table structure for table `category`
--

CREATE TABLE `category` (
  `cname` varchar(500) NOT NULL,
  `description` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `category`
--

INSERT INTO `category` (`cname`, `description`) VALUES
('fashion', 'jeans , shoes , shirts and other fashion accessories.'),
('furniture', 'different kinds of furniture like chairs , sofa set , beds and table etc.'),
('house hold things', 'household daily used grocery such as spices , oil etc.'),
('kitchen accessories', 'microwave , spoons, and all other devices used in kitchen.'),
('medicines', 'vitamins , minerals and other medicines to boost health.');

-- --------------------------------------------------------

--
-- Table structure for table `members`
--

CREATE TABLE `members` (
  `memberid` int(11) NOT NULL,
  `memberentityname` varchar(500) NOT NULL,
  `poc` varchar(500) NOT NULL,
  `mobile` varchar(500) NOT NULL,
  `email` varchar(500) NOT NULL,
  `password` varchar(500) NOT NULL,
  `addoncardname1` varchar(500) NOT NULL,
  `addoncardname2` varchar(500) NOT NULL,
  `addoncardname3` varchar(500) NOT NULL,
  `parentstore` int(11) NOT NULL,
  `status` varchar(500) NOT NULL DEFAULT 'pending'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `members`
--

INSERT INTO `members` (`memberid`, `memberentityname`, `poc`, `mobile`, `email`, `password`, `addoncardname1`, `addoncardname2`, `addoncardname3`, `parentstore`, `status`) VALUES
(4, 'Harpreet Singh', '123456', '6280406195', 'harpreet.singh96@yahoo.com', '123', '123c1', '123c2', '123c3', 6, 'pending');

-- --------------------------------------------------------

--
-- Table structure for table `photos`
--

CREATE TABLE `photos` (
  `photoid` int(11) NOT NULL,
  `pid` int(11) NOT NULL,
  `photopath` varchar(500) NOT NULL,
  `type` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `photos`
--

INSERT INTO `photos` (`photoid`, `pid`, `photopath`, `type`) VALUES
(9, 10, 'jeans2.jpg', 'front photo'),
(10, 11, 'sofa2.jpg', 'photo1'),
(11, 11, 'sofa4.jpg', 'photo2'),
(12, 12, 'cookingoil3.jpg', 'photo1'),
(13, 13, 'oven3.jpg', 'photo1');

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `productid` int(11) NOT NULL,
  `productname` varchar(500) NOT NULL,
  `price` float NOT NULL,
  `priceafterdiscount` float NOT NULL,
  `description` varchar(500) NOT NULL,
  `brand` varchar(500) NOT NULL,
  `cname` varchar(500) NOT NULL,
  `photo` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`productid`, `productname`, `price`, `priceafterdiscount`, `description`, `brand`, `cname`, `photo`) VALUES
(10, 'jeans', 1520, 1250, 'jeans for summer and winter season.', 'nike', 'fashion', 'jeans1.jpg'),
(11, 'sofa set', 20500, 19000, 'comfortable sofa set', 'other', 'furniture', 'sfoa1.jpg'),
(12, 'cooking oil', 350, 320, 'cooking oil for household things', 'other', 'house hold things', 'cookingoil2.jpg'),
(13, 'microwave', 11500, 10900, 'best microwave to cook and heat food', 'other', 'kitchen accessories', 'oven2.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `stock`
--

CREATE TABLE `stock` (
  `stockid` int(11) NOT NULL,
  `productid` int(11) NOT NULL,
  `qty` int(11) NOT NULL,
  `storeid` int(11) NOT NULL,
  `expirydate` date NOT NULL,
  `purchasedate` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `stock`
--

INSERT INTO `stock` (`stockid`, `productid`, `qty`, `storeid`, `expirydate`, `purchasedate`) VALUES
(15, 11, 10, 8, '2020-05-30', '2020-05-15'),
(16, 12, 50, 6, '2020-05-29', '2020-05-15'),
(17, 13, 100, 9, '2020-05-30', '2020-05-16'),
(18, 10, 200, 10, '2020-05-30', '2020-05-08'),
(19, 10, 20, 10, '0000-00-00', '0000-00-00');

-- --------------------------------------------------------

--
-- Table structure for table `stores`
--

CREATE TABLE `stores` (
  `storeid` int(11) NOT NULL,
  `title` varchar(500) NOT NULL,
  `emailid` varchar(500) NOT NULL,
  `password` varchar(500) NOT NULL,
  `location` varchar(500) NOT NULL,
  `mobilenumber` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `stores`
--

INSERT INTO `stores` (`storeid`, `title`, `emailid`, `password`, `location`, `mobilenumber`) VALUES
(6, 'Grocery Store', 'grocerystore@gmail.com', '123', 'Amritsar Punjab', '6280406195'),
(7, 'Medicines Store', 'medicinesstore@gmail.com', '123', 'Amritsar Punjab', '6280406195'),
(8, 'Furniture Store', 'furniturestore@gmail.com', '123', 'Amritsar Punjab', '6280406195'),
(9, 'Kitchen Accessories Store', 'kitchenaccessoriesstore@gmail.com', '123', 'Amritsar Punjab', '6280406195'),
(10, 'Fashion Store', 'fashionstore@gmail.com', '123', 'Amritsar Punjab', '6280406195');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`email`);

--
-- Indexes for table `bill`
--
ALTER TABLE `bill`
  ADD PRIMARY KEY (`billid`),
  ADD KEY `memberid` (`memberid`),
  ADD KEY `storeid` (`storeid`);

--
-- Indexes for table `billdetail`
--
ALTER TABLE `billdetail`
  ADD PRIMARY KEY (`bdid`),
  ADD KEY `productid` (`productid`),
  ADD KEY `billid` (`billid`);

--
-- Indexes for table `category`
--
ALTER TABLE `category`
  ADD PRIMARY KEY (`cname`);

--
-- Indexes for table `members`
--
ALTER TABLE `members`
  ADD PRIMARY KEY (`memberid`),
  ADD KEY `parentstore` (`parentstore`);

--
-- Indexes for table `photos`
--
ALTER TABLE `photos`
  ADD PRIMARY KEY (`photoid`),
  ADD KEY `pid` (`pid`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`productid`),
  ADD KEY `category` (`cname`);

--
-- Indexes for table `stock`
--
ALTER TABLE `stock`
  ADD PRIMARY KEY (`stockid`),
  ADD KEY `storeid` (`storeid`),
  ADD KEY `productid` (`productid`);

--
-- Indexes for table `stores`
--
ALTER TABLE `stores`
  ADD PRIMARY KEY (`storeid`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `bill`
--
ALTER TABLE `bill`
  MODIFY `billid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `billdetail`
--
ALTER TABLE `billdetail`
  MODIFY `bdid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `members`
--
ALTER TABLE `members`
  MODIFY `memberid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `photos`
--
ALTER TABLE `photos`
  MODIFY `photoid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `productid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `stock`
--
ALTER TABLE `stock`
  MODIFY `stockid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `stores`
--
ALTER TABLE `stores`
  MODIFY `storeid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `bill`
--
ALTER TABLE `bill`
  ADD CONSTRAINT `bill_ibfk_1` FOREIGN KEY (`memberid`) REFERENCES `members` (`memberid`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `bill_ibfk_2` FOREIGN KEY (`storeid`) REFERENCES `stores` (`storeid`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `billdetail`
--
ALTER TABLE `billdetail`
  ADD CONSTRAINT `billdetail_ibfk_1` FOREIGN KEY (`billid`) REFERENCES `bill` (`billid`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `billdetail_ibfk_2` FOREIGN KEY (`productid`) REFERENCES `products` (`productid`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `members`
--
ALTER TABLE `members`
  ADD CONSTRAINT `members_ibfk_1` FOREIGN KEY (`parentstore`) REFERENCES `stores` (`storeid`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `photos`
--
ALTER TABLE `photos`
  ADD CONSTRAINT `photos_ibfk_1` FOREIGN KEY (`pid`) REFERENCES `products` (`productid`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `products`
--
ALTER TABLE `products`
  ADD CONSTRAINT `products_ibfk_1` FOREIGN KEY (`cname`) REFERENCES `category` (`cname`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `stock`
--
ALTER TABLE `stock`
  ADD CONSTRAINT `stock_ibfk_1` FOREIGN KEY (`productid`) REFERENCES `products` (`productid`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `stock_ibfk_2` FOREIGN KEY (`storeid`) REFERENCES `stores` (`storeid`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
