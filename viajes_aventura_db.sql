-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 25-11-2025 a las 19:27:18
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `viajes_aventura_db`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `destinos`
--

CREATE TABLE `destinos` (
  `id` int(10) NOT NULL,
  `nombre` varchar(250) NOT NULL,
  `descripcion` varchar(250) NOT NULL,
  `actividades` varchar(250) NOT NULL,
  `costo` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `destinos`
--

INSERT INTO `destinos` (`id`, `nombre`, `descripcion`, `actividades`, `costo`) VALUES
(1, 'San Pedro de Atacama', 'Un pueblo en medio del desierto más árido del mundo. Es famoso por sus paisajes lunares, salares y por tener uno de los cielos más limpios del planeta para la astronomía.', 'Visita al Valle de la Luna y Valle de la Muerte. Madrugar para ver los Geysers del Tatio. Tour astronómico nocturno. Flotar en la Laguna Cejar.', 350000),
(2, 'Pucón y Zona Lacustre', 'El centro del turismo aventura en el sur de Chile. Rodeado de lagos, bosques y dominado por el imponente Volcán Villarrica. Ideal para ir en verano o invierno.', 'Ascenso al cráter del Volcán Villarrica. Rafting en el río Trancura. Visita a los Ojos del Caburgua.', 250000),
(3, 'Torres del Paine', 'Considerada la octava maravilla del mundo. Un paraíso para el trekking con montañas de granito, glaciares y lagos turquesa. Estando tú en Punta Arenas, esto te queda mucho más cerca.', 'Trekking a Base Torres (full day). Circuito W (4-5 días). Navegación al Glaciar Grey. Avistamiento de pumas y guanacos.', 400000),
(4, 'Valparaíso', 'Ciudad puerto bohemia, Patrimonio de la Humanidad. Famosa por sus cerros llenos de casas coloridas, arte callejero, ascensores antiguos y vida nocturna.', 'Caminar por Cerro Alegre y Concepción. Visitar \"La Sebastiana\" (Casa de Pablo Neruda). Paseo en lancha por el puerto. Comer mariscos en el mercado.', 150000),
(5, 'Archipiélago de Chiloé', 'Una isla mágica llena de mitología, iglesias de madera (Patrimonio de la Humanidad) y una gastronomía única.', 'Ver los Palafitos en Castro. Trekking en el Muelle de las Almas o Parque Tantauco. Comer un Curanto al hoyo. Ruta de las Iglesias.', 200000);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `paquetes`
--

CREATE TABLE `paquetes` (
  `id` int(10) NOT NULL,
  `nombre` varchar(250) NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_fin` date NOT NULL,
  `precio` float NOT NULL,
  `cupos_disponibles` smallint(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `paquetes`
--

INSERT INTO `paquetes` (`id`, `nombre`, `fecha_inicio`, `fecha_fin`, `precio`, `cupos_disponibles`) VALUES
(1, 'Sur y Norte de Chile', '2025-11-24', '2025-11-28', 800000, 10),
(2, 'Norte con Aventuras', '2025-11-27', '2025-12-01', 400000, 20);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `paquete_destinos`
--

CREATE TABLE `paquete_destinos` (
  `id` int(11) NOT NULL,
  `id_paquete` int(11) DEFAULT NULL,
  `id_destino` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `paquete_destinos`
--

INSERT INTO `paquete_destinos` (`id`, `id_paquete`, `id_destino`) VALUES
(3, 2, 1),
(4, 2, 4),
(5, 1, 5),
(6, 1, 3),
(7, 1, 4);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reservas`
--

CREATE TABLE `reservas` (
  `id` int(11) NOT NULL,
  `fecha` date NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `id_paquete` int(11) NOT NULL,
  `estado` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `apellido` varchar(50) NOT NULL,
  `direccion` varchar(250) NOT NULL,
  `telefono` varchar(50) NOT NULL,
  `correo` varchar(50) NOT NULL,
  `password` varchar(250) NOT NULL,
  `rut` varchar(12) NOT NULL,
  `rol` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `nombre`, `apellido`, `direccion`, `telefono`, `correo`, `password`, `rut`, `rol`) VALUES
(12, 'Diomedes', 'Trinidad', 'Lautaro Navarro 0362', '8095992210', 'diomedesinf39@hotmail.com', '$2b$12$kmJ2w..lZbuDdNbIj3U92e2o8QMDNE8VWSBa0f.Qi/MGhfEABlIGK', '27840245-2', 'usuario'),
(13, 'Administrador', '', '', '8095992210', 'admin', 'admin123', '', 'admin'),
(14, 'Administrador', '', '', '', 'admin01@viajesaventura.cl', '$2b$12$iOOJy5Ds.wwvQsky4025LeZCruxHWleI2Cp.Q4VodrCxH3c/wIj7i', '18903077-0', 'admin');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `destinos`
--
ALTER TABLE `destinos`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `paquetes`
--
ALTER TABLE `paquetes`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `paquete_destinos`
--
ALTER TABLE `paquete_destinos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_paquete` (`id_paquete`),
  ADD KEY `id_destino` (`id_destino`);

--
-- Indices de la tabla `reservas`
--
ALTER TABLE `reservas`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_correo` (`correo`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `destinos`
--
ALTER TABLE `destinos`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `paquetes`
--
ALTER TABLE `paquetes`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `paquete_destinos`
--
ALTER TABLE `paquete_destinos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `reservas`
--
ALTER TABLE `reservas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `paquete_destinos`
--
ALTER TABLE `paquete_destinos`
  ADD CONSTRAINT `paquete_destinos_ibfk_1` FOREIGN KEY (`id_paquete`) REFERENCES `paquetes` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `paquete_destinos_ibfk_2` FOREIGN KEY (`id_destino`) REFERENCES `destinos` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
