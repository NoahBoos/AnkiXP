"""
Code source original de Noah Boos.
Ce fichier fait partie du code source d'AnkiXP.

Original source code from Noah Boos.
This file is part of the AnkiXP source code.

GitHub Repo : https://github.com/NoahBoos/AnkiXP.
"""
# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo
# import all of the Qt GUI library
from aqt.qt import *

from anki import hooks
from aqt import gui_hooks

# Système de sauvegarde
import json
configPath = mw.addonManager.addonsFolder() + "\AnkiXP\config.json"

def SaveConfig(data):
    # Accède le fichier "config.json" en écriture seule, le stock dans "f".
    # Écris le fichier "config.json".
    with open(configPath, 'w') as f:
        # Conversion de "data" en objet JSON et le stock dans "f".
        return json.dump(data, f, indent=4)

def LoadConfig():
    # Accède le fichier "config.json" en lecture seule, le stock dans "f".
    # Lis le fichier "config.json".
    with open(configPath, 'r') as f:
        # Retourne le contenu du fichier.
        return json.load(f)

# Initialisation des variables avec les données de l'utilisateur
def GatherConfigData():
    retrievedData = LoadConfig()
    return retrievedData

configData = GatherConfigData()

# Variables
playerLevel = configData['playerLevel']
playerCurrentXP = configData['playerCurrentXP']
playerRequiredXP = configData['playerRequiredXP']

# Variables liées aux gains d'expériences.
expForEasy = configData['expForEasy']
expForMedium = configData['expForMedium']
expForHard = configData['expForHard']
expForMissed = configData['expForMissed']

# Schéma de sauvegarde JSON
savingPattern = {
  "playerLevel": playerLevel,
  "playerCurrentXP": playerCurrentXP,
  "playerRequiredXP": playerRequiredXP,
  "expForEasy": expForEasy,
  "expForMedium": expForMedium,
  "expForHard": expForHard,
  "expForMissed": expForMissed
}

# Sauvegarde les données lors de la fermeture de l'application


# Gain d'expérience
def OnReviewResults(reviewer, card, ease):
    global playerCurrentXP
    global savingPattern
    # Carte facile
    if ease == 4:
        playerCurrentXP = playerCurrentXP + expForEasy
    # Carte moyenne
    elif ease == 3:
        playerCurrentXP = playerCurrentXP + expForMedium
    # Carte complexe
    elif ease == 2:
        playerCurrentXP = playerCurrentXP + expForHard
    # Carte non appris
    elif ease == 1:
        playerCurrentXP = playerCurrentXP + expForMissed
    else:
        playerCurrentXP = playerCurrentXP + 0
    # Vérifie si le joueur peut monter de niveau
    LevelingUp()
    # Actualise le paterne de sauvegarde.
    UpdateSavingPattern()
    # Sauvegarde des données en utilisant un paterne de sauvegarde
    SaveConfig(savingPattern)
# Hooking de la fonction plus haute à "reviewer_did_answer_card".
gui_hooks.reviewer_did_answer_card.append(OnReviewResults)

# Gain de niveau
def LevelingUp():
    global playerLevel
    global playerCurrentXP
    global playerRequiredXP
    global expForEasy
    global expForMedium
    global expForHard
    if playerCurrentXP >= playerRequiredXP:
        while playerCurrentXP >= playerRequiredXP:
            playerLevel = playerLevel + 1
            playerCurrentXP = playerCurrentXP - playerRequiredXP
            playerRequiredXP = playerLevel * 50
            expForEasy = expForEasy + 0.15
            expForMedium = expForMedium + 0.125
            expForHard = expForHard + 0.10

# Affiche l'expérience du joueur ainsi que son niveau.
def ShowXP() -> None:
    showInfo("Niveau : " + str(playerLevel) + "\nXP : " + str(playerCurrentXP) + "/" + str(playerRequiredXP))

# def CreateProgressBar():
#     # Progress bar container widget
#     cwProgressBar = QWidget()
#     # Progress bar widget
#     wProgressBar = QProgressBar(cwProgressBar)
#     wProgressBar.setMinimum(0)
#     wProgressBar.setMaximum(playerRequiredXP)
#     wProgressBar.setValue(playerCurrentXP)
#     # Agencement verticale
#     verticalLayout = QVBoxLayout()
#     verticalLayout.addWidget(wProgressBar)
#     # Application de l'agencement verticale
#     cwProgressBar.setLayout(verticalLayout)
#
#     return cwProgressBar
#
# def AddProgressBarToMainWindow():
#     cwProgressBar = CreateProgressBar()
#
#     mw.mainLayout.addWidget(cwProgressBar)
#
# gui_hooks.profile_did_open.append(AddProgressBarToMainWindow)

action = QAction("Mon profil", mw)
qconnect(action.triggered, ShowXP)
mw.form.menubar.addAction(action)
mw.form.menubar.addAction(action)