from flask import Flask, render_template, request, send_file, Response
from rembg import remove
from PIL import Image
from io import BytesIO

app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
def upload_cropped_image():

    if request.method == 'POST':
        # Read from "croppedImage" in post request form data
        file = request.files['croppedImage'].read()
        # debug
        print(file)
        if file:
            try:
                input_image = Image.open(BytesIO(file))
                output_image = remove(input_image, post_process_mask=True)

                img_io = BytesIO()
                output_image.save(img_io, 'PNG')
                img_io.seek(0)
                # send image for ajax to download

                return send_file(img_io, mimetype='image/png', as_attachment=True, download_name='processed_image.png')
            except Exception as e:
                return Response(f"Error processing image: {str(e)}", status=500)

        else:
            return Response("No image data received", status=400)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5100)
