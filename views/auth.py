# from flask import request
# from flask_restx import Resource, Namespace
#
#
# auth_ns = Namespace('auth')
#

# @auth_ns.route('/')
# class AuthView(Resource):
#     def post(self):
#         data = request.json
#         username = data.get('username')
#         password = data.get('password')
#
#         if not username or not password:
#             return "Нет пароля или логина", 400
#
#         user = user_service.get_by_username(username=username)
#
#         return generate_token(username=username,
#                               password=password,
#                               password_hash=user.password,
#                               is_refresh=False), 201
#
#     def put(self):
#         data = request.json
#         if not data.get('refresh_token'):
#             return "", 400
#
#         return approve_token(data.get('refresh_token')), 200

import datetime
import calendar

import jwt
from flask import request
from flask_restx import Resource, Namespace

from constants import JWT_SECRET, JWT_ALGORITHM
from dao.model.models import User
from setup_db import db

auth_ns = Namespace('auth')


def generate_tokens(data) -> dict:
    # 30 min access_token
    min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    data["exp"] = calendar.timegm(min30.timetuple())
    access_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)

    # 130 days refresh_token
    days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
    data["exp"] = calendar.timegm(days130.timetuple())
    refresh_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }


@auth_ns.route('/')
class AuthView(Resource):
    def post(self):
        req_json = request.json
        username = req_json.get("username", None)
        password = req_json.get("password", None)
        if None in [username, password]:
            return "Нет логина или пароля", 400

        user = db.session.query(User).filter(User.username == username).first()

        if user is None or not user.compare_passwords(password):
            return "нет такого пользователя или неправильный пароль", 404

        data = {
            "username": user.username,
            "password": user.password,
            "role": user.role
        }

        tokens = generate_tokens(data)

        return tokens, 201

    def put(self):
        req_json = request.json
        token = req_json.get("refresh_token")

        try:
            data = jwt.decode(jwt=token, key=JWT_SECRET, algorithms=[JWT_ALGORITHM])
            username = data.get("username")
            password = data.get("password")

            user = db.session.query(User).filter(User.username == username).first()

            if user is None or user.password != password:
                return "нет такого пользователя или неправильный пароль", 404

            tokens = generate_tokens(data)
            return tokens, 201

        except jwt.ExpiredSignatureError as ex:
            return "срок действия токена истёк", 401

        except jwt.InvalidTokenError as ex:
            return "некорректный токен", 401
