# Contre-revue : où notre propre analyse peut être attaquée

*Exercice de red team appliqué à nos propres livrables (02, 04, 05). Objectif : savoir quelles affirmations sont robustes avant de les porter en consultation, et lesquelles un contradicteur (ACER, OET, un autre acteur) pourrait contester. Chaque point indique la parade ou la réserve à afficher.*

| # | Affirmation de la revue | Objection plausible | Solidité | Parade ou réserve à afficher |
|---|---|---|---|---|
| C1 | Les déficits varient d'un facteur 30 selon l'UC ; la VAN/MW des actifs d'un facteur 6 à 23 (batterie) | Le teaser est illustratif, non calibré, loin de l'équilibre (une seule itération EVA) ; l'option MILP est celle que nous jugeons invalide, donc le ×30 mesure la sensibilité d'une option fausse, pas l'erreur de l'option par défaut | **Moyenne** | Présenter le ×30 comme preuve que **l'UC est une convention dominante non tranchée**, pas comme l'erreur du LP. L'erreur propre du LP n'est mesurable qu'avec un clustered UC entier (expérience « 10 unités », §4 de 04). Les ordres de grandeur ne se transposent pas tels quels au modèle UE |
| C2 | Les contributions par technologie ne bouclent pas (EnR comptée deux fois) | Le notebook ACER retire l'EnR ; la métrique par co-mouvement est un **choix explicite** de la spécification (éq. 13.8) | **Forte** pour l'absence de bouclage des sorties publiées ; **moyenne** pour « ne mesure pas la valeur » (un seul contrefactuel, sur un seul système) | Insister sur l'exigence de bouclage (P4) et sur le résidu « RES/Curtailment » du notebook, qui absorbe les erreurs. Pour la valeur : demander des contrefactuels systématiques plutôt qu'affirmer une généralité |
| C3 | La méthode probabiliste surestime massivement les besoins non couverts (8 760 h contre 360 h) | Notre correction ajoute la puissance de stockage **sans contrainte d'état de charge** : c'est une borne haute de la marge, donc la vraie réduction est plus faible | **Forte** sur le principe (non-conformité avec la FNAM 10(2)), **moyenne** sur l'ampleur | Annoncer « jusqu'à » et demander le calcul avec état de charge |
| C4 | L'oracle intraday biaise à la baisse les besoins de court terme | Nos tests d'horizon encadrent l'effet sans reproduire une vraie révélation progressive avec prévisions intermédiaires | **Forte** sur le sens, désormais **mesuré** (8 h : +13 à +22 %) ; **moyenne** sur l'ampleur réelle (borne basse ; 1 % de fenêtres infaisables traitées en mode tolérant) | Présenter +13-22 % comme une borne basse ; demander à ACER une expérience de révélation séquentielle |
| C5 | Bande d'équilibre EVA : adéquation fixée à un facteur 2-3 près par le prix de rareté | Calcul simplifié de type « screening » sur une pointe : pas de rentes inframarginales, une technologie | **Moyenne** | Présenter comme ordre de grandeur ; l'argument structurel (le niveau d'adéquation dépend du plafond et de la VoLL) relève de la théorie standard et n'est pas contestable. Demander les sensibilités exigées par l'art. 19e(2)(a) |
| C6 | Écarts à la FNAM | La FNAM s'impose aux GRT pour les rapports **nationaux** ; l'outil de l'ACER n'y est pas juridiquement soumis | **Moyenne** juridiquement, **forte** fonctionnellement | Fonder l'argument sur la **comparabilité** (art. 19e(7) : analyse des rapports nationaux ; 19e(7)(a) : cohérence méthodologique) et non sur une obligation |
| C7 | Version préliminaire | ACER a déclaré que ce n'est pas le modèle final ; des corrections peuvent exister en interne | **Forte** objection de procédure | Formuler les remarques comme des **exigences pour la version finale** et demander un second tour de consultation et un journal des modifications |
| C8 | Référentiel d'état de l'art (05) | Plusieurs sources consultées par extraits (CAISO, EirGrid, Elia, PLEXOS) ; documents primaires d'Elia inaccessibles ; briques « construites » par nous, donc contestables | **Moyenne** | Dans la réponse publique, citer les briques **établies** (SDDP, pas sub-horaire, clustered UC, convergence MC, multi-années) comme exigences fortes, et les briques **construites** comme propositions |
| C9 | Reproductibilité | Environnement reconstruit avec `uv`/pip (versions identiques au lock, binaires différents des paquets conda) | **Faible** risque | Indiquer l'environnement ; nos conclusions ne reposent pas sur des écarts numériques fins |
| C10 | Passage à l'échelle (F-18) | Extrapolation hypothétique | **Faible** | Ne pas en faire un argument de consultation (et la qualité, non la vitesse, est le critère retenu) |
| C11 | Biais de producteur | Un producteur a intérêt à des besoins faibles (moins de soutien à de nouveaux concurrents) ou forts (plus de rémunération de la flexibilité existante) | **Risque de crédibilité** | Notre conclusion est que **ni le sens ni l'ampleur de l'erreur ne sont connus** (§ « direction des biais » de 06/07) : la demande porte sur la rigueur et la quantification de l'incertitude, pas sur un résultat |

## Affirmations les plus solides (à porter en priorité)

1. Les indicateurs de déficit de court terme sont mal définis : écarts signés qui se compensent, et méthode probabiliste non conforme aux marges de la FNAM 10(2).
2. Le stockage fictif est sans pertes, contrairement à la FNAM 8(10) ; la cible est imposée par année climatique, contrairement à la FNAM 8(12)(a).
3. Les erreurs de prévision par défaut sont synthétiques, contrairement à la FNAM 10(1), avec un effet de facteur 2,3 mesuré.
4. L'EVA ne propose aucune sensibilité aux hypothèses de prix (art. 19e(2)(a)), aucun traitement du risque lié aux pics de prix (alors même que l'ERAA en impose un), et aucune garantie ni statut de convergence publié.
5. Aucune quantification d'incertitude ; validation (rétro-simulation) promise mais non publiée.
6. Indicateurs uniquement zonaux, alors que l'art. 19e(7)(b) demande une évaluation au niveau de l'Union.

## Affirmations à formuler avec prudence

- Ampleurs issues du teaser (×30, ×23, ×2,3) : **ordres de grandeur illustratifs**.
- Effet oracle : sens établi, ampleur encadrée seulement.
- Briques construites du référentiel 05 : propositions, pas des normes.
