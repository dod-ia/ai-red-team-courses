# GO-TM-TMC-001: Threat Model - Concepts fondamentaux

## Définition du Threat Modeling

Le **Threat Modeling** (modélisation des menaces) consiste à identifier les actifs à protéger, les menaces qui pèsent sur le système, les vulnérabilités exploitables et les mesures de sécurité à mettre en place.

L'objectif est d'**anticiper les scénarios d'attaque avant qu'ils ne deviennent des incidents de sécurité**. Il est ainsi possible d'influer sur l'implémentation d'un système et son cycle de vie afin de limiter le risque sous-jacent à sa mise en production.

> [!IMPORTANT]
> Produire un *Threat Model* demande une connaissance avancée des systèmes d'information et de leurs interactions. Un *Threat Model* nécessite notamment des connaissances en architecture, en réseau, en sécurité offensive et défensive...

## Vulnérabilité, risque et menace

Dans le cadre du Threat Modeling, il est essentiel de distinguer trois notions complémentaires :

* **Menace (Threat)** : événement ou action susceptible de porter atteinte à un système, à ses actifs ou à ses données. Elle peut notamment résulter d'une action malveillante d'un attaquant.

* **Vulnérabilité (Vulnerability)** : faiblesse technique, humaine ou organisationnelle pouvant être exploitée pour compromettre un système.

* **Risque (Risk)** : possibilité qu'un scénario de menace se réalise et entraîne des conséquences négatives. Son évaluation prend notamment en compte la vraisemblance du scénario et son impact potentiel.

<details>
<summary><strong>Exemple : une API permettant d'accéder à des données utilisateur</strong></summary>

| Notion            | Exemple                                                                                                             |
| ----------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Menace**        | Un attaquant cherche à accéder aux données d'un autre utilisateur.                                                  |
| **Vulnérabilité** | L'API ne vérifie pas correctement les autorisations d'accès aux données.                                            |
| **Risque**        | Des données confidentielles peuvent être divulguées, entraînant un préjudice pour les utilisateurs et l'entreprise. |

</details>

<br>

> La menace représente ce qui peut arriver, la vulnérabilité correspond à une faiblesse exploitable et le risque traduit les conséquences potentielles et la probabilité de la réalisation d'un scénario.

## Deux perspectives complémentaires : attaquant et défenseur

Un *Threat Model* peut être perçu par deux points de vue : celui de l'attaquant et celui du défenseur :

* L'attaquant cherche comment **compromettre le système**
* Le défenseur cherche comment **identifier, prévenir et limiter ces attaques**.

| Critère                 | Vue attaquant (Attacker Perspective)                                         | Vue défenseur (Defender Perspective)                                              |
| ----------------------- | ---------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| **Objectif**            | Identifier les moyens de compromettre le système.                            | Protéger le système contre les menaces.                                           |
| **Question principale** | Comment puis-je exploiter ce système ?                                       | Comment ce système peut-il être attaqué et comment le protéger ?                  |
| **Cible**               | Actifs intéressants à compromettre.                                          | Actifs critiques à protéger.                                                      |
| **Approche**            | Rechercher les vulnérabilités, les points d'entrée et les chemins d'attaque. | Identifier les menaces, évaluer les risques et définir les contrôles de sécurité. |
| **Analyse**             | Techniques d'exploitation, escalade de privilèges, mouvement latéral.        | Prévention, détection, réponse et réduction de la surface d'attaque.              |
| **Résultat**            | Scénarios d'attaque et chemins de compromission possibles.                   | Mesures de sécurité, mécanismes de détection et plan de traitement des risques.   |
| **Exemple**             | Comment accéder aux données d'un autre utilisateur via une API ?             | Comment empêcher les accès non autorisés aux données via cette API ?              |

En pratique, un *Threat Model* efficace **combine les deux perspectives**. La vision de l'attaquant permet d'anticiper les scénarios d'attaque ; celle du défenseur permet de définir les mesures de prévention, de détection et de réduction des risques. 

Le Threat Modeling ne se limite donc pas à identifier des vulnérabilités. Il cherche surtout à comprendre les scénarios d'attaque, les conditions nécessaires à leur réalisation et leurs conséquences potentielles.

## Les grandes étapes d'un Threat Model

Un *Threat Model* est défini par cinq étapes:

