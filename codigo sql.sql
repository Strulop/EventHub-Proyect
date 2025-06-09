DROP TABLE ubicacion;
DROP TABLE categoria;
DROP TABLE tickets;
DROP TABLE eventos;
DROP TABLE usuarios;



-- Tabla de Usuarios
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    contra VARCHAR(500) NOT NULL,
    rol ENUM('organizador', 'asistente') NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE categoria (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL
);

CREATE TABLE ubicacion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL
);

-- Tabla de Eventos
CREATE TABLE eventos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    duracion INT NOT NULL CHECK (duracion>0), -- minutos
    hora_inicio TIME NOT NULL,
    precio INT NOT NULL CHECK (precio>0),
    fecha DATE NOT NULL,
    capacidad INT NOT NULL CHECK (capacidad>0),
    tickets_disponibles INT NOT NULL CHECK (tickets_disponibles>0),
    url_imagen VARCHAR(255) NOT NULL,
    id_organizador INT NOT NULL,
    id_categoria INT NOT NULL,
    id_ubicacion INT NOT NULL,
	FOREIGN KEY (id_organizador) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (id_categoria) REFERENCES categoria(id) ON DELETE CASCADE,
    FOREIGN KEY (id_ubicacion) REFERENCES ubicacion(id) ON DELETE CASCADE
    
);

-- Tabla de Tickets
CREATE TABLE tickets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    evento_id INT NOT NULL,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    fecha_compra TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (evento_id) REFERENCES eventos(id) ON DELETE CASCADE
);


INSERT INTO usuarios (nombre, email, contra, rol, fecha_registro) VALUES
('Tomas', 'tomas@gmail.com', 'scrypt:32768:8:1$cV7Ufg79QIuRabcc$d8e4699f0f23f98f01d3e632161032af73471628d3af935a5c261f449547642adbdde7c31b6c73e7ee2be94a306a80a1f0926498786de53ba134949767546c5a', 'asistente', '2025-02-27 00:00:00'),
('Manuel', 'manuel@gmail.com', 'scrypt:32768:8:1$DQFwEvyvPcxHfuq0$ea529b94a6f8759ddceaea14ea4a808d18253789fb09fcadcb6d06b5c756d36a0d83561b61ef30009c8fd3f12bd3378e216d3e4dd77947c47e3863e78703ea4e', 'organizador', '2025-02-27 00:00:00');




INSERT INTO categoria (nombre) VALUES
('Conciertos'),
('Conferencias'),
('Deportes'),
('Teatro'),
('Gastronomía');

INSERT INTO ubicacion (nombre) VALUES
('Madrid'),
('Barcelona'),
('Valencia'),
('Sevilla'),
('Toledo'),
('Malaga'),
('Bilbao');

INSERT INTO eventos (nombre, descripcion, duracion, hora_inicio, precio, fecha, capacidad, tickets_disponibles, url_imagen, id_organizador, id_categoria, id_ubicacion)
VALUES
('Charla Tech 2030', 'Una charla sobre las tendencias tecnológicas del año 2030, inteligencia artificial, IoT y más.', 120, '18:00:00', 20, '2025-06-15', 200, 200, 'https://ik.imagekit.io/otcvghwe9/Imagenes_Eventos/evento_conferencia_1.png?updatedAt=1740678888383', 2, 2, 2),
('Concierto Nocturno de Estrellas', 'Un espectáculo musical con artistas emergentes bajo un cielo estrellado.', 180, '21:30:00', 50, '2025-07-10', 500, 500, 'https://ik.imagekit.io/otcvghwe9/Imagenes_Eventos/concierto.png?updatedAt=1740682617533', 2, 1, 3),
('Maratón 10Km', 'Carrera de 10 kilómetros.', 90, '08:00:00', 15, '2025-05-20',  1000, 1000, 'https://ik.imagekit.io/otcvghwe9/Imagenes_Eventos/maraton.png?updatedAt=1740682617299', 2, 3, 4),
('Obra de Teatro: Sombras del Pasado', 'Una obra de teatro que explora la memoria y los secretos ocultos de una familia.', 150, '20:00:00', 30, '2025-08-05', 300, 300, 'https://ik.imagekit.io/otcvghwe9/Imagenes_Eventos/obra%20teatro.png?updatedAt=1740682617303', 2, 4, 5),
('Feria del Sabor', 'Un evento gastronómico con degustaciones de comida internacional y chefs invitados.', 240, '12:00:00', 25, '2025-09-12', 600, 600, 'https://ik.imagekit.io/otcvghwe9/Imagenes_Eventos/gastro.png?updatedAt=1740682617439', 2, 5, 4),
('Cumbre de Innovación Empresarial', 'Líderes de la industria se reúnen para discutir el futuro de los negocios.', 180, '09:00:00', 100, '2025-10-20', 150, 150, 'https://ik.imagekit.io/otcvghwe9/Imagenes_Eventos/cumbre.png?updatedAt=1740682617499', 2, 2, 2),
('Conferencia sobre situación aranceles', 'Se expondra las posibles consecuencias y soluciones para la actual crisis y malestar, frente a la problematica de los aranceles.', 180, '10:50:00', 100, '2025-09-20', 150, 150, 'https://ik.imagekit.io/otcvghwe9/Imagenes_Eventos/aranceles.png?updatedAt=1740684406926', 2, 1, 2);

