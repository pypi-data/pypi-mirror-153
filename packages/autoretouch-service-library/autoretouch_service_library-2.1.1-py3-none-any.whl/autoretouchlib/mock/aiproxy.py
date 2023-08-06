import json


from requests_mock import Mocker


class AiProxyMock(Mocker):
    def __init__(self, trimap, ghosting, remove_background, **kwargs):
        super().__init__(real_http=True, **kwargs)
        with open(trimap) as t, open(ghosting) as g, open(remove_background) as rb:
            self.trimap = json.load(t)
            self.ghosting = json.load(g)
            self.remove_background = json.load(rb)

    def __enter__(self):
        super().__enter__()
        self.register_uri('POST', 'http://localhost:8283/predict/', json=self.trimap)
        self.register_uri('POST', 'http://localhost:8282/predict/', json=self.ghosting)
        self.register_uri('POST', 'http://localhost:8281/predict/', json=self.remove_background)

        return self
