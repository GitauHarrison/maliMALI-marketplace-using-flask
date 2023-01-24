from app import db, login, app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import jwt
from time import time
from hashlib import md5


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


# =================
# Application Users
# =================


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(128), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    phone = db.Column(db.String(20), default='+254700111222')
    verification_phone = db.Column(db.String(20))
    registered_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


    type = db.Column(db.String(64))

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': 'type'
    }

    def __repr__(self):
        return f'User: {self.username} {self.verification_phone}'

    def two_factor_enabled(self):
        return self.verification_phone is not None

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # @property
    # def is_active(self):
    #     # override UserMixin property which always returns true
    #     # return the value of the active column instead
    #     return self.active

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(
                token,
                app.config['SECRET_KEY'],
                algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'


class Vendor(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)
    shop_name = db.Column(db.String(64), default='Sample eCommerce Shop')
    products_for_sale = db.relationship(
        'ProductsForSale', backref='vendor', lazy='dynamic', passive_deletes=True)

    __mapper_args__ = {
        'polymorphic_identity': 'vendor',
        'polymorphic_load': 'inline'
    }

    def __repr__(self):
        return f'Teacher: {self.first_name} | {self.course}'


class Customer(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)
    residence = db.Column(db.String(64), default='Roselyn, Nairobi')
    purchased_products = db.relationship(
        'PurchasedProducts', backref='customer', lazy='dynamic', passive_deletes=True)

    __mapper_args__ = {
        'polymorphic_identity': 'customer',
        'polymorphic_load': 'inline'
    }

    def __repr__(self):
        return f'Parent: {self.first_name} | {self.residence}'


class Admin(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)
    department = db.Column(db.String(64), default='HR')

    __mapper_args__ = {
        'polymorphic_identity': 'admin',
        'polymorphic_load': 'inline'
    }

    def __repr__(self):
        return f'Admin: {self.username} | {self.department}'

# =================
# End of Application Users
# =================


class ProductsForSale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), default='iPhone 13', nullable=False)
    price = db.Column(db.Integer, default=0, nullable=False)
    currency = db.Column(db.String(20), default='KES', nullable=False)    
    description = db.Column(db.String(64), default='iPhone 13', nullable=False)
    quantity = db.Column(db.Integer, default=0, nullable=False)
    image = db.Column(db.String(64), default='static/images/vendor/uploads', nullable=False)
    allow_status = db.Column(db.Boolean, default=False)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id', ondelete='CASCADE'))


class PurchasedProducts(db.Model): # should be PurchasedProduct()
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), default='iPhone 13', nullable=False)
    cost = db.Column(db.Integer, default=0, nullable=False)
    quantity = db.Column(db.Integer, default=1, nullable=False)
    currency = db.Column(db.String(20), default='KES', nullable=False)
    description = db.Column(db.String(64), default='iPhone 13', nullable=False)
    image = db.Column(db.String(64), default='static/images/vendor/uploads', nullable=False)
    payment_status = db.Column(db.Boolean, default=False)
    vendor_id = db.Column(db.Integer, default=1, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id', ondelete='CASCADE'))
