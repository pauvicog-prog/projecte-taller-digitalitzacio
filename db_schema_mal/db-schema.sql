CREATE DATABASE IF NOT EXISTS taller CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE taller;

DROP TABLE IF EXISTS cites;
DROP TABLE IF EXISTS vehicles;
DROP TABLE IF EXISTS clients;

CREATE TABLE clients (
    idClient INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    telefon VARCHAR(20) NOT NULL,
    correu VARCHAR(100) NOT NULL
);

CREATE TABLE vehicles (
    idVehicle INT AUTO_INCREMENT PRIMARY KEY,
    matricula VARCHAR(20) NOT NULL,
    model VARCHAR(100) NOT NULL,
    any_vehicle INT NOT NULL,
    idClient INT NOT NULL,
    FOREIGN KEY (idClient) REFERENCES clients(idClient)
);

CREATE TABLE cites (
    idCita INT AUTO_INCREMENT PRIMARY KEY,
    data_cita DATE NOT NULL,
    servei VARCHAR(150) NOT NULL,
    estat VARCHAR(50) DEFAULT 'pendent',
    idClient INT NOT NULL,
    idVehicle INT NOT NULL,
    FOREIGN KEY (idClient) REFERENCES clients(idClient),
    FOREIGN KEY (idVehicle) REFERENCES vehicles(idVehicle)
);

INSERT INTO clients (nom, telefon, correu) VALUES
('Marc Garcia', '612345678', 'marc@gmail.com'),
('Laura Perez', '623456789', 'laura@gmail.com');

INSERT INTO vehicles (matricula, model, any_vehicle, idClient) VALUES
('1234ABC', 'Seat Ibiza', 2018, 1),
('5678DEF', 'Volkswagen Golf', 2020, 2);

INSERT INTO cites (data_cita, servei, estat, idClient, idVehicle) VALUES
('2026-05-20', 'Canvi doli', 'pendent', 1, 1),
('2026-05-22', 'Revisio general', 'pendent', 2, 2);