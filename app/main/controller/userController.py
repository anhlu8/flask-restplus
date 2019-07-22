from flask import request
from flask_restplus import Resource

from ..util.dto import UserDto
from ..service.userService import save_new_user, get_all_users, get_a_user

api = UserDto.api
_user = UserDto.user

# api.route: A decorator to route resources
@api.route('/')
class UserList(Resource):
    # api.doc: A decorator to add some api documentation to the decorated object
    @api.doc('list_of_registered_users')
    @api.marshal_list_with(_user, envelope='data')
    def get(self):
        """List all registered users"""
        return get_all_users()
    # api.response: A decorator to specify one of the expected responses
    @api.response(201, 'User successfully created.')
    @api.doc('create a new user')
    # api.expect: A decorator to Specify the expected input model(we still use the userDto for the expected input)
    @api.expect(_user, validate=True)
    def post(self):
        """Creates a new User """
        data = request.json
        return save_new_user(data=data)


@api.route('/<public_id>')
# api.param: A decorator to specify one of the expected parameters
@api.param('public_id', 'The User identifier')
@api.response(404, 'User not found.')
class User(Resource):
    @api.doc('get a user')
    # api.marshal_with: A decorator specifying the fields to use for serialization(This is where we use the userDto we created earlier)
    @api.marshal_with(_user)
    def get(self, public_id):
        """get a user given its identifier"""
        user = get_a_user(public_id)
        if not user:
            api.abort(404)
        else:
            return user
