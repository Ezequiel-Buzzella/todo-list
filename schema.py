instructions = [
    'SET FOREIGN_KEY_CHECKS=0',
    'DROP TABLE IF EXISTS todo',
    'DROP TABLE IF EXISTS usuarios',
    'SET FOREIGN_KEY_CHECKS=1',
    
    """
    CREATE TABLE usuarios (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(100) NOT NULL,
        password VARCHAR(255) NOT NULL,  # Necesitas un campo de contraseña
        email VARCHAR(100)  NOT NULL DEFAULT ''
    )
    """,
    
    """
    CREATE TABLE todo (
        id INT AUTO_INCREMENT PRIMARY KEY,
        created_by INT NOT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        description TEXT NOT NULL,
        completed BOOLEAN NOT NULL DEFAULT FALSE,
        FOREIGN KEY (created_by) REFERENCES usuarios(id)
    )
    """
]
