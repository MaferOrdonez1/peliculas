CREATE DATABASE SistemasExpertosDB;

USE SistemasExpertosDB;

CREATE TABLE Reglas (
    id INT IDENTITY(1,1) PRIMARY KEY,
	genero NVARCHAR(255),
    condiciones NVARCHAR(255),
    conclusion NVARCHAR(255)
);

DELETE FROM Reglas
DROP TABLE [dbo].[Reglas]
-- Insertar reglas en la tabla
INSERT INTO Reglas (genero, condiciones, conclusion) VALUES 
('accion', 'larga', 'Mad Max: Fury Road'),
('accion', 'corta', 'John Wick'),
('drama', 'larga', 'The Shawshank Redemption'),
('drama', 'corta', 'Forrest Gump'),
('comedia', 'corta', 'The Big Sick'),
('comedia', 'larga', 'The Wolf of Wall Street');
