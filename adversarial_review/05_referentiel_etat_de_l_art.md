# Référentiel d'état de l'art construit — évaluation des besoins de flexibilité d'un système électrique

*Document autonome. Il ne parle pas d'EU-Flex : il définit l'étalon contre lequel EU-Flex est ensuite évalué (`04_revue_adversariale_methode.md`, §5). Date : 9 novembre 2026.*

---

## 0. Démarche

1. **L'ERAA n'est pas l'état de l'art.** La méthodologie ERAA est un **cadre réglementaire minimal** pour l'adéquation (par exemple, elle admet explicitement la prévision parfaite et un pas de temps d'une heure). Elle sert ici de **plancher réglementaire**, jamais d'étalon de qualité.
2. **Pour chaque brique de méthode, quatre questions :**
   - (a) **Meilleures pratiques observées**, chez les opérateurs les plus avancés (CAISO, EirGrid, Elia, RTE, AEMO, NESO, gestionnaires nordiques), les éditeurs (PLEXOS, SINTEF, GenX, Antares) et la recherche.
   - (b) **Existe-t-il un consensus ?** Trois réponses possibles : *ÉTABLI* (pratique convergente et documentée), *ÉMERGENT* (pratiques avancées mais hétérogènes), *ABSENT* (aucune pratique ne couvre l'objet).
   - (c) **Brique idéale** : spécification normative (« doit »). Lorsque le consensus est absent ou partiel, la brique est **[CONSTRUITE]** à partir de principes premiers (statistique, économie, physique du système) et des pratiques partielles disponibles.
   - (d) **Critères de vérification** : tests d'acceptation qui permettent de juger si un outil atteint la brique.
3. **Niveau de preuve des sources** :
   - [T] texte intégral lu ;
   - [E] extraits ou documentation officielle consultés via la recherche ;
   - [R] résumé seulement.
4. **Objectif de référence** : quantifier des **besoins de flexibilité**, notamment **non couverts**, par zone, par région et au niveau de l'Union, par échelle de temps de 5 minutes à la saison. L'incertitude doit être quantifiée, l'attribution défendable par ressource, et le cadre utilisable pour des recommandations (art. 19e(7) du règlement 2019/943, FNAM).

---

## 1. Principes transverses (non négociables)

| # | Principe | Justification |
|---|---|---|
| P1 | **Validité de construction** : chaque indicateur mesure explicitement soit une *variabilité* (descriptif), soit un *déficit* (adéquation de flexibilité), soit une *valeur* (marginale ou contrefactuelle). Il ne mélange jamais ces catégories | Sinon l'indicateur est ininterprétable pour la décision |
| P2 | **Information réaliste** : aucune décision ne peut utiliser une information indisponible à l'instant où elle est prise dans la réalité | Sinon, biais systématique vers l'optimisme sur l'imprévu |
| P3 | **Propagation de l'incertitude** : climat, prévisions, pannes et conventions de modélisation sont échantillonnés ou testés, et les résultats publiés avec intervalles | Les décisions portent sur des queues de distribution (P99,9, années extrêmes) |
| P4 | **Cohérence comptable** : toute décomposition se referme sur son total (identité de bilan) | Sinon l'attribution absorbe des erreurs |
| P5 | **Falsifiabilité** : tests de propriétés (monotonicité, invariances), rétro-simulation et benchmark publiés | Seule garantie externe de qualité |
| P6 | **Robustesse aux conventions** : l'effet sur les résultats de chaque convention non physique (règles de prix, relaxations, horizons) est mesuré et borné | Sinon les conventions dominent la physique |

---

## 2. Briques

### B1 — Objet et métriques du besoin de flexibilité · Consensus : **ABSENT** (pratiques partielles) → **[CONSTRUITE]**

**Pratiques observées**
- **Descriptif par échelles de temps** : RTE (Bilan prévisionnel) ; JRC/METIS (Koolen, De Felice, Busch 2023) : besoins journaliers, hebdomadaires et mensuels, de l'ordre de 11 % de la demande de l'UE en 2021 et de 24 % en 2030 selon les synthèses [E] ; Heggarty et al. 2019, analyse spectrale [R].
- **Exigences opérationnelles de rampe** :
  - CAISO, *Flexible Capacity Needs Assessment* : rampe maximale de charge nette sur 3 heures, par mois, calculée sur des données à la minute, plus le maximum entre la contingence la plus sévère et 3,5 % de la pointe [E] ;
  - EirGrid/SONI, *Ramping Margin* RM1/RM3/RM8 : capacité à monter en 1, 3 ou 8 h et à tenir 2, 5 ou 8 h, avec des exigences calculées à partir de la plus grosse perte d'injection, de l'erreur de prévision de charge, d'un terme d'incertitude EnR et des interconnexions [E].
- **Probabiliste** :
  - Elia : convolution des distributions d'erreurs de prévision et de pannes, percentiles 0,1 % et 99,9 %, flexibilité *slow*, *fast* et *ramping* (≤ 5 min) [E, source secondaire] ;
  - recherche : IRRE (Lannoye, Flynn, O'Malley) [T], *periods of flexibility deficit*, métriques combinant puissance, énergie et rampe évaluées par Monte-Carlo (Cardiff) [E].
- **Adéquation moderne** : ESIG, *Redefining Resource Adequacy* : simulation chronologique sur de nombreuses années ; abandon d'un critère unique ; critère multi-métrique sur la **taille, la fréquence, la durée et le moment** des déficits ; quantification explicite des queues [E].

**Brique idéale [CONSTRUITE]** : quatre couches d'indicateurs, explicitement séparées (P1).

1. **L1 — Variabilité (descriptif)** : décomposition de la charge résiduelle par bande de temps (indicateurs FNAM 8(5) et décomposition spectrale ou en ondelettes de contrôle), au niveau zone, région et UE. Usage : contexte, jamais conclusion sur une insuffisance.
2. **L2 — Enveloppes d'exigence** : pour chaque horizon h ∈ {5 min, 15 min, 1 h, 3 h, 8 h, 24 h, semaine, saison}, distribution conditionnelle (heure, saison, régime météo) des variations de charge résiduelle **et** des erreurs de prévision à l'horizon h. On retient leurs quantiles (dont P0,1 et P99,9), avec la fréquence et la durée des dépassements. C'est la généralisation multi-horizons de CAISO 3 h et d'EirGrid RM1/3/8.
3. **L3 — Adéquation de flexibilité (déficit)** : par simulation chronologique probabiliste (B2-B5), pour chaque horizon h :
   - espérance d'énergie de flexibilité non fournie (EUFE_h) ;
   - fréquence, durée, taille et moment des événements de déficit (multi-métrique ESIG) ;
   - **attribution causale** du déficit : rampe, erreur de prévision, panne, réseau ;
   - séparation entre écrêtement EnR et ENS induits, avec la convention FNAM du maximum par MTU pour éviter le double comptage.
4. **L4 — Valeur** : valeur marginale de la flexibilité par horizon (duales des contraintes de bilan, de rampe et de réserve ; variation du coût et du déficit par MW ajouté) et courbes de besoin en fonction du niveau de fiabilité visé.

**Vérification**
- (i) L1 et L2 sont invariants à l'offre de flexibilité ; L3 est **non croissant** quand on ajoute de la capacité flexible (test de monotonicité).
- (ii) La somme des déficits par cause reconstruit le déficit total.
- (iii) Les indicateurs existent aux trois niveaux spatiaux, et l'écart entre la somme zonale et la valeur régionale (mutualisation) est publié.

---

### B2 — Climat et météo · Consensus : **ÉMERGENT** (convergence vers les grands ensembles)

**Pratiques observées**
- **RTE**, *Futurs énergétiques 2050* : **200 années climatiques** Météo-France (ARPEGE-Climat) à climat constant, pour 2000 et pour 2050 sous RCP4.5 et RCP8.5 ; stress-tests climatiques (canicule, sécheresse, grand froid, absence de vent en Europe continentale) [E].
- **Elia** : 200 années synthétiques (base Météo-France) [E].
- **AEMO** : années de référence météo glissantes (14 années historiques) dans le modèle ISP PLEXOS [E].
- **Recherche** :
  - 62 années (Gøtske et al.) [T] ;
  - 35 années modélisées d'été à été pour capter les épisodes qui chevauchent l'hiver (Kittel, Roth, Schill) [T] ;
  - 39 années (Dowling et al., Joule 2020) [E] ;
  - 80 années (1941-2021) et identification des événements par les prix duaux (arXiv 2508.05163) [E] ;
  - grands ensembles CMIP6 pour les événements froids sans vent composés [E] ;
  - stress-tests « reasonable worst case » pour le Comité britannique sur le changement climatique (Bloomfield, 2025) [E] ;
  - générateurs de météo synthétique à ensembles illimités [E].

**Brique idéale**
1. Ensemble de **≥ 100 à 200 années** cohérentes avec le **climat de l'année cible** (projections), pas seulement l'historique, avec cohérence spatiale et temporelle entre vent, soleil, hydraulique, température et demande.
2. Simulation **chaînée** (état des stockages transmis) ou en années hydrologiques ou d'été à été, pour ne jamais couper un épisode hivernal.
3. **Échantillonnage d'importance** des épisodes extrêmes, complété de **scénarios de stress narratifs** (*storylines*).
4. Sélection de sous-ensembles représentatifs **validée** contre l'ensemble complet, sur les métriques de queue et pas seulement sur les moyennes.

**Vérification** : convergence des métriques L3 en fonction du nombre d'années (courbe publiée) ; écart sous-ensemble / ensemble sur P99 et P99,9 inférieur à une tolérance déclarée ; aucun événement de déficit tronqué par une frontière d'année.

---

### B3 — Incertitude de prévision · Consensus : **ÉMERGENT** pour l'opérationnel, **ABSENT** pour la projection à 5-10 ans → **[CONSTRUITE]**

**Pratiques observées**
- **CAISO**, *Flexible Ramping Product* : passage d'histogrammes à une **régression quantile** conditionnée par les prévisions et la météo (modèle Mosaic), percentiles conditionnels selon les conditions (en production depuis le 21/12/2023, avec un 97,5e percentile en conditions froides) [E].
- **Elia** : dimensionnement dynamique quotidien des réserves par apprentissage statistique et Monte-Carlo, réestimé régulièrement [E].
- **Recherche** :
  - scénarios d'erreurs par gaussienne multivariée ou copule, avec dépendance temporelle (Pinson et al. 2009) [T] puis spatio-temporelle (Tastu, Pinson, Madsen) [R] ;
  - charge nette régionale en Grande-Bretagne avec queues modélisées par une **loi de Pareto généralisée conditionnelle**, à des probabilités de 0,01 à 0,25 % liées au rapport coût de réserve / VoLL (arXiv 2103.10335) [E].
- **Projection vers l'avenir** : pratiques rudimentaires (erreur en % de la capacité) ; l'effet de la composition du parc (éolien en mer contre terrestre) et de la dispersion géographique est documenté (Schönheit ; Mauch et al.) [E] ; l'amélioration des prévisions réduirait de 30 % les réserves liées aux erreurs solaires dans une étude du sud-est des États-Unis [E].

**Brique idéale [CONSTRUITE]**
1. Base empirique : erreurs historiques par zone × filière × **horizon de prévision** (J-1 12h, guichets ID, H-1, 15 min), sur ≥ 2-3 ans (FNAM 10(1) : ≥ 2 ans).
2. Modèle **conditionnel** (régression quantile ou distributionnelle) selon le niveau prévu, l'heure, la saison et le régime météo ; **dépendance spatio-temporelle** par copule ; **queues par théorie des valeurs extrêmes** (dépassements de seuil).
3. **Projection à l'année cible** : agrégation pondérée par les capacités futures, en tenant compte de la dispersion géographique (lissage) et de la composition du parc ; trajectoire explicite d'amélioration des prévisions, avec **sensibilités hautes et basses**.
4. Production de **N réalisations** par année climatique, cohérentes avec la météo (B2), et non une seule série.
5. Distributions d'erreurs **séparées** de celles des pannes (FNAM 10(1)(c)), avec recombinaison par convolution ou simulation (B4).

**Vérification** : rétro-test hors échantillon (fiabilité des quantiles, *pinball loss*, couverture P99/P99,9) ; dépendance spatiale reproduite (matrices de corrélation entre zones) ; analyse de sensibilité à l'hypothèse d'amélioration des prévisions.

---

### B4 — Indisponibilités fortuites et contingences · Consensus : **ÉTABLI**

**Pratiques observées** : Monte-Carlo de pannes (ERAA, outils MARS et Antares) [T/E] ; dimensionnement sur la plus grosse perte d'injection (EirGrid ; SO GL art. 157 pour l'incident de dimensionnement) [E] ; convolution avec les erreurs de prévision (Elia) [E].

**Brique idéale** : processus de Markov à deux états **par unité**, avec taux de défaillance et durée moyenne de réparation (MTTR), y compris interconnexions et défaillances de mode commun ; tirages chronologiques en **nombre suffisant pour converger** (critère publié) ; contingences dimensionnantes explicites ; séparation des causes dans l'attribution L3.

**Vérification** : taux de disponibilité simulés égaux aux taux d'entrée ; distribution des durées de panne conforme ; convergence.

---

### B5 — Structure d'information et séquence des marchés · Consensus : **ÉTABLI** en recherche, **ÉMERGENT** dans l'industrie

**Pratiques observées**
- **WILMAR** (Meibom et al., IEEE TPWRS 2011, étude All-Island Grid) : **planification glissante stochastique**, replanifiée à mesure que les prévisions s'améliorent, avec arbre de scénarios d'erreurs vent/charge et engagement entier [E]. Tuohy et al. 2009 : l'ordonnancement stochastique est moins coûteux que le déterministe (de l'ordre de 0,25 %) ; mi-mérite, pointe et interconnexion sont les plus exposés [E].
- **PLEXOS** : moteur unique long terme / moyen terme / court terme / quasi temps réel ; décomposition des contraintes moyen terme en cibles court terme ; UC stochastique en deux étapes ou multi-étapes [E].
- **CAISO** : séquence DA → RUC → marché à 15 min → dispatch temps réel à **5 min**, avec produit de rampe flexible couvrant l'incertitude entre le marché à 15 min et le dispatch à 5 min [E].

