# Lecture automatique de facture 
## Projet de 4ème année - ESME Sudria
Les membres de l'équipe:
* Camille BAYON DE NOYER, 
* Sonia MOGHRAOUI, 
* Maëlle MARCELIN

Durée du projet : 3 mois

> Le contexte:  
> 
> On se place dans la perspective d’une boîte de conseil qui essaye de diversifier son offre d’extraction de texte à partir d’images. En particulier, le client cherche un système capable d’extraire les frais totaux à partir de factures. 
> 
> Le client ne veut pas nous donner de données de facture pour des raisons réglementaires. En conséquence, nous allons devoir construire un système d’extraction de texte à partir d’images à partir de photos de reçus de paiement.
> 
> Notre objectif est donc de pouvoir extraire le total de factures à partir de photos de reçus de paiement.

Nos objectifs:
*	Traitement des images
*	Lecture des textes et reconnaissance du total
*	Déploiement de notre solution en site web

## Sommaire
1. [Démonstration](#demo)
2. [OCR utilisé](#ocr)
3. [Librairies principales utilisées](#lib)
4. [Précision](#accuracy)


## Démonstration <a name="demo"></a>
![Image text](/asset/git/interfaceGIF.gif)

## OCR utilisé <a name="ocr"></a>
Pyteserract et PaddleOCR

## Librairies principales utilisées <a name="lib"></a>
1. traitement d'image: openCV
2. interface: dash

## Précision <a name="accuracy"></a>
Notre précision est de 79,5% pour le jeu de données dataset et 84,61% pour le jeu de données data


<hr>
