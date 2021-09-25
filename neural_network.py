# Big Data, Xarxes Neuronals i Màrqueting: la clau de l'èxit?
# Treball de recerca (TR)
# Marc Vergés Santiago - Escola Pia Mataró
#
#
#
# Copyright (c) 2021, Marc Vergés Santiago
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the <organization> nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY MARC VERGÉS ''AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <copyright holder> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE


import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from keras.utils import np_utils
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.callbacks import EarlyStopping
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
import instaloader
from contrasenyes import usuari, contrasenya


def profile_preferences_to_NN(user):
    L = instaloader.Instaloader()

    L.login(usuari, contrasenya)

    list_to_append_csv = []
    none = 0
    creators_celebrities = 0
    personal_gods = 0
    local_events = 0
    professional_services = 0
    restaurants = 0
    non_profits = 0
    general_interest = 0
    publishers = 0
    transportation_and_accomodation = 0
    business_and_utility = 0
    home_services = 0
    auto_dealers = 0
    food_and_personal_goods = 0
    government_agencies = 0
    content_apps = 0
    grocery = 0
    entities = 0
    lifestyle_services = 0
    geography = 0

    profile = instaloader.Profile.from_username(L.context, user)
    preferences = []
    for followee in profile.get_followees():
        preferences.append(followee.business_category_name)
        print(followee.username + " - " + str(followee.business_category_name))
        if followee.business_category_name == "None":
            none += 1
        if followee.business_category_name == "Creators & Celebrities":
            creators_celebrities += 1
        if followee.business_category_name == "Personal Goods & General Merchandise Stores":
            personal_gods += 1
        if followee.business_category_name == "Local Events":
            local_events += 1
        if followee.business_category_name == "Professional Services":
            professional_services += 1
        if followee.business_category_name == "Restaurants":
            restaurants += 1
        if followee.business_category_name == "Non-Profits & Religious Organizations":
            non_profits += 1
        if followee.business_category_name == "General Interest":
            general_interest += 1
        if followee.business_category_name == "Publishers":
            publishers += 1
        if followee.business_category_name == "Transportation & Accomodation Services":
            transportation_and_accomodation += 1
        if followee.business_category_name == "Business & Utility Services":
            business_and_utility += 1
        if followee.business_category_name == "Home Services":
            home_services += 1
        if followee.business_category_name == "Auto Dealers":
            auto_dealers += 1
        if followee.business_category_name == "Food & Personal Goods":
            food_and_personal_goods += 1
        if followee.business_category_name == "Government Agencies":
            government_agencies += 1
        if followee.business_category_name == "Content & Apps":
            content_apps += 1
        if followee.business_category_name == "Grocery & Convenience Stores":
            grocery += 1
        if followee.business_category_name == "Entities":
            entities += 1
        if followee.business_category_name == "Lifestyle Services":
            lifestyle_services += 1
        if followee.business_category_name == "Geography":
            geography += 1

    print(preferences)

    print("None: " + str(none))
    print("Creators & Celebrities: " + str(creators_celebrities))
    print("Personal Goods & General Merchandise Stores: " + str(personal_gods))
    print("Local Events: " + str(local_events))
    print("Professional Services: " + str(professional_services))
    print("Restaurants: " + str(restaurants))
    print("Non-Profits & Religious Organizations: " + str(non_profits))
    print("General Interest: " + str(general_interest))
    print("Publishers: " + str(publishers))
    print("Transportation & Accomodation Services: " + str(transportation_and_accomodation))
    print("Business & Utility Services: " + str(business_and_utility))
    print("Home Services: " + str(home_services))
    print("Auto Dealers: " + str(auto_dealers))
    print("Food & Personal Goods: " + str(food_and_personal_goods))
    print("Government Agencies: " + str(government_agencies))
    print("Content & Apps: " + str(content_apps))
    print("Grocery & Convenience Stores: " + str(grocery))
    print("Entities: " + str(entities))
    print("Lifestyle Services: " + str(lifestyle_services))
    print("Geography: " + str(geography))

    followers = 0
    following = 0

    for follower in profile.get_followers():
        followers += 1
    for follower in profile.get_followees():
        following += 1

    return preferences

