#!/usr/bin/env python3
import argparse
import json
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class BridgeProfile:
    key: str
    name: str
    description: str
    base_technical_risk: float   # 0–1 (higher = riskier)
    base_economic_risk: float    # 0–1
    base_operational_risk: float # 0–1


PROFILES: Dict[str, BridgeProfile] = {
    "aztec": BridgeProfile(
        key="aztec",
        name="Aztec-style Privacy Bridge",
        description="Bridge for zk privacy rollups with encrypted state and batched proofs.",
        base_technical_risk=0.35,
        base_economic_risk=0.40,
        base_operational_risk=0.30,
    ),
    "zama": BridgeProfile(
        key="zama",
        name="Zama-style FHE Bridge",
        description="Bridge interacting with FHE compute layers and encrypted pipelines.",
        base_technical_risk=0.45,
        base_economic_risk=0.42,
        base_operational_risk=0.38,
    ),
    "soundness": BridgeProfile(
        key="soundness",
        name="Soundness-first Research Bridge",
        description="Bridge designed with formal models and soundness-first engineering.",
        base_technical_risk=0.28,
        base_economic_risk=0.32,
        base_operational_risk=0.27,
    ),
}


def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


def compute_risk(
    profile: BridgeProfile,
    uses_zk: bool,
    uses_fhe: bool,
    has_light_client: bool,
    has_mpc_signers: bool,
    has_timelock: bool,
    has_audits: bool,
    has_formal_specs: bool,
    multi_chain: bool,
    tvl_rank: int,
) -> Dict[str, Any]:
    t = profile.base_technical_risk
    e = profile.base_economic_risk
    o = profile.base_operational_risk

    if uses_zk:
        t -= 0.03
        o += 0.02

    if uses_fhe:
        t += 0.04
        o += 0.03

    if has_light_client:
        t -= 0.06
        e -= 0.03

    if has_mpc_signers:
        t += 0.04
        o += 0.05

    if has_timelock:
        e -= 0.05
        o -= 0.03

    if has_audits:
        t -= 0.07
        o -= 0.04

    if has_formal_specs:
        t -= 0.08
        e -= 0.02

    if multi_chain:
        t += 0.03
        o += 0.04

    tvl_factor = clamp(tvl_rank / 50.0, 0.0, 1.0)
    e += 0.08 * tvl_factor

    t = clamp(t)
    e = clamp(e)
    o = clamp(o)

    overall = clamp(0.45 * t + 0.35 * e + 0.20 * o)

    if overall < 0.25:
        label = "very_low"
    elif overall < 0.45:
        label = "low"
    elif overall < 0.65:
        label = "moderate"
    elif overall < 0.80:
        label = "high"
    else:
        label = "very_high"

    return {
        "profile": profile.key,
        "profileName": profile.name,
        "description": profile.description,
        "usesZk": uses_zk,
        "usesFhe": uses_fhe,
        "hasLightClient": has_light_client,
        "hasMpcSigners": has_mpc_signers,
        "hasTimelock": has_timelock,
        "hasAudits": has_audits,
        "hasFormalSpecs": has_formal_specs,
        "multiChain": multi_chain,
        "tvlRank": tvl_rank,
        "technicalRisk": round(t, 3),
        "economicRisk": round(e, 3),
        "operationalRisk": round(o, 3),
        "overallRisk": round(overall, 3),
        "riskLabel": label,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="bridge_risk_profiler",
        description=(
            "Offline risk profiler for Web3 bridges, conceptually inspired by "
            "Aztec-style zk privacy rollups, Zama-style FHE bridges, and soundness-focused designs."
        ),
    )
    parser.add_argument(
        "--style",
        choices=list(PROFILES.keys()),
        default="aztec",
        help="Base bridge style (aztec, zama, soundness).",
    )
    parser.add_argument(
        "--zk",
        action="store_true",
        help="Bridge uses zk proofs for message validity or state sync.",
    )
    parser.add_argument(
        "--fhe",
        action="store_true",
        help="Bridge interacts with FHE compute or encrypted pipelines.",
    )
    parser.add_argument(
        "--light-client",
        action="store_true",
        help="Bridge uses on-chain light client verification instead of trusted relayers.",
    )
    parser.add_argument(
        "--mpc-signers",
        action="store_true",
        help="Bridge relies on MPC or multisig signers for control.",
    )
    parser.add_argument(
        "--timelock",
        action="store_true",
        help="Bridge has timelock or delay on admin and governance actions.",
    )
    parser.add_argument(
        "--audits",
        action="store_true",
        help="Bridge code has had at least one independent security audit.",
    )
    parser.add_argument(
        "--formal-specs",
        action="store_true",
        help="Bridge or protocol has a public formal specification or model.",
    )
    parser.add_argument(
        "--multi-chain",
        action="store_true",
        help="Bridge connects more than two chains/rollups (multi-chain graph).",
    )
    parser.add_argument(
        "--tvl-rank",
        type=int,
        default=25,
        help=(
            "Rough TVL rank (1 = top TVL, higher = lower TVL). "
            "Used to mildly increase economic risk as capital grows. Default: 25."
        ),
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print JSON instead of human-readable output.",
    )
    return parser.parse_args()


def print_human(result: Dict[str, Any]) -> None:
    print("🌉 bridge_risk_profiler")
    print(f"Base style   : {result['profileName']} ({result['profile']})")
    print(f"Description  : {result['description']}")
    print("")
    print("Design features:")
    print(f"  Uses zk proofs       : {'yes' if result['usesZk'] else 'no'}")
    print(f"  Uses FHE             : {'yes' if result['usesFhe'] else 'no'}")
    print(f"  Light client based   : {'yes' if result['hasLightClient'] else 'no'}")
    print(f"  MPC / multisig       : {'yes' if result['hasMpcSigners'] else 'no'}")
    print(f"  Timelock present     : {'yes' if result['hasTimelock'] else 'no'}")
    print(f"  Audited              : {'yes' if result['hasAudits'] else 'no'}")
    print(f"  Formal specs         : {'yes' if result['hasFormalSpecs'] else 'no'}")
    print(f"  Multi-chain graph    : {'yes' if result['multiChain'] else 'no'}")
    print(f"  TVL rank             : {result['tvlRank']}")
    print("")
    print("Risk scores (0 = minimal, 1 = extreme):")
    print(f"  Technical    : {result['technicalRisk']:.3f}")
    print(f"  Economic     : {result['economicRisk']:.3f}")
    print(f"  Operational  : {result['operationalRisk']:.3f}")
    print("")
    print(f"Overall risk   : {result['overallRisk']:.3f} ({result['riskLabel']})")
    print("")
    print("Note: This is a conceptual, offline profiler. It does not connect to Web3 or")
    print("measure real-world exploits. Use it as a structured checklist and discussion")
    print("tool for bridge design in Aztec-style, Zama-style, or soundness-first systems.")


def main() -> None:
    args = parse_args()
    profile = PROFILES[args.style]

    result = compute_risk(
        profile=profile,
        uses_zk=args.zk,
        uses_fhe=args.fhe,
        has_light_client=args.light_client,
        has_mpc_signers=args.mpc_signers,
        has_timelock=args.timelock,
        has_audits=args.audits,
        has_formal_specs=args.formal_specs,
        multi_chain=args.multi_chain,
        tvl_rank=max(1, args.tvl_rank),
    )

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print_human(result)


if __name__ == "__main__":
    main()
