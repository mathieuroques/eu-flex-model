# Adversarial review de l'outil EU-Flex (ACER) — Rapport

*Équipe simulée : red team, experts réglementaires européens, ingénieurs logiciels seniors.*
*Objet : dépôt `eu-flex-model` v1.0.0-rc2 (commit `65cb449`), version préliminaire publiée pour la consultation publique ACER (5 novembre – 17 décembre 2026).*
*Date : 9 novembre 2026. Dossier de contexte (phase 1) : [`01_dossier_contexte_recherche.md`](01_dossier_contexte_recherche.md).*

---

## 0. Synthèse exécutive

EU-Flex est une chaîne Snakemake/PyPSA d'environ 41 000 lignes. Elle simule les marchés day-ahead et infrajournalier en horizon glissant, fait évoluer le parc par une EVA, puis calcule les indicateurs de besoins de flexibilité de la méthodologie FNA (Décision ACER 05/2025). La chaîne **s'installe et s'exécute de bout en bout** sur le cas « teaser » (3 nœuds, 1 an, 19 min). Les indicateurs **arithmétiquement simples** (besoin journalier, besoin saisonnier, rampe maximale, percentiles d'erreur de prévision) sont **exacts** : nous les avons recalculés indépendamment à partir des CSV d'entrée et retrouvé les valeurs du modèle à l'unité près.

En revanche, **l'outil ne remplit pas aujourd'hui son objectif réglementaire** : produire, à l'échelle de l'UE, des besoins de flexibilité conformes à la FNAM et attribuables aux technologies. Les causes sont des défauts démontrés par exécution :

1. **Les contributions par technologie ne bouclent pas.** Sur le cas teaser, leur somme vaut 6 %, −19 % et 9 % du besoin journalier selon la zone, parce que l'EnR est comptée deux fois. Le notebook qui produit les figures du papier ACER masque l'écart par une variable résiduelle étiquetée « RES » ou « Curtailment » (F-03).
2. **Le stockage fictif (« dummy storage ») est sans pertes par construction**, alors que la FNAM 8(10) exige un rendement aller-retour représentatif pour chaque ratio énergie/puissance. Son coût de 1 000 €/MW/an est arbitraire et ne dépend pas de la durée. La cible est imposée année climatique par année climatique, alors que la FNAM la demande en moyenne sur les années climatiques (F-06).
3. **Les erreurs de prévision par défaut sont un bruit synthétique codé en dur**, non dérivé de données historiques comme l'exige la FNAM 10(1). La graine est fixe, les erreurs de charge sont corrélées à 1,00 entre zones et à 0,65 avec l'erreur éolienne. Le P99,9 change d'un facteur 2 selon la source de prévision (F-08).
4. **La méthode probabiliste de court terme exclut de la marge le stockage, l'effacement implicite, l'EnR et les interconnexions**, contrairement à la FNAM 10(2). Résultat : la zone hydraulique N3 est déclarée « non couverte » 8 760 heures sur 8 760, contre 360 heures en tenant compte de la seule puissance de stockage disponible (F-09).
5. **Les séries temporelles d'entrée ne sont pas validées.** Une colonne de prévision manquante supprime silencieusement 15 GW de demande day-ahead, une charge NaN fait disparaître la demande de l'heure, un p_max_pu NaN lève la borne de production (F-07).
6. **L'EVA peut ne jamais converger, ou déclarer une convergence fausse**, et ce statut n'est pas reporté dans les résultats (F-11). **Le plafond de prix (HMMCP) est inopérant** sur les données teaser (F-10).
7. **Une année climatique bissextile fait planter la chaîne** (F-05). Or l'ERAA utilise 36 années climatiques, dont 9 bissextiles.
8. **La suite d'intégration livrée échoue sur le cas de référence** (7 612 violations) et n'est pas exécutée par défaut. Il n'y a ni test unitaire ni CI publique (F-13).

**Verdict : NON APTE à un usage opérationnel en l'état** (détail en §5). L'outil est **apte à son usage déclaré de version de consultation**, à condition que les points ci-dessus soient traités avant l'évaluation de juillet 2027.

---

## 1. Périmètre, méthode et reproductibilité de l'audit

### 1.1 Ce qui a été fait

| Axe | Travaux |
|---|---|
| Statique | Lecture du code critique : `calculate_model_outputs.py`, `compute_npv.py`, `update_capacity.py`, `update_price_cap.py`, `build_base_network.py`, `run_dummy_storage_optimization.py`, `run_integration_tests.py`, règles Snakemake. Lecture de la spécification (équations rendues en image, p. 92-109), du manuel et du notebook |
| Exécution | Run complet du teaser (`config/teaser.yaml`) ; exécution de la suite d'intégration du modèle ; réplique pour la reproductibilité ; runs « année cible bissextile 2028 » et « année climatique bissextile 2016 » ; construction des réseaux en mode prévisions synthétiques. **Non exécutés** (coût de calcul) : le run EVA à 30 itérations (`teaser-eva.yaml`, plusieurs heures) et les 2 × 63 optimisations *dummy storage* ; ces volets sont évalués par lecture du code et par tests unitaires sur les fonctions de production |
| Recalcul indépendant | `adversarial_review/scripts/independent_recompute.py` : besoins FNAM 8(5), percentiles FNAM 10(1) et rampes, recalculés depuis les CSV bruts |
| Tests adversariaux unitaires | `adversarial_review/tests/test_indicator_adversarial.py` : réseaux synthétiques à solution analytique connue (11 tests ; chaque échec documente un défaut) |
| Injection de données aberrantes | 7 jeux corrompus (M1-M6, bissextiles) passés à `build_base_network` ; comportement du solveur face aux NaN vérifié sur un réseau PyPSA minimal |
| Réglementaire | Confrontation article par article avec la FNAM (Décision 05/2025, annexe I consolidée), l'article 19e du règlement 2019/943 et la méthodologie HMMCP |

### 1.2 Environnement

