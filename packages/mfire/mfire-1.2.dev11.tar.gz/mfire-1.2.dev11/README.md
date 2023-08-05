# MFire [![](docs/images/logo_mf.jpg)](www.meteofrance.com) [![](docs/images/logo_promethee.png)](http://confluence.meteo.fr/display/PROM/Accueil+PROMETHEE)
------

**Status (develop branch)**

[![Lignes de code](http://sonar.meteo.fr/api/project_badges/measure?project=deep_learning%3Aftap_autom&metric=ncloc)](http://sonar.meteo.fr/dashboard?id=deep_learning%3Aftap_autom) [![Maintenabilité Sonar](http://sonar.meteo.fr/api/project_badges/measure?project=deep_learning%3Aftap_autom&metric=sqale_rating)](http://sonar.meteo.fr/dashboard?id=deep_learning%3Aftap_autom) [![Fiabilité Sonar](http://sonar.meteo.fr/api/project_badges/measure?project=deep_learning%3Aftap_autom&metric=reliability_rating)](http://sonar.meteo.fr/dashboard?id=deep_learning%3Aftap_autom) [![Sécurité Sonar](http://sonar.meteo.fr/api/project_badges/measure?project=deep_learning%3Aftap_autom&metric=security_rating)](http://sonar.meteo.fr/dashboard?id=deep_learning%3Aftap_autom) [![coverage report](http://gitlab.meteo.fr/deep_learning/automatisation/ftap_autom/badges/develop/coverage.svg)](http://gitlab.meteo.fr/deep_learning/automatisation/ftap_autom/-/commits/develop) [![Maintenabilité MF](https://maintenabilite.cloudmf.dev/badge/{03214ee2-28cf-4fa4-bfbe-ca8f96e9c796}?cloudmf_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6Im1hcnR5ZiIsInVpZF9udW1iZXIiOjEwMzE4LCJlbWFpbCI6ImZhYmllbi5tYXJ0eUBtZXRlby5mciIsImRpc3BsYXlfbmFtZSI6Ik1BUlRZIEZhYmllbiIsImlhdCI6MTYzNzkxNzM5MiwiZXhwIjo0NzkxNTE3MzkyLCJsaW1pdF90b192aG9zdHMiOlsibWFpbnRlbmFiaWxpdGUiXSwibGltaXRfdG9fdXJpcyI6WyIvYmFkZ2UvKiIsIi9wcm9qZWN0X2JhZGdlLyoiLCIvbGV0dGVyX2JhZGdlLyoiXX0.5UoNfmaCh8JvPrPv4QFYC9VmhJ-I_fg8WjEA2mBXrLs)](https://maintenabilite.cloudmf.dev/dashboards/repository)

[![pipeline status](http://gitlab.meteo.fr/deep_learning/automatisation/ftap_autom/badges/develop/pipeline.svg)](http://gitlab.meteo.fr/deep_learning/automatisation/ftap_autom/-/commits/develop)


## Qu'est-ce-que Prométhée ?
**Prométhée** est un projet visant à automatiser la production de bulletins météorologiques. Ce projet se matérialise par une chaîne de traitement complexe allant de la configuration de bulletin sur Métronome, le traitement des données et la production des composants de bulletin sur super-calculateur, la mise à disposition de ces composants dans un service d'accès (CDP), et enfin l'assemblage de bulletins sur Métronome.

## Qu'est-ce-que MFire ?
**MFire** est la librairie Python créée dans le cadre du projet Prométhée permettant de produire des composants de bulletin météo. Même si cete librairie est développée dans l'idée d'être déployée et utilisée sur super-calculateur, elle est parfaitement utilisable sur toute machine disposant des dépendances requises. 

## Installation
L'installation se fait par le dépôt Python standard de Météo-France : le [Nexus](http://nexm01-sidev.meteo.fr/#browse/search/pypi) ([documentation du Nexus](http://confluence.meteo.fr/display/MOT/Nexus+-+Guide+d%27utilisation#NexusGuided'utilisation-R%C3%A9cup%C3%A9rerunpaquetpythonavecpip))

```sh
pip install --index-url http://nexm01-sidev.meteo.fr/repository/pypi-releases-mfire/simple --trusted-host nexm01-sidev.meteo.fr mfire
```

## Dépendances
Les dépendances sont les suivantes :
```
name: mfire-env
channels:
  - conda-forge
  - anaconda
  - defaults
dependencies:
  - python=3.7.3
  - bottleneck=1.3.2
  - cfgrib=0.9.8.2
  - dask=2.30.0
  - eccodes=2.17.0
  - geojson=2.5.0
  - netcdf4=1.5.3
  - numpy=1.19.1
  - pandas=1.1.3
  - pillow=8.0.0
  - pint=0.16.1
  - pydantic=1.7.3
  - shapely=1.7.1
  - xarray=0.16.1
  - xlrd=1.2.0
  - pip:
    - mflog==0.1.0
    - baseconvert==1.0.0a4
```

**Note :** Il est recommandé d'installer ces dépendances dans un environnement [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) en utilisant ce fichier [environment.yml](envs/prod.yml) et grâce à la commande `conda env create -f environment.yml`.

## Installation en développement
Pour une utilisation en développement, il vous faut :
1. une installation de conda ([Miniconda](https://docs.conda.io/en/latest/miniconda.html) par exemple) ;
2. la commande [make](https://man7.org/linux/man-pages/man1/make.1.html) ;
3. cloner ce dépôt git ;
4. une fois dans le dossier `mfire`, exécuter :

```
make install
```

Voir la documentation complète d'[installation en développement](docs/100-dev-installation-guide.md)

## Documentation
Voir la documentation d'[utilisation](docs/200-usage.md)

## Contribuer à MFire
Voir le [guide de contribution](docs/900-contributing.md)

## Licence
[Licence](LICENSE.md)

------

[![Météo-France](docs/images/logo_mf.jpg)](www.meteofrance.com) [![Prométhée](docs/images/logo_promethee.png)](http://confluence.meteo.fr/display/PROM/Accueil+PROMETHEE)
