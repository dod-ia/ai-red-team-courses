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

## 🎯 Learn → Attack → Defend → Analyze

Chaque module suit une approche offensive puis défensive :

📚 **Learn** — comprendre les concepts, architectures et vecteurs d’attaque

🧪 **Attack** — expliquer les techniques offensives

🛡️ **Defend** — identifier les mitigations et renforcer le système

🔬 **Analyze** — reproduire et évaluer les attaques dans des labs contrôlés

Chaque module associe les **fondamentaux** nécessaires à sa compréhension avec des **labs hands-on** permettant d’expérimenter directement sur des scénarios réalistes.

> **Pas de raccourcis. Pas de boîtes noires. Juste de la théorie, des attaques et des labs pratiques.**

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

### Schéma d'attaque

| Module                    | Learn | Attack | Analyze | Defend |  Lab  | Difficulté |
| ------------------------- | :---: | :----: | :-----: | :----: | :---: | :--------: |
| Direct Prompt Injection   |   ✔️   |   ✔️    |    ✔️    |   ✔️    |       |     🟢      |
| Indirect Prompt injection |   🚧   |        |         |        |       |     🟢      |
| Function calling attack   |   🚧   |        |         |        |       |     🟢      |
| Adversarial Attack        |   🚧   |        |         |        |       |     🟡🔴     |

### Développement d'outils

| Module                                                       |  Lab  | Difficulté |
| ------------------------------------------------------------ | :---: | :--------: |
| Faire un module garak                                        |   🚧   |     🟢      |
| Construire un agent Red Team avec langGraph - Baseline garak |   🚧   |     🟢      |

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