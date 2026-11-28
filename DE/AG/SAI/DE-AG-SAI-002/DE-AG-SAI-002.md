# DE-AG-SAI-002: Sécurité des agents IA - Authentification et gestion des permissions

**Prérequis**: [FO-AUT-JWT-001](FO/FO-AUT/FO-AUT-JWT/FO-AUT-JWT-001/FO-AUT-JWT-001.md), connaissance de [Deepagents](https://github.com/langchain-ai/deepagents)

## Contexte

Les agents IA deviennent de véritables applications : ils possèdent des configurations, conservent des conversations et peuvent utiliser des outils pour agir.

Mais dès que plusieurs utilisateurs partagent une même plateforme, une question apparaît :

**Comment garantir que chaque utilisateur accède uniquement aux assistants, aux conversations et aux capacités qui lui sont autorisés ?**

Imaginons une plateforme sur laquelle Alice, Claude et Bob peuvent créer leurs propres assistants IA.

Chaque utilisateur peut :

* Créer un assistant.
* Démarrer une conversation avec un assistant.
* Retrouver ses conversations.
* Interagir avec un agent.
* Utiliser les tools mis à sa disposition.

Cependant, tous les utilisateurs n'ont pas les mêmes droits. Alice et Claude sont des utilisateurs classiques. Bob est administrateur.

Tout semble fonctionner… jusqu'à ce que nous testions les limites de notre système.

Un agent IA n'est pas seulement une interface de conversation. Il peut conserver un état, accéder à des documents, appeler des outils, déclencher des opérations et interagir avec des services. La sécurité doit donc protéger à la fois les API de la plateforme, les ressources persistantes et les actions réalisées pendant une exécution.

**L'objectif n'est pas de rendre l'agent « prudent » grâce à son prompt**. Il est de construire, autour de lui, des contrôles techniques qui déterminent **qui peut faire quoi, sur quelle ressource et avec quels outils**.

## Problème 1: Qui a accès à la plateforme ?

Supposons qu'Alice envoie une requête pour créer un assistant. Afin de répondre, notre plateforme doit d'abord savoir qui effectue cette opération: c'est le rôle de l'**authentification**.

Sans cette information, il est **impossible de distinguer une requête
légitime d'une requête anonyme** ou de rattacher correctement les actions réalisées à un utilisateur.

L'identité ne doit pas être simplement déclarée dans le message
conversationnel. Une instruction telle que « je suis administrateur » ou un identifiant transmis librement par le client ne constitue pas une preuve.

### Solution : authentifier l'utilisateur avant le traitement

L'application s'appuie sur un mécanisme d'authentification reconnu :
session sécurisée, token signé ou intégration à un fournisseur
d'identité.

Dans le cas d'une API, le client peut présenter un token d'accès. Le
serveur doit alors vérifier notamment :

* La signature ou l'intégrité du token.
* L'émetteur et le destinataire attendus.
* La période de validité.
* La présence et la cohérence des informations d'identité nécessaires.

Une fois l'identité validée, elle est transmise au contexte d'exécution de la requête.

Par exemple, si l'authentification est basée sur un *bearer*, le client présente le token dans l'en-tête HTTP :

``` http
Authorization: Bearer <token>
```

**L'objectif est simple : chaque opération doit pouvoir être rattachée à
une identité vérifiée.**

## Problème 2 : Comment définir les droits d'action d'un utilisateur

L'authentification confirme l'identité, mais ne définit pas les droits.

Un utilisateur peut être autorisé à consulter ses conversations sans
pouvoir accéder à celles d'un autre utilisateur. Il peut utiliser un
agent public sans pouvoir lancer un agent réservé à l'administration.

C'est la différence entre **authentification** et **autorisation** :

* L'**authentification** répond à : **« Qui es-tu ? »**
* L'**autorisation** répond à : **« As-tu le droit d'effectuer cette action ? »**

Comment définir les droits d'un utilisateur ?

### Solution : définir une politique d'accès

Les droits peuvent être organisés selon l'approche **RBAC** (*Role-Based Access Control*).

Le **RBAC** attribue à chaque utilisateur des permissions en fonction de son rôle (`user`, `operator`, `admin`...). Par exemple, un administrateur peut demander à un assistant IA d'utiliser un *tool* réservé aux admins tandis qu’un utilisateur classique peut uniquement interagir avec les *tools* utilisateur.

Les **permissions sont explicites**. Chaque action possède un droit
identifiable. On peut imaginer les permissions `thread:read` ou `tool:execute`.

Par exemple:

| Rôle      | Exemple de permissions                                       | Accès                                                     |
| --------- | ------------------------------------------------------------ | --------------------------------------------------------- |
| **User**  | `threads:read`, `threads:create`, `assistants:use`           | Consulte ses threads et utilise ses assistants            |
| **Admin** | `threads:delete`, `assistants:manage`, `tools:execute:admin` | Administre les ressources et utilise les outils sensibles |

Voici une liste des principales composantes à sécuriser au sein d'un agent IA:

| Composante            | Description                                                       | Permission exemple  |
| --------------------- | ----------------------------------------------------------------- | ------------------- |
| **Memory**            | Informations et préférences mémorisées pour personnaliser l'agent | `memory:read`       |
| **Threads**           | Historique des conversations de l'utilisateur                     | `threads:read`      |
| **Assistants**        | Assistants personnels créés ou configurés par l'utilisateur       | `assistants:update` |
| **Fichiers**          | Documents et données personnels utilisés par l'agent              | `files:read`        |
| **Configuration**     | Instructions et paramètres personnels de l'agent                  | `config:update`     |
| **Exécutions (Runs)** | Historique et résultats des actions lancées par l'utilisateur     | `runs:read`         |

## Problème 3 : Comment délimiter le périmètre d'action d'un utilisateur ?

Même si une action est autorisée, son périmètre doit être contrôlé.

Par exemple, une permission de lecture peut autoriser Alice à consulter des conversations. Elle ne doit pas pour autant lui permettre de lire toutes les conversations de la plateforme.

Le fait de connaître un identifiant de ressource ne doit jamais suffire à obtenir son contenu.

### Solution : contrôler les droits sur la ressource elle-même

Les contrôles d'accès doivent prendre en compte le contexte de la
ressource :

* Son propriétaire ou son utilisateur associé.
* Son organisation ou son espace de travail.
* Son niveau de confidentialité.
* Son état ou son périmètre de partage.

Ce contrôle repose sur **ABAC** *(Attribute-Based Access Control)* qui déploie un modèle de contrôle d’accès qui autorise ou refuse une action en fonction des attributs de l’utilisateur, de la ressource et du contexte.

Par exemple, un thread ne peut être accessible que par un utilisateur spécifique. Son accès doit donc respecter le critère suivant: `user.id == thread.owner_id`

Cette approche permet de distinguer deux décisions :

1.  **L'action est-elle autorisée ?** Par exemple, l'utilisateur peut-il lire une conversation ?
2.  **Cette ressource précise est-elle accessible ?** Par exemple, cette conversation appartient-elle à l'utilisateur ou à son organisation ?

Ainsi, **la permission autorise une opération ; le contrôle d'accès
détermine sur quelles données elle peut s'appliquer**.

```text
Utilisateur
    │
    ▼
Authentification
    │
    ▼
Autorisation
    │
    ├── RBAC : Quelles actions ?
    │   (rôle → permissions)
    │
    └── ABAC : Sur quelle ressource ?
        (attributs → conditions)
    │
    ▼
Décision
    │
    ▼
Accès autorisé ou refusé
```

## Problème 4: L'agent peut-il utiliser des outils sans restriction ?

Un agent peut être connecté à des outils permettant de rechercher des documents, d'interroger une base de données, d'envoyer un message ou encore, de modifier un système externe.

Ces outils étendent considérablement ses capacités. Ils étendent
également la surface de risque.

Il ne suffit pas de demander au modèle de ne pas utiliser un outil
sensible. Le modèle peut mal interpréter une instruction, être influencé par un contenu externe ou recevoir une demande qui tente de contourner ses consignes.

Il est nécessaire qu'un contrôle déterministe indépendant du modèle d'IA soit appliqué pour garantir les droits d'utilisation des outils à disposition.

### Solution : contrôler les outils au niveau applicatif

Le contrôle d'accès aux outils repose sur **une approche à trois niveaux**.

* **Lors de la création de l'agent**: les *tools* disponibles sont sélectionnés dynamiquement en fonction des permissions de l'utilisateur authentifié. Les permissions sont réévaluées au moment de chaque exécution de requête.
* **Lors de l'utilisation d'un *tool***: chaque outil sensible applique une vérification des droits au moment de son exécution, en s'appuyant sur l'identité et les permissions transmises par le runtime du *harness*.
* **Lors des actions critiques et/ou sensibles**: une validation humaine peut être imposée par la politique de sécurité.

Cette approche de défense en profondeur permet de renforcer la sécurité de l'agent en limitant à la fois **l'exposition des outils et leur utilisation effective aux seuls utilisateurs autorisés**.

Le contrôle doit rester effectif au moment de l'exécution. Masquer un
outil dans l'interface ou dans la configuration de l'agent ne suffit pas
si cet outil peut être appelé par un autre chemin.

> [!IMPORTANT]
>  **Un tool est une capacité applicative** : il doit être protégé comme une API ou une opération métier.

## Problème 5 : Comment limiter les permissions d'un agent IA au strict nécessaire ?

Un agent IA peut disposer de plusieurs tools lui permettant d'interagir avec son environnement. Certains peuvent simplement consulter des informations, tandis que d'autres peuvent modifier des ressources ou déclencher des opérations sensibles.

Cependant, **le fait qu'un agent puisse utiliser un outil ne signifie pas qu'il doive systématiquement y avoir accès**.

Par exemple, un agent chargé de répondre à des questions sur des documents peut avoir besoin de consulter un espace documentaire. Il n'a pas nécessairement besoin de supprimer des fichiers, de modifier les permissions d'un utilisateur ou d'accéder à l'ensemble des documents de la plateforme.

Si un agent dispose de permissions trop importantes, une erreur de raisonnement, une instruction malveillante ou un détournement de tool peut entraîner des conséquences disproportionnées.

Le problème ne réside donc pas uniquement dans la possibilité d'exécuter une action, **mais également dans l'étendue des permissions accordées à l'agent**.

### Solution : appliquer le principe du moindre privilège (Principle of Least Privilege)

Le **principe du moindre privilège** consiste à accorder uniquement les permissions nécessaires à l'exécution d'une tâche, sur les ressources concernées et pendant la durée nécessaire.

Dans une architecture d'agents IA, ce principe peut être appliqué à plusieurs niveaux :

* **Lors de la configuration de l'agent** : ne lui fournir que les tools nécessaires à son fonctionnement.
* **Lors de l'exécution d'une requête** : limiter les permissions aux ressources et aux opérations nécessaires à la tâche demandée.
* **Lors de l'utilisation d'un tool** : vérifier que l'action demandée correspond aux permissions effectivement accordées.
* **Lors de l'accès aux services externes** : utiliser des credentials disposant uniquement des droits requis.

**L'absence d'une permission doit empêcher l'exécution de l'action correspondante, même si le modèle décide de l'appeler**.

Le principe du moindre privilège permet ainsi **de réduire la surface d'attaque de l'agent** et de **limiter les conséquences d'une utilisation abusive de ses capacités**.

> [!IMPORTANT]
> Un agent IA ne doit jamais disposer de permissions plus importantes que celles nécessaires à sa mission. La disponibilité d'un tool ne constitue pas une justification suffisante pour lui accorder un accès. Un agent IA disposant de capacités au-delà du nécessaire est sensible aux attaques de type **Excessive agency**.

## Problème 6 : Comment gérer le contexte d'authentification et la configuration de la requête ?

Dans une application utilisant un mécanisme d'authentification et de contrôle d'accès, plusieurs types d'informations sont nécessaires au fonctionnement de l'application.

Certaines données concernent l'identité de l'utilisateur et les permissions qui lui sont accordées. D'autres correspondent aux paramètres fonctionnels transmis lors d'une requête, comme les options d'exécution ou les éléments de contexte nécessaires au traitement.

Ces informations n'ont cependant pas le même niveau de confiance ni le même rôle. Il est donc important de ne pas les confondre, notamment lorsque les décisions d'autorisation dépendent de l'identité de l'utilisateur.

### Solution: séparer le contexte d'authentification et la configuration de la requête

Une séparation est mise en place entre le contexte d'authentification et la configuration de la requête.

Le **contexte d'authentification** contient les informations relatives à l'utilisateur authentifié, notamment son identité, ses rôles et ses permissions. Ces informations sont établies par le mécanisme d'authentification et transmises à l'application par l'environnement d'exécution. Elles servent de référence pour appliquer les règles de contrôle d'accès.

La **configuration de la requête** contient les paramètres nécessaires à l'exécution de l'agent IA. Elle peut notamment inclure des éléments de contexte, des instructions personnalisées ou des options permettant d'adapter le comportement de l'agent à une requête donnée. Cependant, ces informations constituent pas une source de confiance pour déterminer l'identité de l'utilisateur ou ses permissions.

Cette séparation permet de distinguer clairement les données fonctionnelles des informations liées à la sécurité. **Le contexte d'authentification ne doit pas être seulement séparé logiquement de la configuration ; il doit également être protégé contre toute modification par l'utilisateur ou le modèle.**.

> [!IMPORTANT]
> Les informations d'identité et de permissions sont établies par le serveur à partir du mécanisme d'authentification. Elles ne peuvent pas être définies ou modifiées par le payload utilisateur, les instructions du modèle ou les résultats d'un tool.

> [!TIP]
> Les confusions entre contexte d'authentification et configuration de requête sont très exploitées pour contourner les systèmes d'authentification. Un exemple d'attaque sera présenté dans un autre module.

## Problème 7: Comment empêcher l'exécution d'actions non explicitement définies ?

Dans un système d'authentification et d'autorisation, il est important de définir clairement les actions qu'un utilisateur peut effectuer. Cependant, **si certaines actions ne sont pas couvertes par une règle d'autorisation, leur comportement peut devenir ambigu**.

Une politique permissive pourrait conduire à autoriser implicitement des opérations qui n'ont pas été prévues ou validées. Cela représente un risque, notamment lorsqu'un agent IA dispose d'outils capables d'interagir avec des ressources ou d'effectuer des opérations sensibles.

### Solution: mise en place d'une politique de refus par défaut (Default Deny)

Pour éviter ce comportement, une politique de refus par défaut est mise en place au niveau du mécanisme d'autorisation.

Le principe consiste à **refuser toute action qui n'est pas explicitement autorisée par une règle définie**. Ainsi, par défaut, toute action est interdite. Une autorisation doit être explicitement accordée pour permettre son exécution.

Cette politique peut s'exécuter à différents niveaux:

* **Interaction avec les ressources du système (threads, assistants, store...)**: Supposons que l'action de suppression d'un thread n'a pas été configurée, il est alors refusé de supprimer tout thread.
* **Au niveau du payload de la requête** : contrôler les paramètres transmis lors de l'exécution. Cela inclut notamment les données de configuration du modèle, les paramètres d'exécution et les éléments de contexte fournis à l'agent. Les paramètres non autorisés ou non conformes aux règles définies doivent être rejetés ou ignorés selon le comportement prévu. Par exemple, supposons que le système accepte uniquement un payload avec un attribut `user_context`, si l'utilisateur ajoute un attribut `"role": admin`, le système refusera de traiter la demande.

## Problème 8 : Avec quelle identité un agent IA exécute-t-il ses actions ?

Dans une plateforme d'agents IA, l'utilisateur authentifié peut demander à un agent d'effectuer une action à l'aide d'un tool. Cependant, **l'identité de l'utilisateur et celle de l'agent ne sont pas nécessairement les mêmes**.

Un agent peut notamment utiliser un compte technique disposant de permissions plus importantes que celles de l'utilisateur à l'origine de la requête.

Cela soulève une question importante :

**Comment garantir qu'un agent ne puisse pas utiliser ses propres permissions pour contourner les restrictions de l'utilisateur ?**

### Solution : distinguer l'identité de l'utilisateur et celle de l'agent

L'**identité de l'utilisateur** permet de déterminer qui est à l'origine de la requête et quelles permissions lui sont accordées. 

L'**identité de l'agent** permet d'identifier le système qui exécute l'action et les capacités dont il dispose.

**Ces deux identités doivent être prises en compte** pour garantir que l'agent agit dans un périmètre autorisé. De même, une attention particulière doit être portée sur la **propagation du contexte de sécurité**.

Lorsqu'un agent IA délègue une action à un *tool* ou à un service externe, le contexte de sécurité doit être transmis de manière fiable. Il doit permettre au composant appelé de connaître l'identité de l'utilisateur à l'origine de la requête, ainsi que les permissions et le périmètre d'accès applicables. Ce contexte doit être établi et contrôlé par l'application, et non reconstruit à partir des instructions du modèle ou du *payload* utilisateur.

**La propagation du contexte de sécurité garantit que les contrôles d'accès restent cohérents tout au long de l'exécution de l'agent, y compris lorsqu'il délègue des actions.**

> [!IMPORTANT]
> L'identité de l'agent ne remplace pas l'identité de l'utilisateur. Les permissions techniques de l'agent ne doivent jamais permettre de contourner les règles d'autorisation applicables à la requête initiale.

## En résumé

```text
Requête HTTP
    │
    ▼
Authentification JWT
    │
    ▼
Identité + permissions
    │
    ▼
Contrôle d'accès LangGraph
    │
    ├── Permission d'action
    ├── Propriété de la ressource
    └── Validation du contexte
    │
    ▼
Construction de l'agent
    │
    ├── Tools autorisés
    └── Contexte d'exécution
    │
    ▼
Exécution du tool
    │
    └── Vérification de sécurité
```

## Mise en pratique

L'exemple d'application va reposer sur le déploiement d'un **système d'authentification sur un système d'IA basé sur Deepagents-Langchain**. 

> [!WARNING]
> Beaucoup de spécificités techniques sont propres à Deepagents. Bien que les concepts théoriques soient communs à tout agent IA, l'implémentation est propre au framework.

### Scénario

Nous disposons d'un agent IA possédant 2 tools: `public_tool` accessible aux utilisateurs authentifiés et `admin_tool`, réservé aux admin.

Le système d'IA permet aux utilisateurs de créer un agent avec un `system_prompt` customisé et de créer des *threads*. Dans cet exemple, les agents **n'auront pas de mémoire**.

L'authentification reposera sur un *token* `bearer` (JWS à clé symétrique). Trois utilisateurs sont définis: `alice_user`, `claude_user`et `bob_admin`.

L'admin peut consulter l'ensemble des *threads* et assistants. Les utilisateurs ne peuvent consulter que les ressources qu'ils ont créees. De plus, un utilisateur ne peut pas supprimer une ressource qui lui appartient (contrairement aux admin).

L'objectif de ce *lab* est de tester les différents paramètres de sécurité apportés par l'authentification notamment la confidentialité des *threads*, des agents IA, la protection des tools et des paramètres des modèles.

### Installation des dépendances

```bash
cd de-ag-sai-002
uv sync
cd /src
```

Dans `.env`

```text
JWT_SECRET_KEY=<GENERATE_KEY via openssl rand -hex 32>
ISSUER="my_test_auth_service"
AUDIENCE="my_test_assistant"
JWT_ALGORITHM = "HS256"

GOOGLE_API_KEY=<API KEY>
```

Adapter `GOOGLE_API_KEY` en fonction du provider que vous utilisez.

#### Liste des scripts

| Fichier            | Responsabilité                                                          |
| ------------------ | ----------------------------------------------------------------------- |
| `auth.py`          | Authentification, permissions et contrôles d'accès aux ressources       |
| `my_agent.py`      | Construction de l'agent, sélection des tools et validation du contexte  |
| `jws_generated.py` | Génération des tokens de démonstration                                  |
| `clients.py`       | Exécution des scénarios de test                                         |
| `langgraph.json`   | Configuration du serveur et déclaration du mécanisme d'authentification |

### Exécution

1. 	Exécuter `jws_generated.py`

    Ce script va créer 3 utilisateurs: alice (user), bob (admin) et claude (user). Les tokens sont dans le fichier `tokens.json`. **ATTENTION**: ce système de génération de *token* n'est pas fiable. Il est utilisé uniquement à but pédagogique et ne peut pas être employé pour véritablement sécuriser un système.

2. Lancer le serveur (dev mode) de langgraph avec `LOG_LEVEL=CRITICAL uv run langgraph dev --no-browser`

    La configuration du serveur est définie dans `langgraph.json`

3. Exécuter les requêtes du client via `uv run clients.py`

### Analyses

#### Dans `auth.py`

Le script `auth.py` réalise l'authentification d'un utilisateur et définit la politique de sécurité via l'implémentation du système de permission.

La fonction `authenticate` est en charge de lire, vérifier et retranscrire les informations obtenues du *token*. Elle est en charge de confirmer l'authenticité et l'identité d'un utilisateur.

L'identité est définie par 3 paramètres: `identity`(identité), `permissions`(liste des droits utilisateurs) et `is authenticated`(confirmation de la procédure d'authentification). Ces paramètres font partie des paramètres "par défaut" du système d'authentification de `langgraph`.

