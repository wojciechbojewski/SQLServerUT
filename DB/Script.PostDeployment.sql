/*
Post-Deployment Script Template							
--------------------------------------------------------------------------------------
 This file contains SQL statements that will be appended to the build script.		
 Use SQLCMD syntax to include a file in the post-deployment script.			
 Example:      :r .\myfile.sql								
 Use SQLCMD syntax to reference a variable in the post-deployment script.		
 Example:      :setvar TableName MyTable							
               SELECT * FROM [$(TableName)]					
--------------------------------------------------------------------------------------
*/

TRUNCATE TABLE Users
TRUNCATE TABLE Events
TRUNCATE TABLE Logs

INSERT INTO Users (name) VALUES ('TestUser1')
INSERT INTO Events (name, type) VALUES ('Login',1), ('Logout', 1)
INSERT INTO Logs (user_id, event_id) VALUES (1, 1), (1, 2)


