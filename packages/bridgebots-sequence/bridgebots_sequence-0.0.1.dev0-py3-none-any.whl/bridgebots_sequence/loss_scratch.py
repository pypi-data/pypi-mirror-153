import tensorflow as tf
from tensorflow.keras import Input
from tensorflow.keras.layers import Dense, LSTM
from tensorflow.keras.models import Model


def build_model(v_size):
    sequence_input = Input(shape=(None, vocab_size), name="sequences")
    mask_input = Input(shape=(None,), dtype=tf.bool, name="masks")
    lstm_output, state_h, state_c = LSTM(
        units=10,
        return_state=True,
        return_sequences=True,
    )(sequence_input, mask=mask_input)
    output = Dense(v_size, activation="softmax")(lstm_output)
    return Model(
        inputs=[sequence_input, mask_input],
        outputs=output,
    )


def train():
    # Training a sequence prediciton LSTM model using return_sequences
    # 1 is start-of-sequence, 7 is end-of-sequence, 0 is padding
    vocab_size = 7

    sequences = [[1, 2, 3, 0, 0], [1, 4, 5, 6, 0]]
    targets = [[2, 3, 7, 0, 0], [4, 5, 6, 7, 0]]

    masks = tf.not_equal(sequences, 0)
    one_hot_sequences = tf.one_hot(sequences, vocab_size)
    one_hot_targets = tf.one_hot(targets, vocab_size)

    model = build_model(vocab_size)
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-2),
        loss=tf.keras.losses.CategoricalCrossentropy(from_logits=False),
    )
    model.fit(x={"sequences": one_hot_sequences, "masks": masks}, y=one_hot_targets, epochs=1000)
    return model

if __name__ == "__main__":
    model = train()
    model.predict()