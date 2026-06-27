"""Fast sweeps with vectorized coupling."""
import numpy as np
import json, time
from pathlib import Path

LAM, K0 = 1.55, 2*np.pi/1.55
r = np.linspace(0, 60, 500)

def gauss(w):
    return np.sqrt(2/np.pi)*(1/w)*np.exp(-r**2/w**2)

def olap(a, b):
    return 2*np.pi*np.trapz(a*b*r, r)

def build_modes(NA, a):
    n1, lam = 1.457, LAM
    n2 = np.sqrt(n1**2 - NA**2)
    Delta = (n1**2 - n2**2)/(2*n1**2)
    g = np.sqrt(2*Delta)/a
    wg = np.sqrt(a*lam/(np.pi*NA))
    modes, betas = [], []
    for p in range(5):
        x = 2*r**2/wg**2
        Lp = np.ones_like(x)
        if p == 1: Lp = 1 - x
        elif p > 1:
            L2, L1 = np.ones_like(x), 1 - x
            for k in range(2, p+1):
                Lc = ((2*k-1-x)*L1 - (k-1)*L2)/k
                L2, L1 = L1, Lc
            Lp = L1
        psi = np.sqrt(2/np.pi)*(1/wg)*Lp*np.exp(-x/2)
        nrm = 2*np.pi*np.trapz(psi**2*r, r)
        modes.append(psi/np.sqrt(nrm))
        betas.append(K0*n1 - (2*p+1)*g/2)
    return np.array(modes), np.array(betas)

def coupling_stats(NA, a, wsmf, whcf):
    modes, betas = build_modes(NA, a)
    psmf, phcf = gauss(wsmf), gauss(whcf)
    cc = np.array([olap(psmf, m) for m in modes])
    oh = np.array([olap(m, phcf) for m in modes])
    nz = 2000
    z = np.linspace(0, 2000, nz)
    phase = np.exp(1j * betas[:, np.newaxis] * z[np.newaxis, :])
    amp = np.sum(cc[:, np.newaxis] * oh[:, np.newaxis] * phase, axis=0)
    eta = np.abs(amp)**2
    io = np.argmax(eta)
    return z[io], eta[io], -10*np.log10(max(eta[io],1e-15)), eta, z, cc, betas, modes

wsmf, whcf = 5.2, 12.0
results = {}
t0 = time.time()

# ── Baseline ──
zopt, etamax, loss, eta, z, cc, betas, modes = coupling_stats(0.200, 25.0, wsmf, whcf)
print(f"BASELINE: η={etamax*100:.2f}% @ z={zopt:.0f}μm, loss={loss:.3f} dB")
results['baseline'] = {'loss_dB':float(loss), 'z_opt_um':float(zopt), 'coupling_pct':float(etamax*100)}

# ── NA sweep ──
na_vals = np.linspace(0.14, 0.24, 20)
na_l = [coupling_stats(v,25.0,wsmf,whcf)[2] for v in na_vals]
print(f"\nNA SWEEP: min loss={min(na_l):.3f} dB @ NA={na_vals[np.argmin(na_l)]:.3f}")

# ── Core radius sweep ──
a_vals = np.linspace(15, 35, 20)
a_l = [coupling_stats(0.200,v,wsmf,whcf)[2] for v in a_vals]
print(f"CORE SWEEP: min loss={min(a_l):.3f} dB @ a={a_vals[np.argmin(a_l)]:.0f}μm")

# ── HCF spot sweep ──
hcf_vals = np.linspace(8, 16, 20)
hcf_l = [coupling_stats(0.200,25.0,wsmf,v)[2] for v in hcf_vals]
print(f"HCF SWEEP: min loss={min(hcf_l):.3f} dB @ w_hcf={hcf_vals[np.argmin(hcf_l)]:.1f}μm")

# ── Boundary cases ──
print(f"\nBOUNDARY CASES:")
cases = [
    ("Low NA (0.180)", 0.180, 25.0),
    ("High NA (0.220)", 0.220, 25.0),
    ("Small core (23μm)", 0.200, 23.0),
    ("Large core (27μm)", 0.200, 27.0),
    ("Worst: NA=0.18, a=23", 0.180, 23.0),
    ("Best: NA=0.22, a=27", 0.220, 27.0),
]
for label, NA, a in cases:
    zo, em, lo = coupling_stats(NA, a, wsmf, whcf)[:3]
    print(f"  {label}: {lo:.3f} dB @ z={zo:.0f}μm")

# ── Wavelength sweep ──
print(f"\nWAVELENGTH SWEEP:")
wavs = np.linspace(1.26, 1.625, 10)
wav_l = []
for lam in wavs:
    ws = 4.2 + 0.65*(lam-1.31)
    wh = 12.0*(lam/1.55)
    # rebuild modes at this λ
    zopt, emax, lo, _, _, _, _, _ = coupling_stats(0.200, 25.0, ws, wh)
    wav_l.append(lo)
    # But need to rebuild with correct k0...
    # Actually coupling_stats currently uses global K0. Let me handle this inline.
print("  (re-run with correct wavelength below)")

