# Adversarial review d'EU-Flex — index

Revue adversariale indépendante de la version préliminaire 1.0.0-rc2 du modèle EU-Flex (ACER), réalisée le 9 novembre 2026.

| Livrable | Fichier |
|---|---|
| 1. Dossier de contexte et de recherche (phase 1, tenu séparé) | [`01_dossier_contexte_recherche.md`](01_dossier_contexte_recherche.md) |
| 2. Rapport d'adversarial review, findings hiérarchisés (§2-3) | [`02_rapport_adversarial_review.md`](02_rapport_adversarial_review.md) |
| 3. Verdict sur l'adéquation à l'objectif | même rapport, §5 |
| 4. Limites structurelles et améliorations indispensables | même rapport, §6 |

## Preuves reproductibles

| Élément | Contenu |
|---|---|
| `tests/test_indicator_adversarial.py` | 11 tests pytest à solution analytique, appelant les fonctions de production. **Un échec = un défaut confirmé** (identifiant F-xx dans la docstring). Aucun solveur requis, ~10 s |
| `scripts/independent_recompute.py` | Recalcul indépendant des indicateurs FNAM 8(5) et 10(1) depuis les CSV bruts, comparé à `model_outputs.nc` |
| `scripts/make_adversarial_inputs.py` | Génère les jeux d'entrée corrompus (M1-M6) et bissextiles |
| `scripts/analyse_short_term.py` | Expériences sur le bruit synthétique (F-08) et sur la méthode probabiliste (F-09) |
| `evidence/` | Sorties brutes : pytest, rapport de la suite d'intégration du modèle, recalcul indépendant, expériences de court terme, runs complémentaires |

Commandes de reproduction : rapport, §1.3. Les répertoires `runs/` produits par les exécutions ne sont pas versionnés (ils sont dans `.gitignore`).

Ce répertoire n'ajoute ni ne modifie aucun fichier du modèle.
