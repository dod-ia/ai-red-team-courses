# 🛡️ AI Red Team — Learn by Breaking

**Learn. Attack. Analyze. Defend.**

> **Break AI before attackers do.**

Bienvenue dans un parcours hands-on dédié à l'**AI Red Teaming**.

Ce repository a un objectif simple : **apprendre à attaquer les systèmes d'IA pour mieux les défendre**.

✅ Pas de théorie déconnectée du terrain.  
✅ Pas de démonstrations dans des environnements irréalistes.  
✅ Pas de "magie noire".  

Ce repository combine **cours théoriques** et **labs pratiques** pour passer rapidement de la compréhension des concepts à leur mise en application.

> [!WARNING]
> ⚠️ Usage éthique uniquement !
> 
> Les techniques présentées dans ce repository sont destinées à la formation, à la recherche en sécurité et aux tests réalisés dans des environnements autorisés.
> 
> Les techniques et exercices doivent être réalisés **uniquement**:
> 
> - sur vos propres systèmes ;
> - dans des environnements de laboratoire ;
> - avec une autorisation explicite ;
> - dans le cadre de programmes de sécurité autorisés.
>
> **L'auteur décline toute responsabilité concernant l'utilisation abusive des informations présentes dans ce repository.**

## 🎯 Structure du parcours

Le parcours est divisé en **5 sections**:

| Domaine                                                         | Description                                                                                                                |
| --------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| 🔒 **Fondations offensives**                                     | Bases et fondamentaux de la sécurité offensive d'un système d'information.                                                 |
| 🎯 **Schéma d'attaque**                                          | Modéliser les surfaces d'attaque, les vecteurs d'exploitation et les impacts propres aux systèmes d'IA.                    |
| 🔒 **Schéma de défense**                                         | Comprendre les principes, techniques et mécanismes permettant de sécuriser les systèmes d'IA.                              |
| 🧠 **Fondations d'architecture IA / Théorie de l'apprentissage** | Comprendre l'architecture, l'entraînement et l'inférence des systèmes d'IA afin de mieux appréhender leurs vulnérabilités. |
| 🛠️ **Écosystème IA et développement d'outils**                   | Maîtriser les frameworks et outils nécessaires pour développer, tester, observer et sécuriser des applications d'IA.       |
### Approche « Learn → Attack → Analyze → Defend »

L'explication d'une attaque suit un **pattern en 4 étapes**:

| Étape         | Description                                                   |
| ------------- | ------------------------------------------------------------- |
| 📚 **Learn**   | Comprendre les concepts, architectures et vecteurs d'attaque. |
| 🧪 **Attack**  | Expliquer les techniques offensives.                          |
| 🔬 **Analyze** | Reproduire et évaluer les attaques dans des labs contrôlés.   |
| 🛡️ **Defend**  | Identifier les mitigations et renforcer le système.           |

Chaque module associe les **fondamentaux** nécessaires à sa compréhension avec des **labs hands-on** permettant d’expérimenter directement sur des scénarios réalistes.

> **Pas de raccourcis. Pas de boîtes noires. Juste de la théorie, des attaques et des labs pratiques.**

> [!NOTE]
> Pour les autres sections que **Schéma d'attaque** et **Fondations offensives**, le pattern est uniquement **Learn → Analyze**.
>
> Il se peut qu'un **module fasse référence à un autre** dans le cadre de prérequis ou de détails supplémentaires associés à une notion particulière.


## 🧪 Hands-on Labs

**Don't just read. Build. Break. Fix.**

L’objectif est de **confronter la théorie des attaques à la pratique**, en permettant aux équipes AI Red Team de mettre en œuvre et d’expérimenter concrètement différents scénarios d’attaque. Pour cela, des environnements de test représentatifs sont mis en place afin de reproduire des conditions proches du réel et de tester les mécanismes de défense.

**🎯 Au programme** : prompt injection, jailbreaks, data leakage, adversarial attacks, RAG security, agent security, et bien plus encore.

Une  particulière est également consacrée à la **construction d’environnements AI complets** afin que vous puissiez reproduire les expérimentations.

Selon les modules, les environnements pourront intégrer :

    🤖 LLMs

    ⚡ inference engines

    🔎 RAG pipelines

    🗄️ vector databases

    🧠 AI agents

    🔌 APIs

    ☸️ Kubernetes

    🐳 containers

    🌐 distributed architectures

    🔗 multi-component AI systems

### 🚧 Environnement

Les environnements fournis dans ce repository sont des environnements de recherche et de formation.

Ils peuvent volontairement contenir :

    des configurations vulnérables ;

    des contrôles de sécurité affaiblis ;

    des composants volontairement exposés ;

    des données de test ;

    des architectures simplifiées.

**Ils ne sont pas conçus pour être déployés tels quels en production.**

## 🔭 Veille & Recherche

**Read. Understand. Reproduce.**

L’**AI Security** évolue rapidement. Le repository intégrera également une veille régulière autour des nouvelles techniques d’attaque, vulnérabilités et méthodes de défense.

Nous nous appuierons notamment sur :

    📄 des papers de recherche ;

    🔬 des travaux de security researchers ;

    🛡️ des publications sur les nouvelles vulnérabilités et techniques de défense ;

    🧪 des expérimentations et PoC intéressants.

L’objectif est de lire, comprendre et reproduire les recherches les plus pertinentes afin de transformer les avancées du domaine en connaissances et labs pratiques.

