from ast import Yield
from audioop import reverse
from cProfile import label
from cgi import test
from datetime import date
from http.client import ImproperConnectionState
from re import T, template
from sqlite3 import Date
from turtle import goto
from urllib import response
from multiprocessing import context
from xml.etree.ElementTree import Comment
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.db import models
from dashboard.models import Comments, Histo
import datetime
from datetime import date
from django.db.models import Avg,Count
from django.db.models.functions import ExtractMonth,ExtractYear



from dashboard.models import Histo
from dashboard.models import Projet

from dashboard.models import Statut
from dashboard.models import Stopgo




def annulation(request):
    stopgo = Stopgo.objects.get(idStopgo = 1)
    stopgo.statutStopgo = "Stop"
    stopgo.save()
    return redirect('../1')

def details(request):
    template = loader.get_template('dashboard/pageDetails.html')
    commentaire = Comments.objects.last()
    context = {
        'commentaire' : commentaire
    }
    return render (request, "dashboard/pageDetails.html", context=context)
    #return HttpResponse(template.render(context, request))

def index(request):
    # return HttpResponse("Page dashboard !")
    statut = Statut.objects.all().get(idStatut = 1).statut #idStatut = 1 => projet o2, rendre dynamique ?
    template = loader.get_template('dashboard_accueil.html')
    context = {
        'statut' : statut
    }
    return HttpResponse(template.render(context, request))

def dashboard(request, id_projet):
    # Si l'utilisateur n'est pas authentifié, ...
    if not request.user.is_authenticated:
        # Je récupère les 10 derniers relevés
        derniers_releves = Histo.objects.all()[:10]
        
        
        # Je récupère le template de l'accueil publique
        template_accueil_public = loader.get_template('home/public.html')

        # Je crée l'objet à injecter dans le template accueil public
        context = {
            "histos": derniers_releves
            
        }
        
        # L'utilisateur est renvoyé vers la page d'accueil publique
        return HttpResponse(template_accueil_public.render(context, request))
    else:
        # Je récupère le projet à afficher
        projet_a_afficher = Projet.objects.get(codePr=id_projet)

        # Je récupère le template accueil dashboard (dans lequel le projet va être affiché)
        template_accueil_dashboard = loader.get_template('dashboard/accueil.html')
        # Je récupère le statut du scraping
        statut = Statut.objects.all().get(idStatut = 1).statut #idStatut = 1 => projet o2, rendre dynamique ?

        # Je crée l'objet à injecter dans le template accueil dashboard
        context = {
            'projet': projet_a_afficher,
            "statut": statut
        }

        # L'utilisateur est renvoyé vers la page d'accueil du dashboard (qui contient le projet à afficher)
        return HttpResponse(template_accueil_dashboard.render(context, request))

