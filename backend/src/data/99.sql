-- === Insertion des utilisateurs ===
INSERT INTO
    users (id, email, password, username, bio)
VALUES
    (
        1,
        'alban@mail.com',
        '$argon2id$v=19$m=65536,t=3,p=4$d9xEDNiyH/cdO+6fn9k7iw$Eiwz24u4dtvRa1OMH6MPL620vG4uv2XcqQjpiPx1H/w',
        'Alban',
        'Le Créateur'
    ),
    (
        2,
        'lyria@mail.com',
        '$argon2id$v=19$m=65536,t=3,p=4$d9xEDNiyH/cdO+6fn9k7iw$Eiwz24u4dtvRa1OMH6MPL620vG4uv2XcqQjpiPx1H/w',
        'Lyria',
        'Érudite et gardienne des secrets anciens'
    ),
    (
        3,
        'jerome@mail.com',
        '$argon2id$v=19$m=65536,t=3,p=4$d9xEDNiyH/cdO+6fn9k7iw$Eiwz24u4dtvRa1OMH6MPL620vG4uv2XcqQjpiPx1H/w',
        'Jérome',
        'Forgeron'
    ),
    (
        4,
        'annouck@mail.com',
        '$argon2id$v=19$m=65536,t=3,p=4$d9xEDNiyH/cdO+6fn9k7iw$Eiwz24u4dtvRa1OMH6MPL620vG4uv2XcqQjpiPx1H/w',
        'Annouck',
        'Scribe'
    );

-- === Insertion de l'univers "Boréalis" ===
INSERT INTO
    universe (id, creator_id, name, description, version)
VALUES
    (
        1,
        1,
        'Royaume de Boréalis',
        'Un royaume médiéval fantastique où magie, chevaliers et créatures mythiques coexistent. Protégé par la Garde Royale et dirigé par le Roi Aldric le Sage.',
        '1.0'
    );

-- === Insertion des entités (personnages, lieux, objets) ===
-- Entité parent : Le Royaume de Boréalis
INSERT INTO
    entities (id, name, universe_id, creator_id)
VALUES
    (1, 'Royaume de Boréalis', 1, 1);

-- Sous-entités : Lieux emblématiques
INSERT INTO
    entities (id, name, parent, universe_id, creator_id)
VALUES
    (2, 'Forteresse de Glace', 1, 1, 1),
    (3, 'Guilde des Mages', 1, 1, 2),
    (4, 'Forêt d''Ébène', 1, 1, 1),
    (5, 'Ville de Valoria', 1, 1, 3);

-- Sous-entités : Personnages importants
INSERT INTO
    entities (id, name, parent, universe_id, creator_id)
VALUES
    (6, 'Roi Aldric', 1, 1, 1),
    (7, 'Garde Royale', 1, 1, 1),
    (8, 'Archimage Eldrin', 3, 1, 2),
    (9, 'Chevalier Thalric', 7, 1, 3);

-- Sous-entités : Objets légendaires
INSERT INTO
    entities (id, name, parent, universe_id, creator_id)
VALUES
    (10, 'Épée de Lumière', 7, 1, 1),
    (11, 'Grimoire des Ombres', 3, 1, 2),
    (12, 'Pierre de l''Aube', 5, 1, 3);

-- === Insertion des text_blocks ===
-- Text_blocks pour le Royaume de Boréalis
INSERT INTO
    text_blocks (title, content, position, creator_id, entity_id)
VALUES
    (
        'Histoire',
        'Boréalis est un royaume millénaire, connu pour sa magie puissante et ses chevaliers intrépides. Il fut fondé par le Roi Aldric le Sage après la chute de l''Empire des Ténèbres.',
        1,
        1,
        1
    ),
    (
        'Géographie',
        'Le royaume est divisé en plusieurs régions : la Forteresse de Glace au nord, la Forêt d''Ébène à l''est, et la ville de Valoria au sud.',
        2,
        1,
        1
    );

