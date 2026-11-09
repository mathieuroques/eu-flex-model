# Adversarial review d'EU-Flex — index

Revue adversariale indépendante de la version préliminaire 1.0.0-rc2 du modèle EU-Flex (ACER), réalisée le 9 novembre 2026.

| Livrable | Fichier |
|---|---|
| 1. Dossier de contexte et de recherche (phase 1, tenu séparé) | [`01_dossier_contexte_recherche.md`](01_dossier_contexte_recherche.md) |
| 2. Rapport d'adversarial review, findings hiérarchisés (§2-3) | [`02_rapport_adversarial_review.md`](02_rapport_adversarial_review.md) |
| 3. Verdict sur l'adéquation à l'objectif | même rapport, §5 |
| 4. Limites structurelles et améliorations indispensables | même rapport, §6 |
| 5. Notes de recherche sur l'état de l'art (grille Q1-Q12, sources ; remplacé comme étalon par le n° 7) | [`03_etat_de_l_art_methodologique.md`](03_etat_de_l_art_methodologique.md) |
| 6. **Revue adversariale de la méthode** contre l'état de l'art, expériences de robustesse, verdict méthodologique, méthode cible | [`04_revue_adversariale_methode.md`](04_revue_adversariale_methode.md) |
| 7. **Référentiel d'état de l'art autonome** (14 briques ; état de l'art établi ou construit lorsqu'il n'existe pas ; l'ERAA y est un plancher réglementaire) — **étalon de la revue méthodologique** | [`05_referentiel_etat_de_l_art.md`](05_referentiel_etat_de_l_art.md) |

## Preuves reproductibles

| Élément | Contenu |
|---|---|
| `tests/test_indicator_adversarial.py` | 11 tests pytest à solution analytique, appelant les fonctions de production. **Un échec = un défaut confirmé** (identifiant F-xx dans la docstring). Aucun solveur requis, ~10 s |
| `scripts/independent_recompute.py` | Recalcul indépendant des indicateurs FNAM 8(5) et 10(1) depuis les CSV bruts, comparé à `model_outputs.nc` |
| `scripts/make_adversarial_inputs.py` | Génère les jeux d'entrée corrompus (M1-M6) et bissextiles |
| `scripts/analyse_short_term.py` | Expériences sur le bruit synthétique (F-08) et sur la méthode probabiliste (F-09) |
| `scripts/method_experiments.py` | Expériences analytiques de méthode : bootstrap du P99,9, bande d'équilibre EVA, mutualisation régionale |
| `scripts/compare_runs.py` | Comparaison d'un run variante avec la référence (une convention modifiée à la fois : UC binaire, horizon, contrefactuel iDSR) |
| `configs/meth_*.yaml` | Configurations des variantes E-U (UC binaire), E-H (horizon 36/12), E-C (sans iDSR) : `snakemake -c1 --configfile adversarial_review/configs/meth_milp.yaml --directory runs/meth_milp` |
| `evidence/` | Sorties brutes : pytest, rapport de la suite d'intégration du modèle, recalcul indépendant, expériences de court terme, runs complémentaires |

Commandes de reproduction : rapport, §1.3. Les répertoires `runs/` produits par les exécutions ne sont pas versionnés (ils sont dans `.gitignore`).

Ce répertoire n'ajoute ni ne modifie aucun fichier du modèle.
