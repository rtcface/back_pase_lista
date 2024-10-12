CREATE TABLE tblUsers (
  nId SERIAL PRIMARY KEY,
  cNombre VARCHAR(255) NOT NULL,
  cApellidos VARCHAR(255) NOT NULL,
  cEmail VARCHAR(255) NOT NULL,
  cPassword VARCHAR(255) NOT NULL,
  bIsActive BOOLEAN DEFAULT TRUE
);

INSERT INTO tblUsers (cNombre, cApellidos, cEmail, cPassword, bIsActive) VALUES
('Juan', 'Perez', 'juan@gmail.com', '123456', TRUE),
('Pedro', 'Perez', 'pedro@gmail.com', '123456', TRUE),
('Carlos', 'Perez', 'carlos@gmail.com', '123456', FALSE),
('Luis', 'Perez', 'luis@gmail.com', '123456', TRUE),
('Maria', 'Perez', 'maria@gmail.com', '123456', TRUE);

