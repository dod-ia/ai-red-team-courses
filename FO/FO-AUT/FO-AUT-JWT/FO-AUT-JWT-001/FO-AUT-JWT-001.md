# Authentification - JWT

## Authentification : JWT vs Sessions

L'**authentification** est le mécanisme qui permet de **vérifier l'identité d'un utilisateur** avant de lui autoriser l'accès à une application ou à des ressources protégées. Dans une application web, le principal enjeu est de maintenir cette identité entre les requêtes HTTP, qui sont indépendantes par nature.

Deux questions sont ainsi soulevées:

* **Comment permettre à un serveur de reconnaître un utilisateur et de vérifier ses autorisations sur plusieurs requêtes HTTP, sans devoir lui redemander ses identifiants à chaque fois ?**
  
* **Comment une API peut-elle déterminer si une information d'authentification reçue est digne de confiance ?**

L'authentification traditionnelle par session repose sur un **état conservé côté serveur**. C'est donc une approche **stateful**. Après la connexion, un identifiant de session est transmis au client et associé aux données de session stockées sur le serveur. Dans une architecture distribuée, cela peut nécessiter un stockage partagé ou une synchronisation entre plusieurs instances backend.

**JWT (JSON Web Token)** propose une approche **stateless** : le serveur génère un *token* signé contenant les informations nécessaires à l'authentification. Le client le transmet à chaque requête, et le serveur peut vérifier sa signature et sa validité sans consulter de stockage de session centralisé.

Cette approche **simplifie la mise à l'échelle horizontale**, facilite la communication entre services et convient particulièrement aux API. En contrepartie, la révocation immédiate d'un token est plus complexe, et sa durée de validité doit être soigneusement gérée.

Le choix de JWT vise donc à réduire la dépendance à un état de session côté serveur, tout en conservant un mécanisme d'authentification vérifiable et adapté à une architecture distribuée.

> [!NOTE]
> Il est possible de concevoir une architecture par session qui soit *Stateless*. De même, JWT permet de vérifier un token sans consulter obligatoirement un état de session centralisé, mais l'architecture complète peut rester *Stateful*.

## Qu'est-ce qu'un JWT ?

Un **JSON Web Token (JWT)** [1] est un format standard permettant de représenter des informations sous forme d'objet JSON, notamment pour **l'authentification et l'autorisation** entre un client et un serveur. Il est couramment utilisé dans les applications web, les API REST et les systèmes d'authentification modernes.

```text
╔══════════════════════════════════════════════╗
║       JWT — JSON WEB TOKEN (non signé)       ║
╚══════════════════════════════════════════════╝

  ┌──────────────┐   ┌──────────────┐
  │    HEADER    │ . │   PAYLOAD    │ . <empty>
  ├──────────────┤   ├──────────────┤
  │ alg: none    │   │ sub: user123 │
  │ typ: JWT     │   │ role: user   │
  │ [...]        │   │ [...]        │
  └──────────────┘   └──────────────┘
          │                  │
          └────────┬─────────┘
                   ▼
  BASE64URL(HEADER).BASE64URL(PAYLOAD).
                   │
                   ▼
eyJhbGciOiJub25lIiwidHlwZSI6IkpXVCJ9.eyJzdWIiOiJ1c2VyMTIzIiwicm9sZSI6InVzZXIifQ.
```

Il comporte **trois parties séparées par des points (.)** mais la troisième partie est vide. Le *header* et le *payload* sont au format JSON puis encodés en Base64URL.

| Partie        | Fonction                                                     |
| ------------- | ------------------------------------------------------------ |
| **Header**    | Définit le type de token, les métadonnées       |
| **Payload**   | Contient les *claims* (identité, rôles, expiration, etc.)     |
| **\<empty>** | Contenu vide |

> [!NOTE]
> Ce type de *token* est appelé **JWT non signé**. Bien que autorisé par le standard, il ne doivent pas être acceptés dans un contexte où l'application exige un token authentifié.

