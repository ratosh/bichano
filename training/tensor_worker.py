import tensorflow as tf


class TensorWorker:
    def __init__(self, cfg, training_loader, test_loader):
        self.cfg = cfg
        self.training_loader = training_loader
        self.test_loader = test_loader
        self.regularizer = tf.keras.regularizers.l2(l=0.5 * 0.0001)
        self.network = self.create_network()

    def create_network(self):
        input = tf.keras.Input(shape=(10, 64))
        input_planes = tf.keras.layers.Reshape((10, 8, 8))(input)

        flow = self.conv_block('input', input_planes, self.cfg.filters, self.cfg.kernel_size)
        for i in range(self.cfg.blocks):
            flow = self.residual_block('res_{}'.format(i + 1), flow, self.cfg.filters, self.cfg.kernel_size)

        return self.value_head(flow), self.policy_head(flow)

    def conv_block(self, name, input, filters, kernel_size):
        x = tf.keras.layers.Conv2D(
            filters=filters, kernel_size=kernel_size, data_format="channels_first", padding='same', use_bias=False,
            activation='linear', kernel_regularizer=self.regularizer, name=name + '/cl2d')(input)

        x = tf.keras.layers.BatchNormalization(name=name + '/bn', axis=1)(x)
        x = tf.keras.layers.LeakyReLU(name=name + 'relu')(x)

        return x

    def residual_block(self, name, input, filters, kernel_size):
        x = self.conv_block(name + '/1', input, filters, kernel_size)

        x = tf.keras.layers.Conv2D(
            filters=filters, kernel_size=kernel_size, data_format="channels_first", padding='same', use_bias=False,
            activation='linear', kernel_regularizer=self.regularizer, name=name + '/2/res')(x)

        x = tf.keras.layers.BatchNormalization(name=name + '/2/bn', axis=1)(x)
        x = tf.keras.layers.add([input, x])
        x = tf.keras.layers.LeakyReLU()(x)

        return x

    def value_head(self, x):
        x = tf.keras.layers.Conv2D(
            filters=1, kernel_size=(1, 1), data_format="channels_first", padding='same', use_bias=False,
            activation='linear', kernel_regularizer=self.regularizer
        )(x)

        x = tf.keras.layers.BatchNormalization(axis=1)(x)
        x = tf.keras.layers.LeakyReLU()(x)

        x = tf.keras.layers.Flatten()(x)

        x = tf.keras.layers.Dense(
            128, use_bias=False, activation='linear', kernel_regularizer=self.regularizer
        )(x)

        x = tf.keras.layers.LeakyReLU()(x)

        x = tf.keras.layers.Dense(
            1, use_bias=False, activation='tanh', kernel_regularizer=self.regularizer, name='value_head'
        )(x)

        return x

    def policy_head(self, x):
        x = tf.keras.layers.Conv2D(
            filters=2, kernel_size=(1, 1), data_format="channels_first", padding='same', use_bias=False,
            activation='linear', kernel_regularizer=self.regularizer
        )(x)

        x = tf.keras.layers.BatchNormalization(axis=1)(x)
        x = tf.keras.layers.LeakyReLU()(x)

        x = tf.keras.layers.Flatten()(x)

        x = tf.keras.layers.Dense(
            1858, use_bias=False, activation='linear', kernel_regularizer=self.regularizer,
            name='policy_head'
        )(x)

        return x