# Proper wavelength sweep with correct k0
wav_l2 = []
for lam in wavs:
    ws = 4.2 + 0.65*(lam-1.31)
    wh = 12.0*(lam/1.55)
    k0l = 2*np.pi/lam
    n1, NA, a = 1.457, 0.200, 25.0
    n2 = np.sqrt(n1**2 - NA**2)
    Delta = (n1**2 - n2**2)/(2*n1**2)
    g = np.sqrt(2*Delta)/a
    wg = np.sqrt(a*lam/(np.pi*NA))
    mods_l, betas_l = [], []
    for p in range(5):
        x = 2*r**2/wg**2
        Lp = np.ones_like(x)
        if p == 1: Lp = 1 - x
        elif p > 1:
            L2, L1 = np.ones_like(x), 1-x
            for k in range(2, p+1):
                Lc = ((2*k-1-x)*L1 - (k-1)*L2)/k
                L2, L1 = L1, Lc
            Lp = L1
        psi = np.sqrt(2/np.pi)*(1/wg)*Lp*np.exp(-x/2)
        nrm = 2*np.pi*np.trapz(psi**2*r, r)
        mods_l.append(psi/np.sqrt(nrm))
        betas_l.append(k0l*n1 - (2*p+1)*g/2)
    modes_l = np.array(mods_l)
    betas_l = np.array(betas_l)
    psmfl, phcfl = gauss(ws), gauss(wh)
    cc_l = np.array([olap(psmfl, m) for m in modes_l])
    oh_l = np.array([olap(m, phcfl) for m in modes_l])
    zl = np.linspace(0, 2000, 1000)
    phase_l = np.exp(1j*betas_l[:,np.newaxis]*zl[np.newaxis,:])
    amp_l = np.sum(cc_l[:,np.newaxis]*oh_l[:,np.newaxis]*phase_l, axis=0)
    eta_l = np.abs(amp_l)**2
    lo = -10*np.log10(max(eta_l[np.argmax(eta_l)], 1e-15))
    wav_l2.append(lo)
    print(f"  λ={lam:.3f}μm: {lo:.3f} dB")

# ── Monte Carlo ──
print(f"\nMONTE CARLO (2000 samples)")
np.random.seed(42)
mc_losses = []
for _ in range(2000):
    NA = np.clip(np.random.normal(0.200, 0.005), 0.180, 0.220)
    a = np.clip(np.random.normal(25.0, 0.5), 23.0, 27.0)
    zo, emax, lo, eta_arr, zc, cc, betas, modes = coupling_stats(NA, a, wsmf, whcf)
    # Cleave error ±10μm
    za = zo + np.random.normal(0, 10)
    iz = np.argmin(np.abs(zc - za))
    etaa = eta_arr[iz]
    # Offset penalty
    off = min(np.random.exponential(0.5), 2.0)
    phase = np.exp(1j*betas*za)
    psiz = np.sum(cc[:,np.newaxis]*modes*phase[:,np.newaxis], axis=0)
    wrms = np.sqrt(2*np.pi*np.trapz(r**2*np.abs(psiz)**2*r, r))
    penalty = 4.34*(off/max(wrms,0.1))**2
    loss = -10*np.log10(max(etaa,1e-15)) + penalty
    mc_losses.append(loss)

mc = np.array(mc_losses)
print(f"  Mean: {np.mean(mc):.3f} dB")
print(f"  Median: {np.median(mc):.3f} dB")
print(f"  P(<0.2dB): {np.mean(mc<0.2)*100:.0f}%")
print(f"  P(<0.3dB): {np.mean(mc<0.3)*100:.0f}%")
print(f"  P(<0.5dB): {np.mean(mc<0.5)*100:.0f}%")
print(f"  5th-95th: {np.percentile(mc,5):.3f}–{np.percentile(mc,95):.3f} dB")

t1 = time.time()
print(f"\nTotal time: {t1-t0:.1f}s")

# Recompute baseline
zopt_b, etamax_b, loss_b = coupling_stats(0.200, 25.0, wsmf, whcf)[:3]
# Save
Path('/tmp/5g-ssb-whitepaper/simulation').mkdir(exist_ok=True)
with open('/tmp/5g-ssb-whitepaper/simulation/sweep_results.json','w') as f:
    json.dump({
        'baseline_loss_dB': float(loss_b),
        'baseline_z_opt_um': float(zopt_b),
        'baseline_coupling_pct': float(etamax_b*100),
        'mc_mean_dB': float(np.mean(mc)),
        'mc_median_dB': float(np.median(mc)),
        'mc_std_dB': float(np.std(mc)),
        'mc_p05_dB': float(np.percentile(mc,5)),
        'mc_p95_dB': float(np.percentile(mc,95)),
        'mc_p_under_0_2dB': float(np.mean(mc<0.2)*100),
        'mc_p_under_0_3dB': float(np.mean(mc<0.3)*100),
        'mc_p_under_0_5dB': float(np.mean(mc<0.5)*100),
    }, f, indent=2)
print(f"✓ Sweep results saved")
