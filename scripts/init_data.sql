-- Données de test initiales

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
