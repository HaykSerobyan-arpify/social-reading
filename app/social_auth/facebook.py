import facebook


class Facebook:
    """
    Facebook class to fetch the user info and return it
    """

    @staticmethod
    def validate(auth_token):
        """
        validate method Queries the facebook GraphAPI to fetch the user info
        """
        try:
            graph = facebook.GraphAPI(access_token=auth_token)
            profile = graph.get_object('me', fields='first_name,last_name,location,link,email,picture,hometown')
            return profile
        except Exception:
            return "The token is invalid or expired."
