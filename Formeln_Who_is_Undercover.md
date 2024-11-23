1. **Self-Perspective**

describe words in one sentence from its own perspective. Reference from the first level of human indication of intentionality

Suppose it is now the turn of player **α** **(α ∈ {1,...,n})**
to speak, Player α will think as follows:

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/98ad9f53-a23a-4953-a714-20d78dd02eaa/f0442362-fe77-4004-a67a-79c0b1a37131/image.png)

1. **Identity-Determination** 

Player α determines it identity based on the global historical records H :

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/98ad9f53-a23a-4953-a714-20d78dd02eaa/932887a7-ff5b-4037-a929-2cd452a98f97/image.png)

1. **Self-Reflection**

 Player α needs to reflect on itselves to find common features in the description to avoid exposure.

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/98ad9f53-a23a-4953-a714-20d78dd02eaa/d5944251-3b98-4131-bddb-2e7c23620e62/image.png)

1. **Summary Order**

After these reflections, the AI agents will make a summary of ideas Oα, which mainly includes 

self-conclusion and the speaking recommendations, update with rounds:

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/98ad9f53-a23a-4953-a714-20d78dd02eaa/61de6869-fb84-4a51-ad60-8e6ab89e55eb/image.png)

1. **Aktualisierung der Beobachtung O’**α

Nochmal die Erklärung wann die Aktualierung stattfindet:

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/98ad9f53-a23a-4953-a714-20d78dd02eaa/48360eca-e40c-4120-bbfd-ea617f7258fc/image.png)

1. **Word-Speak**

Wα is the content of player α’s final speech in the r round. Itwill be added to the historical records H to drive the game.

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/98ad9f53-a23a-4953-a714-20d78dd02eaa/31bae55d-4225-4dfb-8f06-ce49202d56bb/image.png)

### Phase 2 Refections on the Voting Sessions

Problem: Agent has to derive conclusion on who culd be a Teammate with incomplete Information

MPTTs Approch:

Players review the history of others’ speeches to identify teammates and opponents, comparing and
analyzing characteristics in multiple ways. Before each round of voting opens, e**ach player thinks simultaneously:**

**8.  First-FindTeammate**

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/98ad9f53-a23a-4953-a714-20d78dd02eaa/39c1aec2-af6e-405d-9ec8-1435190c69ac/image.png)

1. **Second-FindTeammate**

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/98ad9f53-a23a-4953-a714-20d78dd02eaa/4464b1ce-fd0d-4110-b97e-5bf8b109e0fd/image.png)

1.  **Game-Decision**

Finally Players use cumulative reflection andjudgement to build more explicit trust,and update Oα to
better adapt to the dynamic situation (refer to Eq. 4 and add
Fα, Jα in it, as well as update Eq.5):

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/98ad9f53-a23a-4953-a714-20d78dd02eaa/1e0169fa-c3a6-4b0c-8d87-24accd219b74/image.png)

1. Word-Vote 

Players are  encouraged to find teammates and fostering cooperation, think strategically in their votes, choosing the right player to vote for to ensure that the results favor their team:

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/98ad9f53-a23a-4953-a714-20d78dd02eaa/eb019877-4b09-476d-911f-c744ec67727b/image.png)

The results of all players’ votes are tallied for each round of the game, the player with the highest number of votes will be out of the game.












### Target Variables

  **1. VictoryRate (VR):**  measures the probability of winning the game → Team Target

 2. **(SR@1):** Survival Rate in the First Round → Individual Target

1.  **(SR@2):** Survival Rate in the Second Round || Werwolf doesn’t have a fixed amout of rounds so 
2. **(SR@X):** Suvival Rate after each Consecutive Round → Individual Target
3. **(X = number of rounds r)  →** ( X **∈ {3,...,n})** 

Dorfbewohner:

 **6. (PST):** Probability of Successfully Trusting Own Team → Individual Target

Nur Wer

1. **(PSA):** measure the team’s ability to recognize teammates and identify opponents → Team Target