# Revue adversariale de la méthode EU-Flex au regard de l'état de l'art

*Question posée : la méthode, dans son ensemble et dans son détail, est-elle compatible avec l'objectif attendu, au regard de ce qui se fait de mieux dans l'industrie et la recherche ? Critère unique : qualité et robustesse du résultat. Le coût de calcul n'est pas un argument recevable.*

*Référentiel : [`03_etat_de_l_art_methodologique.md`](03_etat_de_l_art_methodologique.md) (grille Q1-Q12). Audit logiciel préalable : [`02_rapport_adversarial_review.md`](02_rapport_adversarial_review.md) (défauts F-xx). Ici, on attaque les **choix de méthode**, à supposer le code correct.*

---

## 0. Réponse courte

**L'architecture générale est défendable, mais la méthode telle que spécifiée ne l'est pas.** L'architecture enchaîne une simulation de marché séquentielle day-ahead puis infrajournalière, une EVA, puis un post-traitement d'indicateurs. C'est la voie 7(3)(b) de la FNAM et la famille de méthodes de l'ERAA et d'Elia. En revanche, la méthode ne produit pas des besoins de flexibilité **robustes** au sens de l'état de l'art. Les trois grandeurs qui déterminent les besoins « non couverts » — le **niveau d'adéquation** du parc, la **structure d'information** entre day-ahead et temps réel, et la **distribution des erreurs de prévision** — y sont fixées par convention plutôt que calibrées ou propagées comme des incertitudes. Nos expériences montrent que ces conventions déplacent les résultats d'un ordre de grandeur supérieur aux écarts que l'outil prétend mesurer (§4). Sur le même système physique, l'ENS varie d'un **facteur 30** selon la représentation de l'engagement des unités, le niveau d'adéquation d'un **facteur 2 à 3** selon le prix de rareté supposé, le P99,9 d'un **facteur 2,3** selon le modèle d'erreur, et les déficits de court terme d'un facteur supérieur à **1 000** entre les deux méthodes proposées. Les « besoins » FNAM 8(5), eux, restent strictement inchangés dans toutes ces variantes.

**Positionnement (vérifié sur les textes intégraux de la méthodologie ERAA 2026 et des décisions ACER)** : comparé au standard industriel européen d'adéquation (ERAA), EU-Flex est **en avance** sur la structure d'information (DA/ID avec erreurs et pannes, contre la prévision parfaite de l'ERAA) et sur la cohérence EVA/dispatch. Il est **conforme** sur le pas horaire et l'hydraulique. Il est **en retrait** sur la convergence Monte-Carlo et le traitement des pics de prix dans l'EVA. Les écarts majeurs se situent entre ce niveau ERAA et ce qu'exige **l'objet propre de la FNAM** (déficits de flexibilité probabilisés, 15 min, erreurs historiques, stockage avec pertes), tel que le pratiquent Elia et la recherche.

| Bloc de résultats | Robustesse méthodologique |
|---|---|
| Indicateurs descriptifs de variabilité (FNAM 8(5), rampe maximale) | **Acceptable**, sous réserve du calendrier (semaines ISO, réalignement des jours) et du multi-années |
| Besoins **non couverts** de court terme et de rampe (FNAM 9(4), 10(4)) | **Non robustes** : dépendent d'abord des conventions (EVA, prévision parfaite intra-fenêtre, bruit synthétique) ; métriques mal définies |
| Besoin de stockage pour l'intégration EnR (FNAM 8(10)-(12)) | **Biaisé à la baisse** (sans pertes, année isolée, prévision parfaite) |
| Contributions des technologies (art. 19e(2), 19f) | **Non valides** (ni identité comptable, ni contrefactuel) |
| Quantification de l'incertitude | **Absente** |

---

## 1. Ce que « compatible avec l'objectif » exige

L'objectif (dossier §3) est de fournir à l'ACER, pour l'analyse européenne de l'art. 19e(7), des estimations des **besoins de flexibilité non couverts**, par zone et par échelle de temps, **cohérentes avec la FNAM**. Ces estimations doivent permettre de comparer les rapports nationaux et de recommander des actions transfrontalières, et elles alimenteront indirectement les objectifs nationaux de flexibilité non fossile (art. 19f). Il en découle quatre exigences de méthode :

1. **Validité de construction** : l'indicateur mesure ce qu'il prétend mesurer (un déficit, une contribution).
2. **Robustesse** : le résultat est peu sensible aux conventions arbitraires, et sensible aux facteurs physiques et économiques qui doivent le déterminer.
3. **Représentativité de l'incertitude** : événements extrêmes (climat, erreurs, pannes) échantillonnés à la hauteur des percentiles demandés (P99,9).
4. **Comparabilité** : mêmes définitions que les GRT appliquant la FNAM, mêmes données de référence (ERAA).

---

## 2. La chaîne de causalité des résultats (où l'erreur se propage)

```
Données (1 TY × 1 CY, prévisions)            ← Q2, Q3
  └─ Pré-optimisation hydraulique en prévision parfaite annuelle (cible SOC min) ← Q7
      └─ DA-UCED : fenêtres de 72 h, prévision parfaite des prévisions, UC relaxé (LP)  ← Q4, Q6
          └─ ID-ED : fenêtres de 72 h, prévision parfaite des RÉALISATIONS ; blocage FRR selon l'erreur réalisée ← Q4
              └─ Prix (duales, IPM sans crossover) → revenus → VAN → EVA à pas fixe  ← Q8
                  └─ (itérations) parc final : niveau d'adéquation = f(plafond, coût de délestage, seuil)
                      └─ Indicateurs : variabilité (descriptifs) ; « shortfalls » = différences ID − DA ;
                         contributions par signe ; dummy storage sans pertes par année ← Q1, Q9, Q10
```

**Observation clé.** Les seuls indicateurs qui mesurent un **déficit** (ENS, écrêtement, shortfalls, besoin non couvert) sont des sorties terminales. Ils héritent de toutes les conventions amont. Or l'EVA ajuste le parc jusqu'à ce que les revenus de rareté couvrent les coûts. **Le niveau de déficit résiduel est donc fixé principalement par l'hypothèse de prix de rareté**, et non par la physique du système (M9).

---

## 3. Revue composant par composant

Chaque composant suit la même structure : ce que fait EU-Flex, ce que fait l'état de l'art, l'attaque et sa preuve, la conséquence sur l'objectif, la gravité et le remède.

### M1 — Concept de « besoin » : description de la variabilité contre déficit (Q1) · **Majeure**

- **EU-Flex** : les besoins « daily / weekly / seasonal » et la rampe maximale sont calculés **sur les entrées seules** (demande − potentiel EnR − must-run). Ils sont invariants à toute l'offre de flexibilité : ajouter 50 GW de batteries ne les change pas. Les deux voies vers un déficit de court terme sont incompatibles entre elles :
  - **« simulation »** (défaut) : écart signé écrêtement/ENS entre ID et DA ;
  - **« probabilistic »** : percentile conditionnel − marge DA de certains actifs.
- **État de l'art** : un besoin de flexibilité exploitable pour la décision est une **espérance de déficit** (IRRE de Lannoye et al. ; convolution erreurs × pannes chez Elia ; FNAM 9(4), 10(4)).
- **Preuves (teaser)** :
  - Méthode « simulation » : *short_term_shortfall_curtailment* = **+1 772 GWh en N1 et −1 072 GWh en N2**. Un « déficit » négatif n'a pas de sens physique. Il reflète le **biais de prévision** (éolien N2 surestimé de +0,016 p.u. en moyenne en DA, donc davantage d'écrêtement en DA qu'en ID), pas une insuffisance de flexibilité. Positifs et négatifs se compensent dans tout agrégat.
  - Méthode « probabilistic » sur le même cas : N3 « non couvert » **8 760 h/8 760** ; N2 : 7 647 h à la hausse, soit un besoin non couvert cumulé de 20 945 GWh, alors que l'ENS simulé en ID est de **5,9 GWh**.
  - Les deux méthodes, appliquées aux mêmes réseaux, divergent de **plus de trois ordres de grandeur**. Aucune n'est validée contre l'autre ni contre une référence.
- **Conséquence** : l'outil ne produit pas, en l'état, l'indicateur central de la FNAM (besoin non couvert probabilisé, avec probabilité d'occurrence, énergie attendue, statistiques par événement, art. 10(4)-(6)).
- **Remède** : adopter une métrique d'adéquation de flexibilité (IRRE / EUE par échelle de temps) calculée par **convolution** des distributions d'erreurs et de pannes contre les **marges complètes** (EnR à la baisse, stockage avec SOC, DSR, échanges résiduels, hors FCR), conditionnellement aux états du système. Le contrôle croisé par simulation (art. 9(11), 10(10)) doit reposer sur des écarts **non signés**, avec et sans contrainte, à structure d'information identique.

