class Page:
    def __init__(self, id=-1, validity=0, modified=0, referenced=0, time=0):
        self.id = int(id)
        self.validity = validity  # 1 if page in operating memory, 0 if in swap
        self.referenced = referenced  # 1 if page was referenced recently, 0 otherwise

    def __str__(self):
        return "{0}".format(self.id)


class PageFault(BaseException):
    pass
