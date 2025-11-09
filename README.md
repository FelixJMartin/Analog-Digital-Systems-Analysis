# Analog-Digital-Systems-Analysis
This project focused on the analysis and realization of continuous-time analog filters and the subsequent design of a complete digital sampling system for a measurement application.


## Part 1 — Analysis of Analog Filters

This section analyzes a **second-order active filter** using operational amplifiers, resistors, and capacitors.  
The circuit can realize **three different filter types** depending on which output (`y₁(t)`, `y₂(t)`, or `y₃(t)`) is used.

![Filter](assets/img/Figure1.jpg)

---

### MATLAB Functions Used

- `tf` — Creates system objects for LTIC systems  
- `lsim` — Simulates time-domain responses  
- `iopzplot` — Generates pole-zero plots  
- `impulse` — Plots impulse responses 
- `bode` — Plots frequency responses  
- `repmat` — Helps construct periodic input signals  

---

### Circuit Description

The circuit (Figure 1) consists of five operational amplifiers:
- **OP1**: inverting summer  
- **OP2, OP3**: inverting integrators  
- **OP4, OP5**: inverting amplifiers  

Both integrators share the same `R` and `C`, and amplifiers have identical gain  

$$
-G = -\frac{R_5}{R_4}
$$

where $\(G>0\)$. 


---

### Objective

From the configuration, derive and study the three transfer functions:
$
H_1(s),\ H_2(s),\ H_3(s)
$

Each output corresponds to a different filter type (LP, HP, or BP).  
Subsequent analysis compares **pole-zero plots**, **impulse responses**, and **Bode diagrams** to show how parameters affect behavior.

### Part 1.2 — Derivation of Transfer Functions

![Flow diagram](assets/img/Figure2.png)


**Task:**  
From the flow diagram in Figure 2, derive the transfer functions  

$
H_1(s), H_2(s), H_3(s)
$

which describe the relationship between the input signal $X(s)$ and the analog outputs $Y_1(s)$, $Y_2(s)$, and $Y_3(s)$.  

**Exexution**  
I began with $H_3(s)$, which simplifies most directly from the flow diagram, and then used it to obtain $H_1(s)$ and $H_2(s)$ algebraically.  
The resulting expressions form the foundation for the later frequency-domain and time-domain analyses.

