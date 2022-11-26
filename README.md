
# Apache Airflow

## Structuration
- `dags/`  Dossier en synchrone avec notre container, c'est dans ce dossier que les dags seront écrit.
- `logs/` Contient les logs de notre application.
- `plugins/` Contiendra les plugins externes non présente sur l'image docker

```bash
Airflow/
 |-- dags/
 |   |-- custom_class/
 |   |-- data/
 |   | -- | -- input_files/
 |   | -- | -- output_files/
 |-- logs/
 |-- plugins/
```

![Structure](img/structure.PNG)
`requirements.txt` contiendra les dépendances externes dont nous aurons besoins

## Deployment

Pour lancer le projet

```bash
  docker compose-up
```
puis ouvir votre navigateur `localhost:8080`

