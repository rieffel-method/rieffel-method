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


import time
import json
from json import JSONEncoder
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from contrasenyes import usuari, contrasenya
from matplotlib.pyplot import figure, text
import instaloader
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from data_analytics import matriu_adj, matriu_inc, graf, update_values, in_common, data_representation, like_searcher, profile_preferences_finder
from neural_network import neural_network, profile_preferences_to_NN
from data_visualization import visualize_data
from random import randint
import csv


class User:
    username = ""
    followers = ""
    following = ""
    posts = ""
    follower_list = []
    following_list = []
    likes_per_foto = ""
    biography = ""
    fullname = ""
    web = ""
    businesscategoryname = ""
    isbusinessaccount = ""
    isverified = ""
    isprivate = ""
    grau_graf = ""
    common = ""
    popularitat = ""
    nodes = ""

    # inicialització del mètode o constructor amb totes les parametritzacions
    def __init__(self, username, followers, following, posts, follower_list, following_list, likes_per_foto, biography, fullname, web, businesscategoryname, isbusinessaccount, isverified, isprivate, grau_graf, common, popularitat, nodes):
        self.username = username
        self.fullname = fullname
        self.followers = followers
        self.following = following
        self.posts = posts
        self.follower_list = follower_list
        self.following_list = following_list
        self.likes_per_foto = likes_per_foto
        self.biography = biography
        self.web = web
        self.grau_graf = grau_graf
        self.common = common
        self.popularitat = popularitat
        self.businesscategoryname = businesscategoryname
        self.isbusinessaccount = isbusinessaccount
        self.isverified = isverified
        self.isprivate = isprivate
        self.nodes = nodes

    def information(self):
        print("||     Usuari: " + self.username)
        print("||     Nom complet: " + self.fullname)
        print("||     Seguidors: " + str(self.followers))
        print("||     Seguits: " + str(self.following))
        print("||     Publicacions: " + str(self.posts))
        print("||     Llista de seguidors: ")
        print(self.follower_list)
        print("||     LLista de seguits: ")
        print(self.following_list)
        print("||     Likes per foto: " + str(self.likes_per_foto))
        print("||     Biografia: " + self.biography)
        print("||     Pàgina web: " + self.web)
        print("||     Categoria: " + str(self.businesscategoryname))
        print("||     Business account? " + str(self.isbusinessaccount))
        print("||     Verificada? " + str(self.isverified))
        print("||     Privada? " + str(self.isprivate))
        print("||     Grau graf: " + str(self.grau_graf))
        print("||     En comú: " + str(self.common))
        print("||     Popularitat: " + str(self.popularitat))

    def model(self):
        # popularity = (1-((int(self.common)*int(self.grau_graf)*int(self.likes_per_foto)/int(self.following))/(int(self.followers)*int(self.followers))))*100
        popularity = (int(self.grau_graf)/int(self.nodes))*100
        self.popularitat = popularity
        return popularity


class UserEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


def login():
    framework = ""
    loginurl = "https://www.instagram.com/accounts/login/"
    browser.get(loginurl)
    try:
        browser.find_element_by_xpath('/html/body/div[4]/div/div/button[1]').click()
    except NoSuchElementException:
        framework = "No framework"

    time.sleep(1)
    browser.find_element_by_xpath(
        '/html/body/div[1]/section/main/div/div/div[1]/div/form/div/div[1]/div/label/input').send_keys(usuari)
    browser.find_element_by_xpath(
        '/html/body/div[1]/section/main/div/div/div[1]/div/form/div/div[2]/div/label/input').send_keys(contrasenya)
    browser.find_element_by_xpath('/html/body/div[1]/section/main/div/div/div[1]/div/form/div/div[3]/button').click()


