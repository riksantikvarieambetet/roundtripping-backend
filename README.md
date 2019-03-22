# Roundripping backend

The Swedish National Heritage Board researches and develops a prototype tool to provide improved metadata (translations, data additions...) from Wikimedia Commons back to the source institution. This project runs from November 2018 to June 2019. This repository is a part of the roundtripping research and development project. [Read more about the project.](https://meta.wikimedia.org/wiki/Wikimedia_Commons_Data_Roundtripping)

## Setup and Development

```bash
git clone https://github.com/riksantikvarieambetet/roundtripping-backend.git
cd roundtripping-backend
pipenv install

# start application
cd src && pipenv run python app.py
```

## Deploy

The following applies to the deployment on Tool Forge (Stretch).
Note: Make sure that requirements.txt is in sync with pipenv.

```bash
become roundtripping
webservice --backend=kubernetes python stop
cd www/python
git pull
cd ../..
webservice --backend=kubernetes python shell
source $HOME/www/python/venv/bin/activate
pip install -r $HOME/www/python/requirements.txt
exit
webservice --backend=kubernetes python start
```
