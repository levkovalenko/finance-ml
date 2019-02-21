import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D
from PreProcessors.csv_pre_processor_inctiments import PreProcessor
import matplotlib.pyplot as plt
import os
from keras.layers.normalization import BatchNormalization
from keras.optimizers import SGD
from keras.layers import Convolution2D

batch_size = 200
num_classes = 2
epochs = 10
data_augmentation = True
num_predictions = 20
save_dir = os.path.join(os.getcwd(), 'saved_models')
model_name = 'keras_cifar10_trained_model.h5'

PP = PreProcessor(filename="../index/FX_EURKRW.csv")
PP.start(grade=20, ws_pred=20)
"""
train_x: обучающие данные содержащие в себе heatmap 20X20
train_y: обучающие данные(предсказания) содержащие в себе 7-дневные тренды"""
x_train, y_train = PP.get_train()
"""
test_x: тренировачные данные содержащие в себе heatmap 20X20
test_y: тренировачные данные(предсказания) содержащие в себе 7-дневные тренды"""

x_test, y_test = PP.get_test()
print('x_train shape:', x_train.shape)
print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')


model = Sequential()
model.add(Conv2D(120, kernel_size=(3, 3),
                 activation='relu',
                 input_shape=(20, 20, 1)))
model.add(MaxPooling2D(pool_size=(2, 2), padding='valid'))
model.add(Conv2D(70, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2), padding='valid'))
model.add(Conv2D(50, (2, 2), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2), padding='valid'))
model.add(Conv2D(20, (2, 2), activation='relu'))
model.add(Flatten())
model.add(Dropout(0.5))
model.add(Dense(100))
model.add(Activation('softmax'))
model.add(Dense(20))
model.add(Activation('elu'))
model.add(Dense(1))
model.add(Activation("elu"))

# initiate RMSprop optimizer[0.16458936]
opt = keras.optimizers.rmsprop(lr=0.01, decay=1e-6)
sgd = SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=True)
# Let's train the model using RMSprop
if __name__ == "__main__":
    model.compile(loss='mean_squared_error',
                  optimizer='rmsprop',
                  metrics=['binary_accuracy'])

    """
    history: данные полученные во время обучения сети, необходимые для построения различных графиков"""

    history = model.fit(x=x_train, y=y_train, batch_size=batch_size, epochs=epochs,
                        shuffle=True, validation_data=(x_test, y_test))
    """if not os.path.isdir(save_dir):
        os.makedirs(save_dir)
    model_path = os.path.join(save_dir, model_name)
    model.save(model_path)
    print('Saved trained model at %s ' % model_path)
    
    
    Данные полученные после тестирования сети - точность работы на тренировчном множестве """

    scores = model.evaluate(x_test, y_test, verbose=1)
    print("Точность работы на тестовых данных: %.2f%%" % (scores[1]*100))
    ans = model.predict(x_test, verbose=1)
    print(ans)
    q = 0
    w = 0
    for a, b in zip(ans,y_test):
        if a > 0.17 and b == 1:
            q+=1
        if b == 1:
            w+=1

    print(q/w)
    q = 0
    w = 0
    for a, b in zip(ans,y_test):
        if a < 0.17 and b == 0:
            q+=1
        if b == 0:
            w+=1

    print(q/w)
    plt.plot(history.history['acc'])
    plt.show()