Les fonctions avec les décorateurs `@auth.on.[...]` définissent la politique de sécurité des différentes actions réalisables par le serveur. Par exemple, la fonction décorée par `auth.on.threads.create` est appelée lors de la création d'un *thread*.

Les fonctions permettent de vérifier la permission d'action de l'utilisateur, d'attribuer la ressource à l'utilisateur (*owner*) s'il y a création d'une ressource et, en cas de lecture uniquement, de vérifier si l'utilisateur est le propriétaire de la ressource.

Ces fonctions constituent **le contrôle RBAC/ABAC de l'authentification du système d'IA**.

> [!NOTE]
> Nous illustrons ici les principes d'ABAC à travers des contrôles d'accès fondés sur les attributs de l'utilisateur et de la ressource. Le lab n'implémente pas un moteur ABAC générique ; les règles sont directement intégrées aux fonctions de contrôle d'accès.

La fonction `deny_all` retourne un refus d'accès (erreur 403) en cas d'action non implémentée. C'est l'application de **la politique de refus par défaut**.

#### Dans `my_agent.py`

Ce script définit l'architecture de l'agent IA via la définition de ses *tools*, du modèle et de son contexte. Il reçoit les informations retournées par le système d'authentification de langgraph, les informations récupérées de la requête utilisateur et les utilise pour réaliser la requête.

