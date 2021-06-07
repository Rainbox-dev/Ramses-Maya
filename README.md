# Ramses-Maya
 The Rx Asset Management System (Ramses) Maya Plugin

## Install

- [Download](https://github.com/Rainbox-dev/Ramses-Maya/archive/refs/heads/main.zip) and unzip the module
- (while the add-on is in development, you also need to manually include the [*ramses*](https://github.com/Rainbox-dev/Ramses-Py) python module in the plug-ins folder)
- Edit `Ramses.mod` with a text editor, and replace the path in the first line with the path where you've unzipped the module.
- Copy `Ramses.mod` in one of your modules paths  
    e.g. `C:\Users\User\Documents\Maya\modules`.  
    You may need to create the *modules* folder if it does not exist yet
- Restart *Maya*.


## TODO

### Ramses

- [ ] *WIP* à chaque step, il y a un fichier de travail template vide, ramses le renomme et le place à la création de l'asset/shot

### Grouper les assets

- [x] CHARACTERS (chars)
- [x] PROPS
- [x] ITEMS (assets)
- [x] SETS (correspond aux publish stages)

-> Asset groups dans Ramses

et possibilité d'en ajouter

### Les Steps

#### Asset steps

- [x] Mode
  - [x] Publish abc
  - [x] ajouter publish .mb pour les viewport shaders (cf publish setup actuel)
- [ ] Setup
  - [x] Import modé
  - [x] Update modé
  - [ ] Publish .ma ou .mb
- [ ] Shading
  - [x] Import modé
  - [x] Update modé
  - [ ] Publish .mb

#### Shots steps

- [ ] Layout
  - [ ] Publish .mb
  - [ ] Publish .abc (gpu cache)
- [ ] Animation
  - [ ] Import/update abc du layout
  - [ ] Import/update les chars et props
  - [ ] Publish .abc (sans oublier la caméra)
  - [ ] Ajouter optionnellement l'anim des crease
- [x] FX, Rien pour l'instant
- [ ] Lighting
  - [ ] Import/update Le layout, vire tout ce qui a été baké/publish en abc
  - [ ] Import/update les abc
  - [ ] Import/update les shaders et les assigne : depuis les items et depuis les charas, etc
  - [ ] Publish Rendu exr
- [ ] Compositing
  - [ ] Import/update les exr, eventuelle prépare un arbre, etc
  - [ ] Publish Rendu exr ou png

### Divers
