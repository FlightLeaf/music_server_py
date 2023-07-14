import tensorflow as tf


class WaveClassic(tf.keras.layers.Layer):
    def __init__(self):
        super(WaveClassic, self).__init__()

    def build(self, input_shape):
        self.convs = [tf.keras.layers.Conv1D(filters=64, kernel_size=2, strides=2) for _ in range(3)]
        self.layer_norms = [tf.keras.layers.LayerNormalization() for _ in range(3)]

        self.last_dense = tf.keras.layers.Dense(40, activation=tf.nn.softmax)
        super(WaveClassic, self).build(input_shape)  # 一定要在最后调用它

    def call(self, inputs):
        embedding = inputs

        for i in range(3):
            embedding = self.convs[i](embedding)
            embedding = self.layer_norms[i](embedding)

        embedding = tf.keras.layers.Flatten()(embedding)
        logits = self.last_dense(embedding)
        return logits


def get_wav_model():
    mfc_batch = tf.keras.Input(shape=(532, 40))
    logits = WaveClassic()(mfc_batch)
    model = tf.keras.Model(mfc_batch, logits)
    return model


if __name__ == '__main__':
    get_wav_model()