### M2 — Incertitude climatique et continuité temporelle (Q2) · **Majeure**

- **EU-Flex** : chaque (TY, CY) est simulé **indépendamment, du 1er janvier au 31 décembre**. La pré-optimisation hydraulique est **cyclique sur l'année** (`use_cyclic_soc: true`). Le Monte-Carlo de pannes compte **1 tirage** (graine fixe). Le teaser comporte 1 année climatique. Les années bissextiles cassent la chaîne (F-05).
- **État de l'art** [textes vérifiés] : l'ERAA 2024 fait tourner son dispatch sur 36 scénarios météo. La méthodologie révisée (Décision 04/2026) impose au plus les 30 années historiques récentes, des années pondérées ou des projections, et un **Monte-Carlo avec critère de convergence publié** (α(N)). Elia utilise 200 années synthétiques (source secondaire), Gøtske et al. 62 années. Ruhnau & Qvist montrent que l'année extrême demande plus de deux fois le stockage de l'année moyenne. **Kittel, Roth, Schill modélisent d'été à été** : « better captures the effects of compound drought events spanning across the turn of years, as compared to models using single calendar years ».
- **Attaque** : l'épisode européen le plus extrême documenté (hiver 1996/97, Kittel et al.) **chevauche la frontière d'année**. Dans EU-Flex, il est coupé en deux années climatiques distinctes. Chacune impose au réservoir de revenir à son niveau initial au 31 décembre, et rien ne relie le 31/12/1996 au 01/01/1997. Les événements longs qui chevauchent l'hiver, les plus contraignants pour le stockage saisonnier et la flexibilité longue, sont donc **structurellement tronqués**.
- **Conséquence** : sous-estimation des besoins saisonniers et des besoins de stockage long, précisément là où les décisions d'investissement sont les plus coûteuses.
- **Remède** : simulation **chaînée** des années climatiques (ou années « hydrologiques » octobre-septembre), état de charge transmis d'une année à l'autre, ≥ 30-35 années, plus une analyse dédiée des épisodes extrêmes. Monte-Carlo de pannes avec critère de convergence.

### M3 — Modèle d'erreur de prévision (Q3) · **Majeure**

