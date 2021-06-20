ADD_USER = 'INSERT INTO users (user_id) VALUES (%(id)s) ON CONFLICT DO NOTHING'

ADD_DISTRICT = 'INSERT INTO district (user_id,district_id) VALUES (%(user_id)s,%(district_id)s) ON CONFLICT DO NOTHING'
ADD_PINCODE = 'INSERT INTO pincode (user_id,pincode_num) VALUES (%(user_id)s,%(pincode)s) ON CONFLICT DO NOTHING'

GET_PREFERENCE = 'SELECT age,dose,vaccine,fee,update_interval FROM users WHERE user_id=%(id)s'
SET_PREFERENCE = 'UPDATE users SET age = %(age)s , dose = %(dose)s , vaccine = %(vaccine)s , fee = %(fee)s , update_interval = %(interval)s  WHERE user_id=%(id)s'

GET_DISTRICTS = 'SELECT DISTINCT district_id FROM district'
GET_PINCODES = 'SELECT DISTINCT pincode_num FROM pincode'

GET_USERS = 'SELECT * FROM users'

GET_DISTRICTS_FOR_USER = 'SELECT district_id FROM district WHERE user_id = %(id)s'
GET_PINCODES_FOR_USER = 'SELECT pincode_num FROM pincode WHERE user_id = %(id)s'

UPDATE_LAST_SENT = 'UPDATE users SET last_sent = %(time)s  WHERE user_id=%(id)s'

REMOVE_DISTRICT = 'DELETE FROM district WHERE user_id=%(id)s and district_id=%(district_id)s'
REMOVE_PINCODE = 'DELETE FROM pincode WHERE user_id=%(id)s and pincode_num=%(pincode)s'

GET_ENTRIES_COUNT = 'SELECT (SELECT COUNT(*) FROM district WHERE user_id=%(id)s) + (SELECT COUNT(*) FROM pincode WHERE user_id=%(id)s)'

DELETE_DETAILS = 'DELETE FROM district WHERE user_id=%(id)s;DELETE FROM pincode WHERE user_id=%(id)s;'