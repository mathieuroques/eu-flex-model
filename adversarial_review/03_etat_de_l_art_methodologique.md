# État de l'art méthodologique — référentiel de comparaison pour EU-Flex

*Complément au dossier de contexte (phase 1). Il sert de référentiel à la revue adversariale de la méthode (`04_revue_adversariale_methode.md`). Fiabilité : [FAIT] = source consultée ; [LIT] = résultat publié rapporté d'après son résumé ou ses supports ; [PRATIQUE] = pratique industrielle documentée ; [HYP] = appréciation de l'équipe.*

Le critère de comparaison est **la qualité et la robustesse du résultat**, pas le coût de calcul.

---

## 1. Ce qu'est un « besoin de flexibilité » : trois familles de méthodes

| Famille | Principe | Références | Force | Faiblesse |
|---|---|---|---|---|
| **A. Descriptive (variabilité de la charge résiduelle)** | Décomposer la charge résiduelle par échelle de temps (écarts aux moyennes journalière, hebdomadaire et mensuelle, ou analyse spectrale) et mesurer l'énergie à déplacer | RTE, Bilan prévisionnel 2015 (source des figures 12-13 de la spécification) ; Heggarty, Bourmaud, Girard, Kariniotakis, *Multi-temporal assessment of power system flexibility requirement*, Applied Energy 238 (2019) 1327-1336 (analyse spectrale, sensibilité globale) [LIT] ; FNAM art. 8(5) [FAIT] | Simple, indépendante du parc | **Ne mesure pas une insuffisance** : un besoin n'est pas un déficit. Indicateur invariant à l'offre de flexibilité |
| **B. Adéquation de flexibilité (probabiliste)** | Probabilité ou espérance d'incapacité à suivre une variation de la charge nette, déduite des marges disponibles de toutes les ressources | Lannoye, Flynn, O'Malley, *Evaluation of power system flexibility*, IEEE TPWRS 27(2) 2012 : métrique **IRRE** (*insufficient ramping resource expectation*), dérivée des métriques d'adéquation (LOLE) [LIT] ; extensions avec réseau (2015) [LIT] ; Elia AdeqFlex : erreurs de prévision → pannes → **convolution** des distributions [PRATIQUE] | Mesure un **déficit** avec une probabilité. Cohérente avec les standards de fiabilité | Exige des distributions crédibles et une modélisation fine des marges |
| **C. Optimisation contrefactuelle (valeur ou volume de flexibilité)** | Optimisation conjointe investissement-exploitation sur de nombreuses années météo ; besoin = flexibilité retenue par l'optimum ou nécessaire pour atteindre une cible | Ruhnau & Qvist, ERL 17 (2022) 044018 [LIT] ; Kittel, Roth, Schill, *Coping with the Dunkelflaute* (arXiv 2411.17683) [LIT] ; Gøtske et al., Nat. Commun. (2024) 10.1038/s41467-024-54853-3 [LIT] ; FNAM 8(10)-(12) [FAIT] | Endogénéise les arbitrages entre technologies, avec pertes réelles | Dépend des coûts et du périmètre. Exige beaucoup d'années météo |

**La FNAM combine les trois familles** : A pour 8(5) et 9(1) ; B pour 9(4), 10(4) et les « besoins non couverts » ; C pour 8(10)-(12). **[HYP]** Une implémentation de qualité doit donc exceller sur B (probabilités, marges, distributions) et sur C (multi-années, rendements réels). A est le volet facile.

---

## 2. Bonnes pratiques par composant

### 2.1 Incertitude climatique et nombre d'années

