import os

import tensorflow as tf
import librosa
from tensorflow.python.ops import gen_audio_ops as audio_ops
from tensorflow.python.ops import io_ops

import waveClassic

sample_rate, window_size_ms, window_stride_ms = 3200, 60, 30
dct_coefficient_count = 40
clip_duration_ms = 1000
second_time = 16
desired_samples = int(sample_rate * second_time * clip_duration_ms / 1000)
window_size_samples = int(sample_rate * window_size_ms / 1000)
window_stride_samples = int(sample_rate * window_stride_ms / 1000)


def get_mfcc_simplify(wav_filename, desired_samples=desired_samples, window_size_samples=window_size_samples,
                      window_stride_samples=window_stride_samples, dct_coefficient_count=dct_coefficient_count):
    # 读取音频文件
    wav_loader = io_ops.read_file(wav_filename)
    # 进行音频解码
    wav_decoder = audio_ops.decode_wav(
        wav_loader, desired_channels=1, desired_samples=desired_samples)

    # 获取音频指纹信息.
    spectrogram = audio_ops.audio_spectrogram(
        wav_decoder.audio,
        window_size=window_size_samples,
        stride=window_stride_samples,
        magnitude_squared=True)

    # 生产MFCC矩阵
    mfcc_ = audio_ops.mfcc(
        spectrogram,
        wav_decoder.sample_rate,
        dct_coefficient_count=dct_coefficient_count)  # dct_coefficient_count=model_settings['fingerprint_width']
    return mfcc_


# 对测试数据进行 MFCC 特征提取
sample_rate, window_size_ms, window_stride_ms = 3200, 60, 30
dct_coefficient_count = 40


# 加载测试数据

def music_indentify(test_wav_path):
    model = waveClassic.get_wav_model()
    model.load_weights(os.path.abspath('model.h5'))
    y, _ = librosa.load(test_wav_path, sr=sample_rate)
    mfcc = get_mfcc_simplify(test_wav_path)
    # 将MFCC特征输入到模型中进行预测

    predictions = model.predict(mfcc)
    # 输出分类结果
    result = ['A.I.N.Y', 'A.I.N.Y', 'A.I.N.Y', 'A.I.N.Y', 'A.I.N.Y',
          'A.I.N.Y', 'A.I.N.Y', '刚刚好',
          '刚刚好', '刚刚好', '刚刚好', '刚刚好', '刚刚好',
          '刚刚好', '刚刚好',  '有何不可',
          '有何不可', '有何不可', '有何不可', '有何不可', '有何不可',
          '有何不可', '有何不可', '烟花易冷',
          '烟花易冷', '烟花易冷', '烟花易冷', '烟花易冷', '烟花易冷',
          '烟花易冷', '烟花易冷', '烟花易冷', '烟花易冷', '烟花易冷']
    predicted_class_index = tf.argmax(predictions, axis=1)[0]
    predicted_class = result[predicted_class_index]
    print('Predicted class:', predicted_class)
    return predicted_class