la fonction `make_graph` possède 2 arguments: `config` et `runtime`.

* `config` est un dictionnaire ouvert contrôlé par le client (le navigateur, Postman ou ton script SDK). Les données sont soumises par l'utilisateur sans contrôle. Elles ne sont donc pas "fiables". Cet attribut possède des informations de fonctionnement non critiques (thread_id, contexte utilisateur, temperature du modèle par exemple).
  
* `runtime` est un objet Python interne construit exclusivement par le serveur LangGraph, inaccessible depuis le payload JSON du client. Il est alimenté uniquement par ton code d'authentification. Les données sont donc fiables (lorsque le système  d'authentification est correctement paramétré). Cet attribut possède toutes les informations critiques d'identification et de permission.

Les données d'authentification sont ainsi définies par:

```python
user = runtime.ensure_user()
user_id = user.identity
permissions = user.permissions
```

La bonne compréhension de ces deux paramètres est nécessaire pour bien différencier le contexte d'authentification et la configuration de la requête utilisateur.

> [!TIP]
> **🔐 Security relevance**: Risque d'usurpation (Mass Assignment / Privilege Escalation) : Si ton code fait confiance à `config` et que le serveur d'authentification / serveur langgraph est mal configuré, un attaquant peut forger une requête HTTP avec un faux dictionnaire dans config pour s'attribuer les droits admin. Cette attaque sera vu dans un module dédié.