> Scoping → Modélisation → Analyse des risques → Contre-mesures → Validation et suivi

| Étape                      | Description                                             |
| -------------------------- | ------------------------------------------------------- |
| **1. Scoping**             | Définir le système et les actifs à protéger.            |
| **2. Modélisation**        | Représenter l'architecture et identifier les menaces.   |
| **3. Analyse des risques** | Évaluer et prioriser les menaces.                       |
| **4. Contre-mesures**      | Définir les protections adaptées.                       |
| **5. Validation et suivi** | Vérifier les protections et maintenir le modèle à jour. |

> [!IMPORTANT]
> Dans une approche centrée sur la construction du modèle de menaces, les activités principales concernent généralement le ***Scoping*, la modélisation et l'analyse des risques**. La définition des contre-mesures, leur validation et le suivi peuvent être intégrés au processus de *Threat Modeling* ou traités dans un processus plus large de gestion des risques, selon la méthode et l'organisation.

### Scoping

Le *Scoping* consiste à **définir les limites du système** étudié et à **identifier les actifs** à protéger afin de cadrer l'analyse des menaces. Il se divise en deux étapes complémentaires :

* La définition du **périmètre** du système à analyser
* L'identification des **actifs** à protéger.

| Étape                                 | Description                                                                                                                                                   | Livrable              |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------- |
| **1. Définir le périmètre (Scope)**   | Délimiter le système à analyser et préciser les composants et fonctionnalités inclus ou exclus de l'analyse.                                                  | Périmètre défini      |
| **2. Identifier les actifs (Assets)** | Recenser les données et ressources à protéger, évaluer leur sensibilité et définir leurs exigences de confidentialité, d'intégrité et de disponibilité (CIA). | Inventaire des actifs |

> [!IMPORTANT]
> Cette étape combine une compréhension métier des actifs et une délimitation technique du système.

### Modélisation

Cette étape consiste à représenter les composants du système, leurs interactions, les flux de données et les frontières de confiance afin de faciliter l'identification des menaces potentielles.

| Élément                     | Description                                                       | Livrable                            |
| --------------------------- | ----------------------------------------------------------------- | ----------------------------------- |
| **Architecture**            | Identifier les composants et leurs interactions.                  | Diagramme d'architecture            |
| **Flux de données**         | Représenter les échanges de données entre les composants.         | Diagramme de flux de données (DFD)  |
| **Frontières de confiance** | Identifier les zones de confiance et leurs points de transition.  | Frontières de confiance identifiées |
| **Points d'entrée**         | Identifier les interfaces permettant d'interagir avec le système. | Liste des points d'entrée           |

### Analyse de risques

L'*analyse des risques* consiste à identifier les scénarios de menace susceptibles d'affecter le système, puis à évaluer les risques associés afin de les caractériser et de les prioriser. Cette phase se divise en deux étapes complémentaires:

* **Identification des menaces** (*Threat Identification*)
* **Evaluation des risques** (*Risk Assessment*)

| Étape                                                    | Description                                                                                                                                    | Livrable                                 |
| -------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------- |
| **Identification des menaces** (*Threat Identification*) | Analyser les composants, les actifs et les flux de données pour identifier les menaces potentielles et les scénarios d'attaque associés.       | Registre des menaces (*Threat Register*) |
| **Évaluation des risques** (*Risk Assessment*)           | Évaluer chaque scénario selon sa probabilité de réalisation et son impact afin de déterminer son niveau de risque et de prioriser les menaces. | Registre des risques (*Risk Register*)   |

#### Identification des menaces

Une *menace* est un événement ou un scénario potentiel susceptible de porter atteinte à la sécurité d'un système, d'un actif ou d'une organisation. Elle représente ce qui pourrait arriver et compromettre la confidentialité, l'intégrité ou la disponibilité d'un système.

> Acteur de menace → exploite une vulnérabilité → réalise un scénario d'attaque → provoque un impact.

Une bonne description doit permettre de répondre à quatre questions :

1. **Qui ?** Quel acteur pourrait être à l'origine du scénario ?
2. **Quoi ?** Quelle action pourrait-il réaliser ?
3. **Comment ?** Dans quelles conditions et par quel mécanisme ?
4. **Avec quelles conséquences ?** Quel actif ou quelle propriété de sécurité serait affecté ?

Un *Threat Model* peut représenter une menace à travers la matrice suivante:

