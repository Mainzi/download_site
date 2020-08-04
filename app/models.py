from app import db
from datetime import datetime, timezone


class Task(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    url = db.Column(db.String, index=True)
    status = db.Column(db.String(64), index=True)
    start_time = db.Column(db.DateTime, index=True, default=datetime.now(timezone.utc))

    def __repr__(self):
        return '<Task {0}: {1}>'.format(self.id, self.status)

# >>> from app import db
# >>> db.create_all()
