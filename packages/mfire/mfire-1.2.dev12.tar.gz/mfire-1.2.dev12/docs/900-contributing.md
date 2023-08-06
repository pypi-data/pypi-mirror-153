# Guide de contribution

## Numéros de versions

### Schéma de version

Afin de respecter la PEP440, les versions publiques de la librarie doivent suivre le schéma suivant:

```txt
N.N[.devN][rcN][.postN]
```

Avec:

- `N.N` : le segment de release final, avec le premier `N` représentant la version majeure et le second `N` représentant la version mineure (e.g. `1.2` comme version finale);
- `[.devN]` : le segment optionnel de developpement (e.g. `1.2.dev14` pour une version de dev de la version finale `1.2`);
- `[rcN]` : le segment optionnel de pre-release (e.g. `1.2rc0` pour une pre-release de la version finale `1.2`);
- `[.postN]` : le segment optionnel de post-release (e.g. `1.2.post3` pour une post-release de la version finale `1.2`);

Exemple de numérotation successive de versions:

```txt
0.9
1.0.dev1
1.0.dev2
1.0.dev3
1.0.dev4
1.0rc1
1.0rc2
1.0
1.0.post1
1.1.dev1
...
```

### Utilitaire de versionnage semi-auto

Il y a le script `tools/version.py` qui permet de gérer le numéro de version.

#### check

La commande suivante permet de vérifier la cohérence de la version avec le status de la branche
passée en argument:

```sh
./tools/version.py check [-s {develop,pre-release,release,post}]
```

#### diff

La commande suivante permet de vérifier si la version actuelle est bien différente de la version installée sur pip (à utiliser avant un upload vers Pypi):

```sh
./tools/version.py diff
```

#### update

La commande suivante permet de mettre à jour la version en respectant le schéma de version. Il est possible de lui passer en argument le nouveau status de la branche.

```sh
./tools/version.py update [-s {develop,pre-release,release,post}]
```

On peut imaginer obtenir l'exemple de numérotation précédent grâce aux commandes précédentes:

```console
$ ./tools/version.py update -s develop
Previous version : 0.9
Will the next release a major one ?
Y: 1.0.dev1
n: 0.10.dev1
Y
Major version change chosen.
Do you confirm version change : '0.9' -> '1.0.dev1' ? [Y/n]
Y
New version '1.0.dev1' confirmed

$ ./tools/version.py update
Previous version : 1.0.dev1
Do you confirm version change : '1.0.dev1' -> '1.0.dev2' ? [Y/n]
Y
New version '1.0.dev2' confirmed

$ ...
$ ...
$ ./tools/version.py update -s pre-release
Previous version : 1.0.dev4
Do you confirm version change : '1.0.dev4' -> '1.0rc1' ? [Y/n]
Y
New version '1.0rc1' confirmed

$ ./tools/version.py update
Previous version : 1.0rc1
Do you confirm version change : '1.0rc1' -> '1.0rc2' ? [Y/n]
Y
New version '1.0rc2' confirmed

$ ./tools/version.py update -s release
Previous version : 1.0rc2
Do you confirm version change : '1.0rc2' -> '1.0' ? [Y/n]
Y
New version '1.0' confirmed

$ ...
```

Schéma du graphe d'états pour respecter le schéma de version:

![versions_states](images/versions.jpg)