- **ERAA** : 35-36 années climatiques historiques (PECD), Monte-Carlo de pannes, critère de **convergence statistique** du nombre de tirages [PRATIQUE]. Le PECD v4.x de Copernicus (C3S) et d'ENTSO-E intègre désormais des **projections climatiques**, et non plus seulement des réanalyses historiques. La v4.1 couvre 1980-2021 ; la v4.2 soutient l'ERAA 2026 [FAIT, Copernicus CDS / ECMWF].
- **Elia AdeqFlex 2025** : année Monte-Carlo construite sur **200 années climatiques synthétiques** (jeu Météo-France), tirages de disponibilité thermique, convergence imposée par la méthodologie ERAA [PRATIQUE].
- **Recherche** : les besoins de stockage sont dominés par des événements rares et longs (« Dunkelflaute »). L'année la plus extrême demande **plus de deux fois** le stockage de l'année moyenne ; la période qui dimensionne peut atteindre ~12 semaines. Raisonner sur des années isolées **sous-estime** les besoins (Ruhnau & Qvist 2022). L'événement européen le plus extrême de la série étudiée par Kittel et al. est l'hiver 1996/97. Gøtske et al. testent 62 années météo (1960-2021) : les systèmes dimensionnés sur des années à événements composés sont plus robustes [LIT].
- **Conséquence** : l'unité d'analyse pertinente est la **série pluriannuelle continue**, et non l'année isolée réinitialisée.

### 2.2 Erreurs de prévision et court terme

- **Génération de scénarios d'erreurs** : conversion des erreurs en variable gaussienne multivariée pour en capturer la **dépendance temporelle** (Pinson et al., Wind Energy 12(1) 2009, 51-62), puis copules gaussiennes adaptatives et dépendance **spatio-temporelle** (Tastu, Pinson, Madsen) [LIT].
- **Dimensionnement des réserves** : SO GL art. 157 (couverture probabiliste des déséquilibres ≥ 99 % du temps et incident de dimensionnement). Elia pratique un **dimensionnement dynamique** (apprentissage statistique + Monte-Carlo, risque estimé heure par heure, réestimé mensuellement) [PRATIQUE].
- **Méthode Elia (AdeqFlex)** : distribution des erreurs de charge résiduelle, puis distribution des pannes fortuites, puis **convolution**, puis besoins de flexibilité par niveau de rapidité [PRATIQUE]. FNAM 10(1)(c) exige précisément de distinguer les deux distributions [FAIT].
- **Queues de distribution** : estimer un P99,9 sur une année horaire revient à s'appuyer sur ~9 points. La pratique statistique pour les quantiles extrêmes est la **théorie des valeurs extrêmes** (dépassements de seuil, loi de Pareto généralisée), ou au minimum le pooling multi-années avec intervalles bootstrap [HYP, standard statistique].
- **Exploitation séquentielle** : les modèles de référence d'intégration EnR simulent l'arrivée progressive de l'information par une **planification glissante stochastique** avec mises à jour de prévision (par ex. WILMAR, Meibom et al., Irlande) [LIT, non consulté en texte intégral].

### 2.3 Résolution temporelle

- **SDAC** est passé au **pas de 15 minutes** (MTU 15 min) le 30 septembre 2025, pour livraison le 1er octobre 2025, dans toutes les zones [FAIT, NEMO Committee, EPEX, Nord Pool]. SIDC et l'équilibrage sont aussi au pas de 15 minutes.
- La FNAM raisonne « par MTU » et distingue la flexibilité « very fast / fast / slow » (5-15 min, 15-60 min, 1 h-J-1) [FAIT].

### 2.4 Engagement des unités et prix

- **UC regroupé** (*clustered UC*) : un entier par cluster de N unités similaires (Palmintier & Webster, IEEE TPWRS 29(3) 2014) donne des erreurs de 0,05 à 0,9 % pour un gain de temps de l'ordre de ×400 [LIT]. Les formulations « tight & compact » (Morales-España et al.) resserrent la relaxation LP [LIT, non vérifié en texte].
- **Point clé** : sur une flotte agrégée, un engagement **binaire** est faux (tout ou rien sur la flotte). La bonne référence est l'entier borné par le nombre d'unités, ou la relaxation LP de cet entier.
- **Formation des prix** : avec engagement non convexe, plusieurs règles coexistent (prix « restreints » à engagement fixé, *convex hull pricing*, prix du LP relaxé). Elles conduisent à des rentes inframarginales différentes [LIT, standard].

