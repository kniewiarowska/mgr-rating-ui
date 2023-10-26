
class Config():
    # Set up the App SECRET_KEY
    PASSWORD = 'ElkaInz2022'
    USERNAME = 'kniewiarowska'
    # This will create a file in <app> FOLDER
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://' + USERNAME + ':' + PASSWORD + '@localhost:3306/db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False