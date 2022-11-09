from . import register_wallet_blueprint
from flask import render_template, request, redirect, url_for
from flask_login import login_user
from ..extensions import db
from ..models import Wallet, User
from .forms import MyForm
from datetime import datetime

@register_wallet_blueprint.route('/', methods=["GET", "POST"])
def register():
    return "Register"

@register_wallet_blueprint.route('/address=<wallet_address>', methods=['GET', 'POST'])
def register_wallet(wallet_address):
    res = Wallet.query.filter_by(address=str(wallet_address)).first()
    if res:
        res.last_connected_at = datetime.utcnow()
        db.session.commit()
        user_id = res.user_id
        user = User.query.filter_by(id=user_id).first()
        login_user(user)
        return f"Successfully updated last visit time"
    else:
        # If no user, create a new user in the db
        u_entry = User()
        db.session.add(u_entry)
        db.session.commit()

        # Add the wallet to the db with the user_id we just created
        user_id = u_entry.id
        w_entry = Wallet(address=wallet_address, user_id=user_id)
        db.session.add(w_entry)
        db.session.commit()

        # login the user
        user = User.query.filter_by(id=user_id).first()
        login_user(user)
        return f"Successfully added wallet and created user"
    # return render_template('index.html', form=form, wallet_address=wallet_address)