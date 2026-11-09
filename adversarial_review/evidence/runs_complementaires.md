# Runs complémentaires — résultats bruts

Environnement : Python 3.12, versions du lock Linux, HiGHS 1.15.1, 4 vCPU. Tous les runs sont des exécutions complètes de la chaîne Snakemake, sauf mention contraire.

## R1 — Run de référence `config/teaser.yaml`

- 19/19 étapes, `real 18m49s` (`user 18m45s` : quasi mono-thread). Day-ahead ≈ 11 min, intraday ≈ 6,5 min, 183 fenêtres de 72 h chacune.
- `resources/convergence/convergence_0.txt` = `Aborted` (max_it = 1). Aucun statut de convergence dans `model_outputs.nc` (73 variables, 6 attributs racine : title, description, target_year, climate_year, created_by, data_source).
- Prix max DA : 4 510 €/MWh (N2, N3) ; prix max ID : 4 510 €/MWh. Délestage DA 2,2 GWh, ID 5,9 GWh (N2). Statut d'engagement fractionnaire : 5,3 % des (heure, unité).
- `ramping_shortfall_*` = 0,0 partout, avec attribut « (disabled) ».

## R2 — Réplique indépendante (`runs/teaser_replica`), mêmes entrées et configuration

- **73/73 variables de `model_outputs.nc` identiques bit à bit.** Prix DA : écart max 0,0. → **Reproductibilité déterministe confirmée** sur la même machine et le même environnement. Non testé : autre OS, autre nombre de threads, autre version du solveur.

## R3 — Année cible bissextile 2028 (données teaser inchangées, `ty: [2028]`)

- Le run aboutit (19/19), mais :
  - les sorties horaires comptent **8 784 heures** pour 8 760 snapshots : 24 heures **NaN** (heures 1 417-1 440, le 29 février fictif) ajoutées par la jointure externe de `consolidate_flexibility_indicators.py` ;
  - `daily_flexibility_need` compte **366 jours**, dont un jour 60 **à besoin nul** (jour fantôme qui biaise toute statistique journalière : moyenne, minimum, percentiles) ;
  - le besoin **hebdomadaire** change avec la seule étiquette de l'année cible, pour des données physiques identiques : N1 39,653 TWh (TY 2028) contre 40,729 TWh (TY 2030), **−2,6 %** ; N2 −0,7 % ; N3 +2,2 %. Cause : `ts.replace(year=TY)` replace les données de l'année climatique 2013 sur le calendrier de l'année cible sans aligner les jours de la semaine (1/1/2013 = mardi, 1/1/2028 = samedi). Le cycle hebdomadaire de la demande est donc découpé selon des semaines décalées. S'y ajoute l'effet des semaines ISO (F-02).
  - Besoins journalier et saisonnier, et P99,9 : inchangés.

## R4 — Année climatique bissextile 2016 (8 784 h, 29 février = copie du 28)

- `build_base_network` : **accepté**, le réseau conserve le 29 février (8 784 snapshots), contrairement aux commentaires du code (« n.snapshots … always leap-day-free »).
- `run_day_ahead` : **échec** :
  `plan_maintenance.py:505` → `Timestamp.replace(year=…)` → `ValueError: day is out of range for month`.
- Note : un premier essai a échoué plus tôt (`Length mismatch: Expected 8760 rows, received 8784`) parce que nos CSV vides de séries de liens et de stockage avaient gardé 8 760 lignes. Artefact de notre préparation, corrigé : il n'est pas imputé au modèle.

## R5 — Jeux d'entrée corrompus (build des réseaux de base uniquement)

| Jeu | Injection | Issue de `build_base_network` | Constat dans le réseau produit |
|---|---|---|---|
| M1 | `N3_load` retirée du CSV de prévision | succès, sans avertissement | DA : `loads_t.p_set` = [N1, N2] ; demande moyenne N3 = **0 MW** (au lieu de 15 000) |
| M2 | p_max_pu NaN ×100, 1,5 ×100, −0,3 ×100 | succès | 100 NaN conservés ; max 1,0, min 0,0 (écrêtage silencieux) |
| M3 | charge −50 000, NaN ×10, 10⁹ | succès | NaN ×10, min −50 000, max 1e9 conservés |
| M4 | prévisions décalées de 12 h | succès | alignement par position, aucun contrôle |
| M5 | p_min_pu 1,2 ; capital_cost < 0 | **échec (pandera)** | rejet correct |
| M5' | rendements de stockage 1,4/1,5 ; max_hours −2 | **échec (pandera)** | rejet correct |
| M6 | rendement 3,0 ; coût marginal −500 ; taux de panne 1,7 ; p_nom de lien −4 000 | succès | valeurs conservées telles quelles |

Comportement du solveur face aux NaN (réseau PyPSA à un nœud, HiGHS) :

```
{}               optimal  solaire 50/50/50, gaz 50/50/50
{'load_nan'}     optimal  heure 2 : solaire 0, gaz 0      -> la demande disparaît
{'pu_nan'}       optimal  heure 2 : solaire 100 (= p_nom) -> la borne p_max_pu disparaît
```

## R6 — Prévisions synthétiques (mode `noise`, valeur par défaut du modèle)

Voir `short_term_experiments.txt` : corrélation des erreurs de charge entre zones = 1,0 ; corrélation erreur de charge / erreur éolienne = 0,647 ; P99,9 N1 = 5 042 MW (contre 11 665 MW avec les prévisions CSV du teaser).

## R7 — Suite d'intégration du modèle sur R1

Voir `integration_test_report_teaser.txt` : **FAILED** (SOC du réservoir N3 à −10,5 % de la cible ; 7 612 violations « ID dispatch within DA commitment » sur N1 Gas, porteur pourtant libre de se ré-engager en ID ; cohérence prix-flux OK).
