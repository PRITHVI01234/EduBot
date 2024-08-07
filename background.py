import base64

class BackgroundCSSGenerator:
    def __init__(self, img1_path, img2_path):
        self.img1_path = img1_path
        self.img2_path = img2_path

    def get_img_as_base64(self, file):
        with open(file, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()

    def generate_background_css(self):
        img1 = self.get_img_as_base64(self.img1_path)
        img2 = self.get_img_as_base64(self.img2_path)

        css = f"""
        <style>
        [data-testid="stAppViewContainer"] > .main {{
            background-image: url("data:image/png;base64,{img1}");
            background-size: cover;
            background-position: center;
        }}

        [data-testid="stSidebar"] > div:first-child {{
            background-image: url("data:image/png;base64,{img2}");
            background-position: center; 
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-size: cover;
        }}

        [data-testid="stHeader"] {{
            background: rgba(0,0,0,0);
        }}

        [data-testid="stToolbar"] {{
            right: 2rem;
        }}
        </style>
        """
        return css