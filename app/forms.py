from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField,\
    SelectField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class LoginForm(FlaskForm):
    """Login Form"""
    username = StringField('Username', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


# Using form inheritance

class User(FlaskForm):
    """General User Data"""
    username = StringField('Username', validators=[DataRequired(), Length(1, 64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('password')])

class VendorRegistrationForm(User):
    """Vendor Registration Form"""
    shop_name = StringField('Shop Name', validators=[DataRequired(), Length(1, 64)])
    submit = SubmitField('Register')

class CustomerRegistrationForm(User):
    """Customer Registration Form"""
    residence = StringField('Residence', validators=[DataRequired(), Length(1, 64)])
    submit = SubmitField('Register')


class AdminRegistrationForm(User):
    """Admin Registration Form"""
    department = SelectField(
        'Department',
        choices=[
            ('Support', 'Support'),
            ('Finance', 'Finance'),
            ('HR', 'HR')
        ])
    submit = SubmitField('Register')


class AddToCart(FlaskForm):
    """Add items to the cart"""
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    add = SubmitField('Add To Cart')
