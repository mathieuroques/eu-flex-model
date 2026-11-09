# Dossier de contexte et de recherche — EU-Flex (ACER)

*Phase 1 de l'adversarial review. Document de référence, tenu séparé du rapport d'audit.*
*Date de constitution : 9 novembre 2026. Objet : dépôt `eu-flex-model`, version 1.0.0 « rc2 » (commit `65cb449`).*

Légende de fiabilité utilisée tout au long du dossier :

- **[FAIT]** : établi par lecture directe d'une source primaire (texte juridique, code, document du dépôt) ou par exécution.
- **[HYP]** : hypothèse raisonnable, non démontrée.
- **[MANQUE]** : information nécessaire à l'évaluation mais non disponible.

---

## 1. Inventaire des sources

### 1.1 Sources primaires juridiques et méthodologiques

| Réf. | Document | Statut | Accès |
|---|---|---|---|
| R1 | Règlement (UE) 2024/1747 modifiant le règlement (UE) 2019/943 (réforme du marché de l'électricité, EMD) : nouveaux articles 19e (évaluation des besoins de flexibilité) et 19f (objectif national indicatif de flexibilité non fossile) | En vigueur | https://eur-lex.europa.eu/eli/reg/2024/1747/oj |
| R2 | Décision ACER n° 05/2025 du 25 juillet 2025 et son annexe I, la méthodologie FNA (*Flexibility Needs Assessment methodology*, ci-après « FNAM ») | En vigueur | https://www.acer.europa.eu/sites/default/files/documents/Individual%20Decisions/ACER-Decision-05-2025-Flexibility-Needs-Assessment-Methodology.pdf ; texte consolidé : https://www.acer.europa.eu/sites/default/files/documents/Publications/ACER-flexibility-needs-assessment-methodology-2025.pdf ; version en suivi de modifications : `.../ACER-Decision-05-2025-FNAM-Annex-Ia.pdf` |
| R3 | Méthodologie ERAA (ENTSO-E, art. 23 du règlement 2019/943), en particulier l'art. 6 (EVA) et l'art. 7 (dispatch économique), à laquelle la FNAM renvoie | En vigueur | Site ACER/ENTSO-E (non téléchargée intégralement) |
| R4 | Méthodologie HMMCP SDAC (Décision ACER 01/2023, amendée par la Décision ACER 02/2026) | En vigueur | https://www.acer.europa.eu/sites/default/files/documents/Individual%20Decisions/ACER-Decision-02-2026-harmonised-clearing-prices-day-ahead.pdf |
| R5 | Recommandation ACER 01/2026 sur le signalement par les ARN des obstacles à la flexibilité | Publiée | https://www.acer.europa.eu/sites/default/files/documents/Recommendations/ACER-Recommendation-01-2026-NRAs-reporting-barriers-to-flexibility.pdf |
| R6 | JRC, *A guide for practitioners on Articles 7-10 of the FNA methodology* (JRC146931) | Publié | https://publications.jrc.ec.europa.eu/repository/handle/JRC146931 (seul le résumé a été consulté) |

### 1.2 Sources du dépôt audité

| Réf. | Document | Remarque |
|---|---|---|
| D1 | `README.md` | Avertissement explicite : version préliminaire, « not the version to be used by ACER to run the EU-wide FNA » |
| D2 | `doc/user_manual.md` / `.pdf` (1 219 lignes) | Options de configuration, sorties, dépannage |
| D3 | `doc/modelling_specification.pdf` v1.0 du 26/10/2026 (142 p., OET) | Formulation mathématique. Les équations sont des images : vérifiées par rendu des pages (p. 92-102) |
| D4 | Code : `src/euflex/eu_flex_model/` (≈ 41 000 lignes Python + Snakemake, 36 scripts, 9 fichiers de règles) | Snakemake ≥ 9, PyPSA 0.33.2, linopy 0.7.0, HiGHS 1.15.1 |
| D5 | Données « teaser » : `data/teaser/ty_2030_cy_2013/` | Système stylisé à 3 nœuds (N1/BE, N2/FR, N3/NL), 8 760 h, année cible 2030, année climatique 2013 |
| D6 | `envs/*.lock.yaml`, `pyproject.toml`, `CITATION.cff`, `.github/` | Environnement verrouillé, pas de CI de tests publique |
| D7 | Historique git | **2 commits seulement** (« 1.0.0 » puis « 1.0.0 - rc2 ») : export depuis une plateforme privée (`eu-flex-platform`, référencée dans `Snakefile` et `paths.py`). L'historique de développement n'est pas auditable. |

### 1.3 Sources secondaires (contexte)

- Communiqué ACER du 21-22/10/2026 : consultation publique du 5 novembre au 17 décembre 2026, webinaire le 17 novembre 2026, première évaluation européenne prévue en juillet 2027. Retours sur le papier et la méthodologie via la consultation, retours sur le modèle via GitHub (Mondo Visione, LexisNexis, Lovguiden).
- Page projet d'Open Energy Transition (OET) « Flexibility assessment platform » et fil openmod (2025) : OET développe la plateforme EU-Flex sur PyPSA pour l'ACER.
- Papier ACER « Preparing for the European flexibility needs assessment » (2026), cité par le README : **[MANQUE]** non trouvé en ligne au moment de l'audit. Les figures 9 à 18 qu'il contient ne peuvent donc pas être comparées.

---

## 2. Cadre réglementaire applicable

### 2.1 Article 19e du règlement 2019/943 (inséré par le règlement 2024/1747) [FAIT, R1]

- **§1** : au plus tard un an après l'approbation de la méthodologie par l'ACER, chaque autorité de régulation (ou entité désignée) adopte un rapport sur les besoins nationaux estimés de flexibilité pour au moins les 5 à 10 années suivantes. Le rapport est mis à jour tous les deux ans.
- **§2** : le rapport évalue les besoins **saisonniers, journaliers et horaires**, le potentiel des ressources non fossiles (en particulier **réponse de la demande et stockage**), les obstacles de marché, la contribution de la numérisation, et la flexibilité disponible dans les autres États membres.
- **§3** : les GRT et GRD fournissent les données et analyses.
- **§4-6** : ENTSO-E (électricité) et l'entité européenne des GRD (EU DSO Entity) proposent conjointement le type et le format des données ainsi que la méthodologie. L'ACER approuve ou amende dans un délai de trois mois.
- **§7** : les rapports nationaux sont transmis et publiés. **L'ACER, dans les 12 mois, émet un rapport qui les analyse** et formule des recommandations sur les questions transfrontalières, notamment sur la suppression des obstacles à la flexibilité non fossile (article 15 du règlement 2019/942 tel que modifié).
- **Article 19f §1** : chaque État membre définit, sur la base du rapport, un objectif national indicatif de flexibilité non fossile, incluant les contributions spécifiques de la réponse de la demande et du stockage.

**Texte intégral vérifié (EUR-Lex, CELEX 32024R1747), compléments décisifs [FAIT] :**

- **19e(1)(a)** : le rapport national doit être « consistent with the European resource adequacy assessment and national resource adequacy assessments ».
- **19e(2)(a)** : évaluer les besoins « at least on a seasonal, daily and hourly basis […] **inter alia, different assumptions in respect to electricity market prices, generation and demand** ». **Des sensibilités aux hypothèses de prix sont donc exigées.**
- **19e(4)(b)(i)** : tenir compte de « all available sources of flexibility in a cost-efficient manner in the different timeframes, including in other Member States ».
- **19e(7)** : dans les 12 mois, l'ACER émet un rapport analysant les rapports nationaux. Parmi les questions transfrontalières, l'ACER **évalue** : (a) l'intégration de l'analyse des besoins de flexibilité avec la méthodologie ERAA et le TYNDP ; **(b) « the estimated flexibility needs in the electricity system at Union level and its projected economically available potential for a period of the next 5 to 10 years taking into account the national reports »** ; (c) d'autres mesures pour libérer le potentiel de flexibilité.

**Conséquence pour l'outil [FAIT, corrigé]** : la première version de ce dossier affirmait que le règlement n'imposait pas à l'ACER sa propre évaluation paneuropéenne. **C'est inexact.** L'art. 19e(7)(b) charge l'ACER d'évaluer **les besoins de flexibilité au niveau de l'Union** et le **potentiel économiquement disponible** (ce qui justifie la présence d'une EVA). EU-Flex est l'instrument de cette évaluation. Trois exigences en découlent :

1. indicateurs définis comme ceux de la FNAM (comparabilité avec les rapports nationaux) ;
2. **un niveau Union**, et pas seulement zonal ;
3. **des sensibilités aux hypothèses de prix** (19e(2)(a)).

### 2.2 Méthodologie FNA, Décision ACER 05/2025, annexe I [FAIT, R2]

Points structurants, avec le numéro d'article de la version consolidée :

| Art. | Exigence | Pertinence pour EU-Flex |
|---|---|---|
| 1(3) | Besoins système quantifiés **par zone de dépôt des offres (bidding zone)** | Le modèle est zonal : conforme dans le principe |
| 2(2)(dd) | **Charge résiduelle** = demande totale − production non pilotable (éolien, solaire…) − production soumise à des contraintes de *must-run*, par MTU | Éq. 13.1 de la spécification |
| 2(2)(y) | Besoins de **rampe** : variations de la charge résiduelle **en prévision parfaite** | Art. 9 |
| 2(2)(ff) | Besoins de **court terme** : variations inattendues de la charge résiduelle (erreurs de prévision) **et indisponibilités fortuites** en infrajournalier et équilibrage | Art. 10 |
| 2(2)(jj) | Besoins **non couverts** : besoins additionnels non satisfaits par les ressources existantes ou nouvelles | Notion pivot, distincte du « besoin brut » |
| 6(5) | Au moins les mêmes années climatiques que le dispatch économique (ED) de l'ERAA/NRAA. Au premier cycle, celles de l'EVA | ERAA : 35-36 années climatiques |
| 7(1) | Au moins un scénario cohérent avec un scénario de référence ERAA ; **EVA selon l'art. 6 de la méthodologie ERAA** | EU-Flex implémente une EVA « inspirée ERAA » |
| 7(3)(b) | Possibilité d'un ED indépendant, s'il intègre les besoins de rampe et/ou de court terme | Voie choisie par EU-Flex |
| 8(2)-(4) | Séries d'**écrêtement EnR** par MTU, caractérisées par moyenne, max, min, distribution, percentiles, profil horaire/journalier, **corrélation avec vent, soleil, demande** | Partiellement couvert |
| 8(3) | Ajouter à l'écrêtement celui qui résulte des besoins de rampe et de court terme **descendants non couverts** (max des deux par MTU). Facultatif pour le premier rapport | |
| **8(5)** | Indicateurs de variabilité de la charge résiduelle : **(a) horaire** = Σ\|charge résiduelle horaire − moyenne journalière\| ; **(b) journalier** = Σ\|moyenne journalière − moyenne hebdomadaire\| ; **(c) saisonnier** = Σ\|moyenne mensuelle − moyenne annuelle\| | EU-Flex les nomme « daily / weekly / seasonal » (décalage de nomenclature : son « daily need » est l'indicateur **horaire** de la FNAM) |
| 8(6)-(9) | Comparer l'écrêtement à l'**objectif d'intégration EnR** dérivé de la cible EnR du PNEC. Besoin non couvert = écrêtement au-delà de l'objectif | Dans EU-Flex, la comparaison PNEC est désactivée par défaut et le fichier n'est pas fourni |
| **8(10)** | Ressources de flexibilité additionnelles caractérisées au moins par puissance, énergie, ratio énergie/puissance, disponibilité et **rendement aller-retour** ; ratios **2, 4, 8, 20, 50, 100 et 200 h** avec **le rendement aller-retour le plus représentatif pour chaque ratio** | Le *dummy storage* d'EU-Flex est **sans pertes par construction** (voir rapport, F-06) |
| 8(12)(a) | Avec un ED, atteindre l'objectif annuel d'intégration EnR **en moyenne sur les scénarios météorologiques** | À comparer à la contrainte 13.51 |
| 9(1) | Variations de la charge résiduelle entre MTU consécutifs : moyenne, max, min, distribution, percentiles, profil, corrélations | EU-Flex : « maximum ramping requirement » uniquement (valeur absolue, sans séparer hausse et baisse) |
| 9(2)-(4) | **Marges résiduelles de rampe** (production, y compris EnR, stockage, demande, échanges), puis besoins de rampe non couverts = variations − capacité des marges | |
| 9(11) | Avec un ED qui intègre déjà les rampes : comparer ENS et écrêtement **avec et sans contraintes de rampe** | EU-Flex : « ramping shortfall », **désactivé** dans la configuration du papier ACER |
| **10(1)** | Besoins de court terme = **percentiles 0,1 et 99,9** de la distribution des erreurs de prévision de la charge résiduelle (J-1 12h00 contre temps réel). Les erreurs sont **extrapolées d'au moins deux années d'erreurs historiques**, en tenant compte de l'évolution de la charge, des capacités installées et des **améliorations de prévision** | Mode par défaut d'EU-Flex : **bruit synthétique codé en dur** (voir F-08) |
| 10(1)(b) | **Distributions distinctes** par période (heure, jour, saison) ou condition système | Méthode « simulation » (défaut) : distribution unique. Méthode « probabilistic » : 4 conditions |
| 10(1)(c) | Distinguer les distributions d'indisponibilités fortuites de celles des erreurs de prévision (éviter le double comptage) | |
| **10(2)-(4)** | Marges résiduelles de court terme sur **production (y compris EnR), stockage, demande, échanges** ; besoin non couvert = besoin − marges **(hors FCR)** ; la contribution FRR peut être analysée séparément | Méthode probabiliste d'EU-Flex : **exclut stockage, iDSR, EnR et interconnexions**, et déduit aussi la FRR (voir F-09) |
| 10(4)(c), 10(5), 10(6) | Probabilité d'occurrence, énergie attendue = capacité × probabilité, statistiques par événement | |
| 13-14 | Affinage par besoins réseau (GRT/GRD), indisponibilités liées à la préqualification réseau et aux limites temporaires | EU-Flex : besoins réseau = **données fictives aléatoires**, désactivées par défaut |
| 16 | Critères d'orientation sur la capacité des sources de flexibilité à couvrir les besoins | Contributions par technologie |

### 2.3 Plafonds de prix harmonisés (HMMCP) [FAIT partiel, R4]

- Le mécanisme d'ajustement automatique du prix maximal SDAC (seuil de déclenchement en % du plafond, nombre de MTU et de jours dans une fenêtre glissante de 30 jours, incrément, période de transition) a été **amendé à plusieurs reprises** (Décision 01/2023, puis 02/2026).
- **[FAIT, vérifié sur le texte]** Décision ACER 01/2023, annexe 1, art. 4 : plafond de référence SDAC **+4 000 €/MWh** (plancher −500). Hausse de **+500 €/MWh** si le prix de clôture, **dans au moins une zone**, dépasse **70 % du plafond harmonisé en vigueur**, pendant au moins 2 MTU sur au moins 2 jours différents, dans les 30 jours glissants qui suivent le premier pic. **Période de transition de 28 jours.** La Décision ACER 02/2026 amende la méthodologie sur les **conditions d'exclusion** (pics non représentatifs, liquidité, découplage d'un NEMO) sans modifier ces paramètres.
- **Comparaison avec EU-Flex** : incrément, fenêtre, transition et règle « au moins une zone » sont conformes. **Écart** : le seuil est calculé sur 70 % du plafond **initial** (`spike_threshold = starting_price_or * 0.7`) et non du plafond **en vigueur**, ce qui déclenche trop facilement les hausses successives. Les conditions d'exclusion de 2026 ne sont pas modélisées. Plafond de départ par défaut : 5 000 €/MWh (hypothèse prospective, et non la valeur de référence de 4 000).

---

## 3. Objectif réel de l'outil, utilisateurs, cas d'usage

| Élément | Constat | Source |
|---|---|---|
| Objectif déclaré | Simuler le marché électrique européen (day-ahead et infrajournalier/équilibrage), faire évoluer le parc par une EVA, puis calculer les indicateurs de besoins de flexibilité conformes à la Décision ACER 05/2025, les contributions par technologie et par interconnexion, et des indicateurs de marché | D1, D3 §1-2 [FAIT] |
| Utilisateur opérationnel | ACER, pour l'évaluation européenne de 2027 (art. 19e(7)) | D1, D3 [FAIT] |
| Utilisateurs de la version publiée | Parties prenantes de la consultation : GRT, ARN, industriels, chercheurs. Usage de **revue**, pas de production de résultats | D1 [FAIT] |
| Statut | **Préliminaire.** « not the version to be used by ACER ». Le jeu teaser est « illustratif », sans valeur prédictive | D1 [FAIT] |
| Échelle visée | Toutes les zones de l'UE + voisins (≈ 60 zones), années cibles 2028-2037, 36 années climatiques (1982-2017), tirages Monte-Carlo de pannes, EVA itérative | D3 §3.1 [FAIT] |
| Échelle testée publiquement | 3 nœuds, 1 année cible, 1 année climatique, 1 tirage | D5 [FAIT] |
| Données réelles d'entrée (ERAA, PECD, PNEC, FBMC) | **Non fournies.** Les données FBMC ne sont pas redistribuables, le fichier PNEC n'est pas livré, les besoins réseau sont fictifs | D2 §3.5, §3.15 ; D3 p. 105 [FAIT] |

**Résultats attendus** : pour chaque (année cible, année climatique, zone) — besoins journaliers, hebdomadaires et saisonniers ; rampe maximale ; besoins de court terme (percentiles P0,1/P99,9 et P1/P99) ; écrêtement ; déficits de court terme ; contributions par technologie et par interconnexion ; résultats EVA (capacités, VAN/MW) ; dimensionnement du *dummy storage* par ratio E/P et par cible d'écrêtement.

**Hypothèses structurantes [FAIT, D3]** : zones en « plaque de cuivre » ; agrégation des centrales par flotte ; engagement des unités (UC) **linéarisé** (relaxation LP) par défaut ; horizon glissant de 72 h avec 24 h de recouvrement ; pré-optimisation du stockage à pas grossier (8 h, ou 4 h dans le teaser) en prévision parfaite ; maintenance planifiée par recuit simulé ; pannes fortuites appliquées au seul infrajournalier ; marché infrajournalier et équilibrage fusionnés en un seul dispatch économique ; prix = duales du bilan nodal ; EVA à pas fixe en MW, par seuil de VAN/MW.

---

## 4. Exigences de référence retenues pour l'audit

Exigences dérivées des sources ci-dessus. Le rapport les cite sous la forme « EXG-n ».

**Réglementaires**

- EXG-1 : indicateurs de variabilité de la charge résiduelle conformes à la FNAM 8(5) (périodes calendaires correctes).
- EXG-2 : indicateurs de court terme conformes à la FNAM 10 (P0,1/P99,9 ; erreurs dérivées de données historiques ; distributions conditionnelles ; marges incluant stockage, demande, échanges ; hors FCR).
- EXG-3 : rampe conforme à la FNAM 9 (variations caractérisées, hausse et baisse distinctes, marges, besoins non couverts).
- EXG-4 : dimensionnement des ressources additionnelles conforme à la FNAM 8(10) (ratios E/P 2-200 h **avec rendement aller-retour représentatif**).
- EXG-5 : objectif d'intégration EnR dérivé des PNEC (8(6)-(9)), atteint en moyenne sur les années climatiques (8(12)(a)).
- EXG-6 : EVA cohérente avec l'art. 6 de la méthodologie ERAA (convergence, critères économiques).
- EXG-7 : plafonds de prix cohérents avec la méthodologie HMMCP en vigueur.

**Techniques et fonctionnelles**

- EXG-8 : exactitude numérique des indicateurs (identités comptables vérifiables : somme des contributions = besoin).
- EXG-9 : robustesse aux données (validation des séries temporelles, rejet explicite des valeurs aberrantes et des colonnes manquantes).
- EXG-10 : reproductibilité (graines, versions, déterminisme du solveur) et traçabilité (statut de convergence, provenance).
- EXG-11 : passage à l'échelle (≈ 60 zones × 36 années climatiques × N années cibles × itérations EVA).
- EXG-12 : sécurité de la chaîne logicielle (dépendances, CI, exécution de code).
- EXG-13 : transparence et auditabilité (code, historique, tests, documentation cohérente avec le code).

---

## 5. Outils comparables (contexte)

| Outil | Nature | Pertinence |
|---|---|---|
| ERAA (ENTSO-E) | Adéquation européenne avec EVA, plusieurs outils (Antares, PLEXOS, BID3…) | Référence méthodologique de l'EVA, et source de données imposée par la FNAM |
| PyPSA-Eur | Modèle ouvert du système européen (planification) | Base logicielle d'EU-Flex. EU-Flex en réutilise du code (licence MIT) |
| Bilan prévisionnel RTE (2015 et suivants) | Indicateurs de flexibilité journalière, hebdomadaire et saisonnière par écarts à la moyenne | **Source directe des figures 12-13** de la spécification (méthode de décomposition) |
| Études nationales d'adéquation et de flexibilité (par ex. Elia) | Besoins de flexibilité par décomposition temporelle et par percentiles d'erreurs | Comparaison de résultats [MANQUE : non effectuée] |
| JRC (R6) | Guide d'application des articles 7-10 avec un cas synthétique d'une semaine | Référence d'interprétation [MANQUE : texte intégral non consulté] |

---

## 6. Faits établis, hypothèses, manques — synthèse

**Faits établis (par lecture ou exécution)**

1. Le code public est un export de la plateforme privée d'OET : 2 commits, pas de tests unitaires livrés, pas de CI de test (le seul workflow GitHub accuse réception des issues).
2. La chaîne s'installe et s'exécute sous Python 3.12 avec les versions verrouillées (environnement reconstruit avec `uv` à partir des versions du lock Linux ; conda n'était pas disponible dans le conteneur d'audit).
3. Les indicateurs sont calculés dans `calculate_model_outputs.py` (5 020 lignes) ; l'EVA dans `compute_npv.py` et `update_capacity.py` ; les marchés dans `market_functions.py`.
4. Les écarts avec la FNAM portent sur l'efficacité du stockage fictif, les marges de court terme, l'origine des erreurs de prévision et la caractérisation des rampes. Le détail figure dans le rapport.

**Hypothèses**

- H1 : l'ACER utilisera EU-Flex comme référence face aux rapports nationaux. C'est plausible, mais le rôle exact des résultats d'EU-Flex dans le rapport de 2027 n'est pas défini publiquement.
- H2 : la version opérationnelle utilisera les données ERAA 2024/2025 (PECD, capacités) et des prévisions historiques. Non vérifiable.
- H3 : les écarts relevés dans la version préliminaire subsisteront dans la version opérationnelle s'ils ne sont pas signalés. La consultation est le canal prévu pour les corriger.

**Informations manquantes**

- M1 : papier ACER 2026 (figures 9-18) pour comparer quantitativement les résultats teaser.
- M2 : données d'entrée réelles (ERAA, PECD, prévisions historiques J-1, PNEC, FBMC).
- M3 : suite de tests et historique de développement de la plateforme privée.
- ~~M4 : texte HMMCP~~ : **résolu**, voir §2.3 (Décisions 01/2023 et 02/2026 lues).
- M5 : texte intégral du guide JRC (R6), non récupéré.
- M6 : documents primaires d'Elia (AdeqFlex 2025, méthodologie de flexibilité de court terme) : **accès refusé (HTTP 403)** par téléchargement direct et par récupération web ; seuls des extraits de recherche des documents Elia ont été exploités.

---

## 7. Inventaire d'accès aux sources (vérification du 9/11/2026, après la question « as-tu bien récupéré les documents ? »)

| Source | Accès | Mode de lecture | Usage |
|---|---|---|---|
| FNAM, Décision ACER 05/2025 (consolidée + annexe Ia en suivi de modifications) | ✅ PDF intégral | Texte extrait, art. 1-10 lus intégralement | Référentiel principal |
| Règlement 2024/1747 (art. 19e, 19f) | ✅ HTML intégral EUR-Lex | Texte extrait, art. 19e cité verbatim (§2.1) | Corrections apportées au §2.1 |
| Spécification EU-Flex v1.0 (142 p.), manuel, code | ✅ intégral | Lu ; équations rendues en image p. 92-109 | Objet de l'audit |
| Méthodologie ERAA révisée (Décision ACER 04/2026, annexe Ia, 66 p.) | ✅ PDF intégral | Articles sur le dispatch économique, le Monte-Carlo, l'hydraulique et l'EVA lus | Référentiel ERAA |
| ACER, Décision 07/2025 ERAA 2024 : annexe III technique, annexe Ie (EVA fondée sur les revenus) | ✅ PDF intégral | Chapitre EVA lu | Écart EVA/ED |
| ERAA 2024, rapport exécutif (version approuvée et amendée d'août 2025) | ✅ PDF intégral | Recherché | Contexte |
| ACER, Décision 06/2024 (ERAA 2023) | ✅ PDF intégral | Téléchargé, parcouru | Contexte |
| HMMCP : Décision 01/2023 (annexe 1), Décision 02/2026 | ✅ PDF intégral | Paramètres lus | §2.3 |
| Kittel, Roth, Schill (arXiv 2411.17683) ; Gøtske et al. (arXiv 2404.12178) ; Pinson et al. 2009 ; Lannoye, Flynn, O'Malley (UCD) | ✅ PDF intégral | Affirmations vérifiées par recherche dans le texte | État de l'art |
| Heggarty et al. 2019/2020 (HAL) | ❌ page anti-robot | Résumé seulement | État de l'art (marqué [LIT]) |
| Palmintier & Webster 2014 (MIT DSpace, CORE) | ❌ 404/403 | Résumé et notice seulement | État de l'art (marqué [LIT]) |
| Elia AdeqFlex 2025 et méthodologie de flexibilité de court terme | ❌ 403 (elia.be) | Extraits de recherche des documents Elia | Pratique industrielle (marqué « source secondaire ») |
| Guide JRC (JRC146931) | ❌ non tenté en texte intégral | Notice seulement | Contexte |
| Ruhnau & Qvist 2022 | ⚠️ résumé (DOAJ/IOP) | Résumé | État de l'art |
| Papier ACER « Preparing for the European flexibility needs assessment » (2026) | ❌ introuvable | — | Figures 9-18 non comparées |

### 7.1 Hypothèses méthodologiques de référence extraites des textes intégraux

**Méthodologie ERAA (Décision ACER 04/2026, annexe Ia)**

- **Prévision parfaite** dans le dispatch économique : « Unless the modelling framework allows for a proper characterisation of unforeseen imbalances, the ED shall rely on a "perfect foresight" principle: […] forecast errors of wind, solar, hydro generation, of planned outages as well as of demand are ignored in the ED. Additionally, unplanned outages are assumed to be known in advance. » → **La référence industrielle européenne ignore elle-même les erreurs de prévision** ; EU-Flex va au-delà avec un DA et un ID.
- **MTU** : « The MTU shall be smaller than or equal to an hour. » → le pas horaire est conforme à l'ERAA, mais pas au marché réel (15 min depuis le 1/10/2025) ni à la granularité de la FNAM 10(1)(e).
- **Climat** : PECD avec corrélations inter-zones et inter-temporelles ; scénarios centraux fondés soit sur la meilleure projection climatique, soit sur des années climatiques pondérées, soit sur **au plus les 30 années historiques les plus récentes**.
- **Monte-Carlo** : années MC = années climatiques × tirages de pannes (au moins thermiques et interconnexions) ; **convergence par le coefficient de variation de l'ENS** avec critère d'arrêt ; publication de N et de α(N).
- **Hydraulique** : pré-optimisation *ex ante* à pas grossier (hebdomadaire ou saisonnier) autorisée, respect des trajectoires min/max ; elle doit refléter les « expected operational principles » des exploitants. → La pré-optimisation d'EU-Flex est **conforme au standard ERAA** ; la critique de la valeur de l'eau (revue M7) porte sur la recherche, pas sur l'ERAA.
- **EVA** : soit viabilité fondée sur les revenus (rendement attendu comparé au taux de rendement exigé ou au WACC), soit minimisation du coût total (simplification sous concurrence parfaite). **Atténuation de la réaction des investisseurs aux pics de prix** : par défaut, « partial discounting of Monte Carlo sample years with the highest revenues ».

**ERAA 2024 (annexe III technique de la décision ACER)**

- EVA formulée en minimisation du coût ; **3 scénarios météo dans l'EVA contre 36 dans le dispatch**. L'ACER constate des écarts de LOLE moyenne de **1,7 à 4 h** entre l'EVA et le dispatch, et des revenus gaz différents : « scarcity situations and pricing are not accurately reflected in the EVA, distorting investment signals ».

**Elia (source secondaire)**

- Besoins de flexibilité de court terme en 3 étapes, avec **convolution** des distributions (erreurs de prévision et pannes) ; **percentiles 0,1 % et 99,9 %** ; métriques « slow », « fast » et « ramping » (rampe ≤ 5 min).

**Kittel, Roth, Schill**

- 35 années météo, modélisation **d'été à été** : « our summer-to-summer modeling approach better captures the effects of compound drought events spanning across the turn of years, as compared to models using single calendar years » ; épisode extrême : hiver 1996/97 ; jusqu'à 351 TWh de stockage longue durée.