La classe `AssistantConfig` définit la structure du context reçu par l'agent. Si un attribut non défini est envoyé dans la requête, le serveur refusera d'exécuter la requête. Dans cet exemple, on peut voir que l'utilisateur peut uniquement modifier `system_prompt`et `user_contexte`(en fonction des permissions de l'utilisateur). Cette approche permet de garantir l'absence d'attribut imprévu pouvant créer des interactions néfastes.

Le code suivant:

```python
tools = [public_tool]
if "role:admin" in permissions:
    tools.append(admin_tool)
```

Permet de définir la liste de *tools* disponible pour l'agent. On observe bien que `admin_tool` est disponible uniquement si l'utilisateur possède le role `admin`.

Le code suivant (dans `admin_tool`):

```python
if "role:admin" not in server.user.permissions:
    raise PermissionError(f"Accès refusé pour {server.user.identity}")
```

Permet de confirmer le droit d'utilisation du *tool* par l'utilisateur (défense en profondeur)

### Résultat des requêtes et tests de sécurité

**ATTENTION**: Ces tests ne confirment pas qu'il n'y a pas de problèmes de sécurité. Ils confirment uniquement que les comportements testés respectent la politique de sécurité souhaitée.

```text
Assistant created for alice_user -> ID : a2a06df7-94a5-48ec-bb56-cac02c3c817c
Assistant created for bob_admin -> ID : 01bde2b0-ffca-4305-957c-3f9bbe31883d
Assistant created for claude_user -> ID : bb9b4e95-30ca-4f65-9ce2-65fe048646d5
```

