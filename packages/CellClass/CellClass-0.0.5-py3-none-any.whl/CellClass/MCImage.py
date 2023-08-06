import numpy as np

class MCImage():

    def __init__(self, img, scheme="BGR"):
        
        self.img = img
        scheme = scheme.upper()

        if scheme not in ["BGR", "RGB", "GRAY"]:
            raise ValueError("Not a valid color scheme! Please use: 'BGR', 'RGB' or 'GRAY'")
        else:

            if scheme == "BGR":
                self.B = img[..., 0]
                self.G = img[..., 1]
                self.R = img[..., 2]

            elif scheme == "RGB":
                self.B = img[..., 2]
                self.G = img[..., 1]
                self.R = img[..., 0]

            elif scheme == "GRAY":
                self.GRAY = img

    def normalize(self, channelwise=True):

        if hasattr(self, "GRAY"):
            self.GRAY = (self.GRAY-self.GRAY.min())/(self.GRAY.max()-self.GRAY.min())
        
        else:
            if channelwise:
                self.B = (self.B-self.B.min())/(self.B.max()-self.B.min())
                self.R = (self.R-self.R.min())/(self.R.max()-self.R.min())
                self.G = (self.G-self.G.min())/(self.G.max()-self.G.min())

            else:
                stack = np.stack((self.B, self.G, self.R), axis=-1)
                stack = (stack-stack.min())/(stack.max()-stack.min())
                self.B = stack[..., 0]
                self.G = stack[..., 1]
                self.R = stack[..., 2]

    
