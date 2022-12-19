from app import db


class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    status = db.Column(
        db.String(255),
        nullable=False,
        default='Unnotified'  # Notified, Inactive (disabled acc)
    )
    notifs_received = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f"Customer { self.id } -- { self.name } -- { self.email }"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)


'''
CREATE TABLE customer(
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    status VARCHAR(255) NOT NULL DEFAULT 'Unnotified',
    notifs_received INT NOT NULL DEFAULT 0,
);
'''