def releve(request, id_projet):
    import datetime
    import requests
    from urllib.parse import urlparse
    from urllib.parse import urlunparse
    from bs4 import BeautifulSoup
    import csv 
    from cleantext import clean
    from django.http import HttpResponseRedirect
    #from django.test import Client
    
    import urllib.request
    from urllib.request import Request, urlopen
    from urllib.error import URLError, HTTPError
    

    from dashboard.models import Threads
    from dashboard.models import Comments
    from dashboard.models import Projet
    from dashboard.models import Histo
    from dashboard.models import Statut
    import logging
    
    template_accueil_dashboard = loader.get_template('dashboard/accueil.html')
    projet_a_afficher = Projet.objects.get(codePr=id_projet)
    context = {
            'projet': projet_a_afficher
        }

    #Suppression contenu table Threads et Comments et valeur d'init ???? a faire ou pas????
    #temporaire = Threads.objects.all()
    #temporaire.delete()
    #temporaire2 = Comments.objects.all()
    #temporaire2.delete()
    #return redirect('../1')
    #Il faut ajouter 3 valeurs dans Threads pour la première execution dans une table Threads vide
    
    id_de_thread_a_traitee = 1678
    logging.basicConfig(level=logging.WARNING, filename="script.log", filemode="a",format='%(asctime)s - %(levelname)s - %(message)s')

    def getSoupObject(domain, url_path): # Va sur la page et renvoie son contenu
        thread_url = urlunparse(('https', domain, url_path, "", "", "")) # construct the url to access the posts for each thread
        page = requests.get(thread_url)
        soup = BeautifulSoup(page.content, "html.parser")

        return soup

    def getPostsFromPage(soup, posts_content):# Renvoi le contenu des comm (même un peu plus...)
        thread_results = soup.find_all("div", class_="lia-message-body-content") #Recup des contenu des comm du threads

        for page_posts_content in thread_results:
            body_content = page_posts_content.get_text()   
            #Entrée bdd table Comments
            entreComment = Comments(comment = body_content, threadId_id = der_id_de_thread_plus )
            entreComment.save()
            posts_content.append(body_content)
        return posts_content

    def getNextPageUrl(soup): # Passe à la page de commentaire suivant dans un thread
        # get to next page 
        all_next_page_link_components = soup.find_all("li", class_="lia-paging-page-next")
        if len(all_next_page_link_components) < 2: # case where the thread just have one page to navigate
            return None
        
        next_page_link_component = all_next_page_link_components[1] # second child makes reference to the url we need
        
        if not next_page_link_component: #case where there is just one navigation page
            return None
        
        link = next_page_link_component.find("a")
        if not link: #case were we checked all the navigation pages
            return None
        else:
            next_page_url = link["href"] # get the url for the next page 
        return next_page_url

    def getLienPageSuivante(soup):
        lienPageSuivante = soup.find("li", class_="lia-paging-page-next")
        lienPageSuivante = lienPageSuivante.find("a")
        lienPageSuivante = lienPageSuivante["href"]

        return lienPageSuivante

    def recupInfoThreads(results,threads):
        for thread_title in results:
            first_element = thread_title.find("div") # get first children - the div
            link = first_element.find("a")
            
            title = link["title"] # get the title and save it 
            url = link["href"] # get the link towards the post of the thread 
            threads.append((title, url))
        return threads

    def donnerDate():
        dateLogs = datetime.datetime.now()
        dateLogsDay = dateLogs.strftime('%d')
        dateLogsMonth = dateLogs.strftime('%b')
        dateLogsYear = dateLogs.strftime('%Y')
        dateLogsHour = dateLogs.strftime('%H')
        dateLogsMinute = dateLogs.strftime('%M')
        dateLogsSecond = dateLogs.strftime('%S')
        dateLogsMicrosecond = dateLogs.strftime('%f')

        dateDebut = str(dateLogsDay) + "_" + str(dateLogsMonth) + "_" + str(dateLogsYear) + "_" + str(dateLogsHour) + "_" + str(dateLogsMinute) + "_" + str(dateLogsSecond) + "_" + str(dateLogsMicrosecond)
        return dateDebut

    def nouveauStatutReleve(nouveauSatut): #ajouter id du projet en parametre pour dynamisme
        statut = Statut.objects.all().get(idStatut = 1) #idStatut = 1 => projet o2, rendre dynamique ?
        statut.statut = nouveauSatut
        statut.save()

    def testDeCo(URLe):
        while True:
            req = Request(URLe)
            try:
                response = urlopen(req)
            except HTTPError as e:
                nouveauStatutReleve("Echec")
                print('The server couldn\'t fulfill the request.')
                print('Error code: ', e.code)
                return redirect('../1')
            except URLError as e:
                nouveauStatutReleve("Echec")
                print('We failed to reach a server.(yield)')
                print('Reason: ', e.reason)
                return redirect('../1')
                print("return ne break pas")
            else:
                print ('Website is working fine def')
                return

    

    nbRelThreads = 0
    nbRelCom = 0
    
    #Statut du relevé------
    nouveauStatutReleve("En cours")


    #Création fichiers logs.txt
    dateDebut = donnerDate()
    log = open("logs.txt", "a")
    log.write("\n Début \n" + dateDebut + "\n")


    #Url de la page en cours de scraping
    URL = "https://community.o2.co.uk/t5/Discussions-Feedback/bd-p/4"

    #daemon = Thread(target=testDeCo(URL), daemon=True, name='Monitor')
    #daemon.start()
    #print("test")

    #c = Client()
    #response = c.get(URL)
    #print(response.status_code)

    logTotalPosts = 0

    # Permet threads épinglés scrappé que une fois
    threadsEpinglés = 0 

    der_id_de_thread = (Threads.objects.last()).idThread
    der_id_de_thread_plus = der_id_de_thread + 1
    print(der_id_de_thread_plus)

    x = 0
    derPage = 2 # Valeur 2 permet seulement d'entrer dans la boucle, modifié systematiquement à la suite
    while x < 1 : #Déterminer le nombre de pages à scrapper manuellement #ici derPage à mettre!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        x += 1

        #Aller sur la page -----------------------
        logPageTraitee = "URL de la page qui va être traitée: " + URL
        print(logPageTraitee)

        #log = open("logs.txt", "a") #Entrée dans le log
        log.write(logPageTraitee + "\n")
        #pas .close tte suite...ou si plus simple non ?

        #Vérifier connexion au site essai 1------------------
        #testCo1 = urllib.request.urlopen(URL).getcode()
        #print(testCo1)
        #if testCo1 != 200:
        #    nouveauStatutReleve("Echec!!!!!")
        #    log.write("Code erreur" + str(testCo1))
        #    return redirect('../1')

        #Vérifier connexion au site essai 2--------------------
        #r = requests.head(URL).status_code
        #print(r)


        #Vérifier connexion au site essai 3----------------------

        #---------------------------------------------------------------------------
        #testDeCo(URL)
        req = Request(URL)
        try:
            response = urlopen(req)
        except HTTPError as e:
            nouveauStatutReleve("Echec")
            
            #Entrée dans table Histo
            dateRelev = datetime.datetime.now()
            entreeHisto = Histo(dateRel = dateRelev, nbThreadsRel = 0, nbCommRel = 0, projetId_id = 1, status = False )# Ducoup pas enregistrer dans thread et comm ?
            entreeHisto.save()
            
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', e.code)
            return redirect('../1')
        except URLError as e:
            nouveauStatutReleve("Echec")
            
            #Entrée dans table Histo
            dateRelev = datetime.datetime.now()
            entreeHisto = Histo(dateRel = dateRelev, nbThreadsRel = 0, nbCommRel = 0, projetId_id = 1, status = False )# Ducoup pas enregistrer dans thread et comm ?
            entreeHisto.save()
            
            print('We failed to reach a server.ici')
            print('Reason: ', e.reason)
            return redirect('../1')
        else:
            print ('Website is working fine')
        #---------------------------------------------------------------------------
        

            
        
        domain = urlparse(URL).netloc
        page = requests.get(URL)

        

        #Récup contenu de la page-----------------
        soup = BeautifulSoup(page.content, "html.parser")
        
        li_last_page = soup.find_all("li", class_="lia-paging-page-last")[0].find("a").string
        derPage = int(li_last_page)

        #Récup contenu infos des threads (titre, date, lien,...)
        if threadsEpinglés == 0:
            threadsEpinglés +=1
            results = soup.find_all("article", class_="custom-message-tile") #correspond à touts les posts
        else:
            results = soup.find_all("article", class_="custom-message-tile custom-thread-unread") #correspond seulements aux posts non-épinglé 

        
        #results = soup.find_all("article", class_="custom-message-tile custom-thread-unread")
        
        #Récup des infos threads-------------------------
        threads = [] #Contiendra (title, url) de chaque threads

        # get all threads titles and urls
        threads = recupInfoThreads(results,threads)
        
        #icicicicicicicicicicicicicicicicicciciicciiciiiiiiiiiiiiiiiiccccccccccccccccciiiiiiiiiiiiiiii Entrée BDD Table Threads
        
        print("test"+ str(der_id_de_thread_plus))
        for elt in threads:
            entreeThreads = Threads(nomThread = elt[0], projetId_id = 1 ) #projetId_id ? #ajouter dynamisme id projet non fixe
            entreeThreads.save()

        #Emoji à enlever
        
        
        #Récup de la liste des articles en .txt => variable threads mit dans un .txt
        #liste_des_art = open("liste_des_articles.txt","a") #Attention pas créer seulement ouverts, ajouter create if not exist ?
        #liste_des_art.write(str(threads))
        #liste_des_art.close()

        # get all post content for each thread
        all_thread_posts = [] # Contient tout les threads (et comm?)
        for thread in threads:      
            thread_posts = []
            thread_url_path = thread[1]

            '''
            #---------------------------------------------------------------------------
            #testDeCo(URL)
            req = Request(URL)
            try:
                response = urlopen(req)
            except HTTPError as e:
                nouveauStatutReleve("Echec")
                print('The server couldn\'t fulfill the request.')
                print('Error code: ', e.code)
                return redirect('../1')
            except URLError as e:
                nouveauStatutReleve("Echec")
                print('We failed to reach a server.ici')
                print('Reason: ', e.reason)
                return redirect('../1')
            else:
                print ('Website is working fine')
            #---------------------------------------------------------------------------
            '''

            soupObject = getSoupObject(domain, thread_url_path) # Va sur la page du thread  et renvoie le contenu de la page 

            thread_posts = getPostsFromPage(soupObject, thread_posts) # Renvoi le contenu des comm (même un peu plus...)

            next_page_url = getNextPageUrl(soupObject) # Passe à la page de commentaire suivant dans un thread

            #Récup de tout les comm d'un thread
            while next_page_url:
                
                #Cancel le relevé si user clique sur annuler
                if Stopgo.objects.get(idStopgo=1).statutStopgo == "Stop":
                    #Entrée dans table Statut
                    nouveauStatutReleve("Echec")
                    #Entrée dans table Histo
                    dateRelev = datetime.datetime.now()
                    entreeHisto = Histo(dateRel = dateRelev, nbThreadsRel = nbRelThreads, nbCommRel = nbRelCom, projetId_id = 1, status = False )# Ducoup pas enregistrer dans thread et comm ?
                    entreeHisto.save()
                    #Vérification si données ont été scraped
                    print(der_id_de_thread)
                    print((Threads.objects.last()).idThread)
                    if der_id_de_thread - (Threads.objects.last()).idThread <0: # ou  der_id_de_thread + (Threads.objects.last()).idThread == der_id_de_thread / 2 pour éviter erreur proche de 0. [der_id_de_thread - (Threads.objects.last()).idThread == 0]
                        #La suppression cause un bug au niveau de l'identifiant => les valeurs sont supprimé mais leurs id utilisé ne sont pas reinitialisé => faire une variable = nbDeThreadsScrappedBugOccured qui sera ajouté a der_id_plus au niveau des comms pour éviter le FK introuvé

                        print("entré dans condition 0 ")#ATTENTION => PAS LE RESULTAT ATTENDU MAIS -13 JUSTE AU DESSUS
                        
                    
                        #Suppression des éléments scraped
                        der_id_a_suppr0 = (Threads.objects.last()).idThread
                        id_a_suppr0 = der_id_de_thread + 1
                        id_a_suppr_comms0 = der_id_de_thread + 1
                        
                        #Suppression des Threads
                        while id_a_suppr0 <= der_id_a_suppr0:
                            a_suppr0 = Threads.objects.get(idThread=id_a_suppr0)
                            a_suppr0.delete()
                            id_a_suppr0 += 1
                        
                        #Bouclier anti-bug
                        bouclier = Threads(nomThread = "Bouclier anti-bug", projetId_id = 1)
                        bouclier.save()

                        #Suppression des Comments
                        while id_a_suppr_comms0 <= der_id_a_suppr0:
                            #a_suppr = Comments.objects.all().get(threadId_id = id_a_suppr_comms)
                            #a_suppr.delete()
                            Comments.objects.filter(threadId_id = id_a_suppr_comms0).delete()
                            print(id_a_suppr_comms0)
                            id_a_suppr_comms0 += 1
                        stopgo = Stopgo.objects.get(idStopgo = 1)
                        stopgo.statutStopgo = "Go"
                        stopgo.save() 
                        return


                    

                
                
                
                # get all posts for given a page
                next_page_url_path = urlparse(next_page_url).path

                '''
                #---------------------------------------------------------------------------
                #testDeCo(URL)
                req = Request(URL)
                try:
                    response = urlopen(req)
                except HTTPError as e:
                    nouveauStatutReleve("Echec")
                    print('The server couldn\'t fulfill the request.')
                    print('Error code: ', e.code)
                    return redirect('../1')
                except URLError as e:
                    nouveauStatutReleve("Echec")
                    print('We failed to reach a server.ici')
                    print('Reason: ', e.reason)
                    return redirect('../1')
                else:
                    print ('Website is working fine')
                #---------------------------------------------------------------------------
                '''

                soupObject = getSoupObject(domain, next_page_url_path)
                thread_posts = getPostsFromPage(soupObject, thread_posts)
                next_page_url = getNextPageUrl(soupObject)
            
            id_de_thread_a_traitee += 1

            
            der_id_de_thread_plus += 1

            logNbPosts = f'Nombre de post extrait du thread "{thread[0]}": {len(thread_posts)}' # Logs
            all_thread_posts.append((thread[0], thread_posts)) # adding tuples with the title of a thread and the array containing all the posts content of a thread, pas compris
            
            logTotalPosts += len(thread_posts)

            #logs
            sansEmoji = clean(logNbPosts, no_emoji=True) #Enleve les emoji pour eviter les erreurs
            log.write(sansEmoji + '\n')
            print(sansEmoji)
            
            #Extraction des posts vers un csv
            contenu_des_posts = open("contenu_des_posts.csv","w",encoding="utf-8")
            writer = csv.writer(contenu_des_posts)
            for elements in all_thread_posts:
                writer.writerow(elements)
            contenu_des_posts.close()

            #Extraction vers BDD
        
        logNbThreads = "Nombre de threads scrappé:" + str(len(all_thread_posts))
        nbRelThreads += len(all_thread_posts)
        print(logNbThreads)


        
        #logs
        log.write(logNbThreads + '\n')

        URL = getLienPageSuivante(soup) #Lien vers la page suivante

    dateFin = donnerDate()

    logFin = "\n Fin" + '\n' + 'Scrapping terminé à ' + dateFin  #Afficher le nb de thread et commentaire récoltés

    #logs
    log.write('Total posts scrappé: ' + str(logTotalPosts))
    log.write(logFin)
    print(logFin)
    log.close()
    #fermer logs !!
    
    dateRelev = datetime.datetime.now()
    nbRelCom = str(logTotalPosts)
    
    #Supression des valerus ajouté dans les tables Threads et Comments quand manque de données relevé => Echec------------------------------------------------------------------------
    if nbRelThreads < 9*x: #nbRelThreads à la place de 2 => (test)
        
        #Entrée dans table Histo
        entreeHisto = Histo(dateRel = dateRelev, nbThreadsRel = nbRelThreads, nbCommRel = nbRelCom, projetId_id = 1, status = False )# Ducoup pas enregistrer dans thread et comm ?
        entreeHisto.save()
        #Entrée dans table Statut
        nouveauStatutReleve("Echec")

        #supprimer les entrée liées dans threads et commentaires !!!!!!!!
        repet = ((Threads.objects.last()).idThread) - der_id_de_thread
        repet += 1 #nb de fois que boucle doit s'éxecuter
        
        der_id_a_suppr = (Threads.objects.last()).idThread
        id_a_suppr = der_id_de_thread + 1
        id_a_suppr_comms = der_id_de_thread + 1
        
        #Suppression des Threads
        while id_a_suppr <= der_id_a_suppr:
            a_suppr = Threads.objects.get(idThread=id_a_suppr)
            a_suppr.delete()
            id_a_suppr += 1

        #Suppression des Comments
        while id_a_suppr_comms <= der_id_a_suppr:
            #a_suppr = Comments.objects.all().get(threadId_id = id_a_suppr_comms)
            #a_suppr.delete()
            Comments.objects.filter(threadId_id = id_a_suppr_comms).delete()
            print(id_a_suppr_comms)
            id_a_suppr_comms += 1

        return redirect('../1')
    
    #Supression des données antécedantes car nouvelles données considéré comme bonnes
    else:
        #Suppression des Threads
        first_id_thread = (Threads.objects.first()).idThread
        print("first_id_thread = " + str(first_id_thread))
        id_a_suppr = first_id_thread
        
        while id_a_suppr <= der_id_de_thread:
            if Threads.objects.filter(idThread = id_a_suppr).exists() == False:
                break
            else:
                Threads.objects.get(idThread = id_a_suppr).delete()
                print(id_a_suppr)
                id_a_suppr += 1
        
        #Suppression des Comments
        
        while id_a_suppr <= der_id_de_thread:
            Comments.objects.filter(threadId_id = id_a_suppr).delete()
            print(id_a_suppr)
            id_a_suppr += 1



        entreeHisto = Histo(dateRel = dateRelev, nbThreadsRel = nbRelThreads, nbCommRel = nbRelCom, projetId_id = 1, status = True )
        entreeHisto.save()
        
        # template = loader.get_template('dashboard_accueil.html')
        # return HttpResponse(template.render())
        
        
        nouveauStatutReleve("Terminé le " + str(dateRelev))
        

        if not request.user.is_authenticated:
            return redirect('login')
        #return HttpResponseRedirect(reverse('dashboard', args=(1)))
        #return HttpResponseRedirect(template_accueil_dashboard.render(context, request))
        
        #TestJS 01
        #result, tempfile = js2py.run_file("dashboard\static\script_scrap.js")
        #result = tempfile.actualiser()
        
        return redirect('../1') 
        #return render(request, 'dashboard_accueil.html')
        
        #template = loader.get_template('dashboard_accueil.html')
        #context ={
        #    'statut' : statutReleve,
        #}
        #return HttpResponse(template.render(context, request))
    #ferner logs !!
    # template = loader.get_template('dashboard_accueil.html')
    # return HttpResponse(template.render())




#graph

def pageGraph(request,id_projet):
    
    Histos =Histo.objects.filter(status=1,projetId = id_projet,dateRel__year=2022,dateRel__month__gte=7).annotate(month=ExtractMonth('dateRel'),year=ExtractYear('dateRel')).order_by().values('month','year').annotate(average=Avg('nbThreadsRel'),nbRel=Count('nbThreadsRel')).values('month','year','average','nbRel')
    date=[]
    nbThreads=[]
    nbRel=[]
    print(Histos)
    for Hist in Histos:
        date.append(str(Hist['month'])+"/"+str(Hist['year']))
        nbThreads.append(Hist['average'])
        nbRel.append(Hist['nbRel'])
    context={'dates':date,'nbThreads':nbThreads,'nbRel':nbRel,'idProjet':id_projet}
    print(context) 
    return render(request,'dashboard/pageGraph.html',context = context)

#Historique

def historique(request,id_projet):

    if not request.user.is_authenticated:
        return render(request, 'home/public.html', context= context)

    context = {}
    context["historiques"] = Histo.objects.filter(projetId = id_projet)
    context["idProjet"] = id_projet
    

    return render(request, 'dashboard/historique.html', context = context)