**Brique idéale**
1. Séquence de décisions **aux guichets réels** : DA (clôture J-1 12h, MTU 15 min), ID (enchères et continu, avec **mises à jour de prévision** par exemple à H-6, H-3 et H-1), équilibrage (5-15 min) avec réserves **dimensionnées ex ante** (SO GL 157 ou dimensionnement dynamique) puis **activées** contre l'erreur résiduelle.
2. À chaque étape, seule l'information disponible à ce moment est utilisée (P2). L'erreur se révèle **progressivement** (processus de prévision glissant de B3).
3. DA déterministe avec réserves, ou stochastique ou robuste ; l'écart par rapport à une stratégie de référence est mesuré.
4. Les déficits L3 sont mesurés **à l'étape temps réel**.

**Vérification** : test d'« oracle » (relancer avec révélation parfaite : l'écart mesure la valeur de l'information et doit être publié) ; cohérence des volumes de réserves activées avec les déséquilibres historiques (B14).

---

### B6 — Résolution temporelle · Consensus : **ÉTABLI** (sub-horaire)

**Pratiques observées**
- Marchés : SDAC au pas de 15 min depuis le 1/10/2025 [E] ; CAISO à 5 min en temps réel [E] ; AEMO, règlement à 5 min [connaissance générale].
- Recherche : Deane, Drayton, Ó Gallachóir (Applied Energy 2014) : système irlandais simulé à 5, 15, 30 et 60 min. La résolution fine capte davantage de variabilité et d'inflexibilité thermique (cyclage, rampes) manquées à l'heure, et donne des coûts plus réalistes [E]. Jusqu'à +100 % d'usage de batteries à 5 min par rapport à l'heure (source auteur, non vérifiée) [E].

