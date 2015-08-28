from sqlalchemy import update
from sqlalchemy.orm import sessionmaker
import models


class DBSession(object):

    def __init__(self, engine):
        self.session = sessionmaker(bind=engine)()

    def get(self, model, filters):
        result = []
        model = getattr(models, model)
        for row in self.session.query(model).filter_by(**filters):
            result.append(row)
        if len(result):
            return result[0]
        else:
            return None

    def getMulti(self, model, filters):
        result = []
        model = getattr(models, model)
        for row in self.session.query(model).filter_by(**filters):
            result.append(row)
        return result

    def create_or_update(self, model, fields):
        target_model = getattr(models, model)
        record_id = fields.get('id', None)
        if record_id is not None:
            record = self.get(model, {'id':record_id})
            if record:
                self.session.query(target_model).filter(target_model.id == record_id).update(fields)
#                 self.session.execute(update(model, fields))
        else:
            self.session.add(target_model(**fields))
    
    def rollback(self):
        self.session.rollback()

    def save(self):
        self.session.commit()