-- Text_blocks pour la Forteresse de Glace
INSERT INTO
    text_blocks (title, content, position, creator_id, entity_id)
VALUES
    (
        'Description',
        'Une forteresse légendaire sculptée dans la glace, siège du pouvoir royal et symbole de la résistance contre les forces obscures.',
        1,
        1,
        2
    ),
    (
        'Gardiens',
        'La forteresse est protégée par la Garde Royale, dont les membres sont équipés d''armes enchantées.',
        2,
        1,
        2
    );

-- Text_blocks pour la Guilde des Mages
INSERT INTO
    text_blocks (title, content, position, creator_id, entity_id)
VALUES
    (
        'Rôle',
        'La guilde est chargée de préserver la magie ancienne et de former les mages du royaume.',
        1,
        2,
        3
    ),
    (
        'Archimage Eldrin',
        'Un mage légendaire, connu pour avoir scellé le démon Malagar il y a 20 ans.',
        2,
        2,
        3
    );

-- Text_blocks pour la Forêt d'Ébène
INSERT INTO
    text_blocks (title, content, position, creator_id, entity_id)
VALUES
    (
        'Faune et flore',
        'La forêt est peuplée de créatures mystiques : dryades, licornes et dragons mineurs.',
        1,
        1,
        4
    ),
    (
        'Danger',
        'Attention aux ombres mouvantes qui rôdent entre les arbres...',
        2,
        1,
        4
    );

-- Text_blocks pour la Ville de Valoria
INSERT INTO
    text_blocks (title, content, position, creator_id, entity_id)
VALUES
    (
        'Marché',
        'Le marché de Valoria est réputé pour ses épices, ses tissus magiques et ses artefacts anciens.',
        1,
        3,
        5
    ),
    (
        'Taverne',
        'La Taverne du Dragon Volant est le lieu de rassemblement des aventuriers.',
        2,
        3,
        5
    );

-- Text_blocks pour le Roi Aldric
INSERT INTO
    text_blocks (title, content, position, creator_id, entity_id)
VALUES
    (
        'Biographie',
        'Âgé de 65 ans, le Roi Aldric est un dirigeant sage et juste, connu pour son amour des arts et de la magie.',
        1,
        1,
        6
    ),
    (
        'Règne',
        'Il règne depuis 30 ans et a restauré la paix après la Grande Guerre des Ombres.',
        2,
        1,
        6
    );

-- Text_blocks pour le Chevalier Thalric
INSERT INTO
    text_blocks (title, content, position, creator_id, entity_id)
VALUES
    (
        'Profil',
        'Chevalier de la Garde Royale, Thalric est un guerrier redoutable doté d''une épée enchantée.',
        1,
        3,
        9
    ),
    (
        'Quête',
        'Il est en mission pour retrouver l''Épée de Lumière, volée par des brigands.',
        2,
        3,
        9
    );

-- === Insertion des invites ===
-- Invitation de Lyria (id=2) à rejoindre l'univers en tant qu'éditrice
INSERT INTO
    invitations (sender_id, receiver_id, universe_id, status)
VALUES
    (1, 2, 1, 'accepted'),
    -- Invitation de Garrick (id=3) à rejoindre l'univers en tant qu'administrateur
    (1, 3, 1, 'accepted'),
    -- Invitation de Thalric (id=4) à rejoindre l'univers en tant que membre
    (1, 4, 1, 'accepted');

-- === Insertion des rôles utilisateurs dans l'univers ===
INSERT INTO
    user_universe (user_id, universe_id, admin_role)
VALUES
    (1, 1, 'creator'),
    (2, 1, NULL),
    (3, 1, 'super administrator'),
    (4, 1, NULL);

-- === Insertion des rôles utilisateurs pour les entités ===
-- Elnar (id=1) est administrateur de toutes les entités
INSERT INTO
    user_entity (user_id, entity_id, role)
