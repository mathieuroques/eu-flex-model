# EU-Flex (ACER) — Note de synthèse pour un producteur / investisseur

*2 pages. Version préliminaire 1.0.0-rc2 soumise à consultation jusqu'au **17 décembre 2026** ; webinaire ACER le **17 novembre 2026**. Détail et preuves : dossier `adversarial_review/`.*

## 1. Pourquoi c'est un sujet d'investissement, pas seulement de modélisation

Le règlement 2019/943 modifié (textes lus en intégralité) crée une chaîne de décision directe :

| Étape | Texte | Conséquence pour un producteur ou investisseur |
|---|---|---|
| Rapports nationaux sur les besoins de flexibilité, analyse européenne par l'ACER, **besoins au niveau de l'Union** | art. 19e(1), 19e(7)(b) | EU-Flex sert d'étalon pour juger les rapports nationaux |
| **Objectif national indicatif de flexibilité non fossile**, avec contributions spécifiques de la DSR et du stockage | art. 19f | Fixe le volume « cible » de nouvelle flexibilité non fossile |
| **Dispositifs de soutien** : paiements pour la capacité disponible de **nouveaux** DSR et stockage, adaptation des mécanismes de capacité | art. 19g | Revenus hors marché pour de nouveaux entrants ; concurrence pour les actifs marchands existants (batteries, hydraulique, thermique flexible) |
| Garde-fous : « pas au-delà du nécessaire », « éviter les distorsions », préserver l'exposition au signal prix | art. 19h(a), (f) | **Point d'appui juridique** pour exiger des besoins robustes et des fourchettes d'incertitude |

Une surestimation des besoins non couverts conduit à surdimensionner les soutiens, qui cannibalisent les revenus de la flexibilité marchande. Une sous-estimation affaiblit le signal d'investissement et le dimensionnement des mécanismes de capacité. **Ce qui compte pour l'investisseur, c'est la fiabilité et la fourchette du chiffre, pas son niveau.**

## 2. Constat principal

L'architecture est saine : un outil ouvert, une simulation de marché day-ahead puis intraday, et une EVA cohérente avec cette simulation (mieux que l'ERAA 2024, où l'ACER relève 1,7 à 4 h d'écart de LOLE entre EVA et dispatch). Mais **les besoins « non couverts », les revenus et la viabilité des actifs sont aujourd'hui pilotés par des conventions de modélisation plus que par la physique du système.** Mesures sur le cas de démonstration ACER, valant comme ordres de grandeur et non comme prévisions :