def search(username):
    time.sleep(5)
    browser.find_element_by_xpath('/html/body/div[1]/section/nav/div[2]/div/div/div[2]/input').send_keys(username)
    time.sleep(3)
    browser.find_element_by_xpath(
        '/html/body/div[1]/section/nav/div[2]/div/div/div[2]/div[3]/div/div[2]/div/div[1]/a/div/div[2]/div[1]/div/div/div[1]').click()
    time.sleep(3)


def coincidence_follower(a, b):
    # Entra al perfil de la primera persona
    search(a)
    time.sleep(3)
    follower_list_a = follower_list()
    browser.find_element_by_xpath('/html/body/div[5]/div/div/div[1]/div/div[2]/button/div').click()
    search(b)
    time.sleep(3)
    follower_list_b = follower_list()

    i = 0
    j = 0
    print("||     Coincidències:")
    while i < len(follower_list_a):
        while j < len(follower_list_b):
            if follower_list_a[i] == follower_list_b[j]:
                print("||     " + follower_list_a[i])
            j += 1
        j = 0
        i += 1


def coincidence_following(a, b):
    # Entra al perfil de la primera persona
    search(a)
    time.sleep(3)
    following_list_a = following_list()
    browser.find_element_by_xpath('/html/body/div[5]/div/div/div[1]/div/div[2]/button/div').click()
    search(b)
    time.sleep(3)
    following_list_b = following_list()

    i = 0
    j = 0
    print("||     Coincidències:")
    print("||")
    while i < len(following_list_a):
        while j < len(following_list_b):
            if following_list_a[i] == following_list_b[j]:
                print("||     " + following_list_a[i])
            j += 1
        j = 0
        i += 1