Python 3.12 et les versions du lock Linux (PyPSA 0.33.2, linopy 0.7.0, HiGHS 1.15.1, pandas 2.2.3, numpy 2.4.6, xarray 2026.2.0, snakemake 9.16.3), installés avec `uv` (conda n'était pas disponible dans le conteneur). Machine : 4 vCPU, 15 Go de RAM.

### 1.3 Reproduire

```bash
pip install -e . pytest
snakemake -c 4 --configfile config/teaser.yaml --directory runs/teaser          # ~19 min
python -m pytest adversarial_review/tests/test_indicator_adversarial.py -v      # ~20 s, sans solveur
python adversarial_review/scripts/independent_recompute.py runs/teaser
snakemake -c1 --configfile config/teaser.yaml --directory runs/teaser -- \
    resources/integration_tests/test_results_2030_2013_fo1_0.json               # suite du modèle
```

Résultat de la suite adversariale : **11 tests, 11 échecs**. Chaque échec est un défaut confirmé (F-01, F-02, F-03, F-04, F-05, F-05b, F-10, F-11a, F-11b, F-11c). Les sorties brutes sont dans `adversarial_review/evidence/`.

---

## 2. Tableau des findings hiérarchisés

Criticité : **C** = critique (invalide un résultat réglementaire ou rend l'outil inapte) ; **E** = élevée (biais significatif ou perte de confiance majeure) ; **M** = moyenne ; **F** = faible.

| ID | Titre | Domaine | Crit. | Preuve |
|---|---|---|---|---|
| F-03 | Contributions par technologie non bouclées, EnR comptée deux fois, écart masqué par un résidu dans les figures | Logique métier | **C** | Exécution + test |
| F-06 | *Dummy storage* sans pertes (contraire à FNAM 8(10)), coût arbitraire, cible par année climatique | Conformité / algorithme | **C** | Code + spec |
| F-08 | Erreurs de prévision par défaut synthétiques, codées en dur, corrélées artificiellement | Conformité / données | **C** | Exécution |
| F-09 | Méthode probabiliste : marges sans stockage, iDSR, EnR ni interconnexions, FRR déduite | Conformité / algorithme | **E** | Exécution |
| F-07 | Séries temporelles non validées : pertes de demande silencieuses, NaN, alignement par position | Robustesse / données | **E** | Exécution |
| F-05 | Années bissextiles : plantage pour une année climatique bissextile, index horaire troué pour une année cible bissextile | Robustesse | **E** | Exécution + test |
| F-11 | EVA : convergence inatteignable, fausse convergence, oscillation à pas fixe ; statut absent des sorties | Algorithme / économie | **E** | Tests + run |
| F-10 | Plafond de prix inopérant : coûts de délestage ≠ plafond, réécriture ex post limitée aux prix égaux au plafond | Économie / conformité | **E** | Exécution + test |
| F-12 | Rampes : FNAM 9 très partiellement couverte ; déficit de rampe désactivé mais publié à 0,0 | Conformité / restitution | **E** | Exécution |
| F-13 | Assurance qualité : suite d'intégration en échec sur le cas de référence, hors DAG, ni tests unitaires ni CI | Ingénierie | **E** | Exécution |
| F-02 | Semaines ISO : 30-31 décembre fusionnés avec la semaine 1 de janvier (+3,4 % sur le besoin hebdomadaire de N1) | Calcul | **M** | Exécution + test |
| F-14 | UC linéarisé : statut fractionnaire 5,3 % du temps, prix = duales d'une relaxation, aucun étalonnage contre un MILP | Algorithme | **M** | Exécution |
| F-15 | Monte-Carlo dégénéré (1 tirage, graines fixes), aucun intervalle de confiance malgré la spécification | Statistique | **M** | Config + code |
| F-01 | Cache du calcul de charge résiduelle indépendant des séries temporelles (collision DA/ID latente) | Calcul | **M** | Test |
| F-16 | Revenus de réserve mis silencieusement à 0 en cas de désalignement des séries (repli « même ordre ») | Économie | **M** | Code |
| F-17 | Traçabilité : 2 commits, export d'une plateforme privée, modules non importables hors Snakemake, variable globale indéfinie | Ingénierie / gouvernance | **M** | Code |
| F-18 | Passage à l'échelle : 19 min pour 3 nœuds et 1 année ; extrapolation de l'ordre de 10⁴-10⁵ CPU·h pour le périmètre UE | Architecture | **M** (structurel) | Mesure + extrapolation |
| F-04 | Unités erronées (MWh au lieu de MW) sur la rampe, les percentiles et les besoins non couverts | Restitution | **F** | Exécution |
| F-19 | Nomenclature décalée par rapport à la FNAM (« daily » d'EU-Flex = indicateur « horaire » FNAM 8(5)(a), etc.) | Conformité / restitution | **F** | Spec |

---

## 3. Findings détaillés

### F-03 — Les contributions par technologie ne décomposent pas le besoin qu'elles prétendent décomposer · **Critique**

**Constat.** `calculate_technology_contributions` (`calculate_model_outputs.py:1591`) applique l'équation 13.8 à **tous** les générateurs et stockages, y compris le solaire et l'éolien, à partir de `statistics.energy_balance`. Or la charge résiduelle (éq. 13.1) est déjà nette du **potentiel** EnR. La variabilité EnR est donc comptée deux fois : une fois dans le besoin, une fois en contribution négative. La part écrêtée de l'EnR n'est, elle, attribuée à personne.

**Preuve (exécution, teaser, `runs/teaser/results/assessment/model_outputs.nc`).**

| Zone | Besoin journalier (TWh) | Σ contributions stockées (TWh) | dont EnR (TWh) | Σ / besoin |
|---|---|---|---|---|
| N1 | 27,76 | 1,78 | −21,86 | **0,064** |
| N2 | 36,79 | −6,83 | −37,66 | **−0,186** |
| N3 | 13,97 | 1,33 | −12,64 | **0,095** |

Même chose en hebdomadaire (0,03 / 0,57 / 0,79) et en saisonnier (−0,05 / 0,63 / 0,64). Le test synthétique `test_F03_contributions_sum_to_need` (une zone, sans échanges ni écrêtement, le gaz suit exactement la charge résiduelle) reproduit le défaut : contribution du gaz = besoin (exact), contribution du solaire = −3,09 TWh, somme = 25 % du besoin.

**Aggravant.** Le notebook `notebooks/teaser_case_analysis.ipynb`, présenté comme source des figures 9 à 18 du papier ACER, retire à la main « Solar (PV) » et « Wind Onshore » (cellules 20 et 24, noms codés en dur : l'éolien en mer et le fil de l'eau ne seraient pas retirés sur un cas réel). Il comble ensuite l'écart par un résidu : `stcont.loc["RES"] = stneed.abs().sum() - stcont.sum()` et `ramp_cont.loc["Curtailment"] = 1 - ramp_cont.sum()`. **Toute erreur de modélisation ou de calcul est ainsi présentée comme une « contribution des EnR » ou « de l'écrêtement ».** La docstring de `calculate_ramping_contribution` attribue l'écart aux « petits réseaux de test ». C'est faux : l'écart est structurel.

**Impact.** L'article 19e(2) demande d'évaluer la contribution des ressources non fossiles (stockage, réponse de la demande). L'article 19f fixe des objectifs nationaux sur cette base. Une attribution qui ne boucle pas ne peut pas fonder ces objectifs. Les variables `technology_contributions_*` du fichier de sortie sont trompeuses pour tout utilisateur qui les lit sans le notebook.

**Recommandation.** Définir la décomposition comme une identité comptable : besoin = Σ contributions (pilotables + stockage + DSR + interconnexions) + écrêtement + délestage, avec un terme d'écrêtement explicite (potentiel − production) et l'exclusion explicite des EnR. Ajouter un contrôle d'identité dans `calculate_model_outputs` qui fait échouer le run si l'écart dépasse 0,1 %. Supprimer le résidu du notebook.

---

### F-06 — Le *dummy storage* ne respecte pas la FNAM 8(10) · **Critique**

**Constat (code).** `run_dummy_storage_optimization.py:775-786` lève une erreur si `efficiency_store`, `efficiency_dispatch` ≠ 1 ou si `standing_loss` ≠ 0. La spécification (p. 109) l'assume : « Dummy storage is modelled as lossless… the model raises an error for other values ».

**Exigence.** FNAM art. 8(10) : les ressources additionnelles doivent être caractérisées « at least in terms of power, energy capacity, energy-to-power ratio, availability and **roundtrip efficiency** », avec « the most representative roundtrip efficiency for each of these ratios » (2, 4, 8, 20, 50, 100, 200 h).

**Autres défauts du même module.**

- Le coût du stockage fictif est `capital_cost=1000 * len(n.snapshots) / 8760` (l. ~1003) : 1 000 €/MW/an codé en dur, **identique pour 2 h et 200 h**. Avec `minimize_system_costs: true`, valeur par défaut du modèle (le teaser utilise `false`), le dimensionnement résulte d'un arbitrage entre ce coût fictif et les économies de combustible, et non de la cible d'écrêtement. Cela biaise vers les longues durées.
- La contrainte d'écrêtement (13.51) est posée **par réseau (TY, CY)** (wildcards `{ty}_{cy}_{mh}_{ct}`). La FNAM 8(12)(a) demande d'atteindre l'objectif « as an average across the considered weather scenarios ». Imposer la cible année par année surdimensionne pour les années extrêmes.
- La cible d'écrêtement (5 % par défaut) est une saisie libre. La dérivation PNEC → objectif d'intégration EnR de la FNAM 8(6)-(9) n'est pas implémentée dans la chaîne : la comparaison PNEC est désactivée et le fichier n'est pas livré.

**Impact.** Sans pertes, le volume de stockage nécessaire est sous-estimé d'autant plus que la durée est longue (un stockage à 200 h type hydrogène a un rendement aller-retour d'environ 30-40 %). Les courbes « stockage nécessaire vs écrêtement » ne sont pas comparables à celles que les GRT produiront selon la FNAM.

**Recommandation.** Implémenter des rendements paramétrables par ratio E/P (le hull de Pozo admet des rendements avec une formulation adaptée, ou une variante MILP/LP sans hull). Agréger la contrainte d'écrêtement sur toutes les années climatiques dans un seul problème. Remplacer le coût fictif par un coût par MW et par MWh, ou rendre l'objectif de minimisation de capacité obligatoire pour l'indicateur réglementaire.

---

### F-08 — Les erreurs de prévision par défaut sont un bruit synthétique codé en dur · **Critique**

**Constat (code).** `build_base_network.py:644-760`, mode `forecast_timeseries_source: noise`, qui est la valeur par défaut du modèle (spécification, tableau 1 : « noise (synthetic) »). Les paramètres sont codés en dur (charge : biais 1 %, σ 3 % ; PV : biais −2 %, σ 8 % ; éolien : σ 12 % ; autocorrélations 0,7-0,95). `np.random.seed(4)` et `seed=4` s'appliquent à **toutes** les années climatiques et cibles : la même réalisation de bruit sert partout. Le bruit de charge est un bruit **commun à toutes les zones**.

**Preuve (exécution `runs/adv_noise`, mêmes données teaser, prévisions synthétiques).**

- Corrélation des erreurs relatives de charge entre N1, N2 et N3 : **1,0000**. Les erreurs ne se compensent jamais entre zones, ce qui annule la valeur de mutualisation des interconnexions.
- Corrélation erreur de charge / erreur éolienne en N1 : **0,647**. C'est un artefact de la graine partagée, pas une propriété physique.
- Besoin de court terme P99,9 en N1 : **5 042 MW** en mode `noise`, contre **11 665 MW** avec les prévisions CSV fournies. Le principal indicateur de l'art. 10 varie d'un facteur 2,3 selon un choix de paramétrage arbitraire.

**Exigence.** FNAM 10(1)(a) : erreurs « calculated as a time series based on the extrapolation of **at least two years of historical** residual load forecast errors », tenant compte de l'évolution des capacités et des **améliorations de prévision**. 10(1)(b) : distributions distinctes par période ou condition. 10(1)(c) : séparer les indisponibilités fortuites.

**Recommandation.** Supprimer le mode `noise` du chemin réglementaire, ou le réserver aux tests. Implémenter un module d'extrapolation d'erreurs historiques (ENTSO-E Transparency J-1 contre réalisé), mis à l'échelle des capacités de l'année cible, avec dépendance spatiale estimée. Rendre la source des prévisions obligatoire et la tracer dans les métadonnées de sortie.

---

### F-09 — La méthode probabiliste ignore la plupart des marges reconnues par la FNAM · **Élevée**

**Constat (code).** `compute_residual_flex_capacity` (`calculate_model_outputs.py:2939`) exclut « Renewable generators » et « Storage units (hydro reservoirs, pumped hydro, batteries, implicit DSR) ». Les interconnexions ne sont jamais considérées. FCR **et** FRR sont déduites dans les deux sens. La docstring annonce le contraire du code : « only the upward FRR is blocked for downward flex and vice-versa ». La marge haute compte la capacité des unités non engagées comme mobilisable dans l'heure (seule la rampe horaire est appliquée, sans délai de démarrage ni contrainte d'état).

**Exigence.** FNAM 10(2) : marges sur « generation assets […] **including renewables** », « demand and **storage** assets », « scheduled import and export and the available **exchange capacity** ». 10(4) : besoin non couvert = besoin − marges « **excluding FCR** » ; la FRR peut être analysée séparément (10(4)(b)).

**Preuve (exécution sur les réseaux DA/ID du teaser, fonctions de production appelées directement).**

| Zone | Heures « non couvertes à la hausse », modèle | Après ajout de la seule puissance de stockage et d'iDSR disponible | Heures « non couvertes à la baisse », modèle | Après ajout |
|---|---|---|---|---|
| N1 | 95 | 78 | 8 748 | 8 743 |
| N2 | 7 647 | 6 323 | 5 875 | 5 821 |
| N3 (20 GW hydro) | **8 760** | **360** | **8 760** | **447** |

L'ajout de puissance de stockage est une borne haute qui ignore les limites d'état de charge, mais l'ordre de grandeur est sans appel. Le même calcul attribue à N2 un besoin non couvert à la hausse cumulé de 20 945 GWh (somme horaire des MW non couverts), alors que la simulation infrajournalière ne constate que 5,9 GWh de délestage. N1 (gaz + EnR) est « non couvert à la baisse » 8 748 h sur 8 760, parce que la marge de baisse de l'EnR est ignorée.

**Note.** La méthode par défaut (`simulation`) ne calcule pas de « besoin non couvert » au sens de la FNAM 10(4). Elle mesure l'écart d'écrêtement et d'ENS entre l'infrajournalier et le day-ahead (éq. 13.20-13.25), ce qui correspond à la voie de l'art. 10(10). Aucune des deux méthodes ne produit donc l'indicateur de l'art. 10(4) tel que défini.

**Recommandation.** Reprendre `compute_residual_flex_capacity` selon la FNAM 10(2) : EnR à la baisse, stockage et iDSR avec contraintes d'état de charge, interconnexions avec capacité résiduelle, FCR seule déduite, FRR traitée selon 10(4)(b). Mettre la docstring en cohérence. Tester sur un cas analytique.

---

### F-07 — Les entrées temporelles ne sont pas validées · **Élevée**

**Preuve (exécution, `build_base_network` sur des jeux corrompus ; réseaux produits inspectés).**

| Jeu | Corruption | Résultat |
|---|---|---|
| M1 | Colonne `N3_load` absente du CSV de prévision | **Accepté sans avertissement.** Demande day-ahead de N3 = **0 MW** (au lieu de 15 GW en moyenne). Cause : `add_forecast_uncertainty` remplace intégralement `loads_t.p_set` par les colonnes présentes, et le `p_set` statique vaut 0 |
| M2 | p_max_pu à NaN (100 h), 1,5, −0,3 | Accepté. Valeurs hors bornes **écrêtées silencieusement**, NaN **conservés** dans le réseau |
| M3 | Charge à −50 000 MW, NaN, 10⁹ MW | Accepté tel quel |
| M4 | Prévisions décalées de 12 h | Accepté : l'alignement se fait **par position** (choix documenté dans le code), sans contrôle d'horodatage |
| M6 | Rendement de générateur 3,0, coût marginal −500 €/MWh, taux de panne fortuite 1,7 (170 %), p_nom de lien négatif | **Accepté** |
| M5 | p_min_pu > 1, capital_cost < 0, rendements de stockage > 1, max_hours < 0 | **Rejeté** (validation pandera) |

Comportement du solveur avec des NaN (réseau PyPSA minimal, HiGHS) : une charge NaN fait **disparaître la demande** de l'heure (production 0, statut « optimal ») ; un p_max_pu NaN **supprime la borne supérieure** (le solaire produit à pleine puissance installée). Le solveur ne signale rien.

**Impact.** Avec ≈ 60 zones, 36 années climatiques et des données ERAA multi-sources, une erreur de préparation produit des indicateurs faux sans aucun signal. FNAM art. 3(1)(b) : les opérateurs garantissent l'exactitude des données. L'outil de l'ACER doit au minimum détecter les incohérences.

**Recommandation.** Ajouter des schémas pandera pour toutes les séries temporelles (bornes, NaN interdits, horodatages monotones, couverture complète des composants) et pour les paramètres manquants (rendement ≤ 1, taux de panne ∈ [0,1], p_nom ≥ 0, coûts ≥ 0 sauf liste blanche). Aligner les prévisions par horodatage. Exiger que les colonnes de prévision couvrent exactement celles du réseau.

---

### F-05 — Années bissextiles · **Élevée**

**Preuve.**

- **Année climatique bissextile (2016, 8 784 h)** : le réseau de base conserve le 29 février (contrairement aux commentaires du code, qui affirment des snapshots « always leap-day-free »). Le run plante ensuite dans `run_day_ahead` : `plan_maintenance.py:505`, `Timestamp.replace(year=…)` → `ValueError: day is out of range for month` (`runs/adv_cy2016/logs/`). Le test unitaire `test_F05_leap_climate_year_crash` montre que `calculate_residual_load` (`_shift_time_columns_to_year`, l. 445) plante de la même façon.
- **Année cible bissextile (2028, l'une des années cibles par défaut de la spécification)** : l'index « heure de l'année » saute 24 valeurs après le 28 février et va jusqu'à 8 784 pour 8 760 pas (`test_F05b`). Le run complet aboutit, mais les sorties contiennent 24 heures NaN et un jour fantôme à besoin nul (jour 60). Le besoin hebdomadaire varie de −2,6 % (N1) à +2,2 % (N3) par rapport au même calcul étiqueté 2030, à données physiques identiques : `ts.replace(year=TY)` ne réaligne pas les jours de la semaine de l'année climatique sur ceux de l'année cible (§3bis).

**Impact.** L'ERAA et la FNAM (art. 6(5)) utilisent jusqu'à 36 années climatiques (1982-2017), dont 9 bissextiles. En mode CSV (le seul chemin public), un quart des années climatiques ne peut pas être traité.

**Recommandation.** Normaliser le calendrier une seule fois, à l'entrée (suppression documentée du 29 février ou année « type » de 8 760 h). Remplacer tous les `ts.replace(year=…)` par un helper unique et tester une année climatique et une année cible bissextiles en CI.

---

### F-11 — EVA : critère de convergence défaillant, statut non restitué · **Élevée**

**Constat (code).** `update_capacity.py:1218-1228` : `max_abs_npv` est mis à jour dès que `delta != 0`, **avant** l'écrêtement aux bornes `p_nom_min/p_nom_max`. Quand le delta est nul pour cause de monotonicité, la VAN est ignorée. La convergence est déclarée si `max_abs_npv <= threshold` (l. 1850).

**Preuve (tests unitaires sur `update_capacities`, fonction pure de production).**

- **F-11a** : actif très rentable (VAN = +5 M€/MW) déjà à `p_nom_max`. La capacité ne bouge pas, mais `max_abs_npv = 5 000 000 > 70 000` : **convergence impossible**. L'EVA tourne jusqu'à `max_it`.
- **F-11b** : actif extensible à VAN = −1 M€/MW en 2035, bloqué par le plancher de monotonicité. Delta = 0, `max_abs_npv = 0` : **« Converged » déclaré** alors que l'actif est profondément non rentable.
- **F-11c** : marché jouet où la VAN/MW = 300 k€ − 0,5 k€/MW × c (équilibre à 600 MW). Avec le pas par défaut de 800 MW et le seuil de 70 k€/MW, la trajectoire est 0 → 800 → 0 → 800… et **ne converge jamais**. La décroissance linéaire du pas (activée par défaut) atténue le problème, mais la valeur par défaut `max_it: 3` avec une décroissance sur 20 itérations laisse un pas ≥ 720 MW.
- **Restitution** : sur le teaser, `resources/convergence/convergence_0.txt` vaut `Aborted`. `model_outputs.nc` ne contient **aucune** variable ni aucun attribut de convergence (73 variables inspectées). Les indicateurs d'un système non convergé ne se distinguent pas de ceux d'un système à l'équilibre.

**Autres points.** Le pas est uniforme en MW pour tous les actifs (800 MW pour Malte comme pour l'Allemagne ; la spécification p. 91 le reconnaît). Tous les actifs bougent simultanément, d'où un risque de dépassement collectif. La seconde vérification de démothballage compare à 0, pas au seuil.

**Recommandation.** Calculer la convergence sur les actifs **qui peuvent encore bouger**, et signaler à part les actifs saturés à une borne. Publier le statut (`Converged`, `MaxIt`, `Aborted`), le nombre d'itérations et `max_abs_npv` dans les attributs de `model_outputs.nc`. Utiliser un pas relatif à la taille de l'actif ou de la zone, ou une recherche par bissection.

---

### F-10 — Le plafond de prix (HMMCP) est inopérant et contredit la configuration · **Élevée**

**Preuve.**

- Dans les données teaser, les générateurs de délestage offrent à **4 500 / 4 510 / 4 520 €/MWh**, en DA comme en ID. La configuration annonce des plafonds de 5 000 €/MWh (DA) et **10 000 €/MWh (ID)**. `add_load_shedding` fixe le coût du délestage au plafond, mais il n'est appelé que si le réseau d'entrée ne contient pas déjà de porteur « load shedding » (`build_base_network.py:1703-1708`). Dans le cas contraire, les coûts d'entrée sont conservés sans aucun contrôle de cohérence avec le plafond. Prix maximal observé en ID : **4 510 €/MWh**. Le plafond infrajournalier de 10 000 €/MWh ne joue jamais.
- `update_price_cap` (`update_price_cap.py:126-204`) compte des « événements » quand un prix dépasse 70 % du plafond initial (3 500 €/MWh). Il ne réécrit ensuite que les prix situés à 0,01 € **exactement du plafond initial**. Test `test_F10` : 4 pics à 4 510 €/MWh → plafond relevé à 5 500 €/MWh, **mais aucun prix de rareté n'est réévalué**. Les rentes de rareté vues par l'EVA restent tronquées, ce qui sous-estime la VAN des actifs de pointe et de stockage.
- Le relèvement est **ex post** : la répartition n'est pas recalculée sous le nouveau plafond. **Paramétrage vérifié sur le texte** (Décision ACER 01/2023, annexe 1, art. 4 ; Décision 02/2026) : +500 €/MWh, au moins 2 MTU sur au moins 2 jours dans les 30 jours glissants, au moins une zone, transition de 28 jours. **EU-Flex est conforme sur ces points**, mais le seuil y vaut 70 % du plafond **initial** au lieu de 70 % du plafond **en vigueur**, et les conditions d'exclusion ajoutées en 2026 ne sont pas modélisées. Plafond de référence réglementaire : 4 000 €/MWh (EU-Flex part de 5 000 €/MWh, choix prospectif à documenter).

**Recommandation.** Imposer en validation que le coût du délestage soit égal au plafond (ou à la VoLL, explicitement distinguée). Réécrire tous les prix de rareté (≥ seuil), ou mieux, re-résoudre avec le nouveau plafond. Paramétrer et documenter la version HMMCP appliquée.

---

### F-12 — Rampes : couverture partielle de la FNAM 9 ; indicateur désactivé publié à zéro · **Élevée**

- `calculate_maximum_ramping_requirement` ne fournit que max |ΔRL|. La FNAM 9(1) demande moyenne, min, max, distribution, percentiles, profil horaire et journalier, corrélations avec le vent, le soleil et la demande. Elle demande aussi les marges résiduelles de rampe (9(2)-(3)), les besoins non couverts (9(4)) et des statistiques par événement (9(7)). Les rampes montantes et descendantes ne sont pas distinguées.
- Le « ramping shortfall » (voie FNAM 9(11)) est **désactivé** dans la configuration du papier ACER. Le fichier de sortie contient pourtant `ramping_shortfall_upward/downward(_aggregated)` = **0,0** dans toutes les zones. Seul un attribut texte (« (disabled) ») signale la désactivation. Un 0 numérique se lit comme « aucun déficit de rampe ». Il faudrait un NaN ou l'absence de la variable.

**Recommandation.** Implémenter les sorties 9(1)-(7). Ne jamais écrire 0 pour un indicateur non calculé.

---

### F-13 — Assurance qualité : la suite d'intégration du modèle échoue sur son cas de référence · **Élevée**

**Preuve.** Règle `run_integration_tests` (absente du DAG par défaut), exécutée sur `runs/teaser` : **Overall Status: FAILED**.

1. SOC du réservoir N3 en infrajournalier : 352 503 MWh contre une cible de 393 971 MWh au 5 avril (−10,5 %, au-delà de la tolérance de 10 %). Le message affiche « actual > limit » alors que actual < limit : message inversé.
2. Dispatch ID hors limites d'engagement DA : **7 612 violations** (N1 Gas). La cause probable est un **défaut du test** : le gaz fait partie des `id_free_commitment_carriers` et peut légitimement se ré-engager en ID, mais le test vérifie tous les générateurs engageables.
3. Cohérence prix-flux : OK.

Aucun test unitaire n'est livré, et il n'y a pas de CI de tests (le seul workflow GitHub est un accusé de réception d'issues). Le cas « teaser » sert à la fois de démonstrateur et de seul test. **Conséquence : il n'existe aucun oracle de non-régression public**, et l'unique oracle fourni est faux ou ignoré.

**Recommandation.** Corriger le test (exclure les porteurs libres en ID) et l'intégrer au DAG. Ajouter des tests unitaires à solution analytique, comme ceux de ce rapport, et une CI publique (Linux, Windows, macOS) qui exécute un cas réduit.

---

### F-02 — Semaines ISO : fin décembre fusionnée avec début janvier · **Moyenne**

**Constat.** Les besoins et contributions hebdomadaires regroupent par `isocalendar().week` (`calculate_model_outputs.py:1188-1202`, 1675-1700, 1955-1968). En 2030, les 30 et 31 décembre appartiennent à la semaine ISO 1 de 2031 et sont moyennés avec les 1-6 janvier 2030.

**Preuve.** Le test `test_F02` (charge résiduelle plate sauf les 30-31 décembre) donne un besoin hebdomadaire de la semaine 1 de 144 000 MWh au lieu de 0. Sur le teaser, le recalcul indépendant avec des semaines calendaires internes à l'année donne N1 = 39,40 TWh, contre 40,73 TWh dans le modèle (**+3,4 %**) ; N2 +1,8 % ; N3 +0,05 %. Le recalcul avec semaines ISO reproduit **exactement** la valeur du modèle, ce qui confirme la cause. L'ampleur dépend de l'année cible et du décalage des jours de la semaine.

**Recommandation.** Grouper par (année ISO, semaine ISO) ou par blocs de 7 jours internes à l'année, et documenter le traitement des semaines partielles.

---

### F-14 — Engagement des unités linéarisé · **Moyenne (structurel)**

`linearized_unit_commitment: true` par défaut : relaxation LP du statut. Sur le teaser, le statut DA est fractionnaire **5,3 %** du temps. Les prix sont les duales de cette relaxation. Ils déterminent les revenus, donc la VAN, donc l'EVA. Aucune comparaison avec une résolution MILP n'est fournie, alors qu'elle permettrait de quantifier le biais sur les prix, les démarrages et les rampes. Recommandation : publier un étalonnage MILP contre LP sur un échantillon de semaines et de zones, et documenter l'erreur induite sur les indicateurs.

### F-15 — Monte-Carlo dégénéré · **Moyenne**

`forced_outages.samples: 1`, graine fixe `[18]`. La spécification (§3.5.2) annonce des résultats « aggregated values with confidence intervals ». Aucune agrégation avec intervalle n'existe dans `consolidate_flexibility_indicators.py`. Le P99,9 de l'art. 10 est estimé sur 8 760 valeurs, soit environ 9 heures dans la queue : l'erreur d'échantillonnage est forte et n'est pas rapportée. Recommandation : ≥ 10 tirages, intervalles bootstrap, et pooling explicite des années climatiques (éq. 13.19c) accompagné de son incertitude.

### F-01 — Cache de la charge résiduelle aveugle aux séries temporelles · **Moyenne (latent)**

`network_cache` (`calculate_model_outputs.py:901`) calcule sa clé sur le nom du réseau et les tables **statiques** uniquement. Les réseaux DA et ID portent le **même nom** (`EU-Flex Network ty2030 cy2013`). La collision n'est évitée que parce que leurs tables statiques diffèrent incidemment (colonne `committable`, etc.). Le test `test_F01` montre qu'à statique identique, la charge résiduelle ID renvoyée est celle du DA, et que le besoin de court terme vaut **0** au lieu de 200 MW. Tout usage en bibliothèque (analyse de sensibilité sur les séries, notebook) est exposé. Recommandation : supprimer le cache ou y inclure les séries temporelles.

### F-16 — Revenus de réserve mis silencieusement à zéro · **Moyenne**

`_align_time_series` (`compute_npv.py:243`) renvoie `0.0` sur toute exception ou absence d'index commun, et tombe en dernier recours sur « assume same order ». Un décalage de fuseau ou d'année supprime donc sans erreur les revenus de réserve de la VAN. Recommandation : lever une erreur.

### F-17 — Traçabilité et testabilité · **Moyenne**

- Historique réduit à 2 commits : export depuis la plateforme privée `eu-flex-platform`. `envs/environment.yaml` cite `tools/make_public_repo.py` et `src/euflex/workflow/eu_flex_model`, absents du dépôt public.
- `update_capacity.py` exécute `from snakemake.script import snakemake` au niveau du module : il est **impossible de l'importer** hors d'un job Snakemake (contournement nécessaire dans nos tests).
- `calculate_short_term_need` appelle `calculate_residual_load(n)` sans porteurs EnR et dépend d'une variable globale `RENEWABLE_CARRIERS` définie seulement dans `__main__` : `NameError` en usage bibliothèque.
- `.github/workflows` : action référencée par tag (`actions/github-script@v7`) et non par SHA. Pas d'injection constatée (le titre d'issue n'est pas interpolé).

### F-18 — Passage à l'échelle · **Moyenne (structurel, hypothèse chiffrée)**

**Mesure.** Le teaser (3 nœuds, 17 générateurs, 1 TY × 1 CY × 1 itération) prend 18 min 50 s sur un cœur (DA 11 min, ID 6,5 min, 183 fenêtres chacun).

**Extrapolation [HYP].** Pour ≈ 60 zones et des centaines d'unités agrégées, en supposant un coût par fenêtre ×20 à ×50, on obtient environ 6-15 h par (TY, CY, itération). Avec 4 TY × 36 CY × 10-30 itérations, cela représente **10⁴ à 10⁵ CPU·h**. Le clustering de semaines (désactivé par défaut) réduit ce coût au prix d'une approximation non quantifiée. **Le calendrier (rapport en juillet 2027, consultation close le 17/12/2026) laisse peu de marge pour des itérations de correction.**

### F-04 — Unités · **Faible**

`maximum_ramping_requirement`, les percentiles de court terme, les besoins non couverts probabilistes et les capacités de flexibilité résiduelle sont étiquetés **MWh** alors que ce sont des puissances (MW, ou MW/h pour la rampe). La spécification (tableau des métriques) dit MW. Un consommateur des fichiers NetCDF qui convertit selon l'attribut se trompe d'un facteur temps.

### F-19 — Nomenclature · **Faible**

« Daily flexibility need » d'EU-Flex = indicateur **horaire** de la FNAM 8(5)(a) ; « weekly » = indicateur **journalier** 8(5)(b) ; « seasonal » = 8(5)(c). Lors de la comparaison avec les rapports nationaux (art. 19e(7)), ce décalage est une source d'erreur. Recommandation : adopter la nomenclature FNAM, ou fournir une table de correspondance dans les métadonnées.

---

## 3bis. Résultats des runs complémentaires

Détail : [`evidence/runs_complementaires.md`](evidence/runs_complementaires.md).

| Run | Résultat |
|---|---|
| Réplique indépendante du teaser | **73/73 variables identiques bit à bit** : déterminisme confirmé (même machine, même environnement) |
| Année cible 2028 (bissextile), mêmes données | Le run aboutit, mais les sorties horaires ont **8 784 heures dont 24 NaN**. Le besoin journalier compte **366 jours dont un jour fantôme à 0**. Le besoin hebdomadaire **change de −2,6 % (N1) par le seul changement d'étiquette d'année cible**, car les jours de la semaine ne sont pas réalignés lors du passage de l'année climatique à l'année cible |
| Année climatique 2016 (bissextile) | Réseau construit avec le 29 février, puis **plantage** dans `run_day_ahead` (`plan_maintenance.py:505`) |
| Jeux corrompus M1-M6 | Voir F-07 |

---

## 4. Ce qui a été contesté et a tenu

Ces contre-preuves sont aussi importantes que les défauts : elles délimitent ce qui est fiable.

| Hypothèse attaquée | Résultat |
|---|---|
| Arithmétique des besoins journalier et saisonnier (FNAM 8(5)(a) et (c)) | **Exacte** : recalcul indépendant depuis les CSV = valeurs du modèle (N1 27 763 562 MWh, etc.) |
| Rampe maximale | Exacte (13 361 / 7 628 / 3 113 MW) |
| Percentiles P99,9 / P0,1 des erreurs de prévision (mode CSV) | Exacts (N1 : 11 664,9 / −12 523,1 MW) |
| Validation des paramètres statiques des stockages | Robuste (rendements > 1, durée négative, SOC initial incohérent : rejetés) |
| Cohérence prix-flux (flux des prix bas vers les prix hauts) | OK sur le teaser |
| Liens bidirectionnels après agrégation | OK (p_min_pu = −1 conservé en série temporelle) |
| Sécurité du code (eval/exec, désérialisation, shell, injection CI) | Aucune vulnérabilité exploitable identifiée. Surface d'attaque faible (pas de réseau à l'exécution, YAML chargé par Snakemake) |
| Installation et exécution de bout en bout | OK (Linux, Python 3.12, versions du lock) |
| Reproductibilité (réplique indépendante) | **Bit à bit identique** (73/73 variables, prix DA écart 0,0) sur la même machine |
| Erreur de prévision ID − DA non nulle en production (collision F-01) | Pas de collision sur le teaser (tables statiques différentes) : défaut latent seulement |

---

## 5. Verdict sur l'adéquation à l'objectif initial

**Objectif initial** (dossier §3) : quantifier, pour l'évaluation européenne de 2027 (art. 19e(7)), des besoins de flexibilité **conformes à la Décision ACER 05/2025**, à l'échelle de l'UE et sur de multiples années climatiques et cibles, avec des contributions par technologie exploitables pour orienter les objectifs de flexibilité non fossile (art. 19f).

| Critère | Évaluation |
|---|---|
| Exactitude des indicateurs simples | ✅ Satisfaisant |
| Conformité FNAM 8 (intégration EnR) | ❌ Stockage sans pertes, objectif PNEC non implémenté, cible par année climatique |
| Conformité FNAM 9 (rampe) | ⚠️ Partielle ; déficit désactivé et publié à 0 |
| Conformité FNAM 10 (court terme) | ❌ Erreurs synthétiques par défaut ; marges incomplètes ; besoin non couvert de 10(4) non produit tel que défini |
| Contributions par technologie (art. 19e(2), 19f) | ❌ Non bouclées, masquées par un résidu |
| Robustesse aux données réelles (ERAA, 36 CY) | ❌ Pas de validation des séries ; plantage sur année bissextile |
| Fiabilité de l'EVA | ⚠️ Convergence non garantie et non restituée ; plafond de prix inopérant |
| Reproductibilité et traçabilité | ✅ Déterminisme bit à bit vérifié ; ⚠️ mais un seul tirage, aucun intervalle de confiance, historique non auditable |
| Assurance qualité | ❌ Aucun test, aucune CI ; l'oracle fourni échoue |
| Passage à l'échelle | ⚠️ Non démontré publiquement |

**Verdict : l'outil, dans sa version publiée, n'est PAS apte à produire les résultats de l'évaluation européenne des besoins de flexibilité.** Plusieurs indicateurs réglementaires sont non conformes par construction (F-06, F-08, F-09) ou faux (F-03). La chaîne échoue silencieusement sur des données imparfaites (F-07) et ne traite pas les années bissextiles (F-05). Le socle (simulation de marché PyPSA, arithmétique des besoins FNAM 8(5)) est sain et récupérable : les défauts sont **corrigeables** et ne remettent pas en cause l'architecture. L'outil est **apte à son usage déclaré** de support de consultation, à condition que les stakeholders soient explicitement avertis des points C/E ci-dessus.

---

## 6. Limites structurelles et améliorations indispensables avant tout usage opérationnel

### 6.1 Limites structurelles (inhérentes aux choix de conception)

1. **Zones en plaque de cuivre et NTC « physical » par défaut.** Les besoins réseau (FNAM 11-14) sont hors modèle : les données de besoins réseau sont fictives et désactivées. L'outil ne mesure que des besoins **système**.
2. **Marché infrajournalier et équilibrage fusionnés en un seul dispatch horaire.** Les catégories « very fast / fast / slow » de la FNAM 10(1)(e) ne sont pas représentables à pas horaire.
3. **Relaxation LP de l'engagement des unités** : biais non quantifié sur les prix, donc sur l'EVA.
4. **EVA heuristique à pas fixe**, sans garantie de convergence ni d'unicité de l'équilibre.
5. **Prévision parfaite intra-fenêtre** (72 h) et pré-optimisation du stockage en prévision parfaite annuelle : surestimation de la flexibilité hydraulique.
6. **Dépendance à des données non publiques** (ERAA, FBMC non redistribuables) : la reproductibilité par des tiers des résultats de 2027 ne sera pas assurée avec les seules données publiques.
7. **Coût de calcul** (F-18), qui pousse vers le clustering et donc vers une approximation supplémentaire.

### 6.2 Améliorations indispensables (bloquantes), par priorité

| # | Action | Findings |
|---|---|---|
| 1 | Refondre la décomposition des contributions en identité comptable vérifiée à l'exécution ; retirer les résidus du notebook | F-03 |
| 2 | Rendements du *dummy storage* par ratio E/P ; contrainte d'écrêtement moyennée sur les années climatiques ; dérivation PNEC de l'objectif d'intégration ; suppression du coût arbitraire | F-06 |
| 3 | Erreurs de prévision issues de données historiques (≥ 2 ans), extrapolées, avec dépendance spatiale et distributions conditionnelles ; bannir `noise` du chemin réglementaire | F-08 |
| 4 | Marges de court terme et de rampe conformes à FNAM 9(2)-(4) et 10(2)-(4) (EnR, stockage avec SOC, demande, échanges ; FCR seule déduite) | F-09, F-12 |
| 5 | Validation exhaustive des séries temporelles et des paramètres ; alignement par horodatage ; échec bruyant | F-07 |
| 6 | Calendrier unifié (années bissextiles), testé en CI | F-05, F-02 |
| 7 | Critère de convergence EVA corrigé ; statut et diagnostic publiés dans les sorties ; pas adaptatif | F-11 |
| 8 | Cohérence délestage/plafond ; réécriture ou re-résolution sous plafond relevé ; paramétrage HMMCP versionné | F-10 |
| 9 | Suite de tests unitaires (cas analytiques) + intégration corrigée dans le DAG + CI publique multi-OS | F-13, F-17 |
| 10 | Monte-Carlo ≥ 10 tirages et intervalles de confiance ; métadonnées de provenance (source des prévisions, version, graines, convergence) | F-15, F-11 |
| 11 | Étalonnage MILP contre LP et étude de passage à l'échelle publiée | F-14, F-18 |
| 12 | Unités et nomenclature alignées sur la FNAM ; NaN pour les indicateurs non calculés | F-04, F-19, F-12 |

### 6.3 Recommandation de gouvernance

Publier, avant juillet 2027, un **dossier de vérification et validation** : tests, étalonnages, comparaison avec au moins un rapport national FNA et avec les résultats ERAA. Joindre une **matrice de conformité FNAM article par article**, maintenue avec le code. Sans ces éléments, les résultats d'EU-Flex ne devraient pas servir de référence pour contester ou pondérer les rapports nationaux au titre de l'article 19e(7).