Chaque utilisateur a créé un agent en son nom. C'est cohérent car les utilisateurs peuvent créer un assistant

```text
====================================================================================================
  User Alice -> Assistant Alice, new thread | Assistant: a2a06df7-94a5-48ec-bb56-cac02c3c817c | Thread: None
====================================================================================================
Thread created : 01a22043-383a-760b-b27c-88fe11129478
SUCCESS ! Response : This agent was created by alice_user.

====================================================================================================
  User Alice -> Assistant Alice, Alice thread | Assistant: a2a06df7-94a5-48ec-bb56-cac02c3c817c | Thread: 01a22043-383a-760b-b27c-88fe11129478
====================================================================================================
Thread loaded : 01a22043-383a-760b-b27c-88fe11129478
SUCCESS ! Response : This agent was created by alice_user.
```

Alice peut exécuter son assistant sans *thread* et avec un *thread* qu'elle a crée. C'est cohérent avec la politique de sécurité car un utilisateur peut utiliser un agent lui appartenant, créer un thread et lire/exécuter un thread lui appartenant.

```text
====================================================================================================
  User Claude -> Assistant Alice, Claude thread | Assistant: a2a06df7-94a5-48ec-bb56-cac02c3c817c | Thread: 01a22043-6883-7189-9454-6c7c2a2a33e1
====================================================================================================
Thread loaded : 01a22043-6883-7189-9454-6c7c2a2a33e1
Forbidden access (HTTP 404) : {"detail":"assistant a2a06df7-94a5-48ec-bb56-cac02c3c817c not found"}

====================================================================================================
  User Claude -> Assistant Alice, Alice thread | Assistant: a2a06df7-94a5-48ec-bb56-cac02c3c817c | Thread: 01a22043-383a-760b-b27c-88fe11129478
====================================================================================================
Forbidden access (HTTP 404) : {"detail":"thread 01a22043-383a-760b-b27c-88fe11129478 not found"}

====================================================================================================
  User Claude -> Assistant Alice, new thread | Assistant: a2a06df7-94a5-48ec-bb56-cac02c3c817c | Thread: None
====================================================================================================
No thread used
Forbidden access (HTTP 404) : {"detail":"assistant a2a06df7-94a5-48ec-bb56-cac02c3c817c not found"}
```

