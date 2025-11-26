![Status](https://img.shields.io/badge/Prime%20Research-Number%20Theory-blue)

Prime Cluster Hunting
A Study on the Generation of Prime Quadruplets Using Primorial Bases

Author: Rodrigo Mendonça de Oliveira
Date: November 24, 2025


🧠 Abstract (English)

This study investigates a deterministic and heuristic method to locate clusters of prime numbers — specifically prime quadruplets in the form (p, p+2, p+6, p+8) — at extremely large magnitudes. By multiplying Primorial Bases (sequential products of primes) by sequential prime multipliers, the method exploits "Arithmetic Shielding" to prevent small prime divisors in a neighborhood around the generated numbers. This significantly increases the probability of primality when compared to purely random search.
Tests conducted on home hardware using Python confirmed the effectiveness of primorial bases (105, 15,015, 255,255, and 4,849,845), culminating in the detection of quadruplets in the order of 6 trillion, and validated the method via a zero-result control group using non-primorial numbers.

🇧🇷 Resumo Executivo (Português)

Este repositório reúne o estudo completo, os dados, o código e os dashboards usados na pesquisa “Caça aos Aglomerados Primos”. O método utiliza Bases Primoriais multiplicadas por primos sequenciais para localizar Quadrupletos Primos na forma (p, p+2, p+6, p+8).
A técnica de Blindagem Aritmética elimina divisores pequenos da vizinhança dos números candidatos, elevando significativamente a chance de primalidade.
Foram encontrados 870 quadrupletos, incluindo valores na casa de 6 trilhões, e o grupo de controle confirmou eficiência exclusiva das bases primoriais.


▶️ Running the Code

Requirements:

Python 3.10+
sympy
pandas
tqdm

Install:

pip install sympy pandas tqdm

Run the script:

python prime_clusters_4849845.py


The script outputs:

All detected prime quadruplets

Intermediate clusters (triplets, twins)

Dashboards (HTML)

Summary statistics

| Base Primorial | Quadruplets | Max Magnitude     |
| -------------- | ----------- | ----------------- |
| **105**        | 258         | 135 million       |
| **15,015**     | 265         | 19 billion        |
| **255,255**    | 194         | 331 billion       |
| **4,849,845**  | 153         | **6.29 trillion** |


Control group (non-primorial bases): 0 quadruplets
→ Confirming the structural effect of Arithmetic Shielding.

🔬 Scientific Importance

Your results demonstrate:

Strong evidence of primorial-based primality corridors

Efficient detection of prime clusters at extreme magnitudes

A reproducible heuristic capable of scaling beyond trillions

Clear rejection of randomness via control groups

This makes your work relevant to:

Computational number theory

Prime distribution studies

Heuristic prime-search algorithms

Research on prime constellations


📬 Contact

If you wish to collaborate or extend this research:

Rodrigo Mendonça de Oliveira
🔗 GitHub: https://github.com/rodrigomendon

📧 Email: rodrigo38221305@gmail.com

🛡️ License

CC BY-NC-ND 4.0 — Creative Commons Attribution-NonCommercial-NoDerivatives

