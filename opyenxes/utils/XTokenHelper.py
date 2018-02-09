class XTokenHelper:

    @staticmethod
    def extract_tokens(token_string):
        keys = list(map(lambda elem: elem.strip(), token_string.split("'")))
        return list(filter(lambda key: key != '', keys))

    @staticmethod
    def format_token(token):
        aux = list(map(lambda elem: "'{}'".format(elem) if len(elem.split(" ")) > 1 else elem, token))
        return " ".join(filter(lambda elem: elem.replace(" ", "") != "", aux))