VALUES
    (1, 1, 'entity administrator'),
    (1, 2, 'entity administrator'),
    (1, 3, 'entity administrator'),
    (1, 4, 'entity administrator'),
    (1, 5, 'entity administrator'),
    (1, 6, 'entity administrator'),
    (1, 7, 'entity administrator'),
    (1, 8, 'entity administrator'),
    (1, 9, 'entity administrator'),
    (1, 10, 'entity administrator'),
    (1, 11, 'entity administrator'),
    (1, 12, 'entity administrator'),
    -- Lyria (id=2) est éditrice de la Guilde des Mages et de l'Archimage Eldrin
    (2, 3, 'editor'),
    (2, 8, 'editor'),
    -- Garrick (id=3) est éditeur de la Forteresse de Glace et de l'Épée de Lumière
    (3, 2, 'editor'),
    (3, 10, 'editor'),
    -- Thalric (id=4) est lecteur de la Ville de Valoria
    (4, 5, NULL);

-- === Insertion des commentaires ===
-- Commentaire sur le Royaume de Boréalis
INSERT INTO
    comments (content, creator_id, entity_id)
VALUES
    (
        'Boréalis me fait penser à Lordran de Dark Souls !',
        2,
        1
    ),
    (
        'J''adorerais visiter la Forteresse de Glace !',
        4,
        1
    );

-- Commentaire sur un text_block de la Forteresse de Glace
INSERT INTO
    comments (content, creator_id, entity_id, text_block_id)
VALUES
    (
        'Cette forteresse ressemble étrangement à la Citadelle de Zin dans Elden Ring.',
        2,
        2,
        2
    );

-- === Insertion des commits ===
-- Commit de Lyria pour ajouter des détails sur la Guilde des Mages
INSERT INTO
    commits (message, creator_id, content, status)
VALUES
    (
        'Ajout de détails sur la Guilde des Mages',
        2,
        '{"added": [{"name": "Bibliothèque interdite", "description": "Contient des grimoires maudits"}]}',
        'accepted'
    );

-- Commit de Garrick pour améliorer la description de la Forteresse de Glace
INSERT INTO
    commits (message, creator_id, content, status)
VALUES
    (
        'Mise à jour de la description de la Forteresse',
        3,
        '{"updated": [{"name": "Forteresse de Glace", "description": "Une forteresse sculptée dans un glacier magique, siège du pouvoir royal."}]}',
        'pending'
    );

-- Réinitialise la séquence pour l'ID de la table users
SELECT
    setval(
        pg_get_serial_sequence('users', 'id'),
        COALESCE(MAX(id) + 1, 1),
        false
    )
FROM
    users;

-- Réinitialise la séquence pour l'ID de la table universe
SELECT
    setval(
        pg_get_serial_sequence('universe', 'id'),
        COALESCE(MAX(id) + 1, 1),
        false
    )
FROM
    universe;

-- Réinitialise la séquence pour l'ID de la table entities
SELECT
    setval(
        pg_get_serial_sequence('entities', 'id'),
        COALESCE(MAX(id) + 1, 1),
        false
    )
FROM
    entities;

-- Réinitialise la séquence pour l'ID de la table text_blocks
SELECT
    setval(
        pg_get_serial_sequence('text_blocks', 'id'),
        COALESCE(MAX(id) + 1, 1),
        false
    )
FROM
    text_blocks;

-- Réinitialise la séquence pour l'ID de la table invitations
SELECT
    setval(
        pg_get_serial_sequence('invitations', 'id'),
        COALESCE(MAX(id) + 1, 1),
        false
    )
FROM
    invitations;

-- Réinitialise la séquence pour l'ID de la table comments
SELECT
    setval(
        pg_get_serial_sequence('comments', 'id'),
        COALESCE(MAX(id) + 1, 1),
        false
    )
FROM
    comments;

-- Réinitialise la séquence pour l'ID de la table commits
SELECT
    setval(
        pg_get_serial_sequence('commits', 'id'),
        COALESCE(MAX(id) + 1, 1),
        false
    )
FROM
    commits;