- **EU-Flex** : par défaut, bruit AR(1) multiplicatif aux paramètres codés en dur et à graine fixe, identique pour toutes les années. Le bruit de charge est **commun à toutes les zones** (corrélation 1,00). La corrélation charge-éolien (0,65) est un artefact de graine (F-08). Alternative : un CSV unique de prévisions (une seule réalisation). La FNAM 10(1)(a) exige pourtant une extrapolation d'au moins 2 ans d'erreurs historiques.
- **État de l'art** : scénarios d'erreurs à dépendance **spatio-temporelle** estimée (copules gaussiennes, Pinson et al.), conditionnés aux régimes (heure, saison, niveau de production), recalés sur ENTSO-E Transparency, avec l'amélioration des prévisions modélisée. Convolution séparée des pannes (Elia, FNAM 10(1)(c)).
- **Preuves** :
  - Le P99,9 de N1 passe de 11 665 MW (CSV) à 5 042 MW (bruit) : **facteur 2,3** selon la convention.
  - Même avec un seul jeu d'erreurs, le P99,9 estimé sur une année a un **IC90 % de ±7 % (N1) à ±17 % (N2)** (bootstrap par blocs journaliers, M-A). Le P0,1 de N2 est à ±20 %. Environ 9 heures seulement au-delà du P99,9.
  - La part des **pannes fortuites** dans l'erreur ID − DA se limite à celle du must-run (la charge résiduelle ID multiplie le must-run par la disponibilité). Les pannes des autres unités n'entrent pas dans la « short-term need » mais se manifestent dans le dispatch : la FNAM 10(1)(c) n'est respectée ni dans un sens ni dans l'autre.
- **Remède** : générateur de scénarios d'erreurs calibré (≥ 2 ans d'historique par zone et par filière, dépendance spatiale et temporelle, conditionnement), plusieurs réalisations par année climatique, estimation des quantiles extrêmes par **théorie des valeurs extrêmes** (dépassements de seuil) avec intervalles de confiance publiés.

### M4 — Structure d'information DA → ID → temps réel (Q4) · **Majeure (biais établi par construction, ampleur non quantifiée)**

- **EU-Flex** : le DA optimise sur 72 h de **prévisions** connues d'avance. L'ID ré-optimise sur 72 h de **réalisations** connues d'avance : toute l'erreur des 72 prochaines heures est révélée d'un coup. Le blocage dynamique de la FRR est calculé à partir de **l'erreur réalisée** (spécification éq. 9.7-9.8). Le stockage infrajournalier peut se pré-positionner des heures avant un écart qui, dans la réalité, n'est connu que progressivement.
- **État de l'art** : **niveau industriel (ERAA)** : le dispatch repose sur le principe de **« perfect foresight »**, avec erreurs de prévision et pannes fortuites ignorées, sauf si le cadre de modélisation permet de caractériser correctement les déséquilibres imprévus (méthodologie 2026, art. 4(1)(g), texte vérifié). **Sur ce point, EU-Flex dépasse le standard industriel** : un DA sur prévisions, un ID sur réalisations, des pannes en ID. **Niveau recherche** : révélation séquentielle (prévisions glissantes, plusieurs points de décision ID, équilibrage en temps réel ; planification glissante stochastique de type WILMAR) ; réserves dimensionnées *ex ante* sur la distribution de l'erreur.
- **Attaque** : la grandeur que la FNAM veut mesurer — la capacité du système à absorber l'**imprévu** — est simulée avec un oracle. Tout déficit de court terme mesuré par différence ID − DA est donc une **borne basse** : l'ID « voit venir » les écarts. Expérience E-H (§4) : réduire l'horizon à 36 h avec 12 h de recouvrement ne change presque pas les déficits (+0,3 %), mais augmente les démarrages de 25 à 38 %. Ce test ne lève pas l'oracle (36 h de réalisations restent connues), et l'outil ne permet pas de révélation horaire. **L'ampleur du biais reste à mesurer** ; c'est une priorité de validation.
- **Remède** : ID en fenêtres courtes successives (par ex. horizon de 1 à 4 h, mises à jour horaires), prévisions intermédiaires (J-1 → H-6 → H-1), réserves dimensionnées *ex ante* (SO GL 157 ou dimensionnement dynamique), activation des réserves en temps réel contre l'erreur résiduelle.

### M5 — Résolution temporelle (Q5) · **Majeure pour le court terme** (conforme au standard ERAA d'adéquation)

- **EU-Flex** : pas horaire. Le marché et l'équilibrage infrajournaliers sont fusionnés.
- **État de l'art et réglementation** : **l'ERAA admet un MTU ≤ 1 h** (méthodologie 2026, art. 4(1)(h), texte vérifié) : le pas horaire est conforme au standard industriel d'adéquation. En revanche, le SDAC est au pas de 15 minutes depuis le 1er octobre 2025, le SIDC et l'équilibrage aussi, et la FNAM 10(1)(e) distingue very fast (5-15 min), fast (15-60 min) et slow. Elia distingue « fast », « slow » et « ramping » (≤ 5 min ; source secondaire). L'objet « besoins de flexibilité de court terme » est donc plus exigeant que l'objet « adéquation ».
- **Conséquence** : rampes intrahoraires, besoins « fast / very fast » et valeur des actifs rapides (batteries, DSR) structurellement invisibles. La rampe maximale horaire sous-estime la rampe au MTU. Les revenus des actifs rapides, donc l'EVA, sont biaisés contre eux.
- **Remède** : résolution 15 min au moins pour l'ID et l'équilibrage, éventuellement sur des fenêtres échantillonnées ; à défaut, une couche statistique intrahoraire calibrée.

### M6 — Engagement des unités et formation des prix (Q6) · **Majeure**

