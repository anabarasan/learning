from sqlalchemy.orm import sessionmaker
import models


class DBSession(object):
    def __init__(self, engine):
        self.session = sessionmaker(bind=engine)()

    def get(self, model, Id):
        result = []
        model = getattr(models, model)
        for row in self.session.query(model).filter(model.id == Id):
            result.append(row)
        return result

    def getMulti(self, model):
        result = []
        model = getattr(models, model)
        for row in self.session.query(model):
            result.append(row)
        return result

    def save(self):
        self.session.commit()
