-- Scripts inserts default data after db schema init.
-- Usage for postgres:
-- psql -f app/domain/data.sql mydb
-- Usage for sqlite:
-- sqlite3 -init app/domain/data.sql mydb

INSERT INTO roles (id, name) VALUES
(1, 'Клиент'),
(2, 'Администратор'),
(3, 'Оператор');
SELECT setval('role_id_seq', 3);

INSERT INTO event_types (id, name) VALUES
(1, 'Логин'),
(2, 'Логаут'),
(3, 'Запрос лицензии'),
(4, 'Загрузка лицензии'),
(5, 'Удаление лицензии');
SELECT setval('event_type_id_seq', 5);

INSERT INTO components (id, name) VALUES
(1, 'sensor');
SELECT setval('component_id_seq', 1);

INSERT INTO license_types (id, name) VALUES
(1, 'demo'),
(2, 'not demo');
SELECT setval('license_type_id_seq', 2);

INSERT INTO users (id, login, status, role_id, client_id, full_name, email, phone_number, password_hash) VALUES
(1, 'root', true, 2, NULL, 'root', 'root', 'root', 'scrypt:32768:8:1$hEg68mRD6KFbQLAE$8684cf4cae984635459537837b3729f05d3dc6ad885ee1657e09c45bd47065e0fa9f80e18f03337c5406a620e10c681741aab4502865e2b8aa63a4ed776e49dd'),
(2, 'deleted_user', false, 1, NULL, 'deleted', 'deleted', 'deleted', '!');
SELECT setval('user_id_seq', 2);
