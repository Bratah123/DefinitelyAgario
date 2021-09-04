from circle import Circle


class Blob(Circle):
    """
    Represents the little blobs you pick up in Agario to get bigger
    """

    def __init__(self, blob_id, x, y, radius, color):
        super().__init__(x, y, radius, color)
        self.blob_id = blob_id
