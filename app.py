from signal import pause

from flask import Flask, render_template, abort, request
import os

from flask_cors import CORS, cross_origin

import Music

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = {'wav', 'WAV', 'h5', 'H5'}


# 用于判断文件后缀
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# 用于测试上传
@app.route('/')
def upload_test():
    return render_template('base.html')


# 上传文件
@app.route('/upload', methods=['GET', 'POST'], strict_slashes=False)
@cross_origin()
def api_upload():
    if request.method == 'GET':
        return render_template('base.html')
    else:
        file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        f = request.files['file']  # 从表单的file字段获取文件，myfile为该表单的name值
        if f and allowed_file(f.filename):  # 判断是否是允许上传的文件类型
            file = f.filename
            file_path = os.path.join(file_dir, file)  # 文件保存路径
            f.save(file_path)  # 保存文件到upload目录
            predicted_class = Music.music_indentify(file_path)
            os.remove(file_path)
            return predicted_class
        else:
            return 'error:识别错误！'


@app.route('/uploadH5', methods=['GET', 'POST'], strict_slashes=False)
@cross_origin()
def h5_upload():
    if request.method == 'GET':
        return render_template('base.html')
    else:
        if not os.path.exists(basedir):
            os.makedirs(basedir)
        f = request.files['file']  # 从表单的file字段获取文件，myfile为该表单的name值

        if f and allowed_file(f.filename):  # 判断是否是允许上传的文件类型
            file = f.filename
            file_path = os.path.join(basedir, file)  # 文件保存路径
            f.save(file_path)  # 保存文件到根目录
            return 'success'
        else:
            return 'error:识别错误！'
            # return jsonify({"errno":1001,"errmsg":"上传失败"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8067, debug=True)