| Convention modifiée, à système physique identique | Effet mesuré |
|---|---|
| Représentation de l'engagement des unités (relaxée ou binaire) | ENS **×30** ; VAN/MW batterie **×23** (revenus de réserve ×17) ; nucléaire **−83 %** ; gaz ×6,7 (en négatif) |
| Flottes découpées en 10 unités (référence plus fidèle) | LP : inchangé (±1 %) ; engagement entier : [en cours] |
| Prix de rareté qui fixe l'équilibre EVA (4 500 ou 10 000 €/MWh) | Niveau d'adéquation « convergé » : **5,4-8,4 h** contre **2,4-3,7 h** de rareté par an |
| Source des erreurs de prévision (bruit synthétique par défaut ou prévisions fournies) | Besoin de court terme P99,9 **×2,3** |
| Méthode de court terme (« simulation » ou « probabiliste ») | Écart de plus de **×1 000** |
| Prévision intraday (72 h, 24 h ou 8 h de réalisations connues d'avance) | [à compléter] |
| Stockage fictif avec ou sans pertes réalistes | Avec pertes, le besoin calculé **baisse** (4 h, cible 2 % : 97,5 → 22,4 GW) : l'énergie dissipée compte comme EnR « intégrée ». **La métrique récompense le gaspillage** |
| Toutes les conventions ci-dessus | Besoins « descriptifs » (art. 8(5)) **inchangés** : ils ne mesurent pas une insuffisance |

**Le sens de l'erreur nette est inconnu** : certaines conventions gonflent les besoins non couverts (méthode probabiliste qui ignore stockage, EnR et interconnexions ; revenus incomplets des actifs flexibles), d'autres les réduisent (prévision parfaite en intraday, pas horaire, stockage sans pertes, années climatiques isolées et coupées au 31 décembre, hydraulique en prévision parfaite).

## 3. Les cinq points qui touchent directement la valeur des actifs

1. **EVA et revenus.** Le revenu modélisé couvre l'énergie day-ahead, l'écart intraday et la capacité de réserve. En sont absents l'énergie d'équilibrage, les mécanismes de capacité, la couverture à terme, la forme infra-horaire des prix (le marché est au pas de 15 min depuis le 1/10/2025) et les soutiens. → Valeur des batteries, de la DSR et du thermique rapide **sous-estimée**, sous-investissement dans l'EVA, donc **besoins non couverts gonflés**, qui peuvent justifier des soutiens 19g.
2. **Risque.** VAN neutre au risque, avec un taux par actif. L'ERAA elle-même impose d'atténuer la réaction des investisseurs aux pics de prix ; EU-Flex ne le fait pas. Le profit d'une année cible est **figé jusqu'au démantèlement** (20 ans sur une seule année de marché).
3. **Formation des prix.** Engagement des unités relaxé sur des flottes agrégées, prix duaux sans règle documentée, pas horaire. Le seuil du mécanisme HMMCP est calculé sur 70 % du plafond **initial** au lieu du plafond **en vigueur**, et le coût du délestage est incohérent avec les plafonds : le plafond intraday de 10 000 €/MWh n'est jamais atteint.
4. **Attribution par technologie.** La métrique ne se referme pas sur le besoin et ne mesure pas la valeur. Exemple : 2 % du besoin attribués à la DSR implicite, alors que son retrait multiplie l'ENS par 4. La viabilité des actifs de pointe repose sur très peu d'heures : 95 % de la marge annuelle de la pointe gaz se fait en 50 heures, 100 % de celle de la DSR explicite en 10 heures, sur **une seule** année climatique extrapolée sur 20 ans. Les **contributions des actifs existants** (hydraulique, thermique) sont mal mesurées, alors qu'elles conditionnent le volume « manquant » et la répartition DSR/stockage exigée par l'art. 19f.
5. **Robustesse de la boucle d'investissement.** Dans l'EVA complète, la batterie passe de 100 à 3 100 puis à 245 MW (oscillation), et la boucle **s'arrête à l'itération 3** sur une fenêtre infaisable. Les décisions d'entrée et de sortie simulées ne sont pas stables.
6. **Incertitude et validation.** Aucun intervalle de confiance (le P99,9 repose sur environ 9 heures par année climatique ; IC90 % de ±7 à ±20 %). Aucune rétro-simulation publiée, malgré l'engagement de la spécification.

## 4. Position recommandée

**Message** : *soutenir l'outil ouvert ; exiger qu'aucun chiffre de besoin ne soit utilisé pour fonder des objectifs 19f ou des soutiens 19g sans fourchettes d'incertitude, sensibilités de prix (art. 19e(2)(a)) et validation publiée.*

Demandes prioritaires, toutes vérifiables :
1. Sensibilités aux hypothèses de prix, de VoLL et de plafond, et niveau d'adéquation ancré au standard de fiabilité national.
2. Pile de revenus complète, ou bornée, pour les actifs flexibles ; risque explicite ; diagnostics de revenus publiés par actif.
3. Indicateurs de déficit probabilisés et conformes à la FNAM 10(2) ; attribution comptable fermée et contrefactuelle ; contribution des actifs existants.
4. Engagement des unités par groupes d'unités (entier) ou validation de la relaxation ; pas de 15 min ; révélation séquentielle de l'information en intraday.
5. Multi-années chaînées, erreurs de prévision historiques, stockage fictif avec pertes et cible moyenne.
6. Dossier de validation publié avant juillet 2027 et **second tour de consultation** sur le modèle final.

Projet de réponse en anglais : `07_consultation_response_methodology_EN.md`. Limites de nos propres conclusions : `08_contre_revue.md`.

## 5. Questions à poser au webinaire du 17 novembre

1. Comment les résultats d'EU-Flex seront-ils utilisés vis-à-vis des objectifs nationaux (19f) et des soutiens (19g) ? Avec quelles fourchettes d'incertitude ?
2. Quelle méthode de court terme (« simulation » ou « probabiliste ») sera retenue en 2027 ? Comment sera-t-elle rendue conforme aux marges de la FNAM 10(2) ?
3. Quelles hypothèses de VoLL, de plafonds et de taux de rendement exigés ? Seront-elles publiées et soumises à sensibilité ?
4. Le stockage fictif intégrera-t-il des rendements aller-retour par durée, comme l'exige la FNAM 8(10) ?
5. Une rétro-simulation et une comparaison avec l'ERAA seront-elles publiées ? Un second tour de consultation est-il prévu ?
