#replace localhost with ip address if using a cloud database, likewise replace 3306 with port number if mysql is on another port
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:password@localhost:3306/db_name'

SQLALCHEMY_POOL_RECYCLE = 3600