| Élément | Question |
|---|---|
| Actif | Qu'est-ce que je protège ? |
| Menace | Que pourrait-il se passer ? |
| Vulnérabilité | Quelle faiblesse pourrait rendre ce scénario possible ? |
| Scénario d'attaque | Comment la menace pourrait-elle se concrétiser ? |
| Impact | Quelles seraient les conséquences ? |

#### Evaluation des risques

L'*évaluation des risques* consiste à déterminer le niveau de risque associé à une menace, en tenant compte de sa probabilité de réalisation et de son impact potentiel.

On se pose principalement deux questions :

* **Probabilité (Likelihood)** : quelle est la probabilité que le scénario de menace se réalise ?
* **Impact (Impact)** : quelles seraient les conséquences si le scénario se réalisait ?

On peut utiliser une formule simplifiée : **Risque = Probabilité × Impact**

L'objectif est de déterminer quelles menaces traiter en priorité, en fonction de leur vraisemblance et de leurs conséquences potentielles.

> [!NOTE]
> Cette définition est théorique et la méthode de calcul peut varier selon le protocole retenu.

Ainsi, l'évaluation des risques complète l'identification des menaces :

> Actif → Menace → Vulnérabilité éventuelle → Scénario d'attaque → Évaluation du risque

### Contre-mesures

Les contre-mesures consistent à définir et à mettre en place des mesures de sécurité adaptées aux menaces identifiées afin de réduire les risques associés.

| Étape              | Description                                                                       | Livrable                          |
| ------------------ | --------------------------------------------------------------------------------- | --------------------------------- |
| **Identification** | Définir les mesures de sécurité adaptées aux menaces identifiées.                 | Liste des contre-mesures          |
| **Priorisation**   | Classer les mesures selon la criticité des risques et les ressources nécessaires. | Plan de traitement priorisé       |
| **Mise en œuvre**  | Déployer les mesures retenues                                                     | Contrôles de sécurité implémentés |

Ainsi, la définition des contre-mesures complète l'analyse de risques :

> Actif → Menace → Vulnérabilité éventuelle → Scénario d'attaque → Évaluation du risque → Mesures de sécurité

### Validation et suivi

La validation et le suivi permettent de vérifier l'efficacité des mesures mises en place et d'adapter le modèle de menace aux évolutions du système et aux nouvelles menaces.

On distingue notamment deux niveaux de risque : **le risque inhérent et le risque résiduel** :

| Type de risque | Définition |
|---|---|
| **Risque inhérent (Inherent Risk)** | Niveau de risque auquel un système est exposé avant la mise en place des mesures de sécurité. |
| **Risque résiduel (Residual Risk)** | Niveau de risque qui subsiste après la mise en place des mesures de sécurité destinées à réduire ou à maîtriser ce risque. |

> [!IMPORTANT]
> Le *risque résiduel* correspond au niveau de risque qui subsiste après la mise en œuvre des mesures de sécurité. L'objectif est de le ramener à un niveau jugé acceptable par l'entreprise. Si ce seuil est dépassé, des mesures complémentaires peuvent être nécessaires. Ce seuil repose sur des considérations métier et sur l'appétence au risque de l'organisation.


L'objectif de cette étape est ainsi **d'évaluer le risque résiduel et d'évaluer son évolution (et celles de possibles nouveaux risques) au fil du temps**.

| Étape                                   | Description                                                                                          | Livrable                         |
| --------------------------------------- | ---------------------------------------------------------------------------------------------------- | -------------------------------- |
| **1. Tests de validation**              | Vérifier par des tests que les contre-mesures fonctionnent efficacement.                             | Rapport de validation            |
| **2. Évaluation des risques résiduels** | Réévaluer les risques après la mise en œuvre des mesures de sécurité. Vérifier que le risque résiduel est sous le seuil acceptable.                               | Évaluation des risques résiduels |
| **3. Surveillance**                     | Suivre l'efficacité des contrôles et détecter les nouvelles menaces.                                 | Rapport de suivi                 |
| **4. Mise à jour**                      | Actualiser le modèle de menace en fonction des changements du système et de l'évolution des menaces. | Modèle de menace actualisé       |

Ainsi, le processus final est:

> Actif → Menace → Vulnérabilité éventuelle → Scénario d'attaque → Évaluation du risque → Mesures de sécurité → Risque résiduel.