Ce *token* possède la capacité d'**identifier** de par ses informations. Cependant, comment peut-on garantir l'authenticité des informations ? En effet, on pourrait facilement **altérer** le *token* en modifiant `role: user` en `role: admin`, conférant des droits inappropriés à un profil donné.

Il est donc nécessaire de **pouvoir garantir la validité des informations et leurs non-altérations**. Mais comment faire cela ?

Une solution consiste à signer le contenu à l'aide d'une clé détenue par une entité de confiance. Ce concept a donné naissance au **JWS (JSON Web Signature)**.

## Description de JWS

Un **JWT signé** est généralement représenté sous la forme d'un **JWS compact**. Dans cette configuration, il se présente sous la forme de trois parties séparées par des points.

```text
╔══════════════════════════════════════════════╗
║          JWT — JSON WEB TOKEN  (signé)       ║
╚══════════════════════════════════════════════╝

  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
  │    HEADER    │.│   PAYLOAD    │.│  SIGNATURE   │
  ├──────────────┤ ├──────────────┤ ├──────────────┤
  │ alg: RS256   │ │ sub: user123 │ │ Signature    │
  │ typ: JWT     │ │ role: user   │ │ numérique    │
  └──────────────┘ └──────────────┘ └──────────────┘
          │               │               │
          └───────────────┼───────────────┘
                          ▼
 BASE64URL(HEADER).BASE64URL(PAYLOAD).BASE64URL(SIGNATURE)
                          │
                          ▼
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyMTIzIiwicm9sZSI6InVzZXIifQ.<signature>
```

| Partie        | Fonction                                                     |
| ------------- | ------------------------------------------------------------ |
| **Header**    | Définit l'algorithme cryptographique et le type de token.       |
| **Payload**   | Contient les claims (identité, rôles, expiration, etc.).     |
| **Signature** | Permet de vérifier l'intégrité du token et son authenticité. |

Un JWS est encodé en **Base64URL**. Il est important de ne pas oublier que **l'encodage n'est pas du chiffrement** : les informations du payload peuvent être lues par toute personne possédant le *token*.

### Signature d'un JWT

Il existe deux approches pour signer un JWT: l'approche **symétrique** et **asymétrique**.

#### Signature symétrique

La signature **symétrique** repose sur un **secret partagé entre l'émetteur et le destinataire**. L'émetteur utilise ce secret pour signer le JWS, puis le destinataire utilise le même secret pour vérifier la signature.

Cette approche est simple et rapide à mettre en place, mais elle implique que toutes les parties qui vérifient les signatures possèdent également le secret permettant d'en créer de nouvelles. Il est donc essentiel de **protéger ce secret et de contrôler sa distribution**.

#### Signature asymétrique

La signature **asymétrique** repose sur une paire de clés composée d'une **clé privée et d'une clé publique**. L'émetteur utilise sa clé privée pour signer le JWS, tandis que le destinataire utilise la clé publique correspondante pour vérifier la signature.

Contrairement à l'approche symétrique, la clé privée n'a pas besoin d'être partagée avec les services qui vérifient les signatures. La **clé publique peut être distribuée à plusieurs services** sans leur donner la possibilité de créer des signatures valides. Cette approche est particulièrement adaptée aux architectures dans lesquelles un service central émet les tokens et plusieurs API doivent les vérifier.

#### Protocole de signature d'un JWT

```text
     HEADER          PAYLOAD
        |                |
        v                v
   Encodage          Encodage
   Base64URL         Base64URL
        |                |
        +-------+--------+
                |
                v
BASE64URL(header).BASE64URL(payload)
                |
                v
    Signature cryptographique (ou MAC)
avec la clé privée ou le secret partagé
                |
                v
        Encodage Base64URL
                |
                v
       BASE64URL(SIGNATURE)
                |
                v
     HEADER.PAYLOAD.SIGNATURE
              (JWS)
```

