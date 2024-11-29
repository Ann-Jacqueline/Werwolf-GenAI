# WerwolfIQ- GenAI App
 Unsere Multi Agent GenAI App WerwolfIQ spielt mit einem oder mehreren humans-in-the-loop Players das allbekannte Strategiespiel Werwolf.
 Unsere Multi Agents wurden durch Taktiken des MPTT (Multi Player Team Tatic) besseres Reasoning durch Self-Reflection und Beobachtungszyklen benutzt.
 Diese Taktiken wurden durch ein Custon Multi Head Neuronalen Netztwerk implementiert
 

Mögliche Projektstuktur
Werwolf-GenAI/
├── Config/
│   ├── config.py
│   ├── hyperparameters.yaml
│   └── database_config.yaml
├── data/
│   ├── raw/
│   └── processed/
├── docs/
│   ├── App_Ansätze.md
│   ├── Paper versionierung
│   ├── Werwolf_Spielregeln
│   ├── formulas/
│   │   ├── self_perspective_eq.md
│   │   ├── identity_determination_eq.md
├── models/
│   ├── transformer.py
│   ├── custom_layers.py
│   ├── combined_model.py
│   └── __init__.py
├── references/
│   ├── papers/
│   │   ├── transformer_paper.pdf
│   │   ├── bert_paper.pdf
│   └── frameworks/
│       ├── pytorch_guide.md
├── tests/
│   ├── test_custom_layers.py
│   ├── test_combined_model.py
│   └── __init__.py
├── experiments/
│   ├── playground.py
├── utils/
│   ├── tokenizer.py
│   ├── trainer.py
│   └── data_loader.py
├── main.py
├── ReadME.md
└── TODO.md
