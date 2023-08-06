# zpp-config
## Informations
Librairie pour l'utilisation et la modification de fichier de configuration:<br>
- Charger un ou plusieurs paramètres
- Modifier un paramètre existant
- Ajout un paramètre ou une section
- Supprimer un paramètre ou une section
- Lister les sections disponibles
- Lister les paramètres et/ou sections désactivés

Prends en compte les paramètres commentés.<br>
Compatible avec les fichiers de configuration indentés.<br><br>
Traduit les paramètres pour les types str, int, float, bool, list, dict

### Prérequis
- Python 3
<br>

# Installation
```console
pip install zpp_config
```

# Utilisation
### Conseil d'importation du module
```python
from zpp_config import Config
```

<br>

### Exemple de fichier de config
```xml
[section]
	value1 = key1
	value2 = key2
	value3 = key3

[section2]
	value1 = key1
	value2 = key2
	value3 = key3
```

<br>

### Initialisaton d'un fichier de configuration
```python
c = Config("conf.ini")
```
>En paramètre supplémentaire, nous pouvons mettre:<br/>
>- separator: Définir le séparateur entre la clé et la valeur dans le fichier. (Par défaut: " = ") 
>- escape_line: Définir le caractère utilisé pour commenter une valeur ou une section. (Par défaut: "#")
>- auto_create: Créer le fichier de configuration s'il n'existe pas. (Par défaut: "False")
>- read_only: Ouvrir le fichier de configuration en lecture seule. (Par défaut: "False")

<br>

### Chargement de paramètre

La fonction renvoie la valeur si un unique paramètre a été trouvé, sinon renvoie un dictionnaire avec les différentes valeurs trouvées (classé par section)
Renvoie un tableau vide si aucun paramètre n'a été trouvé

#### Chargement de tous les paramètres
```python
data = c.load()
```
#### Chargement d'une section du fichier
```python
data = c.load(section='section_name')
```
#### Chargement d'une valeur dans tout le fichier
```python
data = c.load(val='value_name')
```
#### Chargement d'une valeur dans une section spécifique
```python
data = c.load(val='value_name', section='section_name')
```

<br>

### Changement de paramètre
#### Changement d'une valeur dans tout le fichier
```python
c.change(val='value_name', key='key_value')
```

#### Changement d'une valeur dans une section spécifique
```python
c.change(val='value_name', key='key_value', section='section_name')
```

<br>

### Ajout de paramètre ou de section

Ajoute une section ou un paramètre dans le fichier de configuration.
Dans le cas de l'ajout d'un paramètre, rajoute la section si elle n'existe pas.

#### Ajout d'une section
```python
c.add(section='section_name')
```

#### Ajout d'un paramètre dans une section
```python
c.add(val='value_name', key='key_value', section='section_name')
```
> Si aucune section est défini, rajoute le paramètre en dehors des sections.

<br>

### Suppression de paramètre ou de section

#### Suppression d'une section
```python
c.delete(section='section_name')
```

#### Suppression d'un paramètre dans une section
```python
c.delete(val='value_name', section='section_name')
```
> Si aucune section est défini, recherche le paramètre en dehors des sections.

<br>

### Liste des paramètres non pris en compte

Retourne la liste des paramètres qui sont non pris en compte dans le fichier de configuration.

```python
data = c.disabled_line()
```
> Possibilité de préciser la section en utilisant le paramètre section

<br>

### Liste les sections disponibles
```python
data = c.list_section()
```