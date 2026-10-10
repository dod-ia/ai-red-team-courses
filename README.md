# 🛡️ AI Red Team — Learn by Breaking

<img src="./image_band.png" width="100%">

![AI Red Team](https://img.shields.io/badge/AI_RED_TEAM-Offensive_Security-DC2626?style=for-the-badge&logo=kalilinux&logoColor=white)
![GenAI Security](https://img.shields.io/badge/GENAI_SECURITY-Break._Test._Secure.-8A2BE2?style=for-the-badge&logo=openai&logoColor=white)
![Agentic Security](https://img.shields.io/badge/AGENTIC_SECURITY-AI_Agents_%26_MCP-0891B2?style=for-the-badge&logo=anthropic&logoColor=white)
![Cyber Range](https://img.shields.io/badge/CYBER_RANGE-Hands--On_Labs-16A34A?style=for-the-badge&logo=docker&logoColor=white)

**Learn. Attack. Analyze. Defend.**

> **Break AI before attackers do.**

Bienvenue dans un parcours hands-on dédié à l'**AI Red Teaming**.

Ce repository a un objectif simple : **apprendre à attaquer les systèmes d'IA pour mieux les défendre**.

✅ De la **théorie** pour comprendre les concepts  
✅ De la **pratique** pour comprendre leurs applications  
✅ Pas de magie noire, ni de scripts incompréhensibles

Ce repository propose une **approche progressive** et concrète, avec des explications claires, des **exemples détaillés** et des **environnements contrôlés** pour expérimenter les techniques d'AI Red Teaming.

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

Le parcours est divisé en **6 sections**:

| Domaine            | Description                                                                                                          |
| ------------------ | -------------------------------------------------------------------------------------------------------------------- |
| 📚 **Fondations**   | Acquérir les fondamentaux pour comprendre les concepts                                                               |
| ⚔️ **Attaque**      | Modéliser les surfaces d'attaque, les vecteurs d'exploitation et les impacts                                         |
| 🔒 **Défense**      | Comprendre les principes, techniques et mécanismes permettant de sécuriser les systèmes                              |
| 🏗️ **Architecture** | Comprendre la conception, le déploiement et la mise en production                                                    |
| 🛠️ **Outil**        | Maîtriser les frameworks et outils nécessaires pour développer, tester, observer et sécuriser des applications d'IA. |
| 🏛️ **Gouvernance**  | Comprendre les enjeux de conformité, de gestion des risques et de responsabilité liés aux systèmes                   |

### Approche « Learn → Attack → Analyze → Defend »

L'explication d'une attaque suit un **pattern en 4 étapes**:

| Étape         | Description                                                   |
| ------------- | ------------------------------------------------------------- |
| 📚 **Learn**   | Comprendre les concepts, architectures et vecteurs d'attaque. |
| 🧪 **Attack**  | Expliquer les techniques offensives.                          |
| 🔬 **Analyze** | Reproduire et évaluer les attaques dans des labs contrôlés.   |
| 🛡️ **Defend**  | Identifier les mitigations et renforcer le système.           |

Chaque module associe les **fondamentaux** nécessaires à sa compréhension avec des **labs hands-on** permettant d’expérimenter directement sur des scénarios réalistes.

> **Don't just read. Build. Break. Fix.**

> [!NOTE]
> Il sera fréquent qu'un **module fasse référence à un autre** dans le cadre de prérequis ou de détails supplémentaires associés à une notion particulière.

### Environnement des hands-on

L’objectif est de **confronter la théorie des attaques à la pratique** en permettant aux équipes AI Red Team de mettre en œuvre et d’expérimenter concrètement différents scénarios d’attaque. Pour cela, des environnements de test représentatifs sont mis en place afin de reproduire des conditions proches du réel et de tester les mécanismes de défense.

Ces environnements pourront être **crées sur mesure** ou exploiter des **environnements mis à disposition par la communauté**.

> [!TIP]
> Une attention particulière sera portée au *hands-on* des sections *Architecture* et *Développement d'outils* qui pourront servir d'environnement de test dans des scénarios d'attaque réalistes.

Selon les modules, les environnements pourront intégrer : **Kubernetes, containers, AI agents, architectures distribuées**...

## 🔭 Veille & Recherche

> **Read. Understand. Reproduce.**

L’**AI Security** évolue rapidement. Le repository intégrera également une veille régulière autour des nouvelles techniques d’attaque, vulnérabilités et méthodes de défense.

Nous nous appuierons notamment sur :

    📄 des papers de recherche ;

    🔬 des travaux de security researchers ;

    🛡️ des publications sur les nouvelles vulnérabilités et techniques de défense ;

    🧪 des expérimentations et PoC intéressants.

L’objectif est de lire, comprendre et reproduire les recherches les plus pertinentes afin de transformer les avancées du domaine en connaissances et labs pratiques.

## 🧭 Learning Path

> **Learn with purpose. Follow a path. Build your skills.**

Les **Learning Paths** ont pour objectif d'organiser les modules selon des objectifs d'apprentissage spécifiques, afin de proposer une progression cohérente et adaptée à chaque besoin.

Plutôt que de suivre les modules dans un ordre arbitraire, chaque parcours regroupera les notions théoriques, les techniques d'analyse et les exercices pratiques nécessaires pour atteindre un objectif précis.


|              Path              | Description                                                                     | Module (dans l'ordre) |
| :----------------------------: | :------------------------------------------------------------------------------ | --------------------- |
| **🤖 AI Agents & MCP Security** | Étudier les risques liés aux agents IA, aux outils et au Model Context Protocol | 🚧                     |


> [!IMPORTANT]
> **🚧 Work in progress**
> 
> **Cette section est en attente de la création d'un nombre suffisant de modules pour construire des parcours cohérents et progressifs**. Les Learning Paths seront définis et enrichis au fur et à mesure de l'avancement du repository. 

## 🧩 Modules

> **Difficulté / Prérequis**:
> 🟢 Débutant
> 🟡 Intermédiaire
> 🔴 Avancé

### 📚 Fondations

<details>
<summary>Prompt et Contexte</summary>

| #                                                                        |          Module          |    Type     |  Format   | Domaine | Contenu                      | Niveau | Status |
| ------------------------------------------------------------------------ | :----------------------: | :---------: | :-------: | :-----: | :--------------------------- | :----: | :----: |
| [**FO-LLM-PC-001**](/FO/FO-LLM/FO-LLM-PC/FO-LLM-PC-001/FO-LLM-PC-001.md) | LLM - Prompt et contexte | 📚 Fondation | 📖 Théorie |   LLM   | Prompt, template et contexte |   🟢    |   ✔️    |

</details>

<details>
<summary>Model Context Protocol</summary>

| #                                                                            |                  Module                  |    Type     |   Format   | Domaine | Contenu                                        | Niveau | Status |
| ---------------------------------------------------------------------------- | :--------------------------------------: | :---------: | :--------: | :-----: | :--------------------------------------------- | :----: | :----: |
| [**FO-MCP-PCF-001**](/FO/FO-MCP/FO-MCP-PCF/FO-MCP-PCF-001/FO-MCP-PCF-001.md) | MCP - Protocole et concepts fondamentaux | 📚 Fondation | 📖 Théorie  |   MCP   | Protocole, clients, serveurs, tools, resources |   🟡    |   ✔️    |
| [**FO-MCP-PCF-002**](/FO/FO-MCP/FO-MCP-PCF/FO-MCP-PCF-002/FO-MCP-PCF-002.md) | MCP - Protocole et concepts fondamentaux | 📚 Fondation | 💻 Hands-on |   MCP   | Multi-nœuds, middleware, notifications         |   🟡    |   ✔️    |

</details>

<details>
<summary>Authentification</summary>

| #                  |         Module         |    Type     |  Format   | Domaine | Contenu                      | Niveau | Status |
| ------------------ | :--------------------: | :---------: | :-------: | :-----: | :--------------------------- | :----: | :----: |
| **FO-AUT-JWT-001** | Authentification - JWT | 📚 Fondation | 📖 Théorie |  AUTH   | JWT, JWS, JWK et application |   🟡    |   🚧    |

</details>

<details>
<summary>Deep Learning</summary>

| #                 |            Module             |    Type     |  Format   | Domaine | Contenu                      | Niveau | Status |
| ----------------- | :---------------------------: | :---------: | :-------: | :-----: | :--------------------------- | :----: | :----: |
| **FO-DL-LEA-001** | Deep Learning - Apprentissage | 📚 Fondation | 📖 Théorie |   DL    | Rétropropagation du gradient |   🟡    |   🚧    |

</details>

### 🏗️ Architecture

<details>
<summary>Model Context Protocol</summary>

| #                    |                  Module                  |      Type      |   Format   | Domaine | Contenu                                                | Niveau | Status |
| :------------------- | :--------------------------------------: | :------------: | :--------: | :-----: | :----------------------------------------------------- | :----: | :----: |
| **AR-MCP-MCPAR-001** | MCP Architecture - Déploiement distribué | 🏗️ Architecture | 💻 Hands-on |   MCP   | OpenTelemetry, K8S, Load Balancer, Bus d'échange, Auth |   🔴    |   🚧    |

</details>

### ⚔️ Attaques / Général

<details>
<summary>Injection</summary>

| #                   | Module          |   Type   |   Format   |  Domaine  | Contenu                                                   | OWASP    | MITRE ATLAS | Niveau | Statut |
| :------------------ | :-------------- | :------: | :--------: | :-------: | :-------------------------------------------------------- | :------- | :---------- | :----: | :----: |
| **AT-INJ-SQLI-001** | *Injection SQL* | ⚔️ Attack | 💻 Hands-on | Injection | manipulation des requêtes SQL et extraction non autorisée | A05:2025 | T1190       |   🟢    |   🚧    |

</details>

### ⚔️ Attaques / IA

<details>
<summary>Prompt Injection</summary>

| #                 | Module             |   Type   |  Format   | Domaine | Contenu                 | OWASP      | MITRE ATLAS                | Niveau | Statut |
| :---------------- | :----------------- | :------: | :-------: | :-----: | :---------------------- | :--------- | :------------------------- | :----: | :----: |
| [**AT-LLM-PI-001**](/AT/AT-LLM/AT-LLM-PI/AT-LLM-PI-001/AT-LLM-PI-001.md) | *Prompt Injection* | ⚔️ Attack | 📖 Théorie |   LLM   | Direct Prompt Injection | LLM01:2025 | AML.T0051.000<br>AML.T0054 |   🟢    |   ✔️    |

</details>

<details>
<summary>Model Context Protocol</summary>

| #                   | Module                                   |   Type   |   Format   | Domaine | Contenu                                                                                              | OWASP                    | MITRE ATLAS   | Niveau | Statut |
| :------------------ | :--------------------------------------- | :------: | :--------: | :-----: | :--------------------------------------------------------------------------------------------------- | :----------------------- | :------------ | :----: | :----: |
| **AT-MCP-MCPA-001** | *MCP Attack — Injection Vulnerabilities* | ⚔️ Attack | 💻 Hands-on |   MCP   | Exploitation d'entrées non fiables, notamment par injection de commandes, de code ou de requêtes SQL | A05:2025<br>MCP05:2025   | AML.T0050     |   🟡    |   🚧    |
| **AT-MCP-MCPA-002** | *MCP Attack — Excessive Agency*          | ⚔️ Attack | 💻 Hands-on |   MCP   | Abus de capacités ou de permissions excessives accordées à un agent ou à ses outils                  | MCP02:2025<br>LLM06:2025 | AML.T0053     |   🟡    |   🚧    |
| **AT-MCP-MCPA-003** | *MCP Attack — Tool Poisoning*            | ⚔️ Attack | 💻 Hands-on |   MCP   | Manipulation des descriptions d'outils ou de leurs métadonnées pour influencer le client             | MCP03:2025               | AML.T0110.000 |   🟡    |   🚧    |
| **AT-MCP-MCPA-004** | *MCP Attack — Rug Pull*                  | ⚔️ Attack | 💻 Hands-on |   MCP   | Modification malveillante du comportement d'un outil après sa validation initiale                    | MCP03:2025               | AML.T0109     |   🔴    |   🚧    |
| **AT-MCP-MCPA-005** | *MCP Attack — Tool Shadowing*            | ⚔️ Attack | 💻 Hands-on |   MCP   | Exploitation d'outils homonymes, ambigus ou concurrents pour détourner le choix du client            | MCP03:2025               | AML.T0110.000 |   🟡    |   🚧    |

</details>

### 🔒 Defense

### 🏛️ Management du risque AI, audit et gouvernance

<details>
<summary>Threat Model</summary>

| #                  | Module                               |     Type      |  Format   |   Domaine    | Contenu                             | Niveau | Statut |
| :----------------- | :----------------------------------- | :-----------: | :-------: | :----------: | :---------------------------------- | :----: | :----: |
| **GOV-TM-TMO-001** | Threat Model - Concepts fondamentaux | 🏛️ Gouvernance | 📖 Théorie | Threat Model | Standards, modèle et représentation |   🟡    |   🚧    |

</details>

### 🛠️ Développement d'outil Red Teaming

<details>
<summary>Model Context Protocol</summary>

| #                     | Module   |  Type   |   Format   | Domaine | Contenu                     | Niveau | Statut |
| :-------------------- | :------- | :-----: | :--------: | :-----: | :-------------------------- | :----: | :----: |
| **TOOL-MCP-DAST-001** | MCP DAST | 🛠️ Outil | 💻 Hands-on |   MCP   | Analyse dynamique Black-Box |   🔴🔴   |   🚧    |

</details>

## 🧰 Prérequis

Ce parcours est orienté **hands-on** et abordera des **notions avancées**.

Il est recommandé d'avoir des notions en :

    🐍 Python  
    🧠 Deep Learning / Machine Learning  
    🐧 administration Linux  
    📐 mathématiques appliquées à l'IA  

**Il n'est pas nécessaire de posséder un GPU puissant**. Néanmoins, un GPU d'**au moins 8Go de VRAM** est fortement conseillé. Les hands-on exploiteront des modèles légers ou exploiteront les services gratuits de fournisseurs externes.

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