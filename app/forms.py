from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, \
    SelectField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, Email, \
    Regexp, ValidationError
from flask_wtf.file import FileField, FileAllowed, FileRequired
import phonenumbers
from app.models import User
from flask_pagedown.fields import PageDownField


class LoginForm(FlaskForm):
    """Login Form"""
    username = StringField('Username', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


# Using form inheritance

class UserForm(FlaskForm):
    """General User Data"""
    username = StringField(
        'Username',
        validators=[DataRequired(), Length(1, 64)],
        render_kw={'placeholder': 'johndoe'})
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()],
        render_kw={'placeholder': 'johndoe@email.com'})
    phone = StringField(
        'Phone Number',
        validators=[DataRequired(), Length(min=2, max=30)])
    password = PasswordField(
        'Password:',
        validators=[DataRequired(), Length(min=8, max=20),
        Regexp(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$',
               message='Password must be at least 8 characters long and '
               'contain at least one letter and one number.')],
        render_kw={'placeholder': 'Use: ecommerceapp123'})
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password')],
        render_kw={'placeholder': 'Confirm Your Password Above'})

    def validate_username(self, username):
        """Check if username already exists"""
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        """Check if email already exists"""
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

    def validate_phone(self, phone):
        p = phonenumbers.parse(phone.data)
        try:
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError) as exc:
            raise ValidationError('Invalid phone number.\n\n', exc ) from exc


class VendorRegistrationForm(UserForm):
    """Vendor Registration Form"""
    shop_name = StringField(
        'Shop Name',
        validators=[DataRequired(), Length(1, 64)],
        render_kw={'placeholder': 'eCommerce Shop 1'})
    submit = SubmitField('Register')


class CustomerRegistrationForm(UserForm):
    """Customer Registration Form"""
    residence = StringField(
        'Residence',
        validators=[DataRequired(), Length(1, 64)],
        render_kw={'placeholder': 'Roselyn, Nairobi'})
    submit = SubmitField('Register')


class AdminRegistrationForm(UserForm):
    """Admin Registration Form"""
    department = SelectField(
        'Department',
        choices=[
            ('Support', 'Support'),
            ('Finance', 'Finance'),
            ('HR', 'HR')
        ],
        validators=[DataRequired()])
    submit = SubmitField('Register')


class AddToCart(FlaskForm):
    """Add items to the cart"""
    quantity = IntegerField(
        'Quantity',
        validators=[DataRequired()],
        render_kw={'placeholder': '1'})
    submit = SubmitField('Add')


class ProductsForSaleForm(FlaskForm):
    name = StringField(
        'Product Name',
        validators=[DataRequired(), Length(1, 64)],
        render_kw={'placeholder': 'iPhone 13 Pro'})
    price = IntegerField('Price', validators=[DataRequired()])
    currency = SelectField(
        'Currency',
        choices=[('KES', 'KES')],
        validators=[DataRequired()])
    description = PageDownField(
        'Product Description',
        validators=[DataRequired(), Length(1, 64)],
        render_kw={'placeholder': 'iPhone 13 Pro'})
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    image = FileField(
        'Product Image',
        validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'svg', 'jpeg'])])
    submit = SubmitField('Add')
