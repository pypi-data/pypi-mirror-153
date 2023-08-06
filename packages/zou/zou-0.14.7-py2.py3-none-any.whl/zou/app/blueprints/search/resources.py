from flask_restful import Resource
from flask_jwt_extended import jwt_required

from zou.app.mixin import ArgsMixin
from zou.app.services import index_service


class SearchResource(Resource, ArgsMixin):

    @jwt_required
    def post(self):
        # TODO manage permissions
        args = self.get_args([("query", "", True)])
        query = args.get("query")
        if len(query) < 3:
            return {
                "assets": []
            }
        return {
            "assets": index_service.search_assets(query)
        }
