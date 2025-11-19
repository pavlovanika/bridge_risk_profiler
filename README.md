# bridge_risk_profiler

bridge_risk_profiler is a tiny CLI tool that estimates conceptual risk for Web3 bridges.

It does not connect to a blockchain. Instead, it uses a few high-level design flags and a base profile to compute rough technical, economic, and operational risk scores between 0.0 and 1.0, along with a qualitative risk label.

The tool is thematically aligned with ecosystems and ideas around:
- Aztec-style zk privacy rollups
- Zama-style FHE compute and bridges
- Soundness-first protocol and bridge design

Exactly two files are expected in this repository:
- app.py
- README.md


Overview

Bridges often combine cross-chain messaging, asset custody, and complex assumptions. This tool provides a structured way to reason about their risk posture.

You choose a base style:
- aztec    (privacy rollup bridge)
- zama     (FHE-aware bridge)
- soundness (formal, soundness-first bridge)

Then you toggle features such as:
- whether the bridge uses zk proofs
- whether it interacts with FHE
- whether it has on-chain light clients
- whether it relies on MPC or multisig signers
- whether there are timelocks, audits, and formal specs
- whether it is multi-chain
- a rough TVL rank

The tool outputs separate risk components and an overall risk score and label.


Installation

Requirements:
- Python 3.8 or newer

Steps:
1. Create a new GitHub repository.
2. Place app.py and this README.md in the root directory.
3. Ensure python is available on your PATH.
4. No external dependencies are required; the script uses only the standard library.


Usage

Run from the repository root.

Basic Aztec-style zk bridge:
python app.py --style aztec --zk --light-client --audits --timelock

Zama-style FHE-heavy bridge:
python app.py --style zama --fhe --zk --mpc-signers --multi-chain --tvl-rank 5

Soundness-first bridge with formal specs and governance protections:
python app.py --style soundness --zk --audits --formal-specs --timelock --tvl-rank 15

JSON mode for dashboards or CI:
python app.py --style aztec --zk --light-client --audits --json


Parameters

--style
Base profile of the bridge architecture.
- aztec      zk privacy bridge inspired by rollups like Aztec.
- zama       FHE-aware bridge interacting with encrypted compute.
- soundness  bridge coming from a soundness-first, formally modeled design culture.

--zk
If set, the bridge uses zero-knowledge proofs in its validation or message path.

--fhe
If set, the bridge touches fully homomorphic encryption components or data flows.

--light-client
If set, the bridge verifies remote consensus via an on-chain light client, reducing reliance on trusted relayers.

--mpc-signers
If set, the bridge is controlled by MPC or multisig signers; this lowers protocol complexity but raises a signer-compromise risk.

--timelock
If set, critical actions and upgrades are delayed by a timelock, reducing economic risk and sudden governance attacks.

--audits
If set, the bridge code has at least one independent security audit.

--formal-specs
If set, the bridge has a formal specification or model, enabling deeper soundness analysis.

--multi-chain
If set, the bridge connects more than two chains, which can increase complexity and operational risk.

--tvl-rank
A rough ranking of TVL; 1 for very high TVL, larger numbers for lower TVL. Higher TVL mildly increases economic risk in the model.

--json
Prints a JSON document instead of formatted text, suitable for dashboards and scripts.


Output

The tool prints:

- base style and description
- the selected design features
- technicalRisk   (0–1)
- economicRisk    (0–1)
- operationalRisk (0–1)
- overallRisk     (0–1)
- riskLabel       (very_low, low, moderate, high, very_high)

Technical risk reflects protocol and cryptographic complexity and trust models.
Economic risk reflects capital at stake and robustness of safety mechanisms.
Operational risk re
