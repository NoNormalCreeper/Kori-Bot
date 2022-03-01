-- 此文件仅用于参考

CREATE TABLE status (message_type TEXT, session_id INT PRIMARY KEY, command_active INT)
CREATE TABLE commands (session_id INT PRIMARY KEY, commands TEXT)

INSERT INTO status (message_type, session_id, command_active) VALUES ('tset', 177777, 1)



SELECT * FROM status WHERE session_id=177777