def neural_network(list):
    # url = 'https://gist.githubusercontent.com/curran/a08a1080b88344b0c8a7/raw/639388c2cbc2120a14dcf466e85730eb8be498bb/iris.csv'
    df = pd.read_csv("data_set3.csv")
    df = df.sample(frac=1).reset_index(drop=True)
    Y = df['Tematica']
    print(Y) # output
    X = df.drop(['Tematica'], axis=1)
    print(X) # input o dataset
    print(X.shape)
    print(Y.shape)
    X = np.array(X)
    Y.head()
    encoder = LabelEncoder()
    encoder.fit(Y)
    encoded_Y = encoder.transform(Y)
    dummy_y = np_utils.to_categorical(encoded_Y, 10)
    print(encoded_Y)
    print(dummy_y)
    model = Sequential()
    model.add(Dense(16, input_shape=(X.shape[1],), activation='relu'))  # input shape is (features,)
    model.add(Dense(16, input_shape=(X.shape[1],), activation='relu'))  # input shape is (features,)
    model.add(Dense(10, activation='softmax'))
    model.summary()

    # compile the model
    model.compile(optimizer='rmsprop',
                  loss='categorical_crossentropy',
                  # this is different instead of binary_crossentropy (for regular classification)
                  metrics=['accuracy'])
    es = keras.callbacks.EarlyStopping(monitor='val_loss',
                                       mode='min',
                                       patience=10,
                                       restore_best_weights=True)  # important - otherwise you just return the last weigths...
    '''
    # now we just update our model fit call
    history = model.fit(X,
                        dummy_y,
                        callbacks=[es],
                        epochs=200,  # you can set this to a big number!
                        batch_size=1,
                        shuffle=True,
                        validation_split=0.2,
                        verbose=1)
    es = keras.callbacks.EarlyStopping(monitor='val_loss',
                                       mode='min',
                                       patience=10,
                                       restore_best_weights=True)  # important - otherwise you just return the last weigths...
    '''
    # now we just update our model fit call
    history = model.fit(X,
                        dummy_y,
                        callbacks=[es],
                        epochs=50,  # you can set this to a big number!
                        batch_size=2,
                        shuffle=True,
                        validation_split=0.2,
                        verbose=1)

    history_dict = history.history

    # learning curve
    # accuracy
    acc = history_dict['accuracy']
    val_acc = history_dict['val_accuracy']

    # loss
    loss = history_dict['loss']
    val_loss = history_dict['val_loss']

    # range of X (no. of epochs)
    epochs = range(1, len(acc) + 1)

    # plot
    # "r" is for "solid red line"
    plt.plot(epochs, acc, 'r', label='Training accuracy')
    # b is for "solid blue line"
    plt.plot(epochs, val_acc, 'b', label='Validation accuracy')
    plt.title('Training and validation accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()

    plt.show()

    preds = model.predict(X)  # see how the model did!
    print(preds[0])  # i'm spreading that prediction across three nodes and they sum to 1
    print(np.sum(preds[0]))  # sum it up! Should be 1
    ## [9.9999988e-01 1.3509347e-07 6.7064638e-16]
    ## 1.0

    # Almost a perfect prediction
    # actual is left, predicted is top
    # names can be found by inspecting Y
    matrix = confusion_matrix(dummy_y.argmax(axis=1), preds.argmax(axis=1))
    matrix
    ## array([[50,  0,  0],
    ##        [ 0, 46,  4],
    ##        [ 0,  1, 49]])

    # more detail on how well things were predicted
    print(classification_report(dummy_y.argmax(axis=1), preds.argmax(axis=1)))

    model.predict(list, batch_size=1, verbose=1)
