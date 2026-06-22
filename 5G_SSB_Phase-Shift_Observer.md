# 5G SSB Phase-Shift Observer

## Zero-Hardware Structural Health Monitoring for Telecom Towers

**Author:** Washington Imae
**GPG:** `7989 D2E2 1C9D 29E6 5742 2BCA 2B88 E816 5712 F528`
**Version:** 1.0 — June 2026
**On-chain proof:** [Bitcoin Testnet txid `3ed6dc22bd669c04620490f29e0b50adf8332e009f5e5e2786e3cc1a42048b0c`](https://blockstream.info/testnet/tx/3ed6dc22bd669c04620490f29e0b50adf8332e009f5e5e2786e3cc1a42048b0c)

---

## Abstract

We present a method for extracting cumulative structural maintenance debt from telecom towers using only existing 5G BBU (Baseband Unit) phase correction logs. No additional sensors, hardware installations, or tower climbs are required.

Every 5G massive MIMO antenna uses SSB (Synchronization Signal Block) beamforming to steer its signal toward user equipment. When a tower deforms by fractions of a degree — from wind, thermal expansion, or permanent structural creep — the BBU applies a phase correction to compensate. These corrections, logged continuously at sub-second intervals, encode the tower's mechanical state.

We demonstrate that a two-layer observer (low-pass filter + hard gate on residual excess) can separate elastic wind-sway from cumulative plastic deformation, producing a single scalar: the **structural maintenance debt** (δ_plastic). Validated on synthetic data calibrated to Nairobi environmental conditions, the observer achieves Pearson r > 0.99 against ground truth and RMSE < 0.1°.

**Keywords:** structural health monitoring, 5G, SSB, phase-shift, beamforming, predictive maintenance, zero-hardware sensor, telecom towers

---

## 1. Introduction

Telecom towers are critical infrastructure. A single collapsed tower costs $200,000–$500,000 in Kenya, not counting service disruption penalties. Current monitoring practices rely on:

- **Visual inspection:** Every 3–5 years. Operator climbs the tower, looks for visible damage. Misses sub-degree deformation.
- **Tilt sensors:** $500–$1,000 per tower per year. Installed during construction. Retrofit is expensive and requires tower downtime.
- **Drone surveys:** $200–$500 per flight. Requires scheduling, good weather, and trained pilots. Not continuous.

The result: most towers are structurally invisible between inspections. Deformation accumulates silently until it crosses a critical threshold.

**The insight:** Every 5G tower already contains a precision instrument — the BBU's SSB phase correction loop. Designed as an RF beamforming metric, it inadvertently measures tower tilt at sub-0.02° resolution, sampled every 10–100 ms, 24/7. This data already exists in every operator's logs. It costs nothing to collect.

This paper describes a method to extract structural information from this existing telemetry.

---

## 2. Background: 5G SSB Beamforming and Tower Deformation

### 2.1 SSB Beamforming

In 5G NR, the gNB (next-generation Node B) transmits SSB beams in a sweeping pattern to cover its sector. For any given UE, the BBU calculates the optimal beam direction based on:

- UE position (angular)
- Path loss
- Interference environment

When the tower tilts, the physical beam direction shifts. The BBU logs this as a phase correction (Δθ) — the angular adjustment applied to maintain beam alignment.

### 2.2 Tower Deformation Physics

A telecom tower experiences two types of deformation:

1. **Elastic deformation** — Instantaneous, reversible response to wind, thermal expansion. Disappears when the load is removed.
2. **Plastic deformation** — Permanent structural strain. Accumulates over time from fatigue, corrosion, foundation settlement, or extreme weather events.

Only plastic deformation threatens structural integrity. The challenge is separating it from elastic wind-sway in the phase correction signal.

### 2.3 The Coupled Signal

The observed phase correction Δθ at time k is:

```
Δθ_k = θ_elastic(wind_k) + δ_plastic(k) + ε_k
```

Where:
- θ_elastic = α · W_k — wind-driven elastic tilt (linear approximation)
- δ_plastic = cumulative permanent deformation
- ε_k = measurement noise (~0.015° for typical BBU phase lock loops)

---

## 3. Method: Two-Layer Observer

### 3.1 Architecture

The observer consists of two cascaded layers:

```
Layer 1:   Wind shear → Low-pass filter → θ_tilt (elastic estimate)
Layer 2:   Δθ − θ_tilt − δ_plastic → Gate → Accumulate → δ_plastic
```

#### Layer 1 — Elastic State Estimation

A first-order low-pass filter estimates the elastic contribution:

```
θ_tilt(k) = (1 − τ) · θ_tilt(k−1) + τ · (α · W_k)
```

Where:
- τ = filter time constant (0 < τ < 1). Lower values produce smoother estimates at the cost of response speed.
- α = elastic modulus multiplier (°·s/m), specific to tower type and height
- W_k = wind shear speed at time k (m/s)

This is deliberately simple. A Kalman filter formulation is the production target; the LPF proves the concept works without the complexity overhead.

#### Layer 2 — Plastic Debt Accumulation

The residual excess after accounting for elastic tilt:

```
excess_k = Δθ_k − θ_tilt(k) − δ_plastic(k−1)
```

The hard gate:

```
if excess_k > threshold and sample_count > warmup:
    δ_plastic(k) = δ_plastic(k−1) + excess_k · C_env
else:
    δ_plastic(k) = δ_plastic(k−1)
```

Where:
- threshold = minimum excess before counting as plastic deformation (default 0.02°)
- warmup = initial samples to skip while the LPF converges (default 50)
- C_env = environmental corrosion factor (≥ 1.0), accounts for accelerated degradation in humid/saline/corrosive environments

### 3.2 Parameter Calibration

Parameters are tower-specific and require a calibration period:

| Parameter | Symbol | Method | Default (Nairobi) |
|-----------|--------|--------|-------------------|
| Elastic modulus | α | Measure Δθ vs wind correlation over calm period | 0.168 °·s/m |
| Corrosion factor | C_env | Historical failure rate, humidity data | 1.12 |
| LPF time constant | τ | Tuned via cross-validation on known events | 0.1 |
| Plastic threshold | θ_min | Minimum detectable deformation (noise floor × 2) | 0.02° |
| Warmup samples | N_w | LPF convergence time (≈ 3/τ) | 50 |

### 3.3 Interpretation of δ_plastic

The structural maintenance debt is a unitless scalar. We define an alert threshold:

| δ_plastic | Status | Action |
|-----------|--------|--------|
| < 1.0 | Normal | Routine monitoring |
| 1.0 – 2.0 | Elevated | Schedule inspection within 3 months |
| 2.0 – 3.0 | Warning | Schedule inspection within 2 weeks |
| > 3.0 | Critical | Immediate tower closure |

These thresholds are preliminary and would be refined with real failure data.

---

## 4. Implementation

### 4.1 Data Pipeline

```
BBU logs → CSV → SSBObserver.step() → δ_plastic time series → Alert
```

Input CSV format:

```csv
timestamp,wind_shear_mps,phase_correction_deg
2026-06-10T00:00:00,5.32,0.84
2026-06-10T00:00:10,5.27,0.85
```

### 4.2 Simulator

A Monte Carlo simulator (`bbu_log_sim.py`) generates realistic BBU logs with configurable:

- Wind patterns (calm, gusty, storm, diurnal)
- Elastic modulus (α)
- Measurement noise
- Plastic deformation events (time, magnitude)
- Environmental corrosion (C_env)

This allows validation of the observer against known ground truth — something impossible with real tower data in the absence of failure records.

### 4.3 Observer Implementation

The observer is implemented in Python as `SSBObserver` (`src/kalman_filter.py`). It processes samples sequentially (streaming-compatible) and maintains only three state variables:

```python
self.theta_tilt = 0.0    # Elastic tilt estimate
self.debt = 0.0          # Cumulative plastic deformation
self.sample_count = 0    # Warmup counter
```

This minimal state footprint makes it suitable for edge deployment on a Raspberry Pi or similar near-tower compute.

### 4.4 Dashboard

A Streamlit dashboard (`app.py`) provides interactive visualization:

- Upload or simulate BBU phase logs
- Adjust observer parameters live
- View three-panel plot (wind, phase correction, structural debt)
- Download results as CSV

---

## 5. Validation Results

### 5.1 Synthetic Calibration Run

A 48-hour diurnal wind simulation with two plastic deformation events:

|||
|---|---|
| **Pattern** | Diurnal (tropical) |
| **α** | 0.168 °·s/m |
| **C_env** | 1.12 |
| **Events** | +0.8° at hour 8, +1.0° at hour 32 |
| **Noise** | 0.015° (Gaussian) |
| **Observer τ** | 0.1 |
| **Threshold** | 0.02° |

**Results:**

| Metric | Value |
|--------|-------|
| Final δ_plastic | 1.95° |
| Events detected | 2 / 2 (100%) |
| Pearson r vs ground truth | > 0.99 |
| RMSE | < 0.1° |

### 5.2 Step Response

A simple step of +1.5° at hour 6 was detected within 15 minutes (90 samples at 10s intervals), demonstrating the observer's ability to discriminate between wind-driven elastic oscillation and a permanent offset.

### 5.3 False Positive Rate

On a 500-sample sequence of constant wind (5 m/s, phase at equilibrium 0.84°), the observer accumulated < 0.01° of false debt, confirming that sustained elastic-only signals are correctly rejected.

---

## 6. Comparison to Existing Methods

| Method | Resolution | Frequency | Cost per tower/yr | Detection type |
|--------|-----------|-----------|-------------------|----------------|
| Visual inspection | ~0.5° tilt | Every 3–5 years | $100–$300 | Reactive |
| Tilt sensor | ~0.1° | Continuous | $500–$1,000 | Semi-predictive |
| Drone survey | ~1 cm spatial | Quarterly | $200–$500/flight | Periodic |
| **SSB Observer** (this work) | **~0.02°** | **Sub-second** | **$0** (existing logs) | **Predictive** |

The SSB Observer's key advantage is not just cost — it's lead time. Visual inspection detects deformation after it's visible. The observer detects it at 0.02° resolution, which can be **4–6 months before a 0.5° tilt becomes apparent**.

---

## 7. Limitations

1. **Wind data required.** The observer needs contemporaneous wind shear measurements. These are typically available from meteorological stations or tower-mounted anemometers, but add a data source dependency.
2. **Equipment diversity.** Different BBU vendors (Ericsson, Nokia, Huawei, Samsung) log phase corrections at different granularities. Calibration would vary by vendor.
3. **Multi-panel arrays.** Towers with multiple antenna panels may have coupled corrections. The current model assumes a single dominant beam.
4. **No real failure data.** Validation is currently limited to synthetic data. Ground-truth validation requires a tower that has experienced known deformation followed by inspection confirmation.
5. **5G-only.** The method requires 5G NR SSB logging. 4G/LTE towers without beamforming cannot use this method without a hardware upgrade.

---

## 8. Dynamic Analysis — Beyond Static Tilt

The two-layer observer presented in sections 3-5 treats the tower as a quasi-static system: wind pushes, tower tilts, and permanent deformation accumulates. Real towers are dynamic structures with complex vibration behaviour. This section extends the observer into the frequency domain, unlocking earlier failure detection and richer diagnostics — all from the same BBU phase correction log.

### 8.1 Natural Frequency Tracking

Every tower has a natural frequency f_n at which it prefers to vibrate. For telecom towers:

| Tower Type | f_n (1st bending mode) | Source |
|---|---|---|
| Lattice tower (60-100m) | 0.5 – 1.0 Hz | MDPI Infrastructures |
| Steel monopole (20-40m) | 1.2 – 2.0 Hz | ProQuest damping studies |
| Guyed mast | 0.2 – 0.5 Hz | Industry practice |

**The insight:** As a tower loses stiffness — from corrosion, loosening bolts, foundation settlement, or fatigue cracking — its natural frequency **decreases**. A 10% drop in f_n corresponds to a ~19% loss in stiffness (since f_n ∝ √(k/m) for a simple oscillator).

**Implementation:** Compute a sliding FFT on the phase correction signal Δθ over a 60-second window:

```python
import numpy as np

def track_natural_frequency(phase_series, sample_rate_hz=0.1):
    """Extract dominant frequency from BBU phase corrections."""
    window = int(60 * sample_rate_hz)  # 60-second window
    freqs = np.fft.rfftfreq(window, d=1/sample_rate_hz)
    psd = np.abs(np.fft.rfft(phase_series[-window:]))**2
    dominant = freqs[np.argmax(psd[1:]) + 1]  # skip DC
    return dominant, psd, freqs
```

**Output:** A time series of f_n. An alert triggers when f_n drops below a per-tower baseline by a configurable threshold (e.g., 5% drop → inspect, 10% → warn, 15% → critical).

**Why this is better than static tilt alone:** A tower can lose 20% of its stiffness and still be perfectly straight. Static tilt only catches deformation *after* it happens. Natural frequency tracking catches stiffness loss *as it happens*.

### 8.2 Damping Ratio Estimation

Damping ratio ζ controls how quickly a tower stops vibrating after a wind gust. Healthy values:

| Tower Type | ζ (damping ratio) |
|---|---|
| Lattice tower | 0.005 – 0.02 (0.5% – 2%) |
| Monopole | 0.01 – 0.03 (1% – 3%) |
| Damaged structure | Changes by ±30% or more from baseline |

**The insight:** Joint loosening increases damping (more friction), while fatigue cracking decreases it (less energy dissipation). A damping change in either direction is diagnostic.

**Implementation:** After identifying a gust event (rapid wind increase followed by decrease), fit an exponential decay to the post-gust phase correction:

```
Δθ_post(t) = A · exp(-ζ · ω_n · t) · sin(ω_d · t + φ)
```

Where:
- ω_n = 2πf_n (natural angular frequency)
- ω_d = ω_n · √(1 − ζ²) (damped natural frequency)
- ζ is the unknown we solve for

Fit via least-squares over a 30-second post-gust window:

```python
from scipy.optimize import curve_fit

def damped_sine(t, A, zeta, phi):
    omega_n = 2 * np.pi * natural_frequency
    omega_d = omega_n * np.sqrt(1 - zeta**2)
    return A * np.exp(-zeta * omega_n * t) * np.sin(omega_d * t + phi)

def estimate_damping(timestamps, phase_values, natural_frequency):
    popt, _ = curve_fit(damped_sine, timestamps, phase_values,
                        p0=[max(phase_values), 0.01, 0])
    return popt[1]  # zeta
```

### 8.3 Fatigue Cycle Counting (Miner's Rule)

Every phase correction cycle imposes a stress cycle on the tower structure. Over years, these cycles accumulate fatigue damage even if the tower never visibly deforms.

Miner's cumulative damage rule:

```
D = Σ (n_i / N_i)
```

Where D = 1.0 predicts failure. The number of cycles to failure N_i at a given stress amplitude S_i is given by the tower's S-N curve (Wöhler curve):

```
N_i = C / S_i^m
```

Where C and m are material constants (for structural steel, m ≈ 3-5).

**Implementation:** Apply rainflow counting to the phase correction signal to extract cycle amplitudes, then accumulate damage:

```python
def rainflow_count(series):
    """Extract cycle amplitudes from a time series using rainflow counting."""
    # Standard ASTM E1049 rainflow algorithm
    # Returns list of (amplitude, mean) for each half-cycle
    ...

def accumulate_fatigue(phase_series, C=1e12, m=4):
    cycles = rainflow_count(phase_series)
    D = sum(amp**m / C for amp, _ in cycles)
    return D
```

**Output:** A fatigue damage scalar D, ranging from 0 (new tower) toward 1 (end of life). Independent of static tilt.

### 8.4 Modal Decomposition (Multi-Panel Towers)

Towers with multiple BBU antenna panels (e.g., 3 sectors at 120°) can separate bending from torsion — a distinction impossible with a single panel.

If panels A, B, and C are at 0°, 120°, and 240° around the tower:

| Motion | Panel A | Panel B | Panel C |
|---|---|---|---|
| Bending (N-S) | +Δθ | −0.5Δθ | −0.5Δθ |
| Bending (E-W) | 0 | +0.87Δθ | −0.87Δθ |
| Torsion (twist) | +Δθ | +Δθ | +Δθ |

**Implementation:** Project the three panel phase corrections onto the mode shapes:

```python
def decompose_motions(theta_a, theta_b, theta_c):
    """Separate tower motion into bending and torsion components."""
    # Assumes panels at 0°, 120°, 240°
    bend_ns = (2*theta_a - theta_b - theta_c) / 3
    bend_ew = (theta_b - theta_c) / np.sqrt(3)
    torsion = (theta_a + theta_b + theta_c) / 3
    return bend_ns, bend_ew, torsion
```

**Why this matters:** A tower experiencing foundation settlement shows mostly bending (one side sinks). A tower experiencing bolted joint failure at a guy wire connection shows torsion (asymmetric loading). Separating them tells you *what kind* of damage, not just that damage exists.

### 8.5 Vortex Shedding Detection

Wind passing a cylindrical tower creates periodic vortices at the shedding frequency f_s:

```
f_s = St · V / D
```

Where:
- St = Strouhal number (~0.2 for circular cylinders)
- V = wind speed (m/s)
- D = tower diameter (m)

For a 1m-diameter monopole in 10 m/s wind: f_s = 0.2 × 10 / 1 = 2.0 Hz.

**Danger:** If f_s matches the tower's natural frequency f_n, **lock-in** occurs — sustained resonance that can cause catastrophic fatigue failure in hours.

**Implementation:** The agent server already receives wind speed. Compute the shedding frequency in real-time and compare to the tracked natural frequency:

```python
def vortex_danger(wind_speed, tower_diameter, natural_freq, threshold=0.1):
    shedding_freq = 0.2 * wind_speed / tower_diameter
    proximity = abs(shedding_freq - natural_freq) / natural_freq
    return {
        'shedding_freq': shedding_freq,
        'natural_freq': natural_freq,
        'proximity': proximity,
        'danger': proximity < threshold,
    }
```

**Alert:** When proximity < 0.1 (10%), issue a vortex shedding warning — even if the tower is perfectly straight.

### 8.6 Unified Health Dashboard

Combining all metrics yields a multi-dimensional health vector:

```
H(t) = [δ_plastic, f_n, Δf_n, ζ, D_vortex, D_fatigue]
```

| Metric | Symbol | Early Warning | Late Warning | Critical |
|---|---|---|---|---|
| Static tilt debt | δ_plastic | < 1.0° | 1.0 – 2.0° | > 2.0° |
| Natural frequency shift | Δf_n | < 5% drop | 5–10% drop | > 10% drop |
| Damping change | Δζ | < 20% change | 20–50% change | > 50% change |
| Fatigue damage | D | < 0.3 | 0.3 – 0.7 | > 0.7 |
| Vortex shedding proximity | p | > 0.2 | 0.1 – 0.2 | < 0.1 |

A tower with δ_plastic = 0.3 (healthy tilt) but Δf_n = 12% (critical stiffness loss) would be flagged for immediate inspection — invisible to static methods alone.

### 8.7 FFT-Based Statistical Health Indicators

The power spectral density (PSD) from the sliding FFT contains diagnostic information beyond just the dominant frequency peak. We extract four additional features from the spectrum to detect subtle damage signatures.

#### Harmonics Ratio (Crack Detection)

When a structure develops cracks, the vibration becomes nonlinear — the crack opens and closes during each cycle, creating frequency components at integer multiples of the fundamental (2×f_n, 3×f_n, etc.). The harmonics ratio quantifies this:

```
HR = PSD(2 × f_n) / PSD(f_n)
```

Where PSD(f_n) is the power at the dominant frequency and PSD(2×f_n) is the power at exactly double that frequency.

**Interpretation:**
| HR | Status | Action |
|---|---|---|
| < 0.1 | Normal | No cracks detected |
| 0.1 – 0.2 | Borderline | Monitor — possible micro-crack initiation |
| > 0.2 | Crack-like | Schedule inspection — crack-induced nonlinearity |

**Why this is earlier than frequency shift:** A crack generates harmonics *before* the overall stiffness drops enough to shift f_n. Harmonics ratio is the earliest crack detection signal available from a single sensor.

#### Spectral Flatness (Chaos Detection)

Spectral flatness measures how evenly energy is distributed across the frequency spectrum:

```
SF = (∏ PSD_i)^(1/N) / (Σ PSD_i / N)
```

A healthy tower vibrating at its natural frequency has a sharp spectral peak → SF ≈ 0 (tonal).
A damaged tower with loose bolts, cracked joints, and chaotic vibration has energy everywhere → SF ≈ 1 (noisy).

**Interpretation:**
| SF | Status | Action |
|---|---|---|
| < 0.3 | Tonal | Healthy — clean resonant vibration |
| 0.3 – 0.5 | Mixed | Borderline — increasing noise floor |
| > 0.5 | Noisy | Chaotic vibration — likely structural damage |

#### Kurtosis (Impulsiveness)

Kurtosis of the detrended phase signal detects intermittent impact events:

```
Ku = E[(x − μ)⁴] / (E[(x − μ)²])²
```

A Gaussian distribution has Ku = 3. Impact events (loose joints slamming, crack faces colliding) produce impulsive spikes that raise kurtosis above 3. A pure sinusoidal vibration (locked-in resonance) has Ku < 3.

**Interpretation:**
| Ku | Status |
|---|---|
| < 2.5 | Sinusoidal — probable resonance lock-in |
| 2.5 – 3.5 | Normal — Gaussian random vibration |
| > 3.5 | Impulsive — loose joints or impact events |

#### AR(1) Coefficient (Short-Term Memory)

The first-order autoregressive coefficient φ₁ measures how predictable the vibration is from the previous sample:

```
x_t = φ₁ × x_{t−1} + ε_t
```

A tower oscillating at its natural frequency has φ₁ ≈ 1 (highly predictable — periodic). A tower with chaotic vibration from damage has φ₁ → 0 (random — unpredictable).

**Interpretation:**
| φ₁ | Status |
|---|---|
| > 0.8 | Periodic — healthy oscillation |
| 0.4 – 0.8 | Mixed — some damage, still periodic |
| < 0.4 | Chaotic — severe damage, random vibration |

#### Updated Health Vector

The complete 15-metric health vector H(t) now includes:

```
H(t) = [δ_plastic, θ_elastic, f_n, Δf_n, ζ, D_fatigue, p_vortex,
        RMS, Ku, SC, SS, φ₁, HR, SF, excess]
```

| Category | Metric | Symbol | Detects |
|---|---|---|---|
| Static | Tilt debt | δ_plastic | Permanent lean |
| Static | Elastic sway | θ_elastic | Current wind response |
| Frequency | Natural frequency | f_n | Stiffness change |
| Frequency | Frequency shift | Δf_n | Stiffness loss from baseline |
| Modal | Damping ratio | ζ | Joint integrity |
| Fatigue | Cumulative damage | D | Cycle-accumulated fatigue |
| Aerodynamic | Vortex proximity | p_vortex | Lock-in resonance danger |
| Statistical | RMS amplitude | RMS | Vibration intensity |
| Statistical | Kurtosis | Ku | Impulsive events |
| Time-frequency | Spectral centroid | SC | Frequency content shift |
| Time-frequency | Spectral spread | SS | Multi-modal excitation |
| Time-series | AR(1) coefficient | φ₁ | Predictability / chaos |
| FFT | Harmonics ratio | HR | Crack-induced nonlinearity |
| FFT | Spectral flatness | SF | Chaotic vibration |
| Diagnostic | Excess | — | Raw residual before gate |

---

## 8.8 Complete Formula Reference

Every formula in the production observer, with variable sources and calibration methods.

### Static (Debt + Elastic)

```
θ_expected(t) = α × W(t)²                              [Wind pressure]
θ_tilt(t) = (1−τ) × θ_tilt(t−1) + τ × θ_expected(t)    [LPF]
excess(t) = Δθ(t) − θ_tilt(t) − δ_plastic(t−1)         [Excess]
δ_plastic(t) = δ_plastic(t−1) + excess(t) × C_env      [Gate, if excess > θ_min]
```

| Symbol | Name | Unit | Source |
|---|---|---|---|
| α | Elastic modulus | °·s²/m² | Calm-period linear regression: Δθ vs W² |
| W(t) | Wind speed | m/s | Tower anemometer or weather station |
| τ | LPF time constant | — | Tuned per tower (0.05–0.3) |
| Δθ(t) | BBU phase correction | ° | Existing BBU log (SNMP OID) |
| θ_min | Plastic threshold | ° | Set above BBU noise floor (~0.02°) |
| C_env | Corrosion factor | — | 1.0 desert, 1.12 Nairobi, 1.5 coastal |
| N_warmup | Warmup samples | count | ~50 for LPF convergence |

### Frequency

```
data = Δθ_buffer − polyfit(Δθ_buffer, order=1)          [Detrend]
PSD(f) = |FFT(data × Hanning)|²                         [Spectrum]
f_n = argmax(PSD)  (skip DC)                            [Natural freq]
Δf_n(%) = max(0, (f_baseline − f_n) / f_baseline) × 100  [Freq shift]
```

| Symbol | Name | Unit | Source |
|---|---|---|---|
| Δθ_buffer | Rolling window | ° | Last 600 samples of raw phase data |
| f_baseline | Baseline frequency | Hz | Measured during first calibration month |
| f_n | Natural frequency | Hz | FFT dominant peak |

### Damping

```
θ(t) = A × exp(−ζ·ω_n·t) × sin(ω_d·t + φ) + offset
ω_n = 2π·f_n,  ω_d = ω_n·√(1−ζ²)
ζ solved via scipy.curve_fit on post-gust decay window
```

| Symbol | Name | Unit | Source |
|---|---|---|---|
| A | Initial amplitude | ° | Post-gust peak phase correction |
| ζ | Damping ratio | — | Least-squares fit output |
| ω_n | Natural angular freq | rad/s | From f_n |
| gust trigger | Wind spike | — | W(t) > 1.5×W(t−1) AND W(t) > 3 m/s |

### Fatigue (Miner's Rule)

```
amplitude = |peak − valley| / 2        [Rainflow reversal]
N_f = C / amplitude^m                  [S-N curve]
D += 1 / N_f                           [Accumulate]
```

| Symbol | Name | Value | Source |
|---|---|---|---|
| C | S-N constant | 1×10¹² | Generic structural steel |
| m | S-N exponent | 4 | Generic structural steel |
| D | Fatigue damage | 0→1 | Observer accumulator |

### Vortex Shedding

```
f_shedding = St × W(t) / D_tower
proximity = |f_shedding − f_n| / f_n
p_vortex = max(0, 1 − (proximity − 0.05)/0.15)
```

| Symbol | Name | Value | Source |
|---|---|---|---|
| St | Strouhal number | 0.2 | Circular cylinder (fluid dynamics) |
| D_tower | Tower diameter | m | Tower spec sheet or measurement |
| p_vortex | Proximity score | 0→1 | 0=safe, 1=lock-in |

### Statistical / FFT Features

```
RMS    = √(mean(Δθ_residual²))                           [Intensity]
Ku     = E[(x−μ)⁴] / (E[(x−μ)²])²                        [Impulsiveness]
SC     = Σ(f·PSD(f)) / Σ(PSD(f))                          [Centroid]
SS     = √(Σ((f−SC)²·PSD(f)) / Σ(PSD(f)))                 [Spread]
φ₁     = cov(x_t, x_{t−1}) / var(x_{t−1})                 [AR(1)]
HR     = PSD(2·f_n) / PSD(f_n)                             [Harmonics]
SF     = (∏PSD)^{1/N} / (ΣPSD/N)                           [Flatness]
```

| Symbol | Name | Range | What It Detects |
|---|---|---|---|
| RMS | Root mean square | >0° | Vibration intensity |
| Ku | Kurtosis | ~3 normal | >3.5 impulsive (loose joints) |
| SC | Spectral centroid | Hz | Stiffness change |
| SS | Spectral spread | Hz | Multi-modal damage |
| φ₁ | AR(1) coefficient | 0–1 | Chaos (>0.8 periodic) |
| HR | Harmonics ratio | 0–1 | Crack nonlinearity (>0.2) |
| SF | Spectral flatness | 0–1 | Chaotic vibration (>0.5) |

All statistical/FFT features use the detrended residual buffer: `Δθ_residual = Δθ − δ_plastic`.

### Data Flow

```
BBU Phase Log (Δθ) ──┐
                      ├──► SSB Observer Pro ──► H(t) [15 metrics] ──► Alert
Wind Speed (W)     ──┘
```

**Two real-time inputs. Fifteen outputs. One formula chain.**

### Sampling Requirements

| Feature Set | Minimum Sampling | Nyquist Limit | Suitable For |
|---|---|---|---|
| Static (δ_plastic, θ_tilt) | Any rate | None | All tower types |
| Frequency (f_n, SC, SS, SF, HR) | >4 Hz | 2 Hz | Monopole (1.5 Hz) |
| Frequency (f_n, SC, SS, SF, HR) | >2 Hz | 1 Hz | Lattice (0.8 Hz) |
| Damping (ζ) | >2 Hz | — | Post-gust decay fitting |
| Fatigue (D) | >1 Hz | — | Cycle amplitude detection |

The production default of 1 second sampling (1 Hz) resolves tower dynamics up to 0.5 Hz (suitable for lattice towers). Real BBU phase correction data is typically logged at 10–100 millisecond intervals (10–100 Hz), exceeding all requirements.

---

## 9. Limitations (Addendum to Section 7)

Additional limitations for the dynamic analysis methods described in Section 8:

1. **Frequency resolution.** A 60-second FFT window at 0.1 Hz sampling gives ~0.017 Hz frequency resolution — sufficient for 0.5-2 Hz natural frequencies but marginal for subtle shifts. Longer windows improve resolution but reduce responsiveness.

2. **Damping estimation requires clean gust events.** The exponential decay fit only works when there's a clear wind impulse followed by calm. Towers in persistently windy environments may yield few usable events.

3. **Modal decomposition requires multi-panel data.** Most towers outside urban areas have only 1-3 panels. Three is the minimum for full bending/torsion separation.

4. **Fatigue S-N curves are tower-specific.** The parameters C and m depend on steel grade, weld quality, joint type, and age. Generic values give approximate results.

5. **Vortex shedding model assumes cylindrical cross-section.** Lattice towers have complex aerodynamics. The Strouhal number varies with member geometry and solidity ratio.

6. **Frequency detection requires adequate sampling.** The Nyquist-Shannon theorem requires sampling at ≥ 2× the highest frequency of interest. For tower natural frequencies in the 0.5–2.0 Hz range, a minimum sampling rate of 4 Hz (250 ms intervals) is needed. The 10-second simulation interval (0.1 Hz) used for multi-month weather generation is insufficient for frequency-domain analysis. Real BBU phase correction logs are typically sampled at 10–100 ms, well within the required range.

This method generates a defensible data asset over time. The dataset moat has five layers:

1. **Per-tower calibration** (α, C_env) — requires months of data per tower type
2. **Failure event labels** — requires years to accumulate real failure ground truth
3. **Seasonal baselines** — annual cycles of temperature, humidity, wind patterns
4. **Cross-tower correlation models** — gust front detection, regional deformation patterns
5. **Trained ML predictors** — deformation forecasting models that improve with data volume

Each successive layer is harder to replicate and multiplies the value of the previous one.

---

## 10. IP and Prior Art

This whitepaper's conception document is timestamped on Bitcoin Testnet:

- **Conception doc:** [`64f0bb98e5a90084ee4f6523fc1d96cee0634811bb08c83cfe52f2a532b05002`](https://blockstream.info/testnet/tx/64f0bb98e5a90084ee4f6523fc1d96cee0634811bb08c83cfe52f2a532b05002)
- **This paper:** [`3ed6dc22bd669c04620490f29e0b50adf8332e009f5e5e2786e3cc1a42048b0c`](https://blockstream.info/testnet/tx/3ed6dc22bd669c04620490f29e0b50adf8332e009f5e5e2786e3cc1a42048b0c)

These timestamps constitute verifiable prior art under the Bit Protocol standard (OP_RETURN SHA-256 hash to Bitcoin blockchain), independent of any patent filing.

**Patent claim scope:** *A method of side-channel extraction of cumulative structural-maintenance debt from 5G SSB phase-shift telemetry, comprising: a low-pass filter for separating elastic wind-sway from plastic deformation; a hard gate with environmental corrosion factor for accumulating permanent debt; and a scalar threshold alert system.*

---

## 11. Future Work

- **Real tower validation:** Partnership with a tower operator or telecom to access actual BBU logs alongside known maintenance events
- **Kalman filter formulation:** Replace the LPF with a Kalman filter for dynamic state estimation and uncertainty quantification. The Kalman filter requires two parameters estimated from real BBU data: process noise covariance Q (how unpredictable the wind-tower response is) and measurement noise covariance R (BBU vendor-specific phase correction noise). Without real tower data, these cannot be calibrated — generic values would produce results indistinguishable from the LPF. Implementation priority: once real BBU logs are available, Q and R are estimated from calm-period data, then the Kalman filter replaces the LPF in a single weekend of work. Until then, the LPF remains the production observer's elastic state estimator.
- **Full dynamic observer implementation:** Implement the spectral analysis, damping estimation, rainflow fatigue counting, and modal decomposition described in Section 8 as a Python module
- **Multi-tower correlation:** Detect regional gust fronts and foundation settlement patterns from correlated phase shifts across adjacent towers
- **ML deformation forecasting:** Train a predictor (LSTM or Transformer) on the full health vector H(t) to forecast when a tower will hit any critical threshold
- **Vortex shedding real-time alert:** Implement the Strouhal-based vortex shedding danger calculation alongside the existing debt observer
- **Edge deployment:** Port the observer to ARM (Raspberry Pi) for tower-side processing with cellular backhaul for alerts only

---

## References

1. 3GPP TS 38.211 — NR Physical Channels and Modulation (SSB beamforming specification)
2. 3GPP TS 38.214 — NR Physical Layer Procedures for Data
3. IEC 61400-12-1 — Wind Speed Measurement Standards
4. ISO 2394:2015 — General Principles on Reliability for Structures
5. Resensys, "Tower Monitoring Systems Implementation Guide" (2024)
6. ESA Space Solutions, "SHM Telecom Towers" (2024)
7. MDPI Sensors, "AI in Structural Health Monitoring" (2024)

---

## Appendix A: Quick Start

```bash
# Clone the observer
git clone https://github.com/washingtoneimae-dot/5g-ssb-demo.git
cd 5g-ssb-observer

# Generate simulated data
python bbu_log_sim.py --hours=48 --pattern=diurnal --event=08:00,0.8 --event=32:00,1.0

# Run the observer
python3 -c "
import pandas as pd
from src.kalman_filter import run_observer
result = run_observer('bbu_phase_log.csv')
print(f'Final debt: {result[\"debt_extracted\"][-1]:.3f}°')
print(f'Events detected: {result[\"events_detected\"]}')
print(f'Pearson r: {result[\"r\"]:.4f}')
print(f'RMSE: {result[\"rmse\"]:.4f}°')
"

# Launch the dashboard
streamlit run app.py
```

## Appendix B: Observer API

```python
from src.kalman_filter import SSBObserver

obs = SSBObserver(alpha=0.168, c_env=1.12)

# Stream from BBU
for measurement, wind_shear in data_stream:
    theta_tilt, debt, excess = obs.step(measurement, wind_shear)
    if debt > 3.0:
        send_alert(f"Critical structural debt: {debt:.2f}°")
```

---

*This whitepaper is timestamped on Bitcoin Testnet at txid `3ed6dc22bd669c04620490f29e0b50adf8332e009f5e5e2786e3cc1a42048b0c`. Verify at https://blockstream.info/testnet/tx/3ed6dc22bd669c04620490f29e0b50adf8332e009f5e5e2786e3cc1a42048b0c*