### 2.5 Stockage hydraulique saisonnier

- **Pratique** : valeurs de l'eau calculées sous incertitude des apports et de la météo (programmation dynamique stochastique, SDDP ; outils EMPS/ProdRisk nordiques). Antares ne calcule pas lui-même les valeurs de l'eau : il les reçoit en entrée (calculées par des outils externes, par ex. `antaresWaterValues` de RTE) ou utilise une heuristique de courbes guides [FAIT, documentation Antares]. Les valeurs de l'eau sont un **coût d'opportunité** qui entre dans la formation des prix [FAIT].
- La planification hydraulique **en prévision parfaite annuelle** est reconnue comme une borne optimiste de la flexibilité hydraulique [HYP, consensus de modélisation].

### 2.6 Viabilité économique (EVA) et équilibre

- **ERAA** : EVA avec années climatiques pondérées. L'ACER a refusé les ERAA 2021 et 2022, notamment pour **l'incohérence entre l'EVA et le dispatch économique** [FAIT, Décision ACER 04/2023]. Elle a approuvé l'ERAA 2023 en l'amendant (scénario central visant à réduire le biais entre EVA et ED ; scénario de sensibilité qui expose les investisseurs à moins de pics de prix) [FAIT, Décision 06/2024]. Pour l'ERAA 2024 (Décision 07/2025), une **EVA fondée sur les revenus** a été testée en étude de cas, jugée encore immature [FAIT]. La révision de la méthodologie ERAA (Décision ACER 04/2026) traite explicitement l'**aversion au risque** des investisseurs par des taux de rendement exigés (*hurdle rates*) [FAIT, titre et résumé].
- **Théorie** : en concurrence parfaite, sans plafond de prix et avec tarification de la rareté à la VoLL, l'équilibre d'investissement coïncide avec l'optimum de coût, obtenu par optimisation directe (capacité + dispatch) ou par complémentarité. Avec des plafonds de prix, le niveau d'adéquation de l'équilibre est **fixé par le plafond et la VoLL** (« missing money ») [LIT, standard].
- **Standard de fiabilité** : chaque État membre fixe un standard (LOLE) à partir de la VoLL et du CONE (art. 25 du règlement 2019/943, méthodologie ACER VoLL/CONE/RS) [FAIT, texte du règlement].

### 2.7 Attribution des contributions

- **Identité comptable** : besoin = Σ contributions de toutes les ressources + écrêtement + délestage. C'est la condition minimale de toute décomposition publiable (Heggarty et al. 2020, *Quantifying power system flexibility provision*, Applied Energy 279 : décomposition de la fourniture de flexibilité par ressource) [LIT].
- **Valeur marginale ou contrefactuelle** : retirer ou ajouter une ressource et mesurer la variation de déficit ou de coût (logique de l'ELCC pour la capacité). Les valeurs de Shapley donnent une attribution qui ne dépend pas de l'ordre [LIT, standard].

### 2.8 Validation (V&V)

- Pratique de référence : rétro-simulation (*backcasting*) d'années historiques (prix, flux, dispatch, écrêtement contre ENTSO-E Transparency) ; comparaison avec des modèles de référence (ERAA) ; tests de propriétés (monotonicité) ; tests unitaires et de régression ; publication des écarts. **La spécification EU-Flex décrit exactement ce programme** (§5, étapes 1 à 3, dont la reproduction de l'ERAA 2023), **mais aucun de ses résultats n'est publié** [FAIT].

---

## 3. Grille d'évaluation dérivée (utilisée dans la revue)

| Code | Critère de qualité | Référence de bonne pratique |
|---|---|---|
| Q1 | L'indicateur mesure un **déficit** (non couvert), probabilisé | Famille B, FNAM 9(4), 10(4) |
| Q2 | Incertitude climatique : ≥ 30 années, séries continues, événements extrêmes, convergence statistique | ERAA, Elia, Ruhnau & Qvist, Gøtske |
| Q3 | Erreurs de prévision empiriques, dépendance spatio-temporelle, conditionnelles, séparées des pannes | FNAM 10(1), Pinson, Elia |
| Q4 | Révélation séquentielle de l'information (pas de prévision parfaite intrajournalière) | Planification glissante stochastique |
| Q5 | Résolution au MTU de marché (15 min) | SDAC/SIDC depuis 2025, FNAM 10(1)(e) |
| Q6 | Engagement des unités adapté à l'agrégation (clustered UC) ; règle de prix explicite | Palmintier & Webster |
| Q7 | Hydraulique valorisée sous incertitude (valeurs de l'eau) | SDDP, Antares + valeurs de l'eau |
| Q8 | EVA cohérente avec l'ED, équilibre bien défini, niveau d'adéquation ancré au standard de fiabilité | ERAA (décisions ACER), art. 25 |
| Q9 | Stockage contrefactuel réaliste (rendements, multi-années) | FNAM 8(10), Ruhnau & Qvist |
| Q10 | Attribution conservative (identité comptable) et/ou contrefactuelle | Heggarty 2020, ELCC/Shapley |
| Q11 | Incertitude des résultats quantifiée (intervalles) | Standard statistique |
| Q12 | V&V publiés (backcasting, benchmark ERAA) | Spécification §5 elle-même |

## 4. Sources

- RTE, *Bilan prévisionnel de l'équilibre offre-demande* (2015).
- Heggarty, Bourmaud, Girard, Kariniotakis (2019), Applied Energy 238:1327-1336 — https://hal.archives-ouvertes.fr/hal-01998837 ; (2020), Applied Energy 279 — https://ideas.repec.org/a/eee/appene/v279y2020ics030626192031326x.html
- Lannoye, Flynn, O'Malley (2012), IEEE TPWRS, DOI 10.1109/TPWRS.2011.2177280 — https://researchrepository.ucd.ie/handle/10197/4753
- Palmintier & Webster (2014), IEEE TPWRS 29(3) — https://dspace.mit.edu/handle/1721.1/102960
- Pinson et al. (2009), Wind Energy 12(1):51-62 — https://backend.orbit.dtu.dk/ws/files/4900902/pinsonetal_wpfscenarios_fin.pdf
- Ruhnau & Qvist (2022), ERL 17 044018 — https://doaj.org/article/3f8dab1761d34116826fba55b72b211f
- Kittel, Roth, Schill, *Coping with the Dunkelflaute* — https://arxiv.org/pdf/2411.17683
- Gøtske, Andresen, Neumann, Victoria (2024), Nat. Commun. — https://arxiv.org/abs/2404.12178v1
- Elia, AdeqFlex 2025 (consultation, annexes) — https://elia.be/-/media/project/elia/elia-site/public-consultations/2024/20241104_public-consultation-on-the-methodology-the-basis-data-and-scenarios/adeqflex25_appendix_g_adequacystudy.pdf ; dimensionnement dynamique FRR — https://www.elia.be/-/media/project/elia/elia-site/public-consultations/2021/22122021_dynmeans_finalreport.pdf ; De Vos et al. (2019) — https://nicolasstevens.github.io/files/DeVos2019.pdf
- ACER, Décisions ERAA : 04/2023 (ERAA 2022), 06/2024 (ERAA 2023), 07/2025 (ERAA 2024, annexes III et Ie), 04/2026 (méthodologie) — https://www.acer.europa.eu/sites/default/files/documents/Individual%20Decisions/ACER_Decision_06-2024_ERAA_2023.pdf ; https://www.acer.europa.eu/sites/default/files/documents/Individual%20Decisions_annex/ACER-Decision-07-2025-ERAA-2024-Annex-Ie-Case-Study-Revenue-Based-EVA_0.pdf
- Copernicus C3S, PECD — https://cds.climate.copernicus.eu/datasets/sis-energy-pecd
- Antares Simulator, *Water values* — https://antares-doc.readthedocs.io/en/latest/reference/water-values/
- NEMO Committee, *15-minute MTU in SDAC was implemented* — https://nemo-committee.eu/assets/files/15-minute-mtu-in-sdac-was-implemented.pdf
