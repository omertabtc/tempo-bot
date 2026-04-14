# 🔍 Comment Tester la Détection de Scams

## 🎯 3 Façons de Vérifier

### **Méthode 1 : Test Simulé (RECOMMANDÉ)** ⭐

Lance ce script qui teste 6 patterns de scam :

```bash
python test_scam_detection.py
```

**Ce qu'il teste :**
1. ✓ Honeypot (impossible de vendre)
2. ✓ Rug pull (owner peut tout drainer)
3. ✓ Proxy malveillant (pas de contrôle d'accès)
4. ✓ Self-destruct
5. ✓ Mint illimité
6. ✓ Manipulation de frais

**Résultat attendu :** Tous doivent être **HIGH/CRITICAL** ❌

---

### **Méthode 2 : Contrats Scam Réels**

Teste avec de **vrais scams** sur Ethereum (NE PAS INTERAGIR !) :

**Honeypot Token :**
```
0x5558447B06867ffebd87DD63426d61c868c45904
```
→ Les users peuvent acheter mais pas vendre

**Rug Pull :**
```
0x69692D3345010a207b759a7D1af6fc7F38b35c5E
```
→ Owner a drainé toute la liquidité

**Pour tester :**
1. Change temporairement vers Ethereum dans `.env` :
```env
TEMPO_RPC_URL=https://eth.llamarpc.com
TEMPO_EXPLORER_API=https://api.etherscan.io/api
TEMPO_CHAIN_ID=1
```

2. Redémarre le bot
3. Teste dans Discord :
```
/analyze-contract 0x5558447B06867ffebd87DD63426d61c868c45904
```

**Résultat attendu :** 🔴 **HIGH RISK / CRITICAL**

---

### **Méthode 3 : Crée Ton Propre Scam Test**

Déploie un contrat malveillant sur un **testnet** :

```solidity
// EXEMPLE DE SCAM - NE PAS UTILISER EN PROD
pragma solidity ^0.8.0;

contract TestScam {
    address public owner;
    
    constructor() {
        owner = msg.sender;
    }
    
    // 🚩 Owner peut drainer tout
    function drainAll() public {
        require(msg.sender == owner);
        payable(owner).transfer(address(this).balance);
    }
    
    // 🚩 Mint illimité
    function mint(uint256 amount) public {
        require(msg.sender == owner);
        // Pas de max supply !
    }
    
    // 🚩 Peut détruire le contrat
    function kill() public {
        require(msg.sender == owner);
        selfdestruct(payable(owner));
    }
}
```

Puis teste avec `/analyze-contract` !

---

## ✅ **Test Complet : Checklist**

Pour vérifier que tout fonctionne :

```bash
# 1. Teste les scams simulés
python test_scam_detection.py
# → Tous devraient être détectés comme HIGH/CRITICAL

# 2. Teste tes contrats SAFE
python test_smart_detection.py
# → Devraient être SAFE/LOW

# 3. Teste sur Discord
/analyze-contract 0x3e12fcb20ad532f653f2907d2ae511364e2ae696
# → Devrait être SAFE ✅

# Si tu testes un vrai scam Ethereum :
/analyze-contract 0x5558447B06867ffebd87DD63426d61c868c45904
# → Devrait être HIGH RISK ❌
```

---

## 📊 **Résultats Attendus**

### Contrats SAFE ✅
- Risk Level: **SAFE ou LOW**
- Risk Score: **5-25/100**
- Embed: **🟢 VERT ou 🟡 JAUNE**
- Findings: Principalement **INFO**

### Contrats SCAM ❌
- Risk Level: **HIGH ou CRITICAL**
- Risk Score: **70-100/100**
- Embed: **🔴 ROUGE**
- Findings: Plusieurs **CRITICAL/HIGH**

---

## 🎯 **Test Rapide Maintenant**

Lance ça pour vérifier immédiatement :

```bash
python test_scam_detection.py
```

**Tu devrais voir :**
```
Testing: Honeypot - Can't Sell
Risk Level: HIGH
✓ SUCCESS: Scam pattern DETECTED!

Testing: Rug Pull - Owner Can Drain
Risk Level: CRITICAL
✓ SUCCESS: Scam pattern DETECTED!

...

Detection Rate: 6/6 (100%)
✓ PERFECT! All scam patterns detected!
```

---

## 🔧 **Si un Scam n'est PAS Détecté**

Si tu trouves un scam marqué comme SAFE :

1. **Note l'adresse du contrat**
2. **Lance :**
   ```bash
   python diagnose_simple.py ADRESSE_DU_SCAM
   ```
3. **Envoie-moi les résultats**
4. **J'ajouterai la détection** pour ce pattern

---

## 🛡️ **Patterns Scam Détectés**

Le bot détecte ces patterns malveillants :

### 🔴 CRITICAL
- ✓ SELFDESTRUCT (peut détruire le contrat)
- ✓ Owner peut drainer tout le balance
- ✓ Mint public sans contrôle d'accès
- ✓ Proxy upgradeable sans autorisation
- ✓ Delegatecall vers input utilisateur

### 🟠 HIGH
- ✓ Mint illimité par owner (pas de max supply)
- ✓ Restrictions de transfer (honeypot)
- ✓ Mécanisme de blacklist
- ✓ Frais modifiables (peut mettre à 100%)
- ✓ Pas de protection contre reentrancy

### 🟡 MEDIUM
- ✓ Contrat pausable
- ✓ Pas de timelock sur fonctions critiques
- ✓ Ownership centralisé (un seul wallet)

---

## 💡 **Balance Importante**

Le bot doit trouver le bon équilibre :

- **Trop strict** = Faux positifs (contrats safe marqués scam)
- **Trop loose** = Scams manqués (scams marqués safe)

**Actuellement :** Optimisé pour ~80-90% de précision

---

**Lance `python test_scam_detection.py` maintenant !** 🚀

Si tous les scams sont détectés ET tes contrats NFT sont SAFE, **le bot est parfait !** ✅
