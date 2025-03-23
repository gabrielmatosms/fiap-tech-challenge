-- Insert admin user
INSERT INTO users (name, email, cpf, role)
VALUES ('Admin User', 'admin@fiap.com', '12345678900', 'ADMIN');

-- Insert categories
INSERT INTO categories (name, description)
VALUES 
    ('Lanches', 'Hambúrgueres e sanduíches'),
    ('Acompanhamentos', 'Batatas fritas, onion rings e outros acompanhamentos'),
    ('Bebidas', 'Refrigerantes, sucos e outras bebidas'),
    ('Sobremesas', 'Sorvetes, milk-shakes e outras sobremesas');

-- Insert products
INSERT INTO products (name, description, price, category_id, image_url)
VALUES 
    -- Lanches
    ('Classic Burger', 'Hambúrguer clássico com queijo, alface, tomate e molho especial', 25.90, 
        (SELECT id FROM categories WHERE name = 'Lanches'),
        'https://images.unsplash.com/photo-1568901346375-23c9450c58cd'),
    ('Double Cheese', 'Hambúrguer duplo com queijo cheddar, bacon e molho barbecue', 32.90, 
        (SELECT id FROM categories WHERE name = 'Lanches'),
        'https://images.unsplash.com/photo-1553979459-d2229ba7433b'),
    ('Chicken Burger', 'Hambúrguer de frango com queijo, alface e maionese especial', 28.90, 
        (SELECT id FROM categories WHERE name = 'Lanches'),
        'https://images.unsplash.com/photo-1595297658326-389599c389de'),
    ('Veggie Burger', 'Hambúrguer vegetariano com queijo, alface, tomate e cebola caramelizada', 27.90, 
        (SELECT id FROM categories WHERE name = 'Lanches'),
        'https://images.unsplash.com/photo-1585730315658-a2e91acbcfa1'),
    
    -- Acompanhamentos
    ('Batata Frita', 'Porção de batatas fritas crocantes', 12.90, 
        (SELECT id FROM categories WHERE name = 'Acompanhamentos'),
        'https://images.unsplash.com/photo-1573080496219-bb080dd4f877'),
    ('Onion Rings', 'Anéis de cebola empanados e fritos', 14.90, 
        (SELECT id FROM categories WHERE name = 'Acompanhamentos'),
        'https://images.unsplash.com/photo-1639024471283-03518883522b'),
    ('Nuggets', 'Porção de nuggets de frango', 15.90, 
        (SELECT id FROM categories WHERE name = 'Acompanhamentos'),
        'https://images.unsplash.com/photo-1586190848861-99aa4a171e90'),
    
    -- Bebidas
    ('Refrigerante', 'Lata de refrigerante 350ml', 6.90, 
        (SELECT id FROM categories WHERE name = 'Bebidas'),
        'https://images.unsplash.com/photo-1622483767028-3f66f32aef97'),
    ('Suco Natural', 'Copo de suco natural 300ml', 9.90, 
        (SELECT id FROM categories WHERE name = 'Bebidas'),
        'https://images.unsplash.com/photo-1613478223719-2ab802602423'),
    ('Água Mineral', 'Garrafa de água mineral 500ml', 4.90, 
        (SELECT id FROM categories WHERE name = 'Bebidas'),
        'https://images.unsplash.com/photo-1560707854-8abc7c8d3f9d'),
    
    -- Sobremesas
    ('Milk-Shake', 'Milk-shake de chocolate, morango ou baunilha', 16.90, 
        (SELECT id FROM categories WHERE name = 'Sobremesas'),
        'https://images.unsplash.com/photo-1579954115545-a95591f28bfc'),
    ('Sundae', 'Sundae de chocolate com calda quente e castanhas', 14.90, 
        (SELECT id FROM categories WHERE name = 'Sobremesas'),
        'https://images.unsplash.com/photo-1551893665-f843f600794e'),
    ('Sorvete', 'Bola de sorvete de diversos sabores', 8.90, 
        (SELECT id FROM categories WHERE name = 'Sobremesas'),
        'https://images.unsplash.com/photo-1580915411954-282cb1b0d780'); 