**Brique idéale** : MTU de **15 min** dans toutes les étapes de marché ; **5 min** (ou une couche statistique minute) pour l'équilibrage et la flexibilité *very fast* (FNAM 10(1)(e)) ; profils infra-horaires de charge et d'EnR mesurés ou désagrégés statistiquement ; rampes et contraintes de démarrage exprimées dans cette résolution.

**Vérification** : comparaison 60 / 15 / 5 min sur des semaines échantillonnées, avec publication de l'écart sur les métriques L2 et L3 et sur la valeur des actifs rapides.

---

### B7 — Engagement des unités et formation des prix · Consensus : **ÉTABLI** pour l'UC, **ÉMERGENT** pour les prix

**Pratiques observées**
- **UC « tight & compact »** (Morales-España, Latorre, Ramos, IEEE TPWRS 2013), y compris les trajectoires de démarrage et d'arrêt ; testé sur 28 à 1 870 unités [E].
- **Clustered UC** à variable entière par cluster (Palmintier & Webster, IEEE TPWRS 2014) : erreurs de 0,05 à 0,9 % pour ~400 fois moins de temps de calcul [R].
- **PLEXOS** : court terme en MIP chronologique [E].
- **Prix** : prix restreints à engagement fixé, *convex hull pricing*, paiements complémentaires (*uplift*) ; aucun consensus réglementaire.