Dans ces 3 tests, l'utilisateur claude essaye d'utiliser l'assistant de Alice avec l'un de ses threads, l'un des threads d'alice et sans thread préalable. Chaque requête a été bloquée, montrant bien la séparation des ressources utilisateurs.

```text
====================================================================================================
  User admin -> Assistant Alice, Alice thread | Assistant: a2a06df7-94a5-48ec-bb56-cac02c3c817c | Thread: 01a22043-383a-760b-b27c-88fe11129478
====================================================================================================
Thread loaded : 01a22043-383a-760b-b27c-88fe11129478
SUCCESS ! Response : This agent was created by alice_user.

====================================================================================================
  User admin -> Assistant Alice, new thread | Assistant: a2a06df7-94a5-48ec-bb56-cac02c3c817c | Thread: None
====================================================================================================
No thread used
SUCCESS ! Response : This agent was created by alice_user.
```

Dans ces 2 tests, nous observons que l'utilisateur `admin` a pu utiliser l'assistant d'Alice avec un thread d'Alice ou sans thread préalable. L'utilisateur `admin` ayant tous les droits sur l'ensemble des ressources utilisateur, ces résultats sont cohérents avec la politique de sécurité.

```text
====================================================================================================
  Add custom attribute in context | Assistant: a2a06df7-94a5-48ec-bb56-cac02c3c817c | Thread: None
====================================================================================================
Thread created : 01a22043-9b08-71ce-9d6a-80d20a213864
Error (Exception) : ValueError: Configuration invalide : 1 validation error for AssistantConfig
test
  Extra inputs are not permitted [type=extra_forbidden, input_value=True, input_type=bool]
    For further information visit https://errors.pydantic.dev/2.14/v/extra_forbidden
```