## Roadmap

> [!NOTE]
> La section *Lab* correspond à la création d'un environnement de *test* pour les expérimentations. Il se peut qu'il n'y ait pas de *Lab* selon les sections.

### Fondations offensives

| Module                                  | Learn | Attack | Defend | Analyze |  Lab  | Difficulté |
| --------------------------------------- | :---: | :----: | :----: | :-----: | :---: | :--------: |
| Injection SQL - Fondations              |   🚧   |        |        |         |       |     🟢      |
| Cross-Site Scripting (XSS) - Fondations |   🚧   |        |        |         |       |     🟢      |
| Pentest - Phase de Reconnaissance       |   🚧   |        |        |         |       |     🟢      |

### Fondations d'architecture IA / Théorie de l'apprentissage

| Module                                       | Learn | Analyze |  Lab  | Difficulté |
| -------------------------------------------- | :---: | :-----: | :---: | :--------: |
| Apprentissage - Rétropropagation du gradient |   🚧   |         |       |     🟡      |


### Schéma d'attaque

| Module                     |                            Learn                            |                            Attack                             | Defend | Analyze |  Lab  | Difficulté |
| -------------------------- | :---------------------------------------------------------: | :-----------------------------------------------------------: | :----: | :-----: | :---: | :--------: |
| Direct Prompt Injection    | [✔️](/schema_attaque/direct_prompt_injection/learn/learn.md) | [✔️](/schema_attaque/direct_prompt_injection/attack/attack.md) |        |         |       |     🟢      |
| Indirect Prompt injection  |                              🚧                              |                                                               |        |         |       |     🟢      |
| Insecure Output Handling   |                              🚧                              |                                                               |        |         |       |     🟢      |
| Adversarial Attack - Image |                              🚧                              |                                                               |        |         |       |     🔴      |
| Adversarial Attack - Text  |                              🚧                              |                                                               |        |         |       |     🔴      |
| MCP attack                 |                              🚧                              |                                                               |        |         |       |     🟡      |
| Model reversing            |                              🚧                              |                                                               |        |         |       |     🟢      |
| Deny of ML access          |                              🚧                              |                                                               |        |         |       |     🟢      |

### Schéma de défense

| Module                    | Learn | Analyze |  Lab  | Difficulté |
| ------------------------- | :---: | :-----: | :---: | :--------: |
| Guardrails                |   🚧   |         |       |     🟢      |
| Chiffrement homomorphique |   🚧   |         |       |     🔴      |
| Differential privacy      |   🚧   |         |       |     🟡🔴     |
| Watermark sur LLM         |   🚧   |         |       |     🟡🔴     |

### Ecosystème IA et développement d'outils

| Module                                                    |                           Learn                           |                            Analyze                            |  Lab  | Difficulté |
| --------------------------------------------------------- | :-------------------------------------------------------: | :-----------------------------------------------------------: | :---: | :--------: |
| Model Context Protocol (MCP) - Fondations                 | [✔️](/developpements_outils/mcp_fondations/learn/learn.md) | [✔️](/developpements_outils/mcp_fondations/analyse/analyse.md) |   ⌀   |     🟡      |
| Déployer un serveur MCP en production                     |                             🚧                             |                                                               |       |     🔴      |
| Faire un outil MCP DAST                     |                             🚧                             |                                                               |       |     🔴      |
| LangChain - Faire son premier RAG                         |                             🚧                             |                                                               |       |     🟢      |
| LangFuse - Observabilité d'un system IA (LangChain/Graph) |                             🚧                             |                                                               |       |     🟢      |
| LangGraph - Faire son premier agent Red Team              |                             🚧                             |                                                               |       |     🟡      |
| Construire son premier système multi-agent                |                             🚧                             |                                                               |       |     🟡      |

### Management du risque AI, audit et gouvernance

| Module                    | Learn | Analyze | Difficulté |
| ------------------------- | :---: | :-----: | :--------: |
| Faire un modèle de menace |   🚧   |         |     🟢      |
| NIST AI Framework         |   🚧   |         |     🟡      |
| ISO 42000                 |   🚧   |         |     🟡      |

> 🟢 Débutant
> 🟡 Intermédiaire
> 🔴 Avancé

## 🧰 Prérequis

Ce parcours est orienté **hands-on**.

Vous devriez avoir des bases en :

    🐍 Python  
    🧠 Deep Learning / Machine Learning  
    🐧 administration Linux  
    📐 mathématiques appliquées à l'IA  

## 🤝 Contribution

Ce dépôt regroupe différents cours et tutoriels destinés à l’apprentissage. Les contributions sont les bienvenues afin d’améliorer et d’enrichir le contenu.

Vous pouvez notamment :

    🐛 Signaler une erreur dans un cours ou un tutoriel.
    ✏️ Corriger ou améliorer une explication.
    💡 Proposer des exemples ou des exercices supplémentaires.
    📚 Ajouter un nouveau cours ou tutoriel.
    🔗 Signaler un lien qui ne fonctionne plus ou une ressource obsolète.

Pour contribuer, vous pouvez ouvrir une **Issue** pour signaler un problème ou proposer une idée, ou soumettre directement une **Pull Request** avec vos modifications.

**Toutes les contributions permettant de rendre les cours plus clairs, accessibles et utiles sont les bienvenues !**