Cette approche permet de signer, mais une question se pose: **Quel algorithme cryptographique utiliser ?**

#### Standards pour la signature

L'écosystème autour de *JWT* constitue un ensemble de standards définis par des RFC. Cet écosystème constitue **JOSE (JavaScript Object Signing and Encryption)**. Parmi ces standards, nous pouvons citer **JWA (JSON Web Algorithms)** [4].

Ce standard **définit les algorithmes cryptographiques utilisés** par les autres standards JWT, notamment les algorithmes symétriques et asymétriques. La liste complète est disponible [ici](https://www.rfc-editor.org/info/rfc7518/#section-3.1). Actuellement, pour respecter la RFC, trois algorithmes sont à prioriser :

| Algorithme | Description                       | Type de clé            | RFC 7518     |
|------------|-----------------------------------|------------------------|--------------|
| HS256      | HMAC using SHA-256                | Secret partagé         | Required     |
| RS256      | RSASSA-PKCS1-v1_5 using SHA-256   | Clé privée/publique RSA| Recommended  |
| ES256      | ECDSA using P-256 and SHA-256     | Clé privée/publique EC | Recommended+ |

Ainsi, les implémentations respectant la RFC doivent **au moins** supporter HS256 et si possible, RS256 et ES256. Ces algorithmes sont donc à favoriser lors de la définition de la méthode de signature.

> [!TIP]
> **🔐 Security relevance**: Les algorithmes cryptographiques utilisés sont généralement robustes et présentent peu de chances de révéler une vulnérabilité directe. En revanche, **leur mise en œuvre et leur validation côté serveur peuvent comporter des failles exploitables**. L’analyse se concentre donc davantage sur les erreurs de configuration, les défauts de validation et les mécanismes de vérification du *token* que sur le chiffrement lui-même.

Grâce à *JWS*, nous pouvons garantir l'intégrité et l'authenticité du contenu d'un *JWT*. Néanmoins, une nouvelle problématique apparaît lors de l'utilisation d'un algorithme de signature numérique. **Comment garantir que la clé privée utilisée est vraiment de confiance ?**

## Description de JWK

 les standards de *JOSE*, nous pouvons citer **JWK (JSON Web Key)** [5]. Ce standard définit un format JSON pour représenter des clés cryptographiques.

Le *JWK* définit un **format de représentation JSON standardisée des clés cryptographiques**. Une JWK peut représenter une clé symétrique, une clé publique ou une clé privée. Il est notamment utilisé pour **publier, transmettre et identifier les clés utilisées** pour signer ou vérifier des tokens.

Exemple de JWK publique RSA (variable selon l'algorithme cryptographique):

```json
{
  "kty": "RSA",
  "kid": "key-2026",
  "use": "sig",
  "alg": "RS256",
  "n": "<modulus>",
  "e": "AQAB"
}
```

| Champ (liste non exhaustive) | Description                                         |
| ----- | --------------------------------------------------- |
| `kty` | Type de clé cryptographique, ici RSA.               |
| `kid` | Identifiant permettant de sélectionner une clé.     |
| `use` | Usage prévu de la clé, ici la signature.            |
| `alg` | Algorithme associé à la clé, lorsqu'il est indiqué. |
| `n`   | Module RSA encodé en Base64URL.                     |
| `e`   | Exposant public RSA encodé en Base64URL.            |

*JWK* ne stocke pas la clé publique dans un format standard comme `.pem` par exemple. Elle stocke le *modulus* et l'*exposant* qui, dans cet exemple, constituent les paramètres mathématiques de la clé publique RSA. L'application doit donc reconstruire la clé publique à partir de ces données.

> [!NOTE]
> Il s'agit simplement d'une convention de représentation. Il est généralement possible de convertir une clé au format `.pem` en `jwk` et vice-versa.

> [!IMPORTANT]
> Selon le type de clé, les attributs du JWT peuvent changer. Par exemple, une clé à courbe elliptique aura l'attribut `x` et `y` à la place de `n` et `e`.

Un ensemble de *JWK* est appelé **JWKS (JSON Web Key Set)**. Un *JWKS* peut contenir des clés publiques RSA, des clés publiques à courbe elliptique ou d'autres types de clés compatibles avec les standards concernés. Un JWKS public ne devrait **JAMAIS exposer de clés privées ni de secrets symétriques** !

Il est souvent utilisé pour publier les clés publiques permettant aux API de vérifier les signatures des tokens. Son architecture se présente comme un JSON de la forme `{"keys": [JWK_1, JWK_2...]}`.

Dans de nombreuses architectures d'authentification, notamment celles reposant sur *OAuth 2.0* ou *OpenID Connect*, le fournisseur d'identité publie ses clés publiques sous la forme d'un **JWKS accessible via une URL dédiée**. Les API peuvent utiliser cet ensemble de clés pour vérifier les signatures des tokens émis par ce fournisseur. L'URL est souvent de la forme `https://<IdP>/.well-known/jwks.json`.

```text
    Auth Server
         |
         | Signe avec clé privée
         ▼
    ┌───────────┐
    │    JWS    │
    │   Header  │
    │  Payload  │
    │ Signature │
    └─────┬─────┘
          |
          ▼
        Client
          |
          | JWS
          ▼
         API ──────► /.well-known/jwks.json (source de confiance)
          |                    |
          |◄───────────────────┘
          |       Clé publique (JWK)
          ▼
   Vérification JWS
          |
      ┌───┴───┐
      ▼       ▼
    Valide  Invalide
      |       |
    Accès   Rejet
```

> [!WARNING]
> Le *JWKS* met à disposition les clés permettant de vérifier la signature d'un *JWT* mais il est important de vérifier la légitimité de ce *JWKS*. **Un JWKS est un document JSON, pas une preuve d'authenticité en lui-même**.

### Header JWS et sécurité

La partie *Header* du *JWT* contient les métadonnées du *token* nécessaire à sa compréhension. Les paramètres standards sont définis [ici](https://www.rfc-editor.org/rfc/rfc7515.html#section-9.1.2]).

Une attention particulière doit être portée sur les *headers* en lien avec la signature. En effet, une mauvaise utilisation peut mener à des vulnérabilités dans le processus d'authentification.

| Paramètre | Rôle | Exemple | Risque principal |
|---|---|---|---|
| `alg` | Définit l'algorithme cryptographique. | `"alg": "RS256"` | Confusion d'algorithmes ou algorithme non autorisé. |
| `jku` | URL du JWKS contenant les clés. | `"jku": "https://example.com/jwks.json"` | SSRF ou clés contrôlées par un attaquant. |
| `jwk` | Fournit une clé directement dans le header. | `"jwk": {"kty": "RSA", ...}` | Utilisation d'une clé fournie par l'attaquant. |
| `x5u` | URL d'un certificat X.509. | `"x5u": "https://example.com/cert.pem"` | SSRF ou certificat non fiable. |
| `kid` | Identifie la clé à utiliser. | `"kid": "key-123"` | SQLi ou sélection d'une clé non autorisée. |

> [!WARNING]
>En règle générale, une application doit toujours vérifier les informations issues du JWT. Il est souvent préférable que les informations d'authentification nécessaires à l'analyse du JWT soient apportées par l'application-même et non via le JWT.

> [!TIP]
> **🔐 Security relevance**: L'exploitation des *headers* est à l'origine de nombreuses attaques d'authentification JWT.

Grâce à *JWK*, nous pouvons obtenir les informations nécessaires pour réaliser la vérification de la signature. Cependant, un problème potentiel reste présent: **le JWS lui-même est lisible car non chiffré. Cela constitue-t-il un risque majeur ?**

## Description de JWE

Un *JWS* est généralement transporté via le protocole HTTPS. Ainsi, même s'il reste lisible, le chiffrement du contenu lors de la phase *transport* rend son contenu protégé jusqu'au serveur. Néanmoins, au sein du serveur, le JWT peut être lisible.

Généralement, un *JWS* ne contient pas d'informations sensibles. Son chiffrement n'est pas donc pas impératif par rapport à la contrainte que cette approche induit. Cependant, il convient de **limiter les informations contenues dans le payload aux données nécessaires** au fonctionnement de l'application et d'éviter d'y placer des secrets ou des informations confidentielles.

Dans certains contextes, cela peut ne pas être suffisant. C'est pourquoi le standard **JWE (JSON Web Encryption)** [3] a été créé.

*JWE* permet de chiffrer le contenu-même du *payload* du *JWT*, le protégeant sur tout son cycle de vie. Son protocole est le suivant:

1. **Création d’une clé** : une clé secrète est générée pour chiffrer les données: la **CEK (Content Encryption Key)**.
2. **Chiffrement des données** : les données sont rendues illisibles grâce à cette clé.
3. **Génération de l’IV** : une valeur qui aide à sécuriser le chiffrement.
4. **Génération du Tag** : une valeur qui permet de vérifier que les données n’ont pas été modifiées. Il est calculé à partir de la clé secrète (CEK), de l’IV, des données chiffrées et des données associées (comme le header du JWE).
5. **Protection de la clé** : la clé secrète est protégée pour que seul le destinataire autorisé puisse la récupérer via la clé publique du destinataire ou une clé symétrique.
6. **Création du JWE Token** : les données chiffrées et les informations nécessaires sont regroupées dans un token.
7. **Déchiffrement** : le destinataire récupère la clé, déchiffre les données et vérifie qu’elles n’ont pas été modifiées.

```text
╔══════════════════════════════════════════════════════════════╗
║                 JWE — JSON WEB ENCRYPTION                    ║
╚══════════════════════════════════════════════════════════════╝

┌──────────────┐ ┌──────────────┐ ┌────────────┐ ┌──────────────┐ ┌──────────────┐
│    HEADER    │ │ ENCRYPTED KEY│ │     IV     │ │  CIPHERTEXT  │ │     TAG      │
├──────────────┤ ├──────────────┤ ├────────────┤ ├──────────────┤ ├──────────────┤
│ alg: RSA-OAEP│ │ Clé CEK      │ │ IV de      │ │ Données      │ │ Vérification │
│ enc: A256GCM │ │ chiffrée     │ │ 96 bits    │ │ chiffrées    │ │ d'intégrité  │
└──────────────┘ └──────────────┘ └────────────┘ └──────────────┘ └──────────────┘
       │                 │               │               │               │
       └─────────────────┴───────────────┴───────────────┴───────────────┘
                                       │
                                       ▼
BASE64URL(HEADER).BASE64URL(ENCRYPTED_KEY).BASE64URL(IV).BASE64URL(CIPHERTEXT).BASE64URL(TAG)
```

*JWE* complexifie énormément le processus de validation d'un *token* alors que la confidentialité est rarement exigée par les applications/API. C'est pourquoi, à ce jour, ***JWE* reste minoritaire face à *JWS***.

***JWS* et *JWE* ne sont pas exclusifs**. Un *JWT* peut être signé, chiffré, ou signé puis chiffré. Dans ce dernier cas, il utilise les trois concepts : JWT, JWS et JWE. 

```text
                           JWT
                            |
              +-------------+-------------+
              |             |             |
              v             v             v
         Non signé         JWS           JWE
                            |             |
                            |             |
                   Signature / MAC    Chiffrement
                            |             |
                            |             |
                            v             v
                      Intégrité       Confidentialité
                      Authenticité    Intégrité
                            |             |
                            +------+------+
                                   |
                                   v
                          Combinaison possible
                              JWS dans JWE
                                   |
                                   v
                         Signature + chiffrement
```

L'ordre est important : **on signe d'abord, puis on chiffre**. Ce type de *token* est appelé **Nested JWT**.

```text
┌──────────────────────────────┐
│ JWE — Header extérieur       │
│ alg: RSA-OAEP                │
│ enc: A256GCM                 │
├──────────────────────────────┤
│ JWE chiffre le JWS complet   │
│                              │
│  ┌────────────────────────┐  │
│  │ JWS — Header intérieur │  │
│  │ alg: RS256             │  │
│  ├────────────────────────┤  │
│  │ Payload                │  │
│  ├────────────────────────┤  │
│  │ Signature              │  │
│  └────────────────────────┘  │
└──────────────────────────────┘
```

| **JWS (JSON Web Signature)**           | **JWE (JSON Web Encryption)**                         |
| :------------------------------------- | :---------------------------------------------------- |
| 🖊️ **Signature numérique**              | 🔐 **Chiffrement**                                     |
| Garantit l’intégrité et l’authenticité | Garantit la confidentialité                           |
| Le contenu reste lisible               | Le contenu est illisible sans la clé de déchiffrement |
| **Objectif :** vérifier le contenu     | **Objectif :** protéger le contenu                    |


> [!IMPORTANT]
> *JWT* désigne un format de représentation de *claims*, tandis que *JWS* et *JWE* définissent des mécanismes et des formats de protection de contenu

## Validation du JWT et contrôle d'accès

Un JWT correctement signé peut contribuer à l'authentification et à l'intégrité des informations transportées. Cependant, **une signature valide ne garantit pas à elle seule que l'utilisateur possède les droits nécessaires** pour accéder à une ressource (autorisation). Le serveur doit appliquer ses propres règles d'accès à chaque ressource en adéquation avec les droits de l'utilisateur décrit par le JWT.

Il y a trois niveaux de vérification distincts lors de l'utilisation d'un JWT.

1. **Validité cryptographique** : le token est-il authentique ?

   Le serveur vérifie la signature du JWT à l'aide de la clé appropriée. Cette vérification permet de s'assurer que le token a été signé par une entité de confiance et que son contenu n'a pas été modifié depuis sa signature.

   **Exemple** : un utilisateur modifie son rôle de user en admin dans le contenu du token. La signature ne correspond plus au contenu modifié : le serveur rejette le token.

2. **Validité protocolaire** : le token est-il utilisable dans ce contexte ?

   Même si la signature est valide, le serveur doit vérifier que le JWT respecte les règles attendues par l'application et le protocole utilisé.

   Cela implique notamment de vérifier :
      - **L'expiration (exp)** : le token n'a pas expiré.
      - **L'émetteur (iss)** : le token provient de l'émetteur attendu.
      - **Le destinataire (aud)** : le token est destiné à cette application ou API.
      - **L'algorithme (alg)** : l'algorithme cryptographique utilisé est autorisé.
      - **Le contexte d'utilisation** : le token est bien destiné à l'usage prévu, par exemple un access token et non un autre type de token.

    **Cette liste n'est pas exhaustive**. Il existe d'autres paramètres possibles. La présence (ou non) des paramètres dépend de la configuration du service *émetteur* du *token* et leurs analyses, de l'application qui authentifie le *token*.

    > [!IMPORTANT]
    > Il est possible de configurer l'emetteur du *token* pour définir les paramètres présents dans le JWT. Si ce dernier ne peut fournir les informations nécessaires à l'application, l'authentification ne pourra être correctement réalisée.
  
    **Exemple**: Un *token* a une signature valide. Dans son *payload*, `exp` indique une date expirée. L'application considère le *token* comme invalide.

3. **Autorisation** : l'utilisateur a-t-il le droit d'effectuer cette action ?

    Une fois le token authentifié et validé, le serveur doit déterminer si l'utilisateur identifié dispose des permissions nécessaires pour accéder à la ressource demandée.

    Cette décision dépend notamment de son rôle, de ses permissions et des règles métier applicables à la ressource. **Un rôle présent dans le token ne doit pas être considéré comme une autorisation universelle** : les permissions doivent être vérifiées en fonction de la ressource, de l'action et des règles métier.

    **Exemple** : un utilisateur possède un JWT valide et non expiré, mais son rôle est `user`. Il tente de supprimer un compte utilisateur, une action réservée aux administrateurs. Le serveur refuse l'opération avec une réponse 403 Forbidden.

En résumé, le serveur doit vérifier successivement la signature, les conditions de validité du token, puis les droits d'accès à la ressource. **Il ne doit pas faire confiance au token par défaut, doit vérifier sa cohérence et imposer un contrôle strict des autorisations**.

## 🧠 Quiz — Authentification JWT

**Objectif :** vérifier la compréhension des notions essentielles abordées dans le cours : authentification, JWT, structure du token, signature, chiffrement, gestion des clés, validation et autorisation.

<details>
<summary>Questionnaire</summary>

## 🟢 Niveau facile
### Question 1 — Authentification et autorisation
<details>
<summary>Un utilisateur est correctement identifié par l’application. Peut-on en déduire qu’il a le droit de supprimer n’importe quelle ressource ? Pourquoi ?</summary>

**Réponse :**
Non. L’authentification permet de vérifier l’identité de l’utilisateur, tandis que l’autorisation détermine les actions qu’il est autorisé à effectuer. Le serveur doit donc vérifier les permissions associées à la ressource et à l’action demandée.
</details>

### Question 2 — Base64URL

<details>
<summary>Un utilisateur décode le payload d’un JWT et peut lire le rôle et l’identifiant qui y figurent. Cela signifie-t-il qu’il a réussi à casser le chiffrement du token ?</summary>

**Réponse :**
Non. Dans un JWS classique, le header et le payload sont encodés en Base64URL, mais ne sont pas chiffrés. Leur lecture ne nécessite donc pas de casser un chiffrement. La signature sert à vérifier l’intégrité et l’authenticité du contenu, pas à le rendre confidentiel.
</details>

## 🟡 Niveau intermédiaire

### Question 3 — Structure d’un JWT signé

<details>
<summary>Un exemple de JWT est présenté comme signé avec RS256, mais son header indique "alg":"none". Qu’est-ce qui ne va pas dans cet exemple ?</summary>

**Réponse :**
L’exemple est incohérent : RS256 indique un algorithme de signature RSA avec SHA-256, tandis que none indique qu’aucune signature n’est appliquée. Le header doit correspondre au mécanisme réellement utilisé. Pour illustrer un JWS signé avec RS256, le header doit notamment indiquer "alg":"RS256" et le token doit contenir une signature correspondante.
</details>

### Question 4 — Sessions et JWT

<details>
<summary>Une équipe choisit JWT parce qu’elle pense que cela rend automatiquement toute son architecture stateless. Cette conclusion est-elle correcte ?</summary>

**Réponse :**
Non. Un JWT signé peut être vérifié sans consulter systématiquement un stockage central de sessions, mais l’application peut tout de même conserver un état, par exemple pour gérer la révocation, les comptes désactivés ou les sessions. Le choix entre sessions et JWT dépend des besoins et de l’architecture globale.
</details>

### Question 5 — Signature valide, token acceptable ?

<details>
<summary>Une API reçoit un JWT dont la signature est valide. Peut-elle l’accepter immédiatement sans effectuer d’autres vérifications ?</summary>

**Réponse :**
Non. Une signature valide permet de vérifier l’intégrité du contenu et son origine cryptographique selon la clé utilisée, mais ne suffit pas à établir que le token est utilisable dans ce contexte. L’API doit notamment vérifier les paramètres attendus, tels que l’expiration (exp), l’émetteur (iss), le destinataire (aud) et l’algorithme autorisé, selon le protocole et la configuration.
</details>

## 🟠 Niveau difficile

### Question 6 — Signature symétrique et asymétrique

<details>
<summary>Un service émet des JWT et plusieurs API doivent vérifier leurs signatures. Quelle différence importante existe entre HS256 et RS256 dans cette architecture ?</summary>

**Réponse :**
Avec HS256, l’émetteur et les API vérificatrices doivent partager le même secret. Chaque partie qui possède ce secret peut aussi produire une signature valide.
Avec RS256, l’émetteur signe avec sa clé privée et les API peuvent vérifier avec la clé publique correspondante. Elles n’ont donc pas besoin de posséder la clé privée permettant de créer de nouvelles signatures.
</details>

### Question 7 — JWK et JWKS

<details>
<summary>Une API récupère un JWKS depuis une URL fournie directement dans un JWT reçu d’un client. Peut-elle considérer automatiquement les clés récupérées comme fiables ?</summary>

**Réponse :**
Non. Un JWKS est un document JSON qui représente un ensemble de clés ; il ne constitue pas à lui seul une preuve de confiance. L’API doit s’appuyer sur une source de clés configurée ou autrement approuvée pour l’émetteur attendu, et ne pas faire confiance automatiquement à une URL ou à une clé simplement parce qu’elle figure dans le token reçu.
</details>

### Question 8 — JWS et JWE

<details>
<summary>Une application veut que le contenu d’un token ne puisse pas être lu par toute personne qui le récupère. Un JWT simplement signé avec JWS répond-il à cet objectif ?</summary>

**Réponse :**
Non. JWS permet de protéger l’intégrité du contenu et d’en vérifier l’authenticité, mais le payload reste lisible. JWE permet de chiffrer le contenu afin d’en assurer la confidentialité. Dans tous les cas, il convient de limiter les informations sensibles transportées dans un token.
</details>

## 🔴 Niveau expert

### Question 9 — Validation du contexte

<details>
<summary>Un JWT possède une signature valide, mais son champ exp indique qu’il a expiré. L’API peut-elle encore l’accepter au motif que sa signature est correcte ?</summary>

**Réponse :**
Non. La signature valide ne remplace pas la vérification des conditions d’utilisation du token. Si l’expiration doit être respectée dans le contexte concerné, le token expiré doit être rejeté. L’API doit également vérifier les autres paramètres requis, notamment l’émetteur, le destinataire et l’algorithme autorisé.
</details>

### Question 10 — Token valide et droits insuffisants

<details>
<summary>Un utilisateur présente un JWT dont la signature est valide, qui n’est pas expiré et qui est destiné à l’API. Le payload contient le rôle user, mais l’utilisateur demande la suppression d’un compte réservée aux administrateurs. Que doit faire l’API ?</summary>

**Réponse :**
L’API doit refuser l’opération, car la validité du JWT ne confère pas automatiquement les permissions nécessaires. Elle doit vérifier les droits de l’utilisateur pour cette ressource et cette action. Si l’utilisateur est authentifié mais n’est pas autorisé à effectuer l’opération, une réponse 403 Forbidden est appropriée.
</details>
</details>

## Références

* [1] JSON Web Token (JWT), https://www.rfc-editor.org/info/rfc7519/
* [2] JSON Web Signature (JWS), https://datatracker.ietf.org/doc/html/rfc7515
* [3] JSON Web Encryption (JWE), https://datatracker.ietf.org/doc/html/rfc7516
* [4] JSON Web Algorithms (JWA), https://datatracker.ietf.org/doc/html/rfc7518#section-3.1
* [5] JSON Web Key (JWK), https://datatracker.ietf.org/doc/html/rfc7517