def following_list():
    following = int(
        browser.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/span').text)
    browser.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[3]/a').click()
    time.sleep(3)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # el nombre és 11 perquè es tracta dels perfils que surten de base sense fer l'scroll down
    # quan fas l'scroll down són 13 perfils que es mostren
    n = (following - 11) / 4
    # find all li elements in list
    fBody = browser.find_element_by_xpath("//div[@class='isgrP']")
    scroll = 0
    while scroll < n:  # baixa n vegades
        browser.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', fBody)
        time.sleep(0.5)
        scroll += 1
    i = 1
    followinglist = []
    while i + 1 < following:
        elem = browser.find_element_by_xpath(
            '/html/body/div[6]/div/div/div[3]/ul/div/li[' + str(i) + ']' + '/div/div[2]/div[1]/div/div/span/a')
        # / html / body / div[6] / div / div / div[3] / ul / div / li[1] / div / div[2] / div[1] / div / div / span / a
        # normalment acostumen a canviar el número del primer div[n] i, a vegades, el del segon div[m]
        followinglist.append(elem.text)
        i += 1
    browser.find_element_by_xpath('/html/body/div[6]/div/div/div[1]/div/div[2]/button/div').click()
    return followinglist


def follower_list():
    followers = int(
        browser.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span').text)
    browser.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[2]/a').click()
    time.sleep(3)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # el nombre és 11 perquè es tracta dels perfils que surten de base sense fer l'scroll down
    # quan fas l'scroll down són 13 perfils que es mostren
    n = (followers - 11) / 4
    # find all li elements in list
    fBody = browser.find_element_by_xpath("//div[@class='isgrP']")
    scroll = 0
    while scroll < n:  # baixa n vegades
        browser.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;',
                               fBody)
        time.sleep(0.5)
        scroll += 1
    i = 1
    followerslist = []
    time.sleep(1)
    while i < followers:
        elem = browser.find_element_by_xpath(
            '/html/body/div[6]/div/div/div[2]/ul/div/li[' + str(i) + ']' + '/div/div[1]/div[2]/div[1]/span/a')
        # normalment acostumen a canviar el número del primer div[n]
        followerslist.append(elem.text)
        i += 1
    browser.find_element_by_xpath('/html/body/div[6]/div/div/div[1]/div/div[2]/button/div').click()
    return followerslist


def data():
    followers = browser.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span').text
    following = browser.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/span').text
    username = browser.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/div[1]/h2').text
    posts = browser.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[1]/span/span').text
    biography = browser.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/div[2]/span').text
    fullname = browser.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/div[2]/h1').text

    try:
        # identifica element
        web = browser.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/div[2]/a[1]').text

    # NoSuchElementException -> no troba l'element
    except NoSuchElementException:
        web = "-"

    follower_list_ = follower_list()
    following_list_ = following_list()

    L = instaloader.Instaloader()
    username2 = usuari
    password = contrasenya
    L.login(username2, password)

    profile = instaloader.Profile.from_username(L.context, username)


    # likes / foto de l'usuari principal a scrappejar
    likes = set()
    total_likes = 0
    print("||    Descarregant likes de l'usuari {}.".format(profile.username))
    for post in profile.get_posts():
        print(post)
        likes = likes | set(post.get_likes())
        total_likes += len(likes)
        likes.clear()



    # instància de l'usuari principal
    person = User(username, followers, following, posts, follower_list_, following_list_, "str(total_likes / int(posts))", biography, fullname, web, profile.business_category_name, profile.is_business_account, profile.is_verified, profile.is_private, "", "", "", "")
    # mostra de la informació
    person.information()

    '''
    json_str = json.dumps(person.__dict__)

    with open("data_file.json", "w") as write_file:
        json.dump(json_str, write_file)
    '''

    # descàrrega d'informació massiva


    list_of_objects = [person]

    # bucle amb la longitud de la llista de seguidors
    # es descarrega informació de l'usuari follower_list_[i]
    for i in range(len(person.follower_list)):
        profile = instaloader.Profile.from_username(L.context, follower_list_[i])
        list_of_objects.append(User(follower_list_[i], "", "", "", [], [], "", profile.biography, profile.full_name, "", profile.business_category_name, profile.is_business_account, profile.is_verified, profile.is_private, "", "", "", ""))

        # descàrrega de likes i posts dels usuaris de descàrrega massiva
        likes2 = set()
        total_likes2 = 0
        posts2 = 0
        print("||    Descarregant likes de l'usuari {}.".format(profile.username))
        for post in profile.get_posts():
            print(post)
            likes = likes2 | set(post.get_likes())
            total_likes2 += len(likes2)
            likes2.clear()
            posts2 += 1

        if posts2 != 0:
            list_of_objects[i].likes_per_foto = total_likes2/posts2
        else:
            list_of_objects[i].likes_per_foto = 1

        list_of_objects[i].posts = posts2

        posts2 = 0
        total_likes2 = 0

        # bucle descàrrega informació followers
        for followee in profile.get_followers():
            list_of_objects[i + 1].follower_list.append(followee.username)

        # bucle descàrrega informació following
        for followee in profile.get_followees():
            list_of_objects[i + 1].following_list.append(followee.username)

        list_of_objects[i + 1].followers = len(list_of_objects[i + 1].follower_list) + 1
        list_of_objects[i + 1].following = len(list_of_objects[i + 1].following_list) + 1

        print("||     Informació descarregada de l'usuari " + follower_list_[i] + "      " + str(i + 1) + "/" + str(
            len(person.follower_list)))

    print("||     Tota la informació s'ha descarregat correctament")

    return list_of_objects


def proves_graf():
    G = nx.DiGraph()

    for i in range(7):
        G.add_edge(1, i)

    nx.draw(G, node_color='w', edgecolors='k', width=0.1, node_size=40)
    plt.show()


def proves():
    print("proves")


def data_adquisition():
    list_of_objects = []
    i = 0
    with open("data_file/data_file.json", "r") as f:
        data = json.loads(f.read())
        while i < len(data):
            list_of_objects.append(
                User(data[i]["username"], data[i]["followers"], data[i]["following"], data[i]["posts"],
                     data[i]["follower_list"], data[i]["following_list"], data[i]["likes_per_foto"], data[i]["biography"], data[i]["fullname"],
                     data[i]["web"], data[i]["businesscategoryname"], data[i]["isbusinessaccount"], data[i]["isverified"], data[i]["isprivate"], "", "", "", ""))
            i += 1
    return list_of_objects


def graph(object_list):
    a = 0
    with open("data_file.json", "w") as write_file:
        while a < len(object_list):
            json.dump(UserEncoder().encode(object_list[a]), write_file, indent=2, sort_keys=True)
            a += 1

    with open("data_file.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="/", quoting=csv.QUOTE_MINIMAL)
        for item in object_list:
            writer.writerow(
                [item.username, item.followers, item.following, item.posts, item.follower_list, item.following_list,
                 item.biography, item.fullname, item.web])

    G = nx.DiGraph()
    item = [1, 2]
    nodes = 0
    i = 0
    j = 0
    while i < len(object_list):
        while j < len(object_list[i].follower_list):
            G.add_edge(object_list[i].username, object_list[i].follower_list[j])
            j += 1
            nodes += 1
        j = 0
        i += 1

    # for j in range(len(list_of_objects))

    pos = nx.spring_layout(G)
    figure(figsize=(19.2, 10.8))
    d = dict(G.degree)
    nx.draw(G, pos=pos, node_color='orange', arrowsize=2, width=0.07, with_labels=False,
            node_size=[d[k] * 45 for k in d])
    for node, (x, y) in pos.items():
        text(x, y, node, fontsize=d[node] * 0.15, ha='center', va='center')

    plt.show()

    print("||     " + str(nodes) + " nodes")


if __name__ == '__main__':

    start_time = time.time()

    # Informació d'introducció

    print("||     Big Data, Xarxes Neuronals i Màrqueting: la clau de l'èxit?")
    print("||     Treball de recerca                            ||")
    print("||     Marc Vergés - Escola Pia Mataró               ||")
    print("||                                                   ||")
    print("||     Copyright (c) 2021, Marc Vergés               ||")
    print("||     Tots els drets reservats.                     ||")
    print("||                                                   ||")
    print("||                                                   ||")
    print("||     Algoritmes:                                   ||")
    print("||     1. Mineria de dades                           ||")
    print("||     2. Coincidències                              ||")
    print("||     3. Anàlisi de dades                           ||")
    print("||     4. Proves                                     ||")
    print("||     5. Proves graf                                ||")
    print("||     6. Xarxa Neuronal Artificial                  ||")
    print("||     7. Preferències de seguidor                   ||")
    print("||     8. Visualització del dataset                  ||")
    print("||                                                   ||")
    print("||     Introdueix número:")
    num = int(input())

    # Diferents casos d'algoritmes depenent de la selecció de l'usuari

    if num == 1:
        print("||     Introdueix usuari:")
        user = input()
        browser = webdriver.Chrome()
        login()
        search(user)
        graph(data())
        browser.quit()

    if num == 2:
        print("||     1. Coincidències seguidors:")
        print("||     2. Coincidències seguits:")
        num2 = int(input())
        if num2 == 1:
            print("||     Introdueix usuari 1:")
            user1 = input()
            print("||     Introdueix usuari 2:")
            user2 = input()
            browser = webdriver.Chrome()
            login()
            coincidence_follower(user1, user2)
        else:
            print("||     Introdueix usuari 1:")
            user1 = input()
            print("||     Introdueix usuari 2:")
            user2 = input()
            browser = webdriver.Chrome()
            login()
            coincidence_following(user1, user2)

    if num == 3:
        a = data_adquisition()
        b = matriu_adj(a)
        matriu_inc(graf(a))
        update_values(a, b, in_common(a))
        data_representation(a)

    if num == 4:
        proves()

    if num == 5:
        proves_graf()

    if num == 6:
        print("||     Introdueix usuari de classificació:")
        a = input()
        neural_network(profile_preferences_to_NN(a))

    if num == 7:
        profile_preferences_finder()
    
    if num == 8:
        visualize_data()

    print("--- %s seconds ---" % (time.time() - start_time))