- **EU-Flex** : flottes agrégées (par exemple « N1 Gas » = 30 GW en un seul générateur) avec engagement **relaxé** (LP), qui revient de fait à une approximation de clustered UC sans intégralité. Statut fractionnaire 5,3 % du temps sur le teaser. Option `linearized_unit_commitment: false` : **binaire sur la flotte entière**, prix calculés en deux étapes. Solveur LP par défaut : point intérieur **sans crossover** (`run_crossover: off`), donc duales non sommet en cas de dégénérescence.
- **État de l'art** : clustered UC à entier borné par le nombre d'unités (Palmintier & Webster : erreur < 1 %), formulations serrées, règle de prix explicitée (prix restreints, convex hull) et paiements complémentaires (*uplifts*).
- **Attaque** : (i) le manuel présente l'option MILP comme la référence de fidélité (« Relax the binary on/off decisions… at some loss of fidelity »). Sur des flottes agrégées, c'est l'inverse : le binaire impose du tout ou rien sur 30 GW avec un minimum technique de 12 GW. **Preuve E-U (§4)** : flotte gaz allumée 34,7 % des heures avec 102 démarrages complets ; **ENS × 30** (5,9 → 175,7 GWh) ; heures de rareté DA 8 → 301 ; prix moyens DA −27 à −40 % et ID +38 à +44 % (N2, N3) ; coût variable +14 %. Le résultat dépend donc d'un ordre de grandeur de la représentation de l'UC, sans référence (clustered UC entier) pour trancher. (ii) Les prix d'IPM sans crossover sur un LP dégénéré (beaucoup de tarifs à 150 €/MWh) sont le centre analytique de la face duale : les rentes inframarginales, donc la VAN, dépendent du choix d'algorithme.
- **Remède** : UC regroupé à entier borné par `n_units` (ou relaxation de cet entier avec resserrement), crossover activé pour les prix, règle de prix documentée, étalonnage sur un sous-échantillon contre un UC unitaire.

### M7 — Valorisation du stockage hydraulique et saisonnier (Q7) · **Modérée** (conforme au standard ERAA, en deçà de la recherche)

