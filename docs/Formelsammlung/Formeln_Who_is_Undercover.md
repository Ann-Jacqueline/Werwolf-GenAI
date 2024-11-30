
### Formeln sind in diesen Dokumenten nochmal erklärt: 
#### [Werwolf Abstract v1.pdf](../App%20Ans%C3%A4tze%20und%20Paperversionierung/Werwolf%20Abstract%20v1.pdf)
#### [Multi agent game tatic.pdf](../../references/Papers_Framworks/Multi%20agent%20game%20tatic.pdf)




### **Self-Perspective**

##### Englisch:
<img src="MPPT_Formeln_Bilder/img_1.png" alt="Monitoring" width="600">


##### Deutsch:

<img src="MPPT_Formeln_Bilder/img_2.png" alt="Monitoring" width="600">

-------------------------------------------------------------------------------------

## RAUS da in Werwolf die eigene Role bekannt ist, Ma also in den Formeln nicht mitbetrachen da die Rolle dem Agent mit als Input gegeben wird
### **Identity-Determination** 

##### Englisch:
<img src="MPPT_Formeln_Bilder/img_3.png" alt="Monitoring" width="600">


##### Deutsch:

<img src="MPPT_Formeln_Bilder/img_4.png" alt="Monitoring" width="600">

-----------------------------------------------------------------------------------

### **Self-Reflection**

 ##### Englisch:
<img src="MPPT_Formeln_Bilder/img_5.png" alt="Monitoring" width="600">


##### Deutsch:

<img src="MPPT_Formeln_Bilder/img_6.png" alt="Monitoring" width="600">

-----------------------------------------------------------------------------------

### **Summary Order**

##### Englisch:
<img src="MPPT_Formeln_Bilder/img_7.png" alt="Monitoring" width="600">


##### Deutsch:

<img src="MPPT_Formeln_Bilder/img_8.png" alt="Monitoring" width="600">

----------------------------------------------------------------------------------
### **Updating Observations: O’α**

##### Englisch:
<img src="MPPT_Formeln_Bilder/img_9.png" alt="Monitoring" width="600">


##### Deutsch:

<img src="MPPT_Formeln_Bilder/img_10.png" alt="Monitoring" width="600">


### **Unterschied von Oα und O'α**


##### Erklärung:
<img src="MPPT_Formeln_Bilder/img.png" alt="Monitoring" width="600">

##### Nochmal an den gleichungen gezeigt:
<img src="MPPT_Formeln_Bilder/img_23.png" alt="Monitoring" width="600">

##### Zusammenfassung:
<img src="MPPT_Formeln_Bilder/img_24.png" alt="Monitoring" width="600">

----------------------------------------------------------------------------------

### **Word-Speak**

##### Englisch:
<img src="MPPT_Formeln_Bilder/img_11.png" alt="Monitoring" width="600">


##### Deutsch:

<img src="MPPT_Formeln_Bilder/img_12.png" alt="Monitoring" width="600">

----------------------------------------------------------------------------------

### **Updating Historical Records**

##### Englisch:
<img src="MPPT_Formeln_Bilder/img_13.png" alt="Monitoring" width="600">


##### Deutsch:

<img src="MPPT_Formeln_Bilder/img_14.png" alt="Monitoring" width="600">

----------------------------------------------------------------------------------


### Phase 2 Refections on the Voting Sessions

### **First-FindTeammate**

##### Englisch:
<img src="MPPT_Formeln_Bilder/img_15.png" alt="Monitoring" width="600">


##### Deutsch:

<img src="MPPT_Formeln_Bilder/img_16.png" alt="Monitoring" width="600">

----------------------------------------------------------------------------------
### **Second-FindTeammate**

##### Englisch:
<img src="MPPT_Formeln_Bilder/img_17.png" alt="Monitoring" width="600">


##### Deutsch:

<img src="MPPT_Formeln_Bilder/img_18.png" alt="Monitoring" width="600">

----------------------------------------------------------------------------------

### **Unsere selbst entwickelte neue Formel, um die Dynamik der Spielrunden besser zu modellieren:**

### **X-FindTeammate**

##### Englisch:
<img src="MPPT_Formeln_Bilder/img_25.png" alt="Monitoring" width="600">
-
<img src="MPPT_Formeln_Bilder/img_26.png" alt="Monitoring" width="600">

##### Deutsch:

<img src="MPPT_Formeln_Bilder/img_27.png" alt="Monitoring" width="600">
-
<img src="MPPT_Formeln_Bilder/img_28.png" alt="Monitoring" width="600">

### Punkte, wo wir die Formel und die Implementierung noch mehr Anpassen müssen und Vorsichtig sein müssen:

<img src="MPPT_Formeln_Bilder/img_29.png" alt="Monitoring" width="600">
-
<img src="MPPT_Formeln_Bilder/img_30.png" alt="Monitoring" width="600">
----------------------------------------------------------------------------------

###  **Game-Decision**

##### Englisch:
<img src="MPPT_Formeln_Bilder/img_19.png" alt="Monitoring" width="600">


##### Deutsch:

<img src="MPPT_Formeln_Bilder/img_20.png" alt="Monitoring" width="600">

----------------------------------------------------------------------------------

### **Word-Vote** 

##### Englisch:
<img src="MPPT_Formeln_Bilder/img_21.png" alt="Monitoring" width="600">


##### Deutsch:

<img src="MPPT_Formeln_Bilder/img_22.png" alt="Monitoring" width="600">

----------------------------------------------------------------------------------
### Target Variables

| **#** | **Variable**         | **Description**                                                                                          | **Target Type**   |
|-------|-----------------------|----------------------------------------------------------------------------------------------------------|-------------------|
| 1     | **VictoryRate (VR)** | Measures the probability of winning the game                                                             | Team Target       |
| 2     | **SR@1**             | Survival Rate in the First Round                                                                         | Individual Target |
| 3     | **SR@2**             | Survival Rate in the Second Round (Werwolf doesn’t have a fixed amount of rounds)                        | Individual Target |
| 4     | **SR@X**             | Survival Rate after each consecutive round                                                               | Individual Target |
| 5     | **X = number of rounds r** | (X **∈ {3,...,n})**                                                                                     | /                 |
| 6     | **PSA**              | Measures the team’s ability to recognize teammates and identify opponents                                | Team Target       |
| 7     | **PST** (Dorfbewohner) | Probability of Successfully Trusting Own Team                                                           | Individual Target |

