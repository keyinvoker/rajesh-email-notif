from flask_restful import Resource


class Index(Resource):
    def get(self):
        return {
            'app_desc': 'this app sends email notifs'
        }
