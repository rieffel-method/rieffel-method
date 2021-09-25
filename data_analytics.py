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


import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.pyplot import figure, text
from contrasenyes import usuari, contrasenya
import instaloader
import numpy as np
from scipy.stats import norm
from csv import writer
import math


def graf(object_list):
    G = nx.DiGraph()
    item = [1, 2]
    nodes = 0
    i = 0
    j = 0
    users = []
    for element in object_list:
        users.append(element.username)

    while i < len(object_list):
        while j < len(object_list[i].follower_list):
            if object_list[i].follower_list[j] in users:
                G.add_edge(object_list[i].username, object_list[i].follower_list[j])
                nodes += 1
            j += 1
        j = 0
        i += 1

    for element in object_list:
        element.nodes = nodes

    pos = nx.spring_layout(G)
    figure(figsize=(19.2, 10.8))
    d = dict(G.degree)
    nx.draw(G, pos=pos, node_color='orange', arrowsize=18, width=1, with_labels=False,
            node_size=[d[k] * 500 for k in d])
    for node, (x, y) in pos.items():
        text(x, y, node, fontsize=d[node] * 1, ha='center', va='center')

    plt.show()

    incidence_matrix = nx.incidence_matrix(G, oriented=True)

    return incidence_matrix


def matriu_adj(object_list):
    print("||     Matriu d'adjacència")
    matrix = [["||    "] * 1 for i in range(len(object_list))]
    i = 0
    j = 0
    list_values = []
    counter = 0
    while i < len(object_list):
        while j < len(object_list):
            if object_list[i].username in object_list[j].follower_list:
                matrix[i].append(1)
                counter += 1
            else:
                matrix[i].append(0)
            j += 1
        j = 0
        matrix[i].append("                    ||")
        list_values.append(counter)
        counter = 0
        i += 1

    # visualització per terminal de la matriu
    for r in matrix:
        for c in r:
            print(c, end=" ")
        print()

    return list_values


def matriu_inc(matrix):
    print("||                                                   ||")
    print("||                                                   ||")
    print("||     Matriu d'incidència                           ||")
    print("||                                                   ||")
    print("||                                                   ||")

    matrix = matrix.toarray()
    matrix = matrix.astype(int)

    for r in matrix:
        print("||     ", end="", flush=True)
        for c in r:
            print(c, end=" ")
        print()


def update_values(object_list, list1, list2):
    print("||     Analitzant graf                               ||")
    print("||                                                   ||")
    print("||     Actualitzant valors                           ||")
    print("||                                                   ||")
    i = 0
    while i < len(object_list):
        object_list[i].grau_graf = list1[i]
        i += 1
    i = 0
    while i < len(object_list):
        object_list[i].common = list2[i]
        i += 1


def in_common(object_list):
    i = 0
    j = 0
    list_values = []
    counter = 0
    while i < len(object_list):
        while j < len(object_list[i].following_list):
            if object_list[i].following_list[j] in object_list[i].follower_list:
                counter += 1
            j += 1
        j = 0
        list_values.append(counter)
        counter = 0
        i += 1

    return list_values


def data_representation(object_list):
    popularitats = []
    users = []
    for element in object_list:
        users.append(element.username)
        popularitats.append(element.model())
        element.information()
        print("||")
        print("||")
        print("||")

    xpoints = np.array(users)
    ypoints = np.array(popularitats)

    plt.rcParams["figure.figsize"] = (19.2, 10.8)

    # reset plt.show window size
    # plt.rcParams["figure.figsize"] = plt.rcParamsDefault["figure.figsize"]

    plt.plot(xpoints, ypoints)
    plt.xticks(fontsize=8)
    plt.xlabel("Usuaris")
    plt.ylabel("Popularitat (%)")

    plt.show()

    # std = standard deviation (desviació estàndard)
    # mu = mean (mitjana)

    mu, std = norm.fit(popularitats)

    # Plot the histogram.
    plt.hist(popularitats, bins=25, density=True, alpha=0.6, color='b')

    # Plot the PDF.
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = norm.pdf(x, mu, std)
    plt.plot(x, p, 'k', linewidth=2)
    title = "Fit results: mu = %.2f,  std = %.2f" % (mu, std)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.xlabel("Popularitat (%)", fontsize=20)
    plt.title(title)

    plt.show()

    # Rang
    rang_max = 0
    rang_min = 100
    for element in popularitats:
        if element > rang_max:
            rang_max = element
        if element < rang_min:
            rang_min = element

    # Desviació mitjana
    desviacions = []
    for element in popularitats:
        desviacions.append(abs(element - mu))

    desviació_mitjana = 0
    for element in desviacions:
        desviació_mitjana += element

    desviació_mitjana = desviació_mitjana / len(desviacions)

    # Variància
    variancia = 0
    for element in popularitats:
        # multiplicat per 1 ja que la freqüència de la dada és 1 sempre, conté decimals i la diferencien de la resta
        variancia = (element - mu) ** 2 * 1
    variancia = variancia / len(object_list)

    # Desviació típica
    desviacio_tipica = math.sqrt(variancia)

    # Coeficient d'asimetria de Pearson
    pearson = (mu - (rang_max + rang_min) / 2) / desviacio_tipica

    # Coeficient d'asimetria de Fisher
    fisher = mu / desviacio_tipica ** 3

    # Curtosi
    curtosi = mu / std ** 4

    # Print de dades
    print("Mitjana (mu): " + str(mu))
    print("Rang: " + str(rang_min) + "-" + str(rang_max))
    print("Desviació mitjana: " + str(desviació_mitjana))
    print("Variància: " + str(variancia))
    print("Desviació típica o estàndard (std): " + str(desviacio_tipica))
    print("Coeficient d'asimetria de Pearson: " + str(pearson))
    print("Coeficient d'asimetria de Fisher: " + str(fisher))
    print("Curtosi: " + str(curtosi))


def like_searcher():
    L = instaloader.Instaloader()

    username = usuari
    password = contrasenya
    L.login(username, password)

    profile = instaloader.Profile.from_username(L.context, "marcvergees")

    likes = set()
    total_likes = 0
    posts = 0
    print("Fetching likes of all posts of profile {}.".format(profile.username))
    for post in profile.get_posts():
        print(post)
        likes = likes | set(post.get_likes())
        total_likes += len(likes)
        likes.clear()
        posts += 1

    likes_per_foto = total_likes / posts
    profile_to_scrap = ""
    profile = instaloader.Profile.from_username(L.context, profile_to_scrap)

    print(profile.business_category_name)


def profile_preferences_finder():
    L = instaloader.Instaloader()

    username = usuari
    password = contrasenya
    L.login(username, password)

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

    profile = instaloader.Profile.from_username(L.context, "martisegraam")
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

    list_to_append_csv = [profile.username, followers, following, none, creators_celebrities, personal_gods,
                          local_events, professional_services, restaurants, non_profits,
                          general_interest, publishers, transportation_and_accomodation, business_and_utility,
                          home_services, auto_dealers, food_and_personal_goods,
                          government_agencies, content_apps, grocery, entities, lifestyle_services, geography]

    with open('data_set.csv', 'a') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(list_to_append_csv)
        f_object.close()