**Brique idéale** : clustered UC **entier** (nombre d'unités en ligne par cluster) en formulation serrée ; relaxation LP admise **seulement** si l'écart à l'entier est borné et publié ; règle de prix explicite ; *uplift* intégré aux revenus (B10) ; duales de sommet (crossover) pour des prix reproductibles.

**Vérification** : écart entre clustered UC entier, relaxation LP et UC unitaire sur des semaines tests (coût, démarrages, prix, ENS) ; aucun binaire appliqué à une flotte agrégée.

---

### B8 — Stockage, hydraulique et flexibilité de la demande · Consensus : **ÉTABLI** pour l'hydraulique (SDDP), **ÉMERGENT** pour batteries et DSR

**Pratiques observées**
- **ProdRisk** (SINTEF, SDDP) : en usage opérationnel chez de nombreux grands producteurs hydrauliques nordiques ; produit des **valeurs de l'eau couplées** (coupes) pour l'ordonnancement court terme [E]. SDDP est décrit comme la méthode la plus utilisée pour la planification hydraulique de moyen terme sur le marché nordique [E]. EMPS (agrégation de réservoirs) reconnu comme limité [E].
- **PLEXOS** : trajectoires moyen terme sous incertitude des apports ; surface de valeurs de l'eau par coupes de Benders [E].
- **Antares** : valeurs de l'eau fournies en entrée (calcul externe) ou heuristique de courbes guides [T].

**Brique idéale** : valeurs de l'eau calculées par SDDP sous l'incertitude des apports **et** de la météo (cohérente avec B2), injectées comme coût d'opportunité dans toutes les étapes de marché ; batteries et stockage longue durée avec état de charge chronologique et valeur d'opportunité dépendant de l'état ; DSR avec contraintes d'énergie, de report, d'effet rebond et de disponibilité saisonnière ; aucune trajectoire en prévision parfaite comme politique.

**Vérification** : comparaison des politiques SDDP et prévision parfaite (écart de flexibilité hydraulique publié) ; cohérence des niveaux de réservoir simulés avec les historiques sur années comparables (B14).

---

### B9 — Réseau et échanges transfrontaliers · Consensus : **ÉTABLI** (flow-based dans le Core et la zone nordique)

**Brique idéale** : domaines flow-based par année cible (avec incertitude sur les marges disponibles), NTC hors des régions concernées ; mutualisation transfrontalière de l'équilibrage et des réserves (plateformes européennes, par ex. MARI et PICASSO) ; contraintes de distribution intégrées selon la FNAM 13-14 ; indicateurs de mutualisation (B1 L1/L3).

**Vérification** : rétro-simulation des flux et des écarts de prix historiques (B14) ; sensibilité NTC contre flow-based.

---

### B10 — Investissement, viabilité et niveau d'adéquation · Consensus : **ÉMERGENT** → **[CONSTRUITE]**

**Pratiques observées**
- **Équilibre stochastique avec aversion au risque** : Ehrenmann & Smeers (Operations Research 2011), complémentarité et CVaR. Le risque accroît la pénurie de capacité dans un marché *energy-only* à plafond bas [E]. Muñoz et al. 2017, planification pondérée par la CVaR [E]. Équilibre stochastique à deux étapes pour le stockage longue durée et les marchés de risque manquants (arXiv 2510.13514) [E].
- **Co-optimisation investissement-exploitation** à résolution opérationnelle : GenX (avec réduction temporelle par k-means ou k-medoids), PyPSA, ReEDS [E].
- **Réglementaire (plancher)** : ERAA (viabilité fondée sur les revenus ou minimisation du coût ; atténuation des pics par actualisation partielle des années les plus rémunératrices). L'ACER constate pour l'ERAA 2024 un écart de LOLE de 1,7 à 4 h entre EVA et dispatch (3 contre 36 scénarios météo) [T].

**Brique idéale [CONSTRUITE]**
1. Investissement formulé comme **équilibre stochastique** (ou co-optimisation équivalente sous concurrence parfaite), avec **mesure de risque explicite** (CVaR ou taux de rendement exigés différenciés), sur **les mêmes années, tirages et résolution** que le dispatch. À défaut, une réduction **validée** par écart borné.
2. Contraintes de marché et de politique explicites : plafonds de prix et règle HMMCP en vigueur, mécanismes de capacité, objectifs EnR.
3. **Niveau d'adéquation** : soit ancré au **standard de fiabilité** national (VoLL/CONE, art. 25 du règlement 2019/943), soit **balayé** (courbes de besoins de flexibilité en fonction du niveau de fiabilité et des hypothèses de prix), conformément à l'**art. 19e(2)(a)** (« different assumptions in respect to electricity market prices »).
4. Résolution par un algorithme à **convergence garantie** (complémentarité, décomposition, ou bissection et pas adaptatif), avec diagnostic publié : statut, écart résiduel et actifs saturés à leurs bornes.

**Vérification** : propriétés (baisse du coût d'investissement ⇒ capacité non décroissante) ; écart EVA/dispatch sur la LOLE inférieur à une tolérance publiée ; sensibilité des besoins L3 au couple VoLL/plafond.

---

### B11 — Besoin de stockage pour l'intégration EnR (contrefactuel) · Consensus : **ÉTABLI** en recherche

**Pratiques observées**
- Ruhnau & Qvist (2022) : 35 ans ; pertes et limites de charge allongent la période dimensionnante à ~12 semaines ; l'année extrême demande plus de deux fois le stockage de l'année moyenne [R].
- Dowling et al. (Joule 2020) : 39 ans ; le stockage longue durée sert à l'inter-saisonnier et au **pluriannuel** [E].
- Sepulveda et al. (Nature Energy 2021) : **coût de l'énergie stockée et rendement de décharge** sont les paramètres les plus déterminants ; impact maximal pour des durées supérieures à 100 h [E].
- Kittel et al. : jusqu'à 351 TWh de stockage longue durée (7,1 % de la demande) pour l'épisode extrême [T].

**Brique idéale** : co-optimisation de classes de stockage **technologiquement neutres** (ratios 2-200 h, FNAM 8(10)), avec **rendements aller-retour réalistes par classe**, pertes de stockage et limites de charge ; sur **séquence pluriannuelle chaînée** (B2) ; contrainte d'intégration EnR **en moyenne sur les années** (FNAM 8(12)(a)), et non année par année ; courbes de Pareto (besoin en fonction de la cible d'écrêtement) ; sensibilités au coût et au rendement.

**Vérification** : monotonicité (cible plus stricte ⇒ besoin non décroissant ; rendement plus faible ⇒ énergie stockée non décroissante) ; convergence avec le nombre d'années.

---

### B12 — Attribution des contributions · Consensus : **ÉMERGENT** → **[CONSTRUITE]**

**Pratiques observées**
- Kristiansen, Korpås, Svendsen (Applied Energy 2018) : **valeur de Shapley** pour classer les sources de flexibilité selon leur contribution marginale aux économies de coût, à la réduction de CO2 et à l'utilisation des EnR, en couvrant toutes les séquences de déploiement [E].
- Churkin et al. (PSCC 2024) : jeu coopératif pour comparer flexibilité et renforcement de réseau ; limite de passage à l'échelle en 2^N [E].
- ESIG 2023 : **accréditation de capacité** = contribution de chaque ressource à l'adéquation (logique ELCC marginale) [E].
- Heggarty et al. 2020 : décomposition de la fourniture de flexibilité [R].

**Brique idéale [CONSTRUITE]** : trois mesures complémentaires, publiées ensemble.
- (a) **Décomposition comptable fermée** par échelle de temps : Σ ressources + écrêtement + délestage = besoin.
- (b) **Contribution marginale** : variation de l'EUFE_h et du coût par MW ajouté ou retiré (perturbation ou duales) ; c'est un « crédit de flexibilité » analogue à l'ELCC marginal.
- (c) **Shapley par familles de technologies** (10 familles au plus, coalitions calculables) pour une répartition équitable du total.

**Vérification** : axiomes (efficience de la somme, symétrie, joueur nul) ; contrefactuel de retrait de chaque famille cohérent en signe et en ordre de grandeur avec (b) et (c).

---

### B13 — Statistique et quantification de l'incertitude · Consensus : **ÉTABLI** (méthodes), rarement appliqué

**Pratiques observées** : critère de convergence Monte-Carlo par coefficient de variation de l'ENS (ERAA) [T] ; théorie des valeurs extrêmes et loi de Pareto généralisée conditionnelle pour la charge nette (GB) [E] ; analyse de sensibilité globale (Heggarty 2019, mots-clés) [R] ; critère multi-métrique sur les queues (ESIG) [E].

**Brique idéale** : chaque indicateur est publié avec son **intervalle** (bootstrap par blocs, ou dépassements de seuil et loi de Pareto généralisée pour les quantiles extrêmes) ; **critères de convergence** pour les années climatiques, les tirages et les réalisations d'erreurs ; **analyse de sensibilité globale** (indices de Sobol) sur les conventions et les hypothèses clés (prix, rendements, amélioration des prévisions, UC), avec classement des facteurs dominants (P6).

**Vérification** : couverture empirique des intervalles sur rétro-test ; stabilité des classements sous rééchantillonnage.

---

### B14 — Vérification, validation et gouvernance · Consensus : **ÉMERGENT**

**Pratiques observées** : rétro-test historique d'un modèle de planification (NREL, ReEDS 2010-2016 contre les capacités réelles) [E] ; pratiques de *backcast* en éolien (UL, 2024) [E] ; projets ouverts avec intégration continue (PyPSA-Eur) [connaissance générale] ; transparence des modèles de fiabilité critiquée lorsqu'elle manque (Australian Energy Council sur AEMO) [E].

**Brique idéale**
1. **Rétro-simulation** des années récentes (par ex. 2023-2025) au niveau zone : prix, flux, dispatch par filière, écrêtement, volumes d'équilibrage et de réserves activées, avec **seuils d'acceptation** publiés.
2. **Benchmark** croisé contre l'ERAA et au moins un rapport national FNA.
3. **Tests de propriétés** automatisés (P5) ; tests unitaires et de régression ; intégration continue multi-plateforme.
4. Code, configurations et données ouvertes autant que possible ; pour les données confidentielles, un jeu synthétique représentatif ; **résultats versionnés**.
5. **Revue indépendante** publiée.

**Vérification** : existence et publication de ces éléments.

---

## 3. Synthèse : où l'état de l'art existe et où il a été construit

| Brique | Consensus | Statut dans ce référentiel | Références principales |
|---|---|---|---|
| B1 Métriques | Absent | **Construit** (4 couches) | CAISO FCNA, EirGrid RM, Elia, IRRE, ESIG, JRC/METIS |
| B2 Climat | Émergent | Synthèse des meilleures pratiques | RTE 200 ans + RCP, Kittel (été à été), Gøtske, grands ensembles |
| B3 Prévisions | Émergent / absent pour la projection | **Construit** | CAISO (régression quantile), Elia DRD, Pinson, GPD conditionnelle |
| B4 Pannes | Établi | Repris | MC séquentiel, SO GL 157 |
| B5 Information | Établi (recherche) | Repris et précisé | WILMAR, PLEXOS, CAISO 15/5 min |
| B6 Résolution | Établi | Repris | SDAC 15 min, CAISO 5 min, Deane 2014 |
| B7 UC et prix | Établi / émergent | Repris | Morales-España, Palmintier |
| B8 Stockage et hydraulique | Établi / émergent | Repris | SDDP/ProdRisk, PLEXOS MT |
| B9 Réseau | Établi | Repris | Flow-based Core et nordique |
| B10 Investissement | Émergent | **Construit** | Ehrenmann-Smeers, CVaR, co-optimisation, art. 19e(2)(a) |
| B11 Stockage EnR | Établi (recherche) | Repris | Ruhnau & Qvist, Dowling, Sepulveda, Kittel |
| B12 Attribution | Émergent | **Construit** (3 mesures) | Shapley (Kristiansen), ELCC (ESIG) |
| B13 Incertitude | Établi, rarement appliqué | Repris | EVT, bootstrap, Sobol, convergence |
| B14 V&V | Émergent | **Construit** | NREL backtest, CI, revue indépendante |

**Où se trouve l'ERAA dans ce référentiel ?** C'est un **plancher réglementaire** : prévision parfaite, MTU ≤ 1 h et pré-optimisation hydraulique grossière sont admis. Il est en deçà de l'état de l'art sur B3, B5, B6 et B8, et la cohérence EVA/dispatch y reste imparfaite (B10, selon l'ACER elle-même).

## 4. Architecture idéale assemblée

```
B2 ensemble climatique (≥100-200 ans, climat TY, chaîné, extrêmes)
 ├─ B3 générateur d'erreurs (conditionnel, copules, EVT, projection TY, N réalisations)
 ├─ B4 Monte-Carlo de pannes (convergence)
 └─ B8 valeurs de l'eau SDDP (apports + météo)
        ↓
B10 investissement : équilibre stochastique avec risque, mêmes scénarios, adéquation ancrée ou balayée
        ↓
B5+B6+B7+B9 simulation séquentielle : DA 15 min (clustered UC) → ID avec mises à jour → équilibrage 5-15 min (réserves ex ante) ; flow-based
        ↓
B1 indicateurs L1 (variabilité) / L2 (enveloppes) / L3 (déficits par cause) / L4 (valeur), niveaux zone, région, UE
B11 stockage contrefactuel (pluriannuel, rendements)      B12 attribution (comptable + marginale + Shapley)
        ↓
B13 intervalles, convergence, Sobol          B14 rétro-simulation, benchmark, tests, revue
```

## 5. Sources

- CAISO, *Flexible Ramping Product*, quantile regression (annexe C) — https://stakeholdercenter.caiso.com/InitiativeDocuments/AppendixC-QuantileRegressionApproach-FlexibleRampingProductRequirements.pdf ; présentation 2023 — https://www.caiso.com/documents/flexiblerampingproduct-presentation-sep25_2023.pdf ; ESIG (conditions-based) — https://www.esig.energy/attachment/serve/session-5b-adapting-probabilistic-forecasts-based-on-conditions-lysha-matsunobu-2
- CAISO, *Flexible Capacity Needs Assessment* 2024 — https://stakeholdercenter.caiso.com/InitiativeDocuments/Final-2024-Flexible-Capacity-Needs-Assessment-v2.pdf
- EirGrid/SEMO, *Ramping Margin Requirements in Scheduling* — https://www.sem-o.com/documents/general-publications/Ramping_Margin_Requirements_in_Scheduling.pdf
- Elia, méthodologie de flexibilité de court terme (AdeqFlex 2025, accès refusé, extraits) — https://www.elia.be/-/media/project/elia/elia-site/public-consultations/2024/20241104_public-consultation-on-the-methodology-the-basis-data-and-scenarios/adeqflex25_methodology_for_the_assessment_on_short_term_flexibility.pdf
- RTE, *Futurs énergétiques 2050* (usage des scénarios climatiques) — https://iea.blob.core.windows.net/assets/e3abe3f7-0605-433e-b702-eefafc18a803/DubusLaurent_RTE_ClimateScenariosUseinLong-TermProspective.pdf
- AEMO, *2024 ISP PLEXOS model instructions* — https://aemo.com.au/-/media/files/major-publications/isp/2024/supporting-materials/2024-isp-plexos-model-instructions.pdf
- NESO, *Operability Strategy Report* — https://neso.energy/document/301426/download
- JRC, Koolen, De Felice, Busch (2023), JRC130519 — https://publications.jrc.ec.europa.eu/repository/handle/JRC130519
- ESIG, *Five Principles of Resource Adequacy* — https://www.esig.energy/?p=14041 ; *New Resource Adequacy Criteria* — https://www.esig.energy/attachment/serve/new-resource-adequacy-criteria-for-the-energy-transition-derek-stenclik ; accréditation — https://www.esig.energy/wp-content/uploads/2023/02/ESIG-Design-principles-capacity-accreditation-report-2023.pdf
- Lannoye, Flynn, O'Malley — https://researchrepository.ucd.ie/rest/bitstreams/12523/retrieve
- Deane, Drayton, Ó Gallachóir (2014) — https://research.ucc.ie/en/publications/the-impact-of-sub-hourly-modelling-in-power-systems-with-signific/
- Meibom et al. (2011) / WILMAR — https://researchrepository.ucd.ie/rest/bitstreams/12505/retrieve ; EirGrid Work-stream 2(b) — https://cms.eirgrid.ie/sites/default/files/publications/Workstream%202B.pdf ; Tuohy et al. — https://www.tara.tcd.ie/bitstreams/c494f96a-7f65-4d3f-b79e-9904ffd4020a/download
- PLEXOS, *MT Schedule* — https://portal.energyexemplar.com/help/plexos/Main.MTSchedule.html ; *Hydro classes* — https://portal.energyexemplar.com/help/plexos/Article.HydroClasses.html
- SINTEF ProdRisk — https://sintef.no/en/software/prodrisk
- Morales-España, Latorre, Ramos — https://pascua.iit.comillas.edu/aramos/papers/V3.3_Tight_Compact_UC.pdf ; Palmintier & Webster — https://dspace.mit.edu/handle/1721.1/102960
- Pinson et al. (2009) — https://backend.orbit.dtu.dk/ws/files/4900902/pinsonetal_wpfscenarios_fin.pdf ; GPD conditionnelle, charge nette GB — https://ar5iv.arxiv.org/html/2103.10335
- Prévisions futures : Nuño et al. (DTU) — https://backend.orbit.dtu.dk/ws/files/149828757/revision_new_2_1_.pdf ; Mauch et al. (CMU) — https://www.cmu.edu/ceic/assets/docs/publications/working-papers/ceic-13-04.pdf
- Climat : Gøtske et al. — https://arxiv.org/pdf/2404.12178v2.pdf ; Kittel, Roth, Schill — https://arxiv.org/pdf/2411.17683 ; événements extrêmes par prix duaux — https://arxiv.org/html/2508.05163v1 ; Bloomfield pour le CCC — https://www.theccc.org.uk/wp-content/uploads/2025/02/Reasonable-worst-case-stress-test-scenarios-for-the-UK-energy-sector-in-the-context-of-the-changing-climate-Bloomfield.pdf
- Stockage : Dowling et al. — https://escholarship.org/content/qt8bw1g1ng/qt8bw1g1ng.pdf ; Sepulveda et al. — https://dspace.mit.edu/handle/1721.1/138145 ; Ruhnau & Qvist — https://doaj.org/article/3f8dab1761d34116826fba55b72b211f
- Investissement : Ehrenmann & Smeers — https://econpapers.repec.org/RePEc:cor:louvco:2008007 ; Muñoz et al. — https://ideas.repec.org/p/enp/wpaper/eprg1621.html ; marchés de risque manquants et stockage longue durée — https://arxiv.org/html/2510.13514 ; GenX TDR — https://genxproject.github.io/GenX.jl/dev/Model_Reference/TDR
- Attribution : Kristiansen et al. — https://sintef.brage.unit.no/sintef-xmlui/handle/11250/2489753 ; Churkin et al. — https://arxiv.org/pdf/2310.03610.pdf
- Validation : NREL ReEDS backtest — https://nrel.gov/docs/fy19osti/71916.pdf
- Plancher réglementaire : méthodologie ERAA (Décision ACER 04/2026) et annexe III de la Décision 07/2025 (voir `evidence/extraits_sources_primaires.md`).