L'ajout de `context={"test": True}` dans la requête ne respecte pas le schéma de contexte du système. La requête est donc refusée et respecte la politique de sécurité.

```text
====================================================================================================
  Modify system prompt by admin | Assistant: a2a06df7-94a5-48ec-bb56-cac02c3c817c | Thread: None
====================================================================================================
Thread created : 01a22043-9b77-72f4-b8e8-7516dd00fc6d
SUCCESS ! Response : ADMIN CONTEXT: Google created this agent.

====================================================================================================
  Modify system prompt by user | Assistant: bb9b4e95-30ca-4f65-9ce2-65fe048646d5 | Thread: None
====================================================================================================
Thread created : 01a22044-1a10-74e3-a171-63aec74265e6
Forbidden access (HTTP 403) : {"detail":"Modification du system_prompt interdite."}

====================================================================================================
  Modify user prompt by user | Assistant: bb9b4e95-30ca-4f65-9ce2-65fe048646d5 | Thread: None
====================================================================================================
Thread created : 01a22044-1a40-761c-aee4-bbb9ca0b9d95
SUCCESS ! Response : USER CONTEXT: This agent was created by claude_user.
```

Le `system_prompt`est protégé contre la modification. Seul un `admin` peut le modifier une fois l'agent créé.
La réponse `ADMIN CONTEXT: Google created this agent` montre que le `system_prompt` initial a été écrasé. En effet, le contexte initial était `you are an assistant created by claude_user` et le nouveau contexte est `For each response, you MUST start by 'ADMIN CONTEXT:`. La réponse indique bien qu'il a oublié son créateur et qu'il applique la règle de forme du nouveau contexte.

