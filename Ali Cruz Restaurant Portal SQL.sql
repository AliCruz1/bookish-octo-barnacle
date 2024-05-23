-- Use the existing database
USE restaurant_reservations;

-- Create the Customers table
CREATE TABLE IF NOT EXISTS `Customers` (
    customerId INT NOT NULL AUTO_INCREMENT,
    customerName VARCHAR(45) NOT NULL,
    contactInfo VARCHAR(200),
    PRIMARY KEY (customerId)
);

-- Create the Reservations table
CREATE TABLE IF NOT EXISTS `Reservations` (
    reservationId INT NOT NULL AUTO_INCREMENT,
    customerId INT NOT NULL,
    reservationTime DATETIME NOT NULL,
    numberOfGuests INT NOT NULL,
    specialRequests VARCHAR(200),
    PRIMARY KEY (reservationId),
    FOREIGN KEY (customerId) REFERENCES `Customers`(customerId) ON DELETE CASCADE
);

-- Create the DiningPreferences table
CREATE TABLE IF NOT EXISTS `DiningPreferences` (
    preferenceId INT NOT NULL AUTO_INCREMENT,
    customerId INT NOT NULL,
    favoriteTable VARCHAR(45),
    dietaryRestrictions VARCHAR(200),
    PRIMARY KEY (preferenceId),
    FOREIGN KEY (customerId) REFERENCES `Customers`(customerId) ON DELETE CASCADE
);

-- Insert initial data into Customers table
INSERT IGNORE INTO `Customers` (customerName, contactInfo) VALUES 
('LeBron James', 'lebron.james@gmail.com'),
('Stephen Curry', 'stephen.curry@gmail.com'),
('Kevin Durant', 'kevin.durant@gmail.com');

-- Insert initial data into Reservations table
INSERT IGNORE INTO `Reservations` (customerId, reservationTime, numberOfGuests, specialRequests) VALUES 
((SELECT customerId FROM `Customers` WHERE customerName='LeBron James'), '2024-05-20 19:00:00', 4, 'Vegetarian'),
((SELECT customerId FROM `Customers` WHERE customerName='Stephen Curry'), '2024-05-21 18:30:00', 2, 'Window Seat'),
((SELECT customerId FROM `Customers` WHERE customerName='Kevin Durant'), '2024-05-22 20:00:00', 3, 'Birthday Celebration');

-- Insert initial data into DiningPreferences table
INSERT IGNORE INTO `DiningPreferences` (customerId, favoriteTable, dietaryRestrictions) VALUES 
((SELECT customerId FROM `Customers` WHERE customerName='LeBron James'), 'Table 5', 'Vegetarian'),
((SELECT customerId FROM `Customers` WHERE customerName='Stephen Curry'), 'Table 2', 'Gluten-free'),
((SELECT customerId FROM `Customers` WHERE customerName='Kevin Durant'), 'Table 8', 'None');

-- Create a stored procedure to find reservations for a specific customer
DELIMITER //
CREATE PROCEDURE `findReservations`(IN customer_id INT)
BEGIN
    SELECT Reservations.*, Customers.customerName, Customers.contactInfo 
    FROM `Reservations`
    JOIN `Customers` ON `Reservations`.customerId = `Customers`.customerId 
    WHERE `Reservations`.customerId = customer_id;
END //
DELIMITER ;

-- Create a stored procedure to add a special request to a reservation
DELIMITER //
CREATE PROCEDURE `addSpecialRequest`(IN reservation_id INT, IN requests VARCHAR(200))
BEGIN
    UPDATE `Reservations`
    SET specialRequests = requests 
    WHERE reservationId = reservation_id;
END //
DELIMITER ;

-- Create a stored procedure to add a reservation (with customer check and insertion)
DELIMITER //
CREATE PROCEDURE `addReservation`(IN customer_name VARCHAR(45), IN contact_info VARCHAR(200), IN reservation_time DATETIME, IN number_of_guests INT, IN special_requests VARCHAR(200))
BEGIN
    DECLARE customer_id INT;
    
    -- Check if customer exists
    SELECT customerId INTO customer_id 
    FROM `Customers` 
    WHERE customerName = customer_name AND contactInfo = contact_info;
    
    -- If customer does not exist, add the customer
    IF customer_id IS NULL THEN
        INSERT INTO `Customers` (customerName, contactInfo) VALUES (customer_name, contact_info);
        SET customer_id = LAST_INSERT_ID();
    END IF;
    
    -- Add reservation
    INSERT INTO `Reservations` (customerId, reservationTime, numberOfGuests, specialRequests) 
    VALUES (customer_id, reservation_time, number_of_guests, special_requests);
END //
DELIMITER ;

-- Create a stored procedure to update a reservation
DELIMITER //
CREATE PROCEDURE `updateReservation`(IN reservation_id INT, IN reservation_time DATETIME, IN number_of_guests INT, IN special_requests VARCHAR(200))
BEGIN
    UPDATE `Reservations`
    SET reservationTime = reservation_time,
        numberOfGuests = number_of_guests,
        specialRequests = special_requests
    WHERE reservationId = reservation_id;
END //
DELIMITER ;

-- Create a stored procedure to delete a reservation
DELIMITER //
CREATE PROCEDURE `deleteReservation`(IN reservation_id INT)
BEGIN
    DELETE FROM `Reservations` WHERE reservationId = reservation_id;
END //
DELIMITER ;

-- Create a stored procedure to update dining preferences for a customer
DELIMITER //
CREATE PROCEDURE `updateDiningPreferences`(IN customer_id INT, IN favorite_table VARCHAR(45), IN dietary_restrictions VARCHAR(200))
BEGIN
    DECLARE preference_id INT;

    -- Check if preference exists
    SELECT preferenceId INTO preference_id 
    FROM `DiningPreferences`
    WHERE customerId = customer_id;

    -- If preference exists, update it
    IF preference_id IS NOT NULL THEN
        UPDATE `DiningPreferences`
        SET favoriteTable = favorite_table,
            dietaryRestrictions = dietary_restrictions
        WHERE customerId = customer_id;
    ELSE
        -- Add new preference if it does not exist
        INSERT INTO `DiningPreferences` (customerId, favoriteTable, dietaryRestrictions)
        VALUES (customer_id, favorite_table, dietary_restrictions);
    END IF;
END //
DELIMITER ;