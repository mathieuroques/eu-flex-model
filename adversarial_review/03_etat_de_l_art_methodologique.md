# État de l'art méthodologique — référentiel de comparaison pour EU-Flex

> **Note (mise à jour)** : ce document rassemble les notes de recherche. **L'étalon de comparaison est désormais le référentiel autonome [`05_referentiel_etat_de_l_art.md`](05_referentiel_etat_de_l_art.md)**, qui définit l'état de l'art brique par brique et construit l'idéal là où il n'existe pas. L'ERAA y est traité comme un **plancher réglementaire**, jamais comme l'état de l'art industriel.

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

- **ERAA** [FAIT, méthodologie révisée, Décision ACER 04/2026 ; annexe III de la Décision 07/2025] : le dispatch de l'ERAA 2024 tourne sur **36 scénarios météo**, mais l'EVA sur **3** seulement. La méthodologie révisée impose pour les scénarios centraux soit la meilleure projection climatique, soit des années climatiques **pondérées**, soit **au plus les 30 années historiques les plus récentes**. Elle impose aussi un Monte-Carlo (années climatiques × tirages de pannes) avec **critère de convergence** sur le coefficient de variation de l'ENS, et la publication de N et de α(N). Le PECD v4.x de Copernicus (C3S) et d'ENTSO-E intègre des **projections climatiques** ; la v4.1 couvre 1980-2021, la v4.2 soutient l'ERAA 2026 [FAIT, Copernicus CDS / ECMWF].
- **Elia AdeqFlex 2025** [source secondaire : extraits de recherche des documents Elia ; PDF primaires inaccessibles, HTTP 403] : année Monte-Carlo construite sur **200 années climatiques synthétiques** (jeu Météo-France), tirages de disponibilité thermique, convergence imposée par la méthodologie ERAA.
- **Recherche** [FAIT pour Kittel et al., texte intégral] : Kittel, Roth et Schill modélisent 35 années météo **d'été à été**, car « our summer-to-summer modeling approach better captures the effects of compound drought events spanning across the turn of years, as compared to models using single calendar years ». L'épisode le plus extrême est l'hiver 1996/97 ; le stockage longue durée atteint jusqu'à 351 TWh (7,1 % de la demande annuelle).
- **Recherche** [LIT] : les besoins de stockage sont dominés par des événements rares et longs (« Dunkelflaute »). L'année la plus extrême demande **plus de deux fois** le stockage de l'année moyenne ; la période qui dimensionne peut atteindre ~12 semaines. Raisonner sur des années isolées **sous-estime** les besoins (Ruhnau & Qvist 2022). L'événement européen le plus extrême de la série étudiée par Kittel et al. est l'hiver 1996/97. Gøtske et al. testent 62 années météo (1960-2021) : les systèmes dimensionnés sur des années à événements composés sont plus robustes [LIT].
- **Conséquence** : l'unité d'analyse pertinente est la **série pluriannuelle continue**, et non l'année isolée réinitialisée.

### 2.2 Erreurs de prévision et court terme

