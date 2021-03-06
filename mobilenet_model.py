from tensorflow.keras import Input
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, BatchNormalization, Dropout, Flatten, Dense, ZeroPadding2D, DepthwiseConv2D, GlobalAveragePooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ReduceLROnPlateau

from load_data import tensor_load

if __name__ == "__main__":
	X_train1, X_test1, y_train1, y_test1 = tensor_load()

	model = Sequential()
	model.add(Input(shape=(28,28,1)))
	model.add(ZeroPadding2D(padding=(2,2)))
	# 1_32
	model.add(Conv2D(32, kernel_size=3, padding="same", activation="relu"))
	model.add(BatchNormalization())
	# 1_64
	model.add(DepthwiseConv2D(kernel_size=3, padding="same", strides=1, activation="relu"))
	model.add(BatchNormalization())
	model.add(Conv2D(64, kernel_size=1, padding="same", activation="relu"))
	model.add(BatchNormalization())
	# 1_128
	model.add(DepthwiseConv2D(kernel_size=3, padding="same", strides=2, activation="relu"))
	model.add(BatchNormalization())
	model.add(Conv2D(128, kernel_size=1, padding="same", activation="relu"))
	model.add(BatchNormalization())
	# 2_128
	model.add(DepthwiseConv2D(kernel_size=3, padding="same", strides=1, activation="relu"))
	model.add(BatchNormalization())
	model.add(Conv2D(128, kernel_size=1, padding="same", activation="relu"))
	model.add(BatchNormalization())
	# 1_256
	model.add(DepthwiseConv2D(kernel_size=3, padding="same", strides=2, activation="relu"))
	model.add(BatchNormalization())
	model.add(Conv2D(256, kernel_size=1, padding="same", activation="relu"))
	model.add(BatchNormalization())
	# 2_256
	model.add(DepthwiseConv2D(kernel_size=3, padding="same", strides=1, activation="relu"))
	model.add(BatchNormalization())
	model.add(Conv2D(256, kernel_size=1, padding="same", activation="relu"))
	model.add(BatchNormalization())
	# 1_512
	model.add(DepthwiseConv2D(kernel_size=3, padding="same", strides=2, activation="relu"))
	model.add(BatchNormalization())
	model.add(Conv2D(512, kernel_size=1, padding="same", activation="relu"))
	model.add(BatchNormalization())
	# 2-6_512
	for _ in range(5):
	    model.add(DepthwiseConv2D(kernel_size=3, padding="same", strides=1, activation="relu"))
	    model.add(BatchNormalization())
	    model.add(Conv2D(512, kernel_size=1, padding="same", activation="relu"))
	    model.add(BatchNormalization())
	# 1_1024
	model.add(DepthwiseConv2D(kernel_size=3, padding="same", strides=2, activation="relu"))
	model.add(BatchNormalization())
	model.add(Conv2D(1024, kernel_size=1, padding="same", activation="relu"))
	model.add(BatchNormalization())
	# 2_1024
	model.add(DepthwiseConv2D(kernel_size=3, padding="same", strides=1, activation="relu"))
	model.add(BatchNormalization())
	model.add(Conv2D(1024, kernel_size=1, padding="same", activation="relu"))
	model.add(BatchNormalization())

	model.add(GlobalAveragePooling2D())
	model.add(Dense(10, activation="softmax"))

	model.compile(optimizer=opt, loss="categorical_crossentropy", metrics=["accuracy"])


	datagen = ImageDataGenerator(
	            rotation_range=12,
	            zoom_range=0.25,
	            width_shift_range=0.25,
	            height_shift_range=0.25,
	            data_format="channels_last",
	            shear_range=15)

	datagen.fit(X_train1)

	opt = RMSprop(lr=0.01)

	reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.25, 
	                                       patience=5, min_lr=0.00001)


	model.fit_generator(datagen.flow(X_train1, y_train1, batch_size=32), steps_per_epoch=X_train1.shape[0]//32, 
	                           epochs=70, validation_data=(X_test1, y_test1), callbacks=[reduce_lr])

	model.save("./dependencies/models/mobilenet.h5")
