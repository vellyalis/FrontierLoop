# 1A. Reconstruct from first principles when gated

この節はFirst-principles lane gateが開いている場合だけ使う。

1. Materialな前提を`Fundamental`、`Derived`、`User Requirement`、`External Contract`、`Environmental`、`Convention`、`Preference`、`Hypothesis`、`Unknown`へ分類し、source、owner、confidence、dependent decision、refutation conditionを残す。
2. Goal、state、lifecycle、information/control flow、resource bound、ownership、failure modeの因果・制約Graphを作る。Leafは一つの因果役割または責任、明示的なinput/outputまたはinvariant、owner、独立した検証またはboundを持つものに限る。
3. すべての有効解が守るIrreducible Constraint、Global Bottleneck、Required Valueの衝突、Current Best固有の制限、Goalを動かせる最小介入を導く。
4. ConstraintからMechanism、state owner、responsibility allocation、information/control flow、system/user/environment boundaryの異なる候補を再構成する。名前、配置、Parameter値だけの違いを構造候補に数えない。

User Requirement、Public Contract、避けられない環境制約は壊さず、ConventionとHypothesisだけを根拠付きで疑う。追加分解がimplementation、ownership、comparison、verificationのいずれも変えない時点で止める。巨大なDossierを必須にせず、既存のADRまたはExperiment Recordへ次のdecision traceだけを残す。

`Goal -> premise -> irreducible constraint -> candidate structure -> Artifact -> evidence -> decision`