- **EU-Flex** : pré-optimisation annuelle en **prévision parfaite** (apports, EnR, demande de l'année climatique), puis contraintes de **SOC minimal** en fin de fenêtre avec écart pénalisé. Aucune valeur de l'eau n'entre dans les offres : l'eau au-dessus de la cible est valorisée à 0, celle en dessous à la pénalité.
- **État de l'art** : **niveau industriel (ERAA)** : une pré-optimisation *ex ante* à pas grossier avec trajectoires min/max est explicitement admise (méthodologie 2026, art. 4(5)(a)). **L'approche d'EU-Flex y est conforme.** **Niveau recherche** : valeurs de l'eau sous incertitude (SDP/SDDP ; Antares avec valeurs de l'eau externes ; EMPS/ProdRisk). La valeur de l'eau est un coût d'opportunité qui forme les prix.
- **Attaque** : (i) la prévision parfaite annuelle donne une **borne optimiste** de la flexibilité hydraulique : le réservoir « sait » quand viendra la Dunkelflaute. (ii) Les prix des zones hydrauliques ne reflètent pas le coût d'opportunité, ce qui biaise les revenus du stockage concurrent et des pointes, donc l'EVA. (iii) La suite d'intégration du modèle constate un écart de SOC de −10,5 % par rapport au plan en ID (F-13) : les cibles ne tiennent pas sous erreur de prévision, ce qui est attendu mais montre que le plan déterministe n'est pas une politique robuste.
- **Remède** : valeurs de l'eau calculées sous incertitude climatique (multi-CY) et intégrées comme coût marginal dans le DA et l'ID ; à défaut, des courbes guides avec bandes, et une analyse de sensibilité à la prévision.

### M8 — Représentation du réseau (Q4/Q12) · **Modérée**

- **EU-Flex** : zones en plaque de cuivre ; échanges « physical/NTC » par défaut. Le FBMC est prévu mais dépend de données ERAA non redistribuables, donc non reproductible par des tiers.
- **État de l'art** : FBMC Core depuis 2022 et Nordic depuis 2024 ; l'ERAA modélise le FB. Les besoins réseau (FNAM 11-14) sont fournis par les GRT/GRD.
- **Conséquence** : la contribution des interconnexions à la flexibilité (centrale pour l'art. 19e(7)) est surestimée ou mal répartie en NTC. Les besoins réseau sont hors périmètre (données fictives).
- **Remède** : FB par défaut dès que les données le permettent, publication d'un domaine FB synthétique réaliste pour la reproductibilité, sensibilité NTC contre FB.

### M9 — EVA : équilibre mal défini, adéquation fixée par convention (Q8) · **Critique**

- **EU-Flex** : itérations à pas fixe en MW ; convergence quand |VAN/MW| ≤ seuil (70 k€/MW par défaut ; 20 k€/MW dans `teaser-eva`) ; neutralité au risque (taux d'actualisation ou hurdle rate) ; revenus DA + écart ID ; plafonds 5 000 / 10 000 €/MWh mais délestage à 4 500 €/MWh dans les données ; défaut `max_it: 3`.
- **État de l'art** [textes vérifiés] : la méthodologie ERAA admet une EVA fondée sur les revenus (rendement attendu comparé au taux exigé ou au WACC) ou une minimisation du coût (§2-6). Elle **impose d'atténuer la réaction des investisseurs aux pics de prix**, par défaut par l'actualisation partielle des années Monte-Carlo les plus rémunératrices (§16), ce qu'EU-Flex ne fait pas. L'ACER exige la **cohérence EVA/dispatch** ; elle a constaté pour l'ERAA 2024 des écarts de **LOLE de 1,7 à 4 h** entre les deux modules (3 scénarios météo dans l'EVA contre 36 dans le dispatch) et conclut que « scarcity situations and pricing are not accurately reflected in the EVA, distorting investment signals ». En théorie, l'équilibre concurrentiel correspond à l'optimum de coût sous tarification VoLL ; avec des plafonds, le niveau d'adéquation est fixé par le plafond. Les États membres ont des **standards de fiabilité** (art. 25 du règlement 2019/943 : VoLL/CONE). Enfin, **l'art. 19e(2)(a) exige d'évaluer les besoins sous différentes hypothèses de prix de marché** (texte vérifié).
- **Preuve (M-B)** : pour la pointe gaz du teaser (capex annualisé 30 k€/MW/an, coût marginal 150 €/MWh, 8 %, 2030-2050), « converger » signifie être entre **5,4 et 8,4 heures de rareté par an** (seuil 70 k€) si la rareté est payée 4 500 €/MWh. Mais **2,4 à 3,7 h** si elle est payée au plafond ID de 10 000 €/MWh. Le niveau d'adéquation du parc final, dont dépendent tous les ENS et besoins non couverts calculés ensuite, varie d'un **facteur 2 à 3 selon une convention de prix**, et de ±25 % de plus selon le seuil. Ajoutons qu'un pas fixe de 800 MW peut osciller sans converger (F-11c).
- **Circularité** : l'EVA construit de la flexibilité tant qu'elle est rentable. Les « besoins non couverts » mesurés ensuite sont donc la **flexibilité qu'il n'est pas rentable de fournir au prix de rareté supposé**. Ce n'est pas un besoin physique, c'est un artefact du design de marché modélisé. C'est légitime **seulement** si l'hypothèse de prix (VoLL, plafonds, HMMCP) est explicitement ancrée et testée en sensibilité.
- **Remède** : formuler l'EVA comme un problème d'équilibre ou d'optimisation (capacité + dispatch) sur l'ensemble des CY, ou comme un pas adaptatif (bissection) avec des tolérances en heures de rareté ; ancrer le niveau d'adéquation au **standard de fiabilité** de chaque État membre ou publier les besoins en fonction de ce niveau ; sensibilités systématiques VoLL/plafond ; risque explicite (CVaR ou hurdle rates différenciés).
- **Point positif à préserver** : l'EVA d'EU-Flex réutilise directement le dispatch et les années climatiques de la simulation de marché. Elle évite donc par construction l'incohérence EVA/dispatch (3 contre 36 scénarios) que l'ACER reproche à l'ERAA 2024. C'est un avantage réel sur le standard industriel, à condition de résoudre l'indétermination de l'équilibre.

### M10 — Attribution des contributions (Q10) · **Critique**

- **EU-Flex** : contribution = Σ (dispatch − moyenne de la période) × signe(écart de charge résiduelle). EnR incluse (comptée deux fois). Pas d'identité comptable. Résidu « RES / Curtailment » dans le notebook (F-03).
- **État de l'art** : une décomposition doit satisfaire l'identité besoin = Σ contributions + écrêtement + délestage (Heggarty et al. 2020). La valeur d'une ressource se mesure par contrefactuel (logique ELCC, Shapley).
- **Attaque (au-delà du bug)** : même corrigée, une attribution par **co-mouvement** récompense la covariation, pas le service rendu. Une ressource qui oscille avec une forte amplitude obtient une grande contribution même si son retrait ne dégraderait rien (substituable), et une ressource rare mais critique obtient peu. **Preuve E-C (§4)** : l'iDSR se voit attribuer ~2 % du besoin journalier (1,7 TWh). Son retrait multiplie pourtant l'ENS de N2 par 4 (5,9 → 23,4 GWh), fait passer les heures de rareté DA de 8 à 22 et coûte +0,41 G€/an de coût variable (+6,2 %). Sa « contribution » est simplement réabsorbée par le gaz (+0,84 TWh) et l'hydraulique (+0,65 TWh). La métrique ne distingue pas un service critique d'une covariation substituable.
- **Remède** : publier deux familles d'indicateurs. (1) Une décomposition comptable fermée, avec un terme d'écrêtement explicite. (2) Des **contributions marginales ou contrefactuelles** (variation de l'ENS, de l'écrêtement, de l'IRRE et du coût quand on retire ou ajoute ΔMW de la ressource), éventuellement Shapley par familles.

### M11 — Besoin de stockage pour l'intégration EnR (Q9) · **Critique**

- **EU-Flex** : *dummy storage* sans pertes, coût fictif identique pour toutes les durées, cible imposée **par année climatique**, réseau d'ED figé, écrêtement-cible exogène, année isolée et cyclique.
- **État de l'art** : FNAM 8(10) (rendement par ratio E/P), 8(12)(a) (moyenne sur les années météo) ; Ruhnau & Qvist (pertes et limites de charge allongent la période dimensionnante à ~12 semaines ; multi-années indispensable).
- **Conséquence** : sans pertes, le besoin est minoré d'un facteur de l'ordre de 1/rendement aller-retour sur l'énergie (≈ ×1,1 pour 2 h à ×2,5-3 pour 200 h type hydrogène). Avec une année isolée cyclique, les besoins pluriannuels sont ignorés. Avec une contrainte par année, le résultat est surdimensionné pour les années extrêmes. Les biais ne se compensent pas de façon contrôlée.
- **Remède** : co-optimisation sur la séquence des CY, rendements par ratio, contrainte en moyenne pluriannuelle, et sensibilité à la cible.

### M12 — Agrégation spatiale et lecture européenne (Q12) · **Modérée**

- **EU-Flex** : indicateurs par zone uniquement. Or l'**art. 19e(7)(b)** charge l'ACER d'évaluer « the estimated flexibility needs in the electricity system **at Union level** » (texte vérifié).
- **Preuve (M-C)** : sur le teaser, le besoin de la région agrégée vaut **77 % (horaire), 82 % (journalier), 70 % (saisonnier)** de la somme des besoins zonaux ; P99,9 : **74 %** ; rampe maximale : 14,7 GW contre 24,1 GW. L'effet de mutualisation, qui est précisément l'objet transfrontalier de l'art. 19e(7), n'est ni calculé ni publié.
- **Remède** : publier les indicateurs aux niveaux zone, région de calcul de capacité et UE, ainsi que la mutualisation effectivement réalisée compte tenu des capacités d'échange.

### M13 — Incertitude et validation (Q11, Q12) · **Critique**

- **EU-Flex** : aucun intervalle de confiance ; un tirage ; aucune rétro-simulation publiée. La spécification §5 promet unit tests, régression, rétro-simulation sur ENTSO-E Transparency et **reproduction de l'ERAA 2023**, mais aucun résultat n'est publié. L'unique oracle livré échoue (F-13).
- **État de l'art** : backcasting publié (prix, flux, dispatch, écrêtement), benchmark contre les modèles de référence, quantification de l'incertitude des percentiles.
- **Remède** : publier le dossier V&V promis par la spécification avant tout usage. Il doit au minimum contenir : rétro-simulation 2023-2025 par zone (erreur de prix, de flux, d'écrêtement), reproduction ERAA, intervalles de confiance des indicateurs.

---

## 4. Expériences de robustesse méthodologique (teaser, exécution complète)

Principe : faire varier **une convention de modélisation à la fois**, à données physiques identiques, et mesurer le déplacement des résultats. Une méthode robuste ne doit pas voir ses indicateurs de besoins bouger plus que les écarts qu'elle prétend résoudre.

### 4.1 Variantes simulées de bout en bout (19 étapes chacune)

| Variante (une seule convention modifiée) | Référence |
|---|---|
| **E-U** : engagement **binaire** (`linearized_unit_commitment: false`, HiGHS MILP, prix par re-résolution à engagement fixé) | Option documentée par le manuel comme plus fidèle |
| **E-H** : horizon 36 h / recouvrement 12 h, au lieu de 72 h / 24 h (DA et ID) | Information moins anticipée |
| **E-C** : contrefactuel sans effacement implicite (`implicit_dsr.enabled: false`, −2,25 GW d'iDSR) | Test de validité de la métrique de contribution |

Sorties brutes : [`evidence/method_experiments_runs.txt`](evidence/method_experiments_runs.txt) (script `scripts/compare_runs.py`).

| Indicateur (zone) | Référence (LP, 72/24) | E-U binaire | E-H 36/12 | E-C sans iDSR |
|---|---|---|---|---|
| ENS ID (GWh), N2 | 5,9 | **175,7 (×30)** | 5,9 (+0,2 %) | **23,4 (×4)** |
| Heures de prix DA ≥ 3 500 €/MWh (N1+N2+N3) | 8 | **301** | 8 | 22 |
| ST shortfall ENS (GWh), N2 | 3,7 | **162,9 (×44)** | 3,7 | 11,6 (×3) |
| ST shortfall écrêtement (GWh, signé), N1 / N2 | +1 772 / −1 072 | +565 / −1 088 | +1 777 / −1 068 | +1 678 / −1 079 |
| Écrêtement ID (TWh), N1 | 7,03 | 7,54 (+7 %) | 6,92 (−2 %) | 7,50 (+7 %) |
| Prix moyen DA (€/MWh), N2 / N3 | 93,5 / 147,7 | **68,0 / 89,4 (−27 % / −40 %)** | 95,7 / 149,2 | 100,2 / 153,2 |
| Prix moyen ID (€/MWh), N2 / N3 | 98,7 / 149,3 | **142,0 / 205,5 (+44 % / +38 %)** | 97,8 / 144,4 | 108,3 / 153,7 |
| Démarrages équivalents DA, gaz N1 | 13,5 | **102** (flotte de 30 GW en tout ou rien ; allumée 34,7 % des heures) | 16,9 (+25 %) | 17,4 |
| Coût variable ID (G€) | 6,50 | 7,42 (+14 %) | 6,54 (+0,6 %) | 6,91 (+6,2 %) |
| Besoins FNAM 8(5) et P99,9 | — | **identiques (0,0 %)** | **identiques** | **identiques** |
| Contribution journalière iDSR (TWh), N1/N2/N3 | 0,60 / 0,71 / 0,35 | 0,72 / 0,85 / 0,24 (±20-30 %) | ≈ (±1 %) | — |

### 4.2 Expériences analytiques (sans solveur)

Sorties : [`evidence/method_experiments_cheap.txt`](evidence/method_experiments_cheap.txt) (script `scripts/method_experiments.py`).

| Expérience | Résultat |
|---|---|
| **M-A** Bootstrap par blocs journaliers du P99,9 / P0,1 (une année) | IC90 % : N1 ±7 %, N2 ±17 % (P99,9) et ±20 % (P0,1), N3 ±10-11 % ; ~9 heures au-delà du P99,9 |
| **M-B** Bande d'équilibre EVA (pointe gaz du teaser) | « Convergé » = 5,4-8,4 h de rareté/an à 4 500 €/MWh ; 2,4-3,7 h à 10 000 €/MWh. Le niveau d'adéquation dépend d'un **facteur 2-3** de la convention de prix |
| **M-C** Mutualisation régionale | Besoin régional / somme zonale = 0,77 (horaire), 0,82 (journalier), 0,70 (saisonnier), 0,74 (P99,9) |
| Bruit synthétique contre CSV (audit F-08) | P99,9 N1 : 5 042 contre 11 665 MW (**facteur 2,3**) |
| Méthode probabiliste contre simulation (audit F-09) | N3 non couvert 8 760 h contre 0 MWh d'ENS simulé ; N2 : 20 945 GWh cumulés contre 5,9 GWh |

### 4.3 Lecture

1. **Les indicateurs de déficit sont dominés par les conventions de modélisation.** Sur un même système physique, l'ENS varie d'un facteur 30 avec la représentation de l'engagement (E-U), d'un facteur 2-3 avec le prix de rareté qui fixe l'équilibre EVA (M-B), et les déficits de court terme d'un facteur supérieur à 1 000 selon la méthode choisie (simulation ou probabiliste). Aucun de ces écarts n'est une incertitude physique : ce sont des choix de méthode non tranchés ni calibrés.
2. **L'option « engagement binaire » est méthodologiquement invalide sur des flottes agrégées** (E-U). Elle ne doit pas être présentée comme la référence de fidélité. La relaxation LP par défaut est la meilleure des deux options proposées, mais elle n'est pas validée contre un clustered UC entier (Palmintier & Webster).
3. **Les « besoins » FNAM 8(5) et le P99,9 sont strictement insensibles** à l'offre de flexibilité, à l'UC et à l'horizon (0,0 % dans toutes les variantes). C'est attendu par construction, et c'est précisément pourquoi ils ne peuvent pas fonder une conclusion sur l'**insuffisance** de flexibilité (M1).
4. **La métrique de contribution ne mesure pas la valeur** (E-C). L'iDSR reçoit ≈ 1,7 TWh de contribution journalière, soit ~2 % du besoin agrégé. Son retrait multiplie pourtant l'ENS par 4, triple les heures de rareté et coûte +0,41 G€/an (+6,2 %). Les autres technologies « absorbent » sa contribution (gaz +0,84 TWh, hydro +0,65 TWh) : le co-mouvement redistribue un total, il ne mesure pas un service.
5. **L'horizon de prévision (E-H) influe peu sur les déficits du teaser** (+0,3 %) mais beaucoup sur l'effort de flexibilité (démarrages +25 à +38 %). **Limite du test** : à 36 h, l'ID garde une prévision parfaite intra-fenêtre ; l'outil ne permet pas de simuler une révélation horaire de l'information. L'effet « oracle » (M4) reste donc **non quantifié** par nos expériences. Il est établi par construction, mais son ampleur est inconnue.

---

## 5. Matrice de conformité à l'état de l'art

| Critère | EU-Flex | Contre l'industrie (ERAA) | Contre la recherche |
|---|---|---|---|
| Q1 Déficit probabilisé | Différences ID − DA signées ; méthode probabiliste aux marges incomplètes | ❌ | ❌ |
| Q2 Climat : années, continuité, convergence | 1 année par simulation, réinitialisation annuelle, 1 tirage, pas de critère de convergence | ❌ (convergence MC exigée par l'ERAA) | ❌ (pas d'été à été, pas de chaînage) |
| Q3 Erreurs de prévision | Bruit synthétique codé en dur, ou un CSV | ✅ au-delà de l'ERAA (qui les ignore) | ❌ (FNAM 10(1) non respectée ; pas de dépendance spatio-temporelle) |
| Q4 Structure d'information | DA sur prévisions, puis ID sur réalisations avec oracle de 72 h | ✅ au-delà de l'ERAA (prévision parfaite) | ❌ |
| Q5 Résolution | Horaire | ✅ (MTU ≤ 1 h admis) | ❌ (marché et FNAM au pas de 15 min) |
| Q6 UC adapté à l'agrégation, prix explicites | LP relaxé (acceptable) ; option MILP invalide ; IPM sans crossover | ⚠️ | ⚠️ |
| Q7 Hydraulique | Prévision parfaite + SOC minimal | ✅ (pré-optimisation *ex ante* admise) | ⚠️ (pas de valeurs de l'eau) |
| Q8 EVA | Revenus et dispatch cohérents (+) ; pas fixe, bande large, pas d'atténuation des pics, adéquation fixée par convention de prix, pas de sensibilité de prix | ⚠️ (cohérence EVA/ED supérieure à l'ERAA ; atténuation des pics absente) | ❌ |
| Q9 Stockage contrefactuel | Sans pertes, par année | ❌ (FNAM 8(10), 8(12)(a)) | ❌ |
| Q10 Attribution | Par co-mouvement, non fermée | ❌ | ❌ |
| Q11 Incertitude quantifiée | Aucune | ❌ (α(N) exigé par l'ERAA) | ❌ |
| Q12 V&V publiés | Programmés dans la spécification, non publiés | ❌ | ❌ |
| Descriptifs FNAM 8(5) | Exacts (vérifié), calendrier fragile | ✅ / ⚠️ | ✅ / ⚠️ |
| Simulation de marché séquentielle DA/ID sur PyPSA | Fondation saine, déterministe, transparente | ✅ | ✅ |

---

## 6. Verdict méthodologique

0. **Positionnement vérifié sur textes intégraux** : par rapport au **standard industriel européen (ERAA)**, EU-Flex est **en avance** sur trois points : la structure DA/ID avec erreurs de prévision et pannes en ID, là où l'ERAA retient la prévision parfaite ; la cohérence EVA/dispatch, là où l'ERAA utilise 3 contre 36 scénarios ; la transparence du code. Il est **conforme** sur le pas horaire et la pré-optimisation hydraulique, et **en retrait** sur la convergence Monte-Carlo et l'atténuation des pics de prix dans l'EVA. Par rapport à **l'objet propre de la FNAM et à la recherche**, il reste en retrait sur les points détaillés ci-dessous. **Les critiques de cette revue portent donc principalement sur l'écart entre un outil d'adéquation de niveau ERAA amélioré et ce qu'exige une mesure robuste des besoins de flexibilité**, qui est un objet plus exigeant que l'adéquation.
1. **L'architecture est compatible avec l'objectif** : simulation de marché séquentielle + EVA + post-traitement selon la FNAM, sur un outil ouvert. C'est la bonne famille, alignée sur l'ERAA et sur la voie 7(3)(b) de la FNAM, et son ouverture est un atout réel face aux outils propriétaires.
2. **La méthode spécifiée n'est pas compatible avec l'objectif de qualité et de robustesse** pour les résultats qui comptent (besoins non couverts, besoins de stockage, contributions). Trois causes de fond :
   - **(a) Conventions non ancrées ni validées** (M3, M6, M9) : erreurs de prévision synthétiques, représentation de l'engagement non étalonnée (×30 sur l'ENS selon l'option), niveau d'adéquation fixé par des prix de rareté arbitraires. Ce sont elles, et non la physique, qui pilotent les déficits.
   - **(b) Indicateurs mal construits** (M1, M10) : des besoins insensibles à l'offre, des déficits signés qui se compensent, des contributions qui ne mesurent ni une identité comptable ni une valeur. Il s'y ajoute un **oracle informationnel** en ID (M4), qui biaise le court terme à la baisse dans une mesure non quantifiée.
   - **(c) Échantillonnage de l'incertitude très en deçà de l'état de l'art** (M2, M11, M13) : une année réinitialisée et un tirage, pour des quantiles à 99,9 % et des événements pluri-semaines.
3. **Les écarts ne sont pas des détails de calibrage.** Plusieurs touchent la **validité de construction** des indicateurs (M1, M10, M11) : améliorer les données ne suffira pas, il faut redéfinir les indicateurs.
4. **Ce qui est réutilisable tel quel** : le moteur de marché, la pré-optimisation comme repli, les indicateurs descriptifs (après correction du calendrier), l'infrastructure de workflow.

**Conclusion** : utiliser la méthode actuelle pour juger ou pondérer des rapports nationaux FNA exposerait l'ACER à des conclusions dominées par des conventions de modélisation. Les GRT qui suivent l'état de l'art (convolution probabiliste, multi-années, 15 min) produiront des besoins non couverts systématiquement **plus élevés** sur le court terme et le stockage long, et **différents** sur les contributions.

---

## 7. Méthode cible recommandée (qualité d'abord)

| # | Brique | Spécification cible | Remplace |
|---|---|---|---|
| 1 | Scénarios climatiques | ≥ 35 CY (PECD v4.2, y compris projections), simulées **en chaîne** avec SOC transmis ; années hydrologiques ; sur-échantillonnage des épisodes extrêmes | 1 CY réinitialisée |
| 2 | Erreurs de prévision | Générateur spatio-temporel (copules) calibré sur ≥ 2 ans d'erreurs J-1 et H-1 par zone et filière, mis à l'échelle des capacités TY, avec amélioration des prévisions ; N réalisations par CY | Bruit AR(1) codé en dur |
| 3 | Pannes | Monte-Carlo avec critère de convergence ; distributions séparées des erreurs (FNAM 10(1)(c)) | 1 tirage |
| 4 | Structure de marché | DA (15 min, horizon J+1, valeurs de l'eau), ID en fenêtres glissantes courtes avec prévisions mises à jour, équilibrage contre l'erreur résiduelle, réserves dimensionnées *ex ante* (SO GL 157) | Oracle 72 h |
| 5 | UC | Clustered UC entier borné (ou relaxé et resserré), crossover, règle de prix et uplift explicites | LP sur flotte, IPM sans crossover |
| 6 | Hydraulique | Valeurs de l'eau SDDP multi-CY | Prévision parfaite + SOC minimal |
| 7 | Adéquation / EVA | Équilibre ou optimisation multi-CY ; ancrage au standard de fiabilité ; aversion au risque ; sensibilités VoLL et plafond | Pas fixe + seuil |
| 8 | Indicateurs de déficit | IRRE/EUE par échelle de temps par convolution (erreurs × pannes) contre les marges complètes, conditionnés aux états du système ; probabilité, énergie attendue, statistiques par événement (FNAM 9(7), 10(6)) ; contrôle croisé par simulation à écarts non signés | Différences ID − DA signées |
| 9 | Stockage EnR | Co-optimisation multi-CY, rendements par ratio, cible moyenne, sensibilité aux cibles PNEC | Dummy sans pertes par année |
| 10 | Contributions | Décomposition comptable fermée + contrefactuels marginaux (ou Shapley par famille) | Co-mouvement non fermé |
| 11 | Échelles spatiales | Zone, région de calcul de capacité (CCR), UE ; mutualisation explicite | Zonal seul |
| 12 | Incertitude et V&V | Intervalles bootstrap et EVT sur tous les quantiles ; backcasting 2023-2025 publié ; reproduction ERAA ; tests de propriétés automatisés | Absents |

**Priorisation par impact démontré sur la robustesse** (et non par coût) :

1. **8 (métrique de déficit)** et **10 (contributions)** : validité de construction, sans laquelle rien n'est interprétable.
2. **5 (UC)** et **7 (ancrage de l'adéquation)** : facteurs ×30 et ×2-3 mesurés.
3. **2-3 (erreurs et pannes)** : facteur ×2,3 mesuré, IC de ±7 à ±20 %.
4. **1 (multi-années chaîné)** et **9 (stockage)** : biais documentés dans la littérature.
5. **4 (information séquentielle)** : biais certain, ampleur à mesurer.
6. Puis 6, 11.

La brique 12 (V&V) conditionne l'acceptabilité de l'ensemble et doit démarrer immédiatement. Elle doit en particulier trancher l'UC (clustered UC entier contre LP) et l'effet oracle.