- **Génération de scénarios d'erreurs** : conversion des erreurs en variable gaussienne multivariée pour en capturer la **dépendance temporelle** (Pinson et al., Wind Energy 12(1) 2009, 51-62), puis copules gaussiennes adaptatives et dépendance **spatio-temporelle** (Tastu, Pinson, Madsen) [LIT].
- **Dimensionnement des réserves** : SO GL art. 157 (couverture probabiliste des déséquilibres ≥ 99 % du temps et incident de dimensionnement). Elia pratique un **dimensionnement dynamique** (apprentissage statistique + Monte-Carlo, risque estimé heure par heure, réestimé mensuellement) [PRATIQUE].
- **Méthode Elia (AdeqFlex)** [source secondaire] : besoins de flexibilité de court terme déterminés en trois étapes, dont une **convolution** des distributions (erreurs de prévision de la charge résiduelle et pannes fortuites, ces dernières issues d'une étude dédiée) ; **percentiles 0,1 % et 99,9 %** pour les besoins à la baisse et à la hausse ; trois métriques : flexibilité « slow », « fast » et « ramping » (sous-ensemble de « fast », réponse ≤ 5 min). La FNAM 10(1)(c) exige précisément de distinguer les deux distributions [FAIT].
- **Queues de distribution** : estimer un P99,9 sur une année horaire revient à s'appuyer sur ~9 points. La pratique statistique pour les quantiles extrêmes est la **théorie des valeurs extrêmes** (dépassements de seuil, loi de Pareto généralisée), ou au minimum le pooling multi-années avec intervalles bootstrap [HYP, standard statistique].
- **Exploitation séquentielle** : les modèles de référence d'intégration EnR simulent l'arrivée progressive de l'information par une **planification glissante stochastique** avec mises à jour de prévision (par ex. WILMAR, Meibom et al., Irlande) [LIT, non consulté en texte intégral].

### 2.3 Résolution temporelle et structure d'information

- **Standard ERAA** [FAIT, méthodologie 2026, art. 4(1)(g)-(h)] : « the MTU shall be smaller than or equal to an hour ». « Unless the modelling framework allows for a proper characterisation of unforeseen imbalances, the ED shall rely on a "perfect foresight" principle » : erreurs de prévision **et pannes fortuites ignorées**. → **Le plancher réglementaire ERAA est en deçà d'EU-Flex** sur la structure d'information. Ce n'est **pas** l'état de l'art : celui-ci (CAISO 15/5 min avec produit de rampe flexible, WILMAR, PLEXOS multi-étapes) est défini dans le référentiel `05`, brique B5.

- **SDAC** est passé au **pas de 15 minutes** (MTU 15 min) le 30 septembre 2025, pour livraison le 1er octobre 2025, dans toutes les zones [FAIT, NEMO Committee, EPEX, Nord Pool]. SIDC et l'équilibrage sont aussi au pas de 15 minutes.
- La FNAM raisonne « par MTU » et distingue la flexibilité « very fast / fast / slow » (5-15 min, 15-60 min, 1 h-J-1) [FAIT].

### 2.4 Engagement des unités et prix

- **UC regroupé** (*clustered UC*) : un entier par cluster de N unités similaires (Palmintier & Webster, IEEE TPWRS 29(3) 2014) donne des erreurs de 0,05 à 0,9 % pour un gain de temps de l'ordre de ×400 [LIT]. Les formulations « tight & compact » (Morales-España et al.) resserrent la relaxation LP [LIT, non vérifié en texte].
- **Point clé** : sur une flotte agrégée, un engagement **binaire** est faux (tout ou rien sur la flotte). La bonne référence est l'entier borné par le nombre d'unités, ou la relaxation LP de cet entier.
- **Formation des prix** : avec engagement non convexe, plusieurs règles coexistent (prix « restreints » à engagement fixé, *convex hull pricing*, prix du LP relaxé). Elles conduisent à des rentes inframarginales différentes [LIT, standard].

### 2.5 Stockage hydraulique saisonnier

- **Pratique** : valeurs de l'eau calculées sous incertitude des apports et de la météo (programmation dynamique stochastique, SDDP ; outils EMPS/ProdRisk nordiques). Antares ne calcule pas lui-même les valeurs de l'eau : il les reçoit en entrée (calculées par des outils externes, par ex. `antaresWaterValues` de RTE) ou utilise une heuristique de courbes guides [FAIT, documentation Antares]. Les valeurs de l'eau sont un **coût d'opportunité** qui entre dans la formation des prix [FAIT]. **Standard ERAA** [FAIT, méthodologie 2026, art. 4(5)(a)] : une pré-optimisation *ex ante* à pas grossier (hebdomadaire ou saisonnier) est admise, avec respect des trajectoires min/max ; elle doit refléter les « expected operational principles » des exploitants. **L'approche d'EU-Flex est donc conforme au standard ERAA** ; seule la recherche va au-delà (valeurs de l'eau stochastiques).
- La planification hydraulique **en prévision parfaite annuelle** est reconnue comme une borne optimiste de la flexibilité hydraulique [HYP, consensus de modélisation].

### 2.6 Viabilité économique (EVA) et équilibre

- **ERAA** [FAIT] : l'EVA est soit une viabilité fondée sur les revenus (rendement attendu comparé au taux de rendement exigé ou au WACC), soit une minimisation du coût total, admise comme simplification (méthodologie 2026, art. EVA §2-6). L'ERAA 2024 a retenu la minimisation du coût, avec une EVA fondée sur les revenus testée en étude de cas. **Atténuation obligatoire de la réaction des investisseurs aux pics de prix**, par défaut une « partial discounting of Monte Carlo sample years with the highest revenues » (§16). L'ACER a refusé les ERAA 2021 et 2022 pour **l'incohérence entre l'EVA et le dispatch** [FAIT, Décision 04/2023]. Pour l'ERAA 2024, elle constate encore des écarts de **LOLE de 1,7 à 4 h** entre EVA et dispatch, dus notamment à **3 scénarios météo dans l'EVA contre 36 dans le dispatch** : « scarcity situations and pricing are not accurately reflected in the EVA, distorting investment signals » [FAIT, annexe III technique]. La révision de la méthodologie (Décision 04/2026) formalise l'aversion au risque (taux de rendement exigés, WACC) [FAIT].
- **Théorie** : en concurrence parfaite, sans plafond de prix et avec tarification de la rareté à la VoLL, l'équilibre d'investissement coïncide avec l'optimum de coût, obtenu par optimisation directe (capacité + dispatch) ou par complémentarité. Avec des plafonds de prix, le niveau d'adéquation de l'équilibre est **fixé par le plafond et la VoLL** (« missing money ») [LIT, standard].
- **Standard de fiabilité** : chaque État membre fixe un standard (LOLE) à partir de la VoLL et du CONE (art. 25 du règlement 2019/943, méthodologie ACER VoLL/CONE/RS) [FAIT, texte du règlement].

### 2.7 Attribution des contributions

- **Identité comptable** : besoin = Σ contributions de toutes les ressources + écrêtement + délestage. C'est la condition minimale de toute décomposition publiable (Heggarty et al. 2020, *Quantifying power system flexibility provision*, Applied Energy 279 : décomposition de la fourniture de flexibilité par ressource) [LIT].
- **Valeur marginale ou contrefactuelle** : retirer ou ajouter une ressource et mesurer la variation de déficit ou de coût (logique de l'ELCC pour la capacité). Les valeurs de Shapley donnent une attribution qui ne dépend pas de l'ordre [LIT, standard].

### 2.8 Validation (V&V)

- Pratique de référence : rétro-simulation (*backcasting*) d'années historiques (prix, flux, dispatch, écrêtement contre ENTSO-E Transparency) ; comparaison avec des modèles de référence (ERAA) ; tests de propriétés (monotonicité) ; tests unitaires et de régression ; publication des écarts. **La spécification EU-Flex décrit exactement ce programme** (§5, étapes 1 à 3, dont la reproduction de l'ERAA 2023), **mais aucun de ses résultats n'est publié** [FAIT].

---

## 3. Grille d'évaluation dérivée (utilisée dans la revue)

| Code | Critère de qualité | Plancher réglementaire (ERAA, texte vérifié) — **pas l'état de l'art** | Meilleures pratiques (détail et brique idéale : référentiel `05`) |
|---|---|---|---|
| Q1 | L'indicateur mesure un **déficit** probabilisé | ENS/LOLE probabilistes (adéquation) ; la FNAM 9(4) et 10(4) transpose la logique à la flexibilité | IRRE (Lannoye) ; convolution (Elia, source secondaire) |
| Q2 | Incertitude climatique | ≤ 30 années récentes, années pondérées ou projections ; MC avec convergence α(N) publiée | 35-62 années, **été à été** (Kittel), événements composés (Gøtske) |
| Q3 | Erreurs de prévision | **Ignorées** dans le dispatch ERAA (prévision parfaite) ; la FNAM 10(1) exige ≥ 2 ans d'historique | Scénarios gaussiens multivariés/copules (Pinson) ; convolution avec les pannes (Elia) |
| Q4 | Structure d'information | **Prévision parfaite**, pannes connues d'avance | Planification glissante stochastique, révélation séquentielle |
| Q5 | Résolution | MTU **≤ 1 h** | 15 min (marché réel depuis le 1/10/2025 ; FNAM 10(1)(e)) |
| Q6 | Engagement des unités | Non prescrit en détail | Clustered UC entier (Palmintier & Webster) ; règle de prix explicite |
| Q7 | Hydraulique | Pré-optimisation *ex ante* à pas grossier, trajectoires min/max | Valeurs de l'eau stochastiques (SDDP) |
| Q8 | EVA | Viabilité fondée sur les revenus ou minimisation du coût ; atténuation des pics (actualisation partielle des années MC les plus rémunératrices) ; cohérence EVA/ED exigée par l'ACER | Équilibre/optimisation multi-années, aversion au risque explicite, ancrage au standard de fiabilité |
| Q9 | Stockage contrefactuel | FNAM 8(10)-(12) : rendement par ratio E/P, moyenne pluriannuelle | Co-optimisation multi-années avec pertes (Ruhnau & Qvist, Kittel) |
| Q10 | Attribution | FNAM 16 (critères d'orientation, peu prescriptifs) | Identité comptable (Heggarty 2020) ; contrefactuel/Shapley |
| Q11 | Incertitude quantifiée | Publication de N et α(N) (ERAA) | Intervalles bootstrap, théorie des valeurs extrêmes |
| Q12 | V&V | Contrôles ACER, publication | Rétro-simulation publiée, benchmark |

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
