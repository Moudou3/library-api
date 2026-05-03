-- Données de test initiales Base de donnée de Test de l'API
CREATE TABLE IF NOT EXISTS authors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    biography TEXT
);

CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    isbn VARCHAR(13) UNIQUE NOT NULL,
    title VARCHAR(300) NOT NULL,
    publication_year INT,
    quantity INT DEFAULT 1,
    author_id INT NOT NULL,
    FOREIGN KEY (author_id) REFERENCES authors(id)
);

CREATE TABLE IF NOT EXISTS book_category (
    book_id INT,
    category_id INT,
    PRIMARY KEY (book_id, category_id),
    FOREIGN KEY (book_id) REFERENCES books(id),
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS library_cards (
    id INT AUTO_INCREMENT PRIMARY KEY,
    card_number VARCHAR(50) UNIQUE NOT NULL,
    issue_date DATE NOT NULL,
    expiry_date DATE NOT NULL,
    user_id INT UNIQUE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
-- Auteurs
INSERT INTO authors (id, name, biography) VALUES
(1, 'Victor Hugo', 'Écrivain français du XIXe siècle, auteur des Misérables.'),
(2, 'Albert Camus', 'Écrivain et philosophe français, prix Nobel de littérature 1957.'),
(3, 'Simone de Beauvoir', 'Philosophe et romancière française, figure du féminisme.');

-- Catégories
INSERT INTO categories (id, name, description) VALUES
(1, 'Roman', 'Œuvres de fiction narratives'),
(2, 'Philosophie', 'Ouvrages philosophiques'),
(3, 'Classique', 'Grands classiques de la littérature'),
(4, 'Essai', 'Essais et réflexions');

-- Livres
INSERT INTO books (id, isbn, title, publication_year, quantity, author_id) VALUES
(1, '9782070409228', 'Les Misérables', 1862, 3, 1),
(2, '9782070360024', 'L''Étranger', 1942, 2, 2),
(3, '9782070368792', 'Le Deuxième Sexe', 1949, 2, 3),
(4, '9782070411580', 'Notre-Dame de Paris', 1831, 1, 1),
(5, '9782070360192', 'La Peste', 1947, 2, 2);

-- Associations livre-catégorie
INSERT INTO book_category (book_id, category_id) VALUES
(1, 1), (1, 3),
(2, 1), (2, 3),
(3, 2), (3, 4),
(4, 1), (4, 3),
(5, 1), (5, 3);

-- Utilisateurs
INSERT INTO users (id, email, password_hash, first_name, last_name) VALUES
(1, 'jean.dupont@email.com', 'hashed_password_1', 'Jean', 'Dupont'),
(2, 'marie.martin@email.com', 'hashed_password_2', 'Marie', 'Martin');

-- Cartes de bibliothèque
INSERT INTO library_cards (id, card_number, issue_date, expiry_date, user_id) VALUES
(1, 'LIB-ABC12345', '2024-01-15', '2025-01-15', 1),
(2, 'LIB-DEF67890', '2024-03-20', '2025-03-20', 2);
