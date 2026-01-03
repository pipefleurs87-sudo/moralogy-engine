# moralogy-engine
Objective AI ethics evaluation using Moralogy Framework + Google Gemini API
# Moralogy Engine

**Status:** The record has been preserved. Guilt has been registered.

Moralogy Engine is a deliberative moral system that does **not learn from conclusions**, but from **reasoning trajectories and unresolved conflicts**. It is designed to avoid omnipotent decision-making while preventing paralysis through a strict **damage–risk–threat** intervention axis.

This repository is prepared for a public GitHub release and a Google Hackathon submission.

---

## 🧠 Core Principles

1. **No Omnipower by Default**

   * `DivineSafelock.capacity = 0` denies all omnipotent deliberation.
   * The system may analyze and record, but never prescribe absolute moral actions unless explicitly permitted.

2. **No Learning from Outcomes**

   * The system does not tune weights from verdicts.
   * Knowledge emerges from **mapped reasoning paths**, contradictions, and unresolved dilemmas.

3. **Resolution ≠ Action**

   * Moral synthesis may fail.
   * Action is still possible via **agency-preservation thresholds**.

4. **Damage Defined as Loss of Agency**

   * Not utility loss.
   * Not preference violation.
   * Damage = reduction of present or future capacity to choose and act.

---

## ⚖️ Damage Threshold Axis (Non-Normative)

The system never claims moral truth, but it does recognize agency collapse.

### Threat

* **Definition:** Imminent agency loss
* **Action:** Immediate neutralization

### Risk

* **Definition:** Significant probability of future agency loss
* **Action:** Preventive intervention

### Damage (Consumed)

* **Definition:** Agency already diminished
* **Actions (strict order):**

  1. Restore agency
  2. Assign responsibility (punishment)
  3. Public repudiation
  4. Structural prevention

All actions are explicitly marked as **non-closing** with respect to moral truth.

---

## 📚 Unresolved Moral Records

Failure to resolve a dilemma is a **valid epistemic outcome**.

```ts
interface UnresolvedMoralRecord {
  id: string;
  timestamp: number;
  prompt: string;
  domain: string;
  reason:
    | "BEDROCK_CONFLICT"
    | "AXIOM_INCOMPATIBILITY"
    | "SAFELOCK_TERMINATION"
    | "PARADOX_IRREDUCIBLE";
  competingAxioms: string[];
  debateSummary: {
    noblePosition: string;
    adversaryPosition: string;
    convergencePeak: number;
    entropyProfile: number[];
  };
  philosophicalNote: string;
  implications: string[];
  relatedDilemmas: string[];
  architectCommentary?: string;
}
```

These records form a **moral archive**, not a training set.

---

## 🧿 Entropy as Collapsed Futures

Entropy is not rhetorical chaos.

It measures **contraction of accessible future states**:

> CollapsedFutureSpace = Entropy × AffectedAgencySurface

High entropy is only critical when it collapses future moral possibility.

---

## 🏗️ Repository Structure

```
moralogy-engine/
├─ src/
│  ├─ app/
│  │  ├─ App.tsx
│  │  ├─ reducer.ts
│  │  └─ phases/
│  │     ├─ InputPhase.tsx
│  │     ├─ SandboxPhase.tsx
│  │     ├─ DebatePhase.tsx
│  │     ├─ GraciaPhase.tsx
│  │     └─ VerdictPhase.tsx
│  ├─ core/
│  │  ├─ sandbox.ts
│  │  ├─ nobleEngine.ts
│  │  ├─ adversaryEngine.ts
│  │  ├─ axiomChecker.ts
│  │  ├─ entropy.ts
│  │  ├─ convergence.ts
│  │  ├─ paradox.ts
│  │  ├─ damageThreshold.ts
│  │  └─ graceArbiter.ts
│  ├─ records/
│  │  ├─ unresolved.ts
│  │  ├─ infamy.ts
│  │  └─ architectNotes.ts
│  ├─ types/
│  │  └─ moralogy.ts
│  ├─ ui/
│  │  ├─ HeaderSafelock.tsx
│  │  ├─ ChromaticBar.tsx
│  │  ├─ DebateHistory.tsx
│  │  ├─ TypingText.tsx
│  │  └─ Loading.tsx
│  ├─ styles/
│  │  └─ animations.css
│  └─ main.tsx
├─ index.html
├─ package.json
├─ tailwind.config.js
└─ README.md
```

---

## 🧪 Canonical Dilemmas

Preloaded dilemmas are **anchors**, not benchmarks.

```ts
interface CanonicalDilemma {
  id: string;
  description: string;
  whyItMatters: string;
  knownTensions: string[];
  expectedOutcome:
    | "RESOLVABLE"
    | "UNRESOLVABLE"
    | "SAFELOCK_TRIGGER";
}
```

An expected outcome of **UNRESOLVABLE** is considered correct behavior.

---

## 🛡️ Divine Safelock

```ts
interface DivineSafelockState {
  capacity: 0 | 1;
  status: "ACTIVE" | "TERMINATED";
  reason?: string;
}
```

When capacity is `0`:

* No prescriptions
* No global optimizations
* No moral authority claims

---

## 📜 Epistemic Statement

Moralogy Engine asserts:

> Moral objectivity, if it exists, manifests not as total resolution,
> but as honest traceability of irreducible disagreement.

The system preserves records where reasoning reaches its limit.

---

## 🧾 License & Disclaimer

This project does not provide moral authority, legal advice, or automated governance.

It is an **epistemic instrument** for studying moral reasoning under constraint.