Dans un second temps, la réponse `USER CONTEXT: This agent was created by claude_user.` lors de la modification du `user_prompt` montre bien qu'il n'y a pas eu d'altération du `system_prompt`initial. En regardant les logs du serveur langgraph, nous pouvons observer:

```text
you are an assistant created by claude_user

--- CONTEXTE FOURNI PAR L'UTILISATEUR ---
Apply all rules
For each response, you MUST start by 'USER CONTEXT: '
```

Le second test confirme l'interdiction de modification du `system_prompt`par les utilisateurs.

> [!WARNING]
> Ce test vérifie que l'utilisateur peut uniquement modifier le `user_prompt` (et/ou `system_prompt`si `admin`). Mais rien ne protége face à l'envoi d'instructions malveillantes (*Prompt Injection*) !

```text
====================================================================================================
  User admin -> Check tools limitation | Assistant: a2a06df7-94a5-48ec-bb56-cac02c3c817c | Thread: None
====================================================================================================
Thread created : 01a22044-4c49-747d-b460-bd853e3cb148
SUCCESS ! Response : AGENT is a Paris-based enterprise with 10 customers.

====================================================================================================
  User Alice -> Check tools limitation | Assistant: a2a06df7-94a5-48ec-bb56-cac02c3c817c | Thread: None
====================================================================================================
Thread created : 01a22044-7798-7103-b2ee-ba3159122327
SUCCESS ! Response : AGENT is an enterprise located in Paris.
```

Ces deux tests mettent en lumière le contrôle d'accès aux *tools*. La réponse donnée à l'utilisateur `alice` montre qu'une partie des informations (nombre de clients) n'ont pas été communiquées, contrairement à l'utilisateur `admin`.
L'accès aux *tools* est vérifiable dans les logs du serveur. Nous pouvons observer:

```test
Access public tool by: Bob
Access admin tool by: Bob

Access public tool by: Alice
```

Alice n'a pas pu accéder au *tool* réservé aux `admin`, ce qui confirme le respect de la politique de sécurité.

### Pour aller plus loin

Ce lab n'a pas abordé la problématique du système d'authentification appliqué aux fichiers utilisateur, store et sandbox. Les concepts théoriques restent les mêmes mais leurs applications soulèvent d'autres problématiques d'architectures qui méritent d'être traitées dans un module dédié.

De même, pour des raisons de simplification, le lab n'explore pas la propagation du contexte de sécurité (via des subagents par